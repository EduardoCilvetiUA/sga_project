from db import execute_query
from querys.nota_queries import (
    get_all_notas,
    get_nota_by_id,
    create_nota,
    update_nota,
    delete_nota,
    get_all_notas_by_seccion,
    get_notas_alumno_in_seccion,
    get_alumno_seccion_by_id,
    get_notas_faltantes_by_alumno_id,
)


class Nota:
    @staticmethod
    def get_all():
        return execute_query(get_all_notas, fetch=True)

    @staticmethod
    def get_by_id(nota_id):
        result = execute_query(get_nota_by_id, (nota_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(alumno_seccion_id, instancia_evaluacion_id, nota):
        return execute_query(
            create_nota, (alumno_seccion_id, instancia_evaluacion_id, nota)
        )

    @staticmethod
    def update(nota_id, nota_valor):
        execute_query(update_nota, (nota_valor, nota_id))
        return nota_id

    @staticmethod
    def delete(nota_id):
        execute_query(delete_nota, (nota_id,))

    @staticmethod
    def get_notas_by_seccion(seccion_id):
        return execute_query(get_all_notas_by_seccion, (seccion_id,), fetch=True)

    @staticmethod
    def get_notas_by_alumno_seccion(alumno_id, seccion_id):
        return execute_query(
            get_notas_alumno_in_seccion, (alumno_id, seccion_id), fetch=True
        )

    @staticmethod
    def get_alumno_seccion_by_id(alumno_id, seccion_id):
        result = execute_query(
            get_alumno_seccion_by_id, (alumno_id, seccion_id), fetch=True
        )
        return result[0]["id"] if result else None

    @staticmethod
    def get_pending_evaluaciones(alumno_id, seccion_id):
        return execute_query(
            get_notas_faltantes_by_alumno_id,
            (seccion_id, alumno_id, seccion_id),
            fetch=True,
        )

    @staticmethod
    def calculate_nota_final(alumno_id, seccion_id):
        notas = Nota.get_notas_by_alumno_seccion(alumno_id, seccion_id)

        if not notas:
            return None

        use_porcentaje = notas[0]["usa_porcentaje"] if notas else True

        group_notas_by_topico = Nota._group_notas_by_topico(notas)

        notas_topico = Nota._calculate_notas_topico(group_notas_by_topico)

        return Nota._calculate_weighted_nota_final(
            notas_topico, group_notas_by_topico, use_porcentaje
        )

    @staticmethod
    def _group_notas_by_topico(notas):
        group_notas_by_topico = {}

        for nota in notas:
            topic_name = nota["topico_nombre"]
            if topic_name not in group_notas_by_topico:
                group_notas_by_topico[topic_name] = {
                    "valor": nota["topico_valor"],
                    "instancias": [],
                }

            group_notas_by_topico[topic_name]["instancias"].append(
                {
                    "nombre": nota["instancia_nombre"],
                    "valor": nota["valor"],
                    "opcional": nota["opcional"],
                    "nota": nota["nota"],
                }
            )

        return group_notas_by_topico

    @staticmethod
    def _calculate_notas_topico(group_notas_by_topico):
        notas_topico = {}

        for topico, data in group_notas_by_topico.items():
            total_value = sum(instancia["valor"] for instancia in data["instancias"])
            weighted_sum = sum(
                instancia["nota"] * instancia["valor"]
                for instancia in data["instancias"]
            )

            if total_value > 0:
                notas_topico[topico] = weighted_sum / total_value
            else:
                notas_topico[topico] = 0

        return notas_topico

    @staticmethod
    def _calculate_weighted_nota_final(
        notas_topico, group_notas_by_topico, use_porcentaje
    ):
        if use_porcentaje:
            total_percentage = sum(
                data["valor"] for data in group_notas_by_topico.values()
            )

            if total_percentage <= 0:
                return None

            nota_final = 0
            for topico, nota in notas_topico.items():
                value = group_notas_by_topico[topico]["valor"]
                nota_final += nota * (value / total_percentage)
        else:
            total_weight = sum(data["valor"] for data in group_notas_by_topico.values())

            if total_weight <= 0:
                return None

            nota_final = 0
            for topico, nota in notas_topico.items():
                value = group_notas_by_topico[topico]["valor"]
                nota_final += nota * (value / total_weight)

        return round(nota_final, 1)
