from db import execute_query
from querys.instancia_queries import (
    get_all_intancias_curso,
    get_instancias_curso_by_id,
    create_instancias_curso,
    update_instancias_curso,
    delete_instancias_curso,
    get_secciones_by_instancia_curso_id,
)


class Instancia:
    @staticmethod
    def get_all():
        return execute_query(get_all_intancias_curso, fetch=True)

    @staticmethod
    def get_by_id(instancia_id):
        result = execute_query(get_instancias_curso_by_id, (instancia_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(curso_id, anio, periodo):
        return execute_query(create_instancias_curso, (curso_id, anio, periodo))

    @staticmethod
    def update(instancia_id, curso_id, anio, periodo):
        execute_query(update_instancias_curso, (curso_id, anio, periodo, instancia_id))
        return instancia_id

    @staticmethod
    def delete(instancia_id):
        execute_query(delete_instancias_curso, (instancia_id,))

    @staticmethod
    def get_sections(instancia_id):
        return execute_query(
            get_secciones_by_instancia_curso_id, (instancia_id,), fetch=True
        )
