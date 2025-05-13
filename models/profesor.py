from db import execute_query
from querys.profesor_queries import (
    get_all_profesores,
    get_profesor_by_id,
    create_profesor,
    update_profesor,
    delete_profesor,
    get_secciones_by_profesor,
)


class Profesor:
    @staticmethod
    def get_all():
        return execute_query(get_all_profesores, fetch=True)

    @staticmethod
    def get_by_id(profesor_id):
        result = execute_query(get_profesor_by_id, (profesor_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(nombre, correo):
        return execute_query(create_profesor, (nombre, correo))

    @staticmethod
    def update(profesor_id, nombre, correo):
        execute_query(update_profesor, (nombre, correo, profesor_id))
        return profesor_id

    @staticmethod
    def delete(profesor_id):
        execute_query(delete_profesor, (profesor_id,))

    @staticmethod
    def get_secciones(profesor_id):
        return execute_query(get_secciones_by_profesor, (profesor_id,), fetch=True)
