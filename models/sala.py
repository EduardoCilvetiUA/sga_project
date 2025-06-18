from db import execute_query
from querys.sala_queries import (
    get_all_salas,
    get_sala_by_id,
    create_sala,
    update_sala,
    delete_sala,
    get_disponibilidad_sala,
)

START_INDEX = 0
CAPACITY_CHECK_NUM = 0
AVAILABILITY_CHECK_NUM = 0
class Sala:
    @staticmethod
    def get_all():
        return execute_query(get_all_salas, fetch=True)

    @staticmethod
    def get_by_id(sala_id):
        result = execute_query(get_sala_by_id, (sala_id,), fetch=True)
        return result[START_INDEX] if result else None

    @staticmethod
    def create(nombre, capacidad):
        if not isinstance(capacidad, int) or capacidad <= CAPACITY_CHECK_NUM:
            raise ValueError("La capacidad debe ser un número entero positivo")
        return execute_query(create_sala, (nombre, capacidad))

    @staticmethod
    def update(sala_id, nombre, capacidad):
        if not isinstance(capacidad, int) or capacidad <= CAPACITY_CHECK_NUM:
            raise ValueError("La capacidad debe ser un número entero positivo")
        execute_query(update_sala, (nombre, capacidad, sala_id))
        return sala_id

    @staticmethod
    def delete(sala_id):
        execute_query(delete_sala, (sala_id,))

    @staticmethod
    def check_availability(sala_id, dia, hora_inicio, hora_fin):
        conflictos = execute_query(
            get_disponibilidad_sala,
            (
                sala_id,
                dia,
                hora_inicio,
                hora_inicio,
                hora_fin,
                hora_fin,
                hora_inicio,
                hora_fin,
            ),
            fetch=True,
        )
        return len(conflictos) == AVAILABILITY_CHECK_NUM
