from db import execute_query
from querys.evaluacion_queries import (
    get_all_topicos_evaluacion,
    get_topicos_evaluacion_by_id,
    create_topicos_evaluacion,
    update_topicos_evaluacion,
    delete_topicos_evaluacion,
    get_instancias_evaluacion_by_topico,
    get_instancia_evaluacion_by_id,
    create_instancia_evaluacion,
    update_instancia_evaluacion,
    delete_instancia_evaluacion,
    get_topico_evaluacion_by_seccion,
    get_seccion_percentage,
    get_total_score_by_seccion,
    get_topico_percentage,
    get_total_score_by_topico,
)


class Evaluacion:
    @staticmethod
    def get_all_topicos():
        return execute_query(get_all_topicos_evaluacion, fetch=True)

    @staticmethod
    def get_topico_by_id(topic_id):
        result = execute_query(get_topicos_evaluacion_by_id, (topic_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create_topico(seccion_id, nombre, valor, usa_porcentaje):
        return execute_query(
            create_topicos_evaluacion, (seccion_id, nombre, valor, usa_porcentaje)
        )

    @staticmethod
    def update_topico(topic_id, nombre, valor, usa_porcentaje):
        execute_query(
            update_topicos_evaluacion, (nombre, valor, usa_porcentaje, topic_id)
        )
        return topic_id

    @staticmethod
    def delete_topico(topic_id):
        execute_query(delete_topicos_evaluacion, (topic_id,))

    @staticmethod
    def get_instancias(topic_id):
        return execute_query(
            get_instancias_evaluacion_by_topico, (topic_id,), fetch=True
        )

    @staticmethod
    def get_instancia_by_id(instance_id):
        result = execute_query(
            get_instancia_evaluacion_by_id, (instance_id,), fetch=True
        )
        return result[0] if result else None

    @staticmethod
    def create_instancia(topico_id, nombre, valor, opcional):
        return execute_query(
            create_instancia_evaluacion, (topico_id, nombre, valor, opcional)
        )

    @staticmethod
    def update_instancia(instance_id, nombre, valor, opcional):
        execute_query(
            update_instancia_evaluacion, (nombre, valor, opcional, instance_id)
        )
        return instance_id

    @staticmethod
    def delete_instancia(instance_id):
        execute_query(delete_instancia_evaluacion, (instance_id,))

    @staticmethod
    def get_topicos_by_seccion(seccion_id):
        return execute_query(
            get_topico_evaluacion_by_seccion, (seccion_id,), fetch=True
        )

    @staticmethod
    def get_seccion_total_percentage(seccion_id):
        seccion_result = execute_query(
            get_seccion_percentage, (seccion_id,), fetch=True
        )

        if not seccion_result:
            return 0

        use_porcentaje = seccion_result[0]["usa_porcentaje"]

        if use_porcentaje:
            result = execute_query(
                get_total_score_by_seccion, (seccion_id,), fetch=True
            )

            if not result or result[0]["total"] is None:
                return 0

            return result[0]["total"]

        return None

    @staticmethod
    def get_topico_total_percentage(topic_id):
        topic_result = execute_query(get_topico_percentage, (topic_id,), fetch=True)

        if not topic_result:
            return 0

        use_porcentaje = topic_result[0]["usa_porcentaje"]

        if use_porcentaje:
            result = execute_query(get_total_score_by_topico, (topic_id,), fetch=True)

            if not result or result[0]["total"] is None:
                return 0

            return result[0]["total"]

        return None
