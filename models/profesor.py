from db import execute_query
from querys.profesor_queries import (
    get_all_professors,
    get_professor_by_id,
    create_professor,
    update_professor,
    delete_professor,
    get_sections_by_professor,
)


class Profesor:
    @staticmethod
    def get_all():
        return execute_query(get_all_professors, fetch=True)

    @staticmethod
    def get_by_id(profesor_id):
        result = execute_query(get_professor_by_id, (profesor_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(nombre, correo):
        return execute_query(create_professor, (nombre, correo))

    @staticmethod
    def update(profesor_id, nombre, correo):
        execute_query(update_professor, (nombre, correo, profesor_id))
        return profesor_id

    @staticmethod
    def delete(profesor_id):
        execute_query(delete_professor, (profesor_id,))

    @staticmethod
    def get_sections(profesor_id):
        return execute_query(get_sections_by_professor, (profesor_id,), fetch=True)
