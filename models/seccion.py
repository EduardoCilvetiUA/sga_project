from db import execute_query
from models.curso_aprobado import CursoAprobado
from models.instancia import Instancia
from querys.seccion_queries import (
    get_all_secciones,
    get_seccion_by_id,
    create_seccion,
    update_seccion,
    delete_seccion,
    get_profesores_by_seccion,
    get_enrolled_alumnos_in_seccion,
    insert_profesor_in_seccion,
    remove_profesor_from_seccion,
    get_curso_id_for_seccion,
    insert_alumno_in_seccion,
    delete_alumno_from_seccion,
    get_not_enrolled_profesores,
    get_not_enrolled_alumnos,
    check_prerequisitos_for_curso,
)


class Seccion:
    @staticmethod
    def get_all():
        return execute_query(get_all_secciones, fetch=True)

    @staticmethod
    def get_by_id(seccion_id):
        result = execute_query(get_seccion_by_id, (seccion_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(instancia_curso_id, number, use_porcentaje=True):
        try:
            instancia_curso_id = int(instancia_curso_id)
            number = int(number)
            use_porcentaje = bool(use_porcentaje)

            print(
                f"Creating section with: {instancia_curso_id}, {number}, {use_porcentaje}"
            )
            result = execute_query(
                create_seccion, (instancia_curso_id, number, use_porcentaje)
            )

            print(f"Section creation result: {result}")
            return result
        except Exception as e:
            print(f"Error en Seccion.create: {str(e)}")
            raise

    @staticmethod
    def update(seccion_id, instancia_curso_id, number, use_porcentaje=True):
        try:
            seccion_id = int(seccion_id)
            instancia_curso_id = int(instancia_curso_id)
            number = int(number)
            use_porcentaje = bool(use_porcentaje)

            execute_query(
                update_seccion, (instancia_curso_id, number, use_porcentaje, seccion_id)
            )
            return seccion_id
        except Exception as e:
            print(f"Error en Seccion.update: {str(e)}")
            raise

    @staticmethod
    def delete(seccion_id):
        execute_query(delete_seccion, (seccion_id,))

    @staticmethod
    def get_profesores(seccion_id):
        return execute_query(get_profesores_by_seccion, (seccion_id,), fetch=True)

    @staticmethod
    def get_alumnos(seccion_id):
        return execute_query(get_enrolled_alumnos_in_seccion, (seccion_id,), fetch=True)

    @staticmethod
    def assign_profesor(seccion_id, profesor_id):
        return execute_query(insert_profesor_in_seccion, (profesor_id, seccion_id))

    @staticmethod
    def remove_profesor(seccion_id, profesor_id):
        execute_query(remove_profesor_from_seccion, (profesor_id, seccion_id))

    @staticmethod
    def enroll_alumno(seccion_id, alumno_id):
        result = execute_query(get_curso_id_for_seccion, (seccion_id,), fetch=True)
        if not result:
            raise Exception("Seccion no encontrada")

        curso_id = result[0]["curso_id"]

        if not Seccion.check_prerequisitos(curso_id, alumno_id):
            raise Exception(
                "El estudiante no cumple con todos los prerrequisitos para este curso"
            )
        return execute_query(insert_alumno_in_seccion, (alumno_id, seccion_id))

    @staticmethod
    def unenroll_alumno(seccion_id, alumno_id):
        execute_query(delete_alumno_from_seccion, (alumno_id, seccion_id))

    @staticmethod
    def get_available_profesores(seccion_id):
        return execute_query(get_not_enrolled_profesores, (seccion_id,), fetch=True)

    @staticmethod
    def get_available_alumnos(seccion_id):
        return execute_query(get_not_enrolled_alumnos, (seccion_id,), fetch=True)

    @staticmethod
    def check_prerequisitos(curso_id, alumno_id):
        prerequisitos = execute_query(
            check_prerequisitos_for_curso, (curso_id,), fetch=True
        )

        if not prerequisitos:
            return True

        for prerequisito in prerequisitos:
            prerequisito_id = prerequisito["prerequisito_id"]

            if not CursoAprobado.is_curso_aprobado(alumno_id, prerequisito_id):
                return False

        return True

    @staticmethod
    def get_curso_id(seccion_id):
        result = execute_query(get_curso_id_for_seccion, (seccion_id,), fetch=True)
        return result[0]["curso_id"] if result else None
