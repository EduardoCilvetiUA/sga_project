from db import execute_query
from datetime import date
from querys.curso_aprobado_queries import (
    get_courses_approved_by_student,
    get_approved_course_by_id,
    check_course_passed_by_student,
    check_there_is_record,
    update_record,
    create_record,
    delete_approved_course,
    get_course_id,
    get_students_id_by_alumno_and_seccion,
    calculate_student_final_grade,
)


class CursoAprobado:
    @staticmethod
    def get_all_by_alumno(alumno_id):
        return execute_query(get_courses_approved_by_student, (alumno_id,), fetch=True)

    @staticmethod
    def get_by_id(curso_aprobado_id):
        result = execute_query(
            get_approved_course_by_id, (curso_aprobado_id,), fetch=True
        )
        return result[0] if result else None

    @staticmethod
    def is_curso_aprobado(alumno_id, curso_id):
        result = execute_query(
            check_course_passed_by_student, (alumno_id, curso_id), fetch=True
        )
        return bool(result)

    @staticmethod
    def register_curso_aprobado(alumno_id, curso_id, seccion_id, nota_final, aprobado):
        existing = execute_query(
            check_there_is_record, (alumno_id, curso_id), fetch=True
        )
        if existing:
            execute_query(
                update_record,
                (seccion_id, nota_final, aprobado, date.today(), existing[0]["id"]),
            )
            return existing[0]["id"]
        else:
            return execute_query(
                create_record,
                (alumno_id, curso_id, seccion_id, nota_final, aprobado, date.today()),
            )

    @staticmethod
    def delete(curso_aprobado_id):
        execute_query(delete_approved_course, (curso_aprobado_id,))

    @staticmethod
    def calculate_and_register_final_grade(alumno_id, seccion_id):
        curso_result = execute_query(get_course_id, (seccion_id,), fetch=True)
        if not curso_result:
            raise Exception("Seccion no encontrada")
        curso_id = curso_result[0]["curso_id"]
        alumno_seccion = execute_query(
            get_students_id_by_alumno_and_seccion, (alumno_id, seccion_id), fetch=True
        )
        if not alumno_seccion:
            raise Exception("Alumno no encontrado en la sección")
        alumno_seccion_id = alumno_seccion[0]["id"]
        grade_result = execute_query(
            calculate_student_final_grade, (alumno_seccion_id,), fetch=True
        )
        nota_final = grade_result[0]["nota_final"] if grade_result else 0
        aprobado = nota_final >= 4.0
        return CursoAprobado.register_curso_aprobado(
            alumno_id, curso_id, seccion_id, nota_final, aprobado
        )
