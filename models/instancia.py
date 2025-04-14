from db import execute_query
from querys.instancia_queries import (
    get_all_course_instances,
    get_course_instance_by_id,
    create_course_instance,
    update_course_instance,
    delete_course_instance,
    get_sections_by_course_instance_id,
)


class Instancia:
    @staticmethod
    def get_all():
        return execute_query(get_all_course_instances, fetch=True)

    @staticmethod
    def get_by_id(instancia_id):
        result = execute_query(get_course_instance_by_id, (instancia_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(curso_id, anio, periodo):
        return execute_query(create_course_instance, (curso_id, anio, periodo))

    @staticmethod
    def update(instancia_id, curso_id, anio, periodo):
        execute_query(update_course_instance, (curso_id, anio, periodo, instancia_id))
        return instancia_id

    @staticmethod
    def delete(instancia_id):
        execute_query(delete_course_instance, (instancia_id,))

    @staticmethod
    def get_sections(instancia_id):
        return execute_query(
            get_sections_by_course_instance_id, (instancia_id,), fetch=True
        )
