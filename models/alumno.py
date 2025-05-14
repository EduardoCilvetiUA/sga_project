from db import execute_query
from querys.alumno_queries import (
    get_all_alumnos,
    get_alumno_by_id,
    create_alumno,
    update_data_alumno,
    delete_alumno,
    get_seccion_alumno,
)


class Alumno:
    @staticmethod
    def get_all():
        return execute_query(get_all_alumnos, fetch=True)

    @staticmethod
    def get_by_id(alumno_id):
        result = execute_query(get_alumno_by_id, (alumno_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(nombre, correo, fecha_ingreso):
        return execute_query(create_alumno, (nombre, correo, fecha_ingreso))

    @staticmethod
    def update(alumno_id, nombre, correo, fecha_ingreso):
        execute_query(update_data_alumno, (nombre, correo, fecha_ingreso, alumno_id))
        return alumno_id

    @staticmethod
    def delete(alumno_id):
        execute_query(delete_alumno, (alumno_id,))

    @staticmethod
    def get_secciones(alumno_id):
        return execute_query(get_seccion_alumno, (alumno_id,), fetch=True)
