import pandas as pd
from db import execute_query
from datetime import datetime, timedelta, time
import random
import traceback
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
        self.hora_almuerzo_inicio = datetime.strptime("13:00", "%H:%M").time()
        self.hora_almuerzo_fin = datetime.strptime("14:00", "%H:%M").time()
        self.hora_fin_dia = datetime.strptime("18:00", "%H:%M").time()

    def get_curso_creditos(self, curso_id):
        result = execute_query(get_course_credits, (curso_id,), fetch=True)
        return result[0]["creditos"] if result else 2

    def get_secciones_sin_horario(self, anio, periodo):
        return execute_query(get_sections_without_schedule, (anio, periodo), fetch=True)

    def get_salas_disponibles(self):
        return execute_query(
            "SELECT id, nombre, capacidad FROM salas ORDER BY capacidad DESC",
            fetch=True,
        )

    def get_profesores_seccion(self, seccion_id):
        return execute_query(get_professors_for_section, (seccion_id,), fetch=True)

    def get_alumnos_seccion(self, seccion_id):
        return execute_query(get_students_for_section, (seccion_id,), fetch=True)

    def check_disponibilidad(self, check_query, entity_id, dia, hora_inicio, hora_fin):
        conflictos = execute_query(
            check_query,
            (
                entity_id,
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

    def check_sala_disponible(self, sala_id, dia, hora_inicio, hora_fin):
        return self.check_disponibilidad(check_room_availability, sala_id, dia, hora_inicio, hora_fin)

    def check_profesor_disponible(self, profesor_id, dia, hora_inicio, hora_fin):
        return self.check_disponibilidad(check_professor_availability, profesor_id, dia, hora_inicio, hora_fin)

    def check_alumno_disponible(self, alumno_id, dia, hora_inicio, hora_fin):
        return self.check_disponibilidad(check_student_availability, alumno_id, dia, hora_inicio, hora_fin)

    def asignar_horario(self, seccion_id, sala_id, dia, hora_inicio, hora_fin):
        execute_query(
            assign_schedule, (seccion_id, sala_id, dia, hora_inicio, hora_fin)
        )

    def es_horario_valido(self, hora_inicio, hora_fin):
        if hora_fin > self.hora_fin_dia:
            return False

        if (hora_inicio < self.hora_almuerzo_inicio and hora_fin > self.hora_almuerzo_inicio):
            return False
            
        return True

    def generar_horarios(self, anio, periodo):
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

        for seccion in secciones:
            seccion_id = seccion["id"]
            curso_codigo = seccion["codigo"]
            curso_id = seccion["curso_id"]
            creditos = self.get_curso_creditos(curso_id)

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

            horario_asignado = False

            dias_random = random.sample(self.dias, len(self.dias))
            for dia in dias_random:
                if horario_asignado:
                    break

                horas_random = random.sample(self.horas_inicio, len(self.horas_inicio))
                for hora_inicio_str in horas_random:
                    if horario_asignado:
                        break

                    hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
                    datetime_inicio = datetime.combine(datetime.today(), hora_inicio)
                    datetime_fin = datetime_inicio + timedelta(hours=creditos)
                    hora_fin = datetime_fin.time()

                    if not self.es_horario_valido(hora_inicio, hora_fin):
                        continue

                    for sala in salas:
                        sala_id = sala["id"]
                        capacidad = sala["capacidad"]

                        if len(alumnos) > capacidad:
                            continue

                        if not self.check_sala_disponible(
                            sala_id, dia, hora_inicio, hora_fin
                        ):
                            continue

                        if not all(self.check_profesor_disponible(
                                profesor["id"], dia, hora_inicio, hora_fin
                            ) for profesor in profesores):
                            continue

                        if not all(self.check_alumno_disponible(
                                alumno["id"], dia, hora_inicio, hora_fin
                            ) for alumno in alumnos):
                            continue

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
        try:
            horarios_db = execute_query(
                get_schedules_for_export, (anio, periodo), fetch=True
            )

            if not horarios_db:
                return {
                    "estado": "no_horarios",
                    "mensaje": "No hay horarios para exportar",
                }

            datos_procesados = []
            
            for row in horarios_db:
                fila = dict(row)
                
                if 'hora_inicio' in fila:
                    if isinstance(fila['hora_inicio'], timedelta):
                        total_segundos = fila['hora_inicio'].total_seconds()
                        horas = int(total_segundos // 3600)
                        minutos = int((total_segundos % 3600) // 60)
                        fila['hora_inicio'] = f"{horas:02d}:{minutos:02d}"
                
                if 'hora_fin' in fila:
                    if isinstance(fila['hora_fin'], timedelta):
                        total_segundos = fila['hora_fin'].total_seconds()
                        horas = int(total_segundos // 3600)
                        minutos = int((total_segundos % 3600) // 60)
                        fila['hora_fin'] = f"{horas:02d}:{minutos:02d}"
                
                datos_procesados.append(fila)
            
            df = pd.DataFrame(datos_procesados)
            
            df_salas = df.copy() if 'sala_nombre' not in df.columns else df.copy().sort_values(["sala_nombre", "dia", "hora_inicio"])
            df_cursos = df.copy() if 'curso_codigo' not in df.columns else df.copy().sort_values(["curso_codigo", "seccion_numero", "dia", "hora_inicio"])
            df_profesores = df.copy() if 'profesor_nombre' not in df.columns else df.copy().sort_values(["profesor_nombre", "dia", "hora_inicio"])

            with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="Horarios", index=False)
                df_salas.to_excel(writer, sheet_name="Salas", index=False)
                df_cursos.to_excel(writer, sheet_name="Cursos", index=False)
                df_profesores.to_excel(writer, sheet_name="Profesores", index=False)

                workbook = writer.book
                hora_format = workbook.add_format({'num_format': 'hh:mm'})
                
                for sheet_name, worksheet in {
                    "Horarios": writer.sheets["Horarios"],
                    "Salas": writer.sheets["Salas"],
                    "Cursos": writer.sheets["Cursos"],
                    "Profesores": writer.sheets["Profesores"]
                }.items():
                    for i, col in enumerate(df.columns):
                        if col == 'hora_inicio' or col == 'hora_fin':
                            worksheet.set_column(i + 1, i + 1, 10, hora_format)
                    
                    worksheet.set_column('A:A', 10)
                    worksheet.set_column('B:B', 10)
                    worksheet.set_column('E:E', 20)
                    worksheet.set_column('F:F', 10)
                    worksheet.set_column('G:G', 30)
                    worksheet.set_column('H:H', 10)
                    worksheet.set_column('I:I', 20)

            return {
                "estado": "exito",
                "mensaje": f"Horarios exportados exitosamente a {file_path}",
                "ruta_archivo": file_path,
            }

        except Exception as e:
            error_trace = traceback.format_exc()
            return {
                "estado": "error",
                "mensaje": f"Error al exportar horarios: {str(e)}",
                "detalle": error_trace
            }