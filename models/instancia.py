from db import execute_query
from querys.instancia_queries import (
    get_all_intancias_curso,
    get_instancias_curso_by_id,
    create_instancias_curso,
    update_instancias_curso,
    delete_instancias_curso,
    get_secciones_by_instancia_curso_id,
    is_instancia_cerrada,
    toggle_instancia_cerrada,
    get_instancia_by_seccion_id,
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
    def get_secciones(instancia_id):
        return execute_query(
            get_secciones_by_instancia_curso_id, (instancia_id,), fetch=True
        )

    @staticmethod
    def is_cerrada(instancia_id):
        result = execute_query(is_instancia_cerrada, (instancia_id,), fetch=True)
        return result[0]["cerrado"] if result else False

    @staticmethod
    def validate_not_cerrada(instancia_id, operation="operación"):
        if Instancia.is_cerrada(instancia_id):
            raise ValueError(f"No se puede realizar esta {operation} en una instancia cerrada")

    @staticmethod
    def toggle_cerrado(instancia_id, cerrado):
        """Cambiar el estado cerrado de una instancia"""
        execute_query(toggle_instancia_cerrada, (cerrado, instancia_id))
        return instancia_id

    @staticmethod
    def get_instancia_by_seccion(seccion_id):
        """Obtener la instancia asociada a una sección"""
        result = execute_query(get_instancia_by_seccion_id, (seccion_id,), fetch=True)
        return result[0] if result else None