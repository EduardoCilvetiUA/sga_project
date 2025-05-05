# models/sala.py
from db import execute_query
from querys.sala_queries import (
    get_all_classrooms,
    get_classroom_by_id,
    create_classroom,
    update_classroom,
    delete_classroom,
    get_classroom_availability
)

class Sala:
    @staticmethod
    def get_all():
        return execute_query(get_all_classrooms, fetch=True)

    @staticmethod
    def get_by_id(sala_id):
        result = execute_query(get_classroom_by_id, (sala_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(nombre, capacidad):
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError("La capacidad debe ser un número entero positivo")
        return execute_query(create_classroom, (nombre, capacidad))

    @staticmethod
    def update(sala_id, nombre, capacidad):
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError("La capacidad debe ser un número entero positivo")
        execute_query(update_classroom, (nombre, capacidad, sala_id))
        return sala_id

    @staticmethod
    def delete(sala_id):
        execute_query(delete_classroom, (sala_id,))

    @staticmethod
    def check_availability(sala_id, dia, hora_inicio, hora_fin):
        """Verifica si la sala está disponible en un horario específico"""
        conflictos = execute_query(
            get_classroom_availability, 
            (sala_id, dia, hora_inicio, hora_inicio, hora_fin, hora_fin, hora_inicio, hora_fin),
            fetch=True
        )
        return len(conflictos) == 0