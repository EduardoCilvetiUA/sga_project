# models/horario.py
from db import execute_query
from querys.horario_queries import (
    get_all_schedules,
    get_schedule_by_id,
    create_schedule,
    update_schedule,
    delete_schedule,
    get_schedule_by_section,
    check_disponibilidad_profesor,
    check_disponibilidad_alumno,
    get_schedule_conflicts,
)


class Horario:
    @staticmethod
    def get_all():
        return execute_query(get_all_schedules, fetch=True)

    @staticmethod
    def get_by_id(horario_id):
        result = execute_query(get_schedule_by_id, (horario_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(seccion_id, sala_id, dia, hora_inicio, hora_fin):
        conflictos = Horario.get_conflicts(
            seccion_id, sala_id, dia, hora_inicio, hora_fin
        )
        if conflictos:
            conflict_type = conflictos[0]["tipo_conflicto"]
            conflict_name = (
                conflictos[0].get("sala_nombre")
                or conflictos[0].get("profesor_nombre")
                or conflictos[0].get("alumno_nombre")
            )
            raise ValueError(
                f"Existe un conflicto de {conflict_type} con {conflict_name}"
            )

        return execute_query(
            create_schedule, (seccion_id, sala_id, dia, hora_inicio, hora_fin)
        )

    @staticmethod
    def update(horario_id, seccion_id, sala_id, dia, hora_inicio, hora_fin):
        conflictos = Horario.get_conflicts(
            seccion_id, sala_id, dia, hora_inicio, hora_fin, exclude_id=horario_id
        )
        if conflictos:
            conflict_type = conflictos[0]["tipo_conflicto"]
            conflict_name = (
                conflictos[0].get("sala_nombre")
                or conflictos[0].get("profesor_nombre")
                or conflictos[0].get("alumno_nombre")
            )
            raise ValueError(
                f"Existe un conflicto de {conflict_type} con {conflict_name}"
            )

        execute_query(
            update_schedule,
            (seccion_id, sala_id, dia, hora_inicio, hora_fin, horario_id),
        )
        return horario_id

    @staticmethod
    def delete(horario_id):
        execute_query(delete_schedule, (horario_id,))

    @staticmethod
    def get_by_section(seccion_id):
        return execute_query(get_schedule_by_section, (seccion_id,), fetch=True)

    @staticmethod
    def check_professor_conflicts(profesor_id, dia, hora_inicio, hora_fin):
        conflictos = execute_query(
            check_disponibilidad_profesor,
            (
                profesor_id,
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
        return conflictos

    @staticmethod
    def check_student_conflicts(alumno_id, dia, hora_inicio, hora_fin):
        conflictos = execute_query(
            check_disponibilidad_alumno,
            (
                alumno_id,
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
        return conflictos

    @staticmethod
    def get_conflicts(seccion_id, sala_id, dia, hora_inicio, hora_fin, exclude_id=None):
        params = [
            sala_id,
            dia,
            hora_inicio,
            hora_inicio,
            hora_fin,
            hora_fin,
            hora_inicio,
            hora_fin,
            seccion_id,
            seccion_id,
            dia,
            hora_inicio,
            hora_inicio,
            hora_fin,
            hora_fin,
            hora_inicio,
            hora_fin,
            seccion_id,
            seccion_id,
            dia,
            hora_inicio,
            hora_inicio,
            hora_fin,
            hora_fin,
            hora_inicio,
            hora_fin,
            seccion_id,
        ]

        if exclude_id:
            query = get_schedule_conflicts + " AND h.id != %s"
            params.append(exclude_id)
            params.append(exclude_id)
            params.append(exclude_id)
        else:
            query = get_schedule_conflicts

        return execute_query(query, tuple(params), fetch=True)
