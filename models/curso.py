from db import execute_query
from models.curso_aprobado import CursoAprobado
from querys.curso_queries import (
    get_all_courses,
    get_course_by_id,
    create_course,
    update_course,
    delete_course,
    get_course_prerequisites,
    add_course_prerequisite,
    remove_course_prerequisite,
    get_course_eligible_students,
    close_course,
    reopen_course,
    is_course_closed
)


class Curso:
    @staticmethod
    def get_all():
        return execute_query(get_all_courses, fetch=True)

    @staticmethod
    def get_by_id(curso_id):
        result = execute_query(get_course_by_id, (curso_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(codigo, nombre, creditos=2, cerrado=False):
        return execute_query(create_course, (codigo, nombre, creditos, cerrado))

    @staticmethod
    def update(curso_id, codigo, nombre, creditos=None):
        if Curso.is_closed(curso_id):
            raise ValueError("No se puede modificar un curso cerrado")
        if creditos is None:
            curso_actual = Curso.get_by_id(curso_id)
            creditos = curso_actual["creditos"]
        if not isinstance(creditos, int) or creditos <= 0:
            raise ValueError("Los créditos deben ser un número entero positivo")
            
        execute_query(update_course, (codigo, nombre, creditos, curso_id))
        return curso_id

    @staticmethod
    def delete(curso_id):
        if Curso.is_closed(curso_id):
            raise ValueError("No se puede eliminar un curso cerrado")
        execute_query(delete_course, (curso_id,))

    @staticmethod
    def get_prerequisites(curso_id):
        return execute_query(get_course_prerequisites, (curso_id,), fetch=True)

    @staticmethod
    def add_prerequisite(curso_id, prerequisito_id):
        if Curso.is_closed(curso_id):
            raise ValueError("No se puede modificar un curso cerrado")
        return execute_query(add_course_prerequisite, (curso_id, prerequisito_id))

    @staticmethod
    def remove_prerequisite(curso_id, prerequisito_id):
        if Curso.is_closed(curso_id):
            raise ValueError("No se puede modificar un curso cerrado")
        execute_query(remove_course_prerequisite, (curso_id, prerequisito_id))

    @staticmethod
    def check_student_prerequisites(curso_id, alumno_id):
        prerequisites = Curso.get_prerequisites(curso_id)
        if not prerequisites:
            return True, []
            
        missing_prerequisites = Curso._find_missing_prerequisites(alumno_id, prerequisites)
        return len(missing_prerequisites) == 0, missing_prerequisites

    @staticmethod
    def _find_missing_prerequisites(alumno_id, prerequisites):
        missing_prerequisites = []
        
        for prerequisite in prerequisites:
            prereq_id = prerequisite["id"]
            if not CursoAprobado.is_curso_aprobado(alumno_id, prereq_id):
                missing_prerequisites.append(
                    {
                        "id": prereq_id,
                        "codigo": prerequisite["codigo"],
                        "nombre": prerequisite["nombre"],
                    }
                )
                
        return missing_prerequisites

    @staticmethod
    def get_students_eligible_for_course(curso_id):
        return execute_query(get_course_eligible_students, (curso_id,), fetch=True)

    @staticmethod
    def close(curso_id):
        execute_query(close_course, (curso_id,))
        
    @staticmethod
    def reopen(curso_id):
        execute_query(reopen_course, (curso_id,))
        
    @staticmethod
    def is_closed(curso_id):
        result = execute_query(is_course_closed, (curso_id,), fetch=True)
        return result[0]["cerrado"] if result else False