from db import execute_query
from querys.alumno_queries import (
    get_all_students,
    get_student_by_id,
    create_student,
    update_student_data,
    delete_student,
    get_student_sections,
)


class Alumno:
    @staticmethod
    def get_all():
        return execute_query(get_all_students, fetch=True)

    @staticmethod
    def get_by_id(alumno_id):
        result = execute_query(get_student_by_id, (alumno_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(nombre, correo, fecha_ingreso):
        return execute_query(create_student, (nombre, correo, fecha_ingreso))

    @staticmethod
    def update(alumno_id, nombre, correo, fecha_ingreso):
        execute_query(update_student_data, (nombre, correo, fecha_ingreso, alumno_id))
        return alumno_id

    @staticmethod
    def delete(alumno_id):
        execute_query(delete_student, (alumno_id,))

    @staticmethod
    def get_sections(alumno_id):
        return execute_query(get_student_sections, (alumno_id,), fetch=True)
