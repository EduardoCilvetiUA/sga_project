from db import execute_query
from models.curso_aprobado import CursoAprobado
from querys.seccion_queries import (
    get_all_sections,
    get_section_by_id,
    create_section,
    update_section,
    delete_section,
    get_professors_for_section,
    get_students_enrolled_in_section,
    assign_professor_to_section,
    remove_professor_from_section,
    get_course_id_for_section,
    enroll_student_in_section,
    unenroll_student_from_section,
    get_not_enrolled_professors,
    get_not_enrolled_students,
    check_student_prerequisites_for_course,
)


class Seccion:
    @staticmethod
    def get_all():
        return execute_query(get_all_sections, fetch=True)

    @staticmethod
    def get_by_id(seccion_id):
        result = execute_query(get_section_by_id, (seccion_id,), fetch=True)
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
                create_section, (instancia_curso_id, number, use_porcentaje)
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
                update_section, (instancia_curso_id, number, use_porcentaje, seccion_id)
            )
            return seccion_id
        except Exception as e:
            print(f"Error en Seccion.update: {str(e)}")
            raise

    @staticmethod
    def delete(seccion_id):
        execute_query(delete_section, (seccion_id,))

    @staticmethod
    def get_professors(seccion_id):
        return execute_query(get_professors_for_section, (seccion_id,), fetch=True)

    @staticmethod
    def get_students(seccion_id):
        return execute_query(
            get_students_enrolled_in_section, (seccion_id,), fetch=True
        )

    @staticmethod
    def assign_professor(seccion_id, profesor_id):
        return execute_query(assign_professor_to_section, (profesor_id, seccion_id))

    @staticmethod
    def remove_professor(seccion_id, profesor_id):
        execute_query(remove_professor_from_section, (profesor_id, seccion_id))

    @staticmethod
    def enroll_student(seccion_id, alumno_id):
        result = execute_query(get_course_id_for_section, (seccion_id,), fetch=True)
        if not result:
            raise Exception("Seccion no encontrada")

        curso_id = result[0]["curso_id"]

        if not Seccion.check_prerequisites(curso_id, alumno_id):
            raise Exception(
                "El estudiante no cumple con todos los prerrequisitos para este curso"
            )
        return execute_query(enroll_student_in_section, (alumno_id, seccion_id))

    @staticmethod
    def unenroll_student(seccion_id, alumno_id):
        execute_query(unenroll_student_from_section, (alumno_id, seccion_id))

    @staticmethod
    def get_available_professors(seccion_id):
        return execute_query(get_not_enrolled_professors, (seccion_id,), fetch=True)

    @staticmethod
    def get_available_students(seccion_id):
        return execute_query(get_not_enrolled_students, (seccion_id,), fetch=True)

    @staticmethod
    def check_prerequisites(curso_id, alumno_id):
        prerequisites = execute_query(
            check_student_prerequisites_for_course, (curso_id,), fetch=True
        )

        if not prerequisites:
            return True

        for prereq in prerequisites:
            prereq_id = prereq["prerequisito_id"]

            if not CursoAprobado.is_curso_aprobado(alumno_id, prereq_id):
                return False

        return True

    @staticmethod
    def get_course_id(seccion_id):
        result = execute_query(get_course_id_for_section, (seccion_id,), fetch=True)
        return result[0]["curso_id"] if result else None
