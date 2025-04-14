from db import execute_query
from querys.nota_queries import (
    get_all_grades,
    get_grade_by_id,
    create_grade,
    update_grade,
    delete_grade,
    get_all_grades_by_section,
    get_student_grades_in_section,
    get_student_section_id,
    get_missing_grades_for_student,
)


class Nota:
    @staticmethod
    def get_all():
        return execute_query(get_all_grades, fetch=True)

    @staticmethod
    def get_by_id(nota_id):
        result = execute_query(get_grade_by_id, (nota_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(alumno_seccion_id, instancia_evaluacion_id, nota):
        return execute_query(
            create_grade, (alumno_seccion_id, instancia_evaluacion_id, nota)
        )

    @staticmethod
    def update(nota_id, nota_valor):
        execute_query(update_grade, (nota_valor, nota_id))
        return nota_id

    @staticmethod
    def delete(nota_id):
        execute_query(delete_grade, (nota_id,))

    @staticmethod
    def get_grades_by_section(seccion_id):
        return execute_query(get_all_grades_by_section, (seccion_id,), fetch=True)

    @staticmethod
    def get_grades_by_student_section(alumno_id, seccion_id):
        return execute_query(
            get_student_grades_in_section, (alumno_id, seccion_id), fetch=True
        )

    @staticmethod
    def get_student_section_id(alumno_id, seccion_id):
        result = execute_query(
            get_student_section_id, (alumno_id, seccion_id), fetch=True
        )
        return result[0]["id"] if result else None

    @staticmethod
    def get_pending_evaluations(alumno_id, seccion_id):
        return execute_query(
            get_missing_grades_for_student,
            (seccion_id, alumno_id, seccion_id),
            fetch=True,
        )

    @staticmethod
    def calculate_final_grade(alumno_id, seccion_id):
        grades = Nota.get_grades_by_student_section(alumno_id, seccion_id)

        if not grades:
            return None

        use_porcentaje = grades[0]["usa_porcentaje"] if grades else True

        group_grades_by_topic = {}
        for grade in grades:
            topic_name = grade["topico_nombre"]
            if topic_name not in group_grades_by_topic:
                group_grades_by_topic[topic_name] = {
                    "valor": grade["topico_valor"],
                    "instancias": [],
                }

            group_grades_by_topic[topic_name]["instancias"].append(
                {
                    "nombre": grade["instancia_nombre"],
                    "valor": grade["valor"],
                    "opcional": grade["opcional"],
                    "nota": grade["nota"],
                }
            )

        topic_grades = {}
        for topic, data in group_grades_by_topic.items():
            total_value = sum(inst["valor"] for inst in data["instancias"])
            weighted_sum = sum(
                inst["nota"] * inst["valor"] for inst in data["instancias"]
            )

            if total_value > 0:
                topic_grades[topic] = weighted_sum / total_value
            else:
                topic_grades[topic] = 0

        if use_porcentaje:
            total_percentage = sum(
                data["valor"] for data in group_grades_by_topic.values()
            )

            if total_percentage <= 0:
                return None

            final_grade = 0
            for topic, nota in topic_grades.items():
                value = group_grades_by_topic[topic]["valor"]
                final_grade += nota * (value / total_percentage)
        else:
            total_weight = sum(data["valor"] for data in group_grades_by_topic.values())

            if total_weight <= 0:
                return None

            final_grade = 0
            for topic, nota in topic_grades.items():
                value = group_grades_by_topic[topic]["valor"]
                final_grade += nota * (value / total_weight)

        return round(final_grade, 1)
