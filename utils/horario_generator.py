import pandas as pd
from db import execute_query
from datetime import datetime, timedelta
import random
from querys.horario_generator_queries import (
    get_course_credits,
    get_sections_without_schedule,
    get_professors_for_section,
    get_students_for_section,
    check_room_availability,
    check_professor_availability,
    check_student_availability,
    assign_schedule,
    get_schedules_for_export,
)


class HorarioGenerator:
    def __init__(self):
        self.dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
        self.horas_inicio = [
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
        ]

    def get_curso_creditos(self, curso_id):
        """Obtiene los créditos de un curso"""
        result = execute_query(get_course_credits, (curso_id,), fetch=True)
        return result[0]["creditos"] if result else 2

    def get_secciones_sin_horario(self, anio, periodo):
        """Obtiene todas las secciones que no tienen horario asignado"""
        return execute_query(get_sections_without_schedule, (anio, periodo), fetch=True)

    def get_salas_disponibles(self):
        """Obtiene todas las salas disponibles"""
        return execute_query(
            "SELECT id, nombre, capacidad FROM salas ORDER BY capacidad DESC",
            fetch=True,
        )

    def get_profesores_seccion(self, seccion_id):
        """Obtiene los profesores de una sección"""
        return execute_query(get_professors_for_section, (seccion_id,), fetch=True)

    def get_alumnos_seccion(self, seccion_id):
        """Obtiene los alumnos de una sección"""
        return execute_query(get_students_for_section, (seccion_id,), fetch=True)

    def check_sala_disponible(self, sala_id, dia, hora_inicio, hora_fin):
        """Verifica si una sala está disponible en un horario específico"""
        conflictos = execute_query(
            check_room_availability,
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
        return conflictos[0]["count"] == 0

    def check_profesor_disponible(self, profesor_id, dia, hora_inicio, hora_fin):
        """Verifica si un profesor está disponible en un horario específico"""
        conflictos = execute_query(
            check_professor_availability,
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
        return conflictos[0]["count"] == 0

    def check_alumno_disponible(self, alumno_id, dia, hora_inicio, hora_fin):
        """Verifica si un alumno está disponible en un horario específico"""
        conflictos = execute_query(
            check_student_availability,
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
        return conflictos[0]["count"] == 0

    def asignar_horario(self, seccion_id, sala_id, dia, hora_inicio, hora_fin):
        """Asigna un horario a una sección"""
        execute_query(
            assign_schedule, (seccion_id, sala_id, dia, hora_inicio, hora_fin)
        )

    def generar_horarios(self, anio, periodo):
        """
        Genera horarios para todas las secciones del semestre
        Retorna un reporte con los resultados
        """
        secciones = self.get_secciones_sin_horario(anio, periodo)
        salas = self.get_salas_disponibles()

        if not secciones:
            return {
                "estado": "no_secciones",
                "mensaje": "No hay secciones sin horario asignado",
                "total": 0,
                "asignados": 0,
                "no_asignados": 0,
                "secciones_asignadas": [],
                "secciones_no_asignadas": [],
            }

        if not salas:
            return {
                "estado": "no_salas",
                "mensaje": "No hay salas disponibles",
                "total": 0,
                "asignados": 0,
                "no_asignados": 0,
                "secciones_asignadas": [],
                "secciones_no_asignadas": [],
            }

        resultados = {
            "estado": "ok",
            "mensaje": "Horarios generados correctamente",
            "total": len(secciones),
            "asignados": 0,
            "no_asignados": 0,
            "secciones_asignadas": [],
            "secciones_no_asignadas": [],
        }

        # Procesamos las secciones en orden descendente de créditos
        for seccion in secciones:
            seccion_id = seccion["id"]
            seccion_num = seccion["numero"]
            curso_codigo = seccion["codigo"]
            curso_id = seccion["curso_id"]
            curso_nombre = seccion["nombre"]
            creditos = self.get_curso_creditos(curso_id)

            # Verificamos que los créditos no excedan las horas disponibles
            if creditos > 4:
                resultados["no_asignados"] += 1
                resultados["secciones_no_asignadas"].append(
                    {
                        "seccion_id": seccion_id,
                        "curso_codigo": curso_codigo,
                        "motivo": f"El curso tiene {creditos} créditos, excede el máximo de 4 horas consecutivas",
                    }
                )
                continue

            # Obtenemos los profesores y alumnos de la sección
            profesores = self.get_profesores_seccion(seccion_id)
            alumnos = self.get_alumnos_seccion(seccion_id)

            if not profesores:
                resultados["no_asignados"] += 1
                resultados["secciones_no_asignadas"].append(
                    {
                        "seccion_id": seccion_id,
                        "curso_codigo": curso_codigo,
                        "motivo": "La sección no tiene profesores asignados",
                    }
                )
                continue

            # Buscamos un horario disponible
            horario_asignado = False

            # Intentamos con diferentes combinaciones de días y horas
            dias_random = random.sample(self.dias, len(self.dias))
            for dia in dias_random:
                if horario_asignado:
                    break

                horas_random = random.sample(self.horas_inicio, len(self.horas_inicio))
                for hora_inicio_str in horas_random:
                    if horario_asignado:
                        break

                    hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
                    hora_fin = (
                        datetime.combine(datetime.today(), hora_inicio)
                        + timedelta(hours=creditos)
                    ).time()

                    # Verificar que no exceda las 18:00
                    if hora_fin > datetime.strptime("18:00", "%H:%M").time():
                        continue

                    # Verificar que no incluya la hora de almuerzo (13:00-14:00)
                    if (
                        hora_inicio < datetime.strptime("13:00", "%H:%M").time()
                        and hora_fin > datetime.strptime("13:00", "%H:%M").time()
                    ):
                        continue

                    # Buscamos una sala disponible con capacidad suficiente
                    for sala in salas:
                        sala_id = sala["id"]
                        capacidad = sala["capacidad"]

                        # Verificar que la sala tenga capacidad suficiente
                        if len(alumnos) > capacidad:
                            continue

                        # Verificar disponibilidad de sala
                        if not self.check_sala_disponible(
                            sala_id, dia, hora_inicio, hora_fin
                        ):
                            continue

                        # Verificar disponibilidad de profesores
                        profesores_disponibles = True
                        for profesor in profesores:
                            if not self.check_profesor_disponible(
                                profesor["id"], dia, hora_inicio, hora_fin
                            ):
                                profesores_disponibles = False
                                break

                        if not profesores_disponibles:
                            continue

                        # Verificar disponibilidad de alumnos
                        alumnos_disponibles = True
                        for alumno in alumnos:
                            if not self.check_alumno_disponible(
                                alumno["id"], dia, hora_inicio, hora_fin
                            ):
                                alumnos_disponibles = False
                                break

                        if not alumnos_disponibles:
                            continue

                        # Si llegamos aquí, tenemos un horario disponible
                        self.asignar_horario(
                            seccion_id, sala_id, dia, hora_inicio, hora_fin
                        )

                        resultados["asignados"] += 1
                        resultados["secciones_asignadas"].append(
                            {
                                "seccion_id": seccion_id,
                                "curso_codigo": curso_codigo,
                                "sala_id": sala_id,
                                "sala_nombre": sala["nombre"],
                                "dia": dia,
                                "hora_inicio": hora_inicio.strftime("%H:%M"),
                                "hora_fin": hora_fin.strftime("%H:%M"),
                            }
                        )

                        horario_asignado = True
                        break

            # Si no se pudo asignar horario
            if not horario_asignado:
                resultados["no_asignados"] += 1
                resultados["secciones_no_asignadas"].append(
                    {
                        "seccion_id": seccion_id,
                        "curso_codigo": curso_codigo,
                        "motivo": "No se encontró un horario disponible sin conflictos",
                    }
                )

        return resultados

    def exportar_horarios_excel(self, anio, periodo, file_path):
        """
        Exporta los horarios a un archivo Excel
        Retorna True si se exportó correctamente, False en caso contrario
        """
        try:
            # Obtener todos los horarios del semestre
            horarios = execute_query(
                get_schedules_for_export, (anio, periodo), fetch=True
            )

            if not horarios:
                return {
                    "estado": "no_horarios",
                    "mensaje": "No hay horarios para exportar",
                }

            # Crear un dataframe para el Excel
            df = pd.DataFrame(horarios)

            # Crear un segundo dataframe para la vista por sala
            df_salas = df.copy()

            # Crear Excel con múltiples hojas
            with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
                # Hoja 1: Horarios por día y hora
                df.to_excel(writer, sheet_name="Horarios", index=False)

                # Hoja 2: Horarios por sala
                df_salas.sort_values(
                    ["sala_nombre", "dia", "hora_inicio"], inplace=True
                )
                df_salas.to_excel(writer, sheet_name="Salas", index=False)

                # Hoja 3: Horarios por curso
                df_cursos = df.copy()
                df_cursos.sort_values(
                    ["curso_codigo", "seccion_numero", "dia", "hora_inicio"],
                    inplace=True,
                )
                df_cursos.to_excel(writer, sheet_name="Cursos", index=False)

                # Hoja 4: Horarios por profesor
                df_profesores = df.copy()
                df_profesores.sort_values(
                    ["profesor_nombre", "dia", "hora_inicio"], inplace=True
                )
                df_profesores.to_excel(writer, sheet_name="Profesores", index=False)

                # Dar formato a las hojas
                workbook = writer.book

                # Formato para las horas
                hora_format = workbook.add_format({"num_format": "hh:mm"})

                # Aplicar formatos a todas las hojas
                for sheet_name in ["Horarios", "Salas", "Cursos", "Profesores"]:
                    worksheet = writer.sheets[sheet_name]

                    # Establecer el ancho de las columnas
                    worksheet.set_column("A:A", 10)  # Día
                    worksheet.set_column("B:C", 10, hora_format)  # Hora inicio y fin
                    worksheet.set_column("D:D", 20)  # Sala
                    worksheet.set_column("E:E", 10)  # Código curso
                    worksheet.set_column("F:F", 30)  # Nombre curso
                    worksheet.set_column("G:G", 10)  # Sección
                    worksheet.set_column("H:H", 20)  # Profesor

            return {
                "estado": "exito",
                "mensaje": f"Horarios exportados exitosamente a {file_path}",
                "ruta_archivo": file_path,
            }
        except Exception as e:
            return {
                "estado": "error",
                "mensaje": f"Error al exportar horarios: {str(e)}",
            }
