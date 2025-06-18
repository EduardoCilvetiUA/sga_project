from db import execute_query
from models.curso_aprobado import CursoAprobado
from querys.curso_queries import (
    get_all_cursos,
    get_curso_by_id,
    create_curso,
    update_curso,
    delete_curso,
    get_curso_prerequisitos,
    add_curso_prerequisitos,
    remove_curso_prerequisitos,
    get_alumnos_eligibles_by_curso,
    get_instancias_by_curso,
    close_instancia_curso,
    reopen_instancia_curso,
    is_instancia_cerrada,
    alumnos_query,
    secciones_query,
)

class Curso:
    @staticmethod
    def get_all():
        return execute_query(get_all_cursos, fetch=True)

    @staticmethod
    def get_by_id(curso_id):
        result = execute_query(get_curso_by_id, (curso_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(codigo, nombre, creditos=2):
        return execute_query(create_curso, (codigo, nombre, creditos))

    @staticmethod
    def update(curso_id, codigo, nombre, creditos=None):
        if creditos is None:
            curso_actual = Curso.get_by_id(curso_id)
            creditos = curso_actual["creditos"]
        if not isinstance(creditos, int) or creditos <= 0:
            raise ValueError("Los créditos deben ser un número entero positivo")

        execute_query(update_curso, (codigo, nombre, creditos, curso_id))
        return curso_id

    @staticmethod
    def delete(curso_id):
        execute_query(delete_curso, (curso_id,))

    @staticmethod
    def get_prerequisitos(curso_id):
        return execute_query(get_curso_prerequisitos, (curso_id,), fetch=True)

    @staticmethod
    def add_prerequisito(curso_id, prerequisito_id):
        return execute_query(add_curso_prerequisitos, (curso_id, prerequisito_id))

    @staticmethod
    def remove_prerequisito(curso_id, prerequisito_id):
        execute_query(remove_curso_prerequisitos, (curso_id, prerequisito_id))

    @staticmethod
    def check_alumno_prerequisitos(curso_id, alumno_id):
        prerequisitos = Curso.get_prerequisitos(curso_id)
        if not prerequisitos:
            return True, []

        missing_prerequisitos = Curso._find_missing_prerequisitos(
            alumno_id, prerequisitos
        )
        return len(missing_prerequisitos) == 0, missing_prerequisitos

    @staticmethod
    def _find_missing_prerequisitos(alumno_id, prerequisitos):
        missing_prerequisitos = []

        for prerequisito in prerequisitos:
            prereq_id = prerequisito["id"]
            if not CursoAprobado.is_curso_aprobado(alumno_id, prereq_id):
                missing_prerequisitos.append(
                    {
                        "id": prereq_id,
                        "codigo": prerequisito["codigo"],
                        "nombre": prerequisito["nombre"],
                    }
                )

        return missing_prerequisitos

    @staticmethod
    def get_alumnos_eligible_for_curso(curso_id):
        return execute_query(get_alumnos_eligibles_by_curso, (curso_id,), fetch=True)

    @staticmethod
    def get_instancias(curso_id):
        return execute_query(get_instancias_by_curso, (curso_id,), fetch=True)

    @staticmethod
    def close_instancia(instancia_id):
        Curso._calcular_notas_finales_instancia(instancia_id)
        
        execute_query(close_instancia_curso, (instancia_id,))

    @staticmethod
    def reopen_instancia(instancia_id):
        execute_query(reopen_instancia_curso, (instancia_id,))

    @staticmethod
    def is_instancia_cerrada(instancia_id):
        result = execute_query(is_instancia_cerrada, (instancia_id,), fetch=True)
        return result[0]["cerrado"] if result else False

    @staticmethod
    def _calcular_notas_finales_instancia(instancia_id):
        secciones = execute_query(secciones_query, (instancia_id,), fetch=True)
        
        for seccion in secciones:
            seccion_id = seccion['id']
            Curso._calcular_notas_finales_seccion(seccion_id)

    @staticmethod
    def _calcular_notas_finales_seccion(seccion_id):
        alumnos = execute_query(alumnos_query, (seccion_id,), fetch=True)
        
        for alumno in alumnos:
            alumno_id = alumno['alumno_id']
            try:
                CursoAprobado.calculate_and_register_final_grade(alumno_id, seccion_id)
            except Exception as e:
                print(f"Error calculando nota final para alumno {alumno_id} en sección {seccion_id}: {e}")
                continue