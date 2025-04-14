from db import execute_query
from querys.evaluacion_queries import (
    get_all_student_topics,
    get_evaluation_topic_by_id,
    create_evaluation_topic,
    update_evaluation_topic,
    delete_evaluation_topic,
    get_evaluation_instances_by_topic,
    get_evaluation_instance_by_id,
    create_evaluation_instance,
    update_evaluation_instance,
    delete_evaluation_instance,
    get_evaluation_topic_by_section,
    get_section_percentage,
    get_total_score_by_section,
    get_topic_percentage,
    get_total_score_by_topic,
)


class Evaluacion:
    @staticmethod
    def get_all_topics():
        return execute_query(get_all_student_topics, fetch=True)

    @staticmethod
    def get_topic_by_id(topic_id):
        result = execute_query(get_evaluation_topic_by_id, (topic_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create_topic(seccion_id, nombre, valor, usa_porcentaje):
        return execute_query(
            create_evaluation_topic, (seccion_id, nombre, valor, usa_porcentaje)
        )

    @staticmethod
    def update_topic(topic_id, nombre, valor, usa_porcentaje):
        execute_query(
            update_evaluation_topic, (nombre, valor, usa_porcentaje, topic_id)
        )
        return topic_id

    @staticmethod
    def delete_topic(topic_id):
        execute_query(delete_evaluation_topic, (topic_id,))

    @staticmethod
    def get_instances(topic_id):
        return execute_query(get_evaluation_instances_by_topic, (topic_id,), fetch=True)

    @staticmethod
    def get_instance_by_id(instance_id):
        result = execute_query(
            get_evaluation_instance_by_id, (instance_id,), fetch=True
        )
        return result[0] if result else None

    @staticmethod
    def create_instance(topico_id, nombre, valor, opcional):
        return execute_query(
            create_evaluation_instance, (topico_id, nombre, valor, opcional)
        )

    @staticmethod
    def update_instance(instance_id, nombre, valor, opcional):
        execute_query(
            update_evaluation_instance, (nombre, valor, opcional, instance_id)
        )
        return instance_id

    @staticmethod
    def delete_instance(instance_id):
        execute_query(delete_evaluation_instance, (instance_id,))

    @staticmethod
    def get_topics_by_section(seccion_id):
        return execute_query(get_evaluation_topic_by_section, (seccion_id,), fetch=True)

    @staticmethod
    def get_section_total_percentage(seccion_id):
        section_result = execute_query(
            get_section_percentage, (seccion_id,), fetch=True
        )

        if not section_result:
            return 0

        use_porcentaje = section_result[0]["usa_porcentaje"]

        if use_porcentaje:
            result = execute_query(
                get_total_score_by_section, (seccion_id,), fetch=True
            )

            if not result or result[0]["total"] is None:
                return 0

            return result[0]["total"]

        return None

    @staticmethod
    def get_topic_total_percentage(topic_id):
        topic_result = execute_query(get_topic_percentage, (topic_id,), fetch=True)

        if not topic_result:
            return 0

        use_porcentaje = topic_result[0]["usa_porcentaje"]

        if use_porcentaje:
            result = execute_query(get_total_score_by_topic, (topic_id,), fetch=True)

            if not result or result[0]["total"] is None:
                return 0

            return result[0]["total"]

        return None
