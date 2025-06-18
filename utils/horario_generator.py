import pandas as pd
from db import execute_query
from datetime import datetime, timedelta
import random
import traceback
from querys.horario_generator_queries import (
    get_creditos_curso,
    get_secciones_sin_horario_by_periodo,
    get_profesores_by_seccion,
    get_alumnos_by_seccion,
    check_disponibilidad_sala,
    check_disponibilidad_profesor,
    check_disponibilidad_alumno,
    create_horario,
    get_horarios_for_export,
    get_salas_ordered_by_capacidad,
)

HOUR_IN_SECONDS = 3600
FIRST_INDEX = 0
ZERO_COUNT = 0
CREDITS_TWO = 2
ADD_ONE = 1
DIVIDE_TO_GET_MINUTES = 60
SET_COLUMN_WIDTH = 10
SET_COLUMN_WIDTH_20 = 20
SET_COLUMN_WIDTH_30 = 30


class HorarioGenerator:
    def __init__(self):
        self.dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
        self.horas_inicio = [
            "09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"
        ]
        self.hora_almuerzo_inicio = datetime.strptime("13:00", "%H:%M").time()
        self.hora_almuerzo_fin = datetime.strptime("14:00", "%H:%M").time()
        self.hora_fin_dia = datetime.strptime("18:00", "%H:%M").time()


    def get_curso_creditos(self, curso_id):
        result = execute_query(get_creditos_curso, (curso_id,), fetch=True)
        return result[FIRST_INDEX]["creditos"] if result else CREDITS_TWO

    def get_secciones_sin_horario(self, anio, periodo):
        return execute_query(get_secciones_sin_horario_by_periodo, (anio, periodo), fetch=True)

    def get_salas_disponibles(self):
        return execute_query(get_salas_ordered_by_capacidad, fetch=True)

    def get_profesores_seccion(self, seccion_id):
        return execute_query(get_profesores_by_seccion, (seccion_id,), fetch=True)

    def get_alumnos_seccion(self, seccion_id):
        return execute_query(get_alumnos_by_seccion, (seccion_id,), fetch=True)


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
        return conflictos[FIRST_INDEX]["count"] == ZERO_COUNT

    def check_sala_disponible(self, sala_id, dia, hora_inicio, hora_fin):
        return self.check_disponibilidad(check_disponibilidad_sala, sala_id, dia, hora_inicio, hora_fin)

    def check_profesor_disponible(self, profesor_id, dia, hora_inicio, hora_fin):
        return self.check_disponibilidad(check_disponibilidad_profesor, profesor_id, dia, hora_inicio, hora_fin)

    def check_alumno_disponible(self, alumno_id, dia, hora_inicio, hora_fin):
        return self.check_disponibilidad(check_disponibilidad_alumno, alumno_id, dia, hora_inicio, hora_fin)


    def asignar_horario(self, seccion_id, sala_id, dia, hora_inicio, hora_fin):
        execute_query(create_horario, (seccion_id, sala_id, dia, hora_inicio, hora_fin))

    def es_horario_valido(self, hora_inicio, hora_fin):
        if hora_fin > self.hora_fin_dia:
            return False
        if hora_inicio < self.hora_almuerzo_inicio and hora_fin > self.hora_almuerzo_inicio:
            return False
        return True


    def generar_horarios(self, anio, periodo):
        secciones = self.get_secciones_sin_horario(anio, periodo)
        salas = self.get_salas_disponibles()
        resultados = self._init_resultados(secciones, salas)
        if resultados["estado"] != "ok":
            return resultados

        for seccion in secciones:
            self._procesar_seccion(seccion, salas, resultados)
        return resultados

    def _init_resultados(self, secciones, salas):
        if not secciones:
            return {
                "estado": "no_secciones",
                "mensaje": "No hay secciones sin horario asignado",
                "total": ZERO_COUNT,
                "asignados": ZERO_COUNT,
                "no_asignados": ZERO_COUNT,
                "secciones_asignadas": [],
                "secciones_no_asignadas": [],
            }
        if not salas:
            return {
                "estado": "no_salas",
                "mensaje": "No hay salas disponibles",
                "total": ZERO_COUNT,
                "asignados": ZERO_COUNT,
                "no_asignados": ZERO_COUNT,
                "secciones_asignadas": [],
                "secciones_no_asignadas": [],
            }
        return {
            "estado": "ok",
            "mensaje": "Horarios generados correctamente",
            "total": len(secciones),
            "asignados": ZERO_COUNT,
            "no_asignados": ZERO_COUNT,
            "secciones_asignadas": [],
            "secciones_no_asignadas": [],
        }

    def _procesar_seccion(self, seccion, salas, resultados):
        seccion_id = seccion["id"]
        curso_codigo = seccion["codigo"]
        curso_id = seccion["curso_id"]
        creditos = self.get_curso_creditos(curso_id)

        if creditos > 4:
            self._registrar_no_asignado(resultados, seccion_id, curso_codigo, f"El curso tiene {creditos} créditos, excede el máximo de 4 horas consecutivas")
            return

        profesores = self.get_profesores_seccion(seccion_id)
        alumnos = self.get_alumnos_seccion(seccion_id)

        if not profesores:
            self._registrar_no_asignado(resultados, seccion_id, curso_codigo, "La sección no tiene profesores asignados")
            return

        horario_asignado = self._buscar_y_asignar_horario(seccion_id, curso_codigo, creditos, profesores, alumnos, salas, resultados)
        if not horario_asignado:
            self._registrar_no_asignado(resultados, seccion_id, curso_codigo, "No se encontró un horario disponible sin conflictos")

    def _registrar_no_asignado(self, resultados, seccion_id, curso_codigo, motivo):
        resultados["no_asignados"] += ADD_ONE
        resultados["secciones_no_asignadas"].append({
            "seccion_id": seccion_id,
            "curso_codigo": curso_codigo,
            "motivo": motivo,
        })

    def _buscar_y_asignar_horario(self, seccion_id, curso_codigo, creditos, profesores, alumnos, salas, resultados):
        for dia in random.sample(self.dias, len(self.dias)):
            for hora_inicio_str in random.sample(self.horas_inicio, len(self.horas_inicio)):
                hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
                hora_fin = (datetime.combine(datetime.today(), hora_inicio) + timedelta(hours=creditos)).time()
                if not self.es_horario_valido(hora_inicio, hora_fin):
                    continue
                for sala in salas:
                    if self._puede_asignar(sala, alumnos, dia, hora_inicio, hora_fin, profesores):
                        self.asignar_horario(seccion_id, sala["id"], dia, hora_inicio, hora_fin)
                        self._registrar_asignado(resultados, seccion_id, curso_codigo, sala, dia, hora_inicio, hora_fin)
                        return True
        return False

    def _puede_asignar(self, sala, alumnos, dia, hora_inicio, hora_fin, profesores):
        if len(alumnos) > sala["capacidad"]:
            return False
        if not self.check_sala_disponible(sala["id"], dia, hora_inicio, hora_fin):
            return False
        if not all(self.check_profesor_disponible(profesor["id"], dia, hora_inicio, hora_fin) for profesor in profesores):
            return False
        if not all(self.check_alumno_disponible(alumno["id"], dia, hora_inicio, hora_fin) for alumno in alumnos):
            return False
        return True

    def _registrar_asignado(self, resultados, seccion_id, curso_codigo, sala, dia, hora_inicio, hora_fin):
        resultados["asignados"] += ADD_ONE
        resultados["secciones_asignadas"].append({
            "seccion_id": seccion_id,
            "curso_codigo": curso_codigo,
            "sala_id": sala["id"],
            "sala_nombre": sala["nombre"],
            "dia": dia,
            "hora_inicio": hora_inicio.strftime("%H:%M"),
            "hora_fin": hora_fin.strftime("%H:%M"),
        })

    def exportar_horarios_excel(self, anio, periodo, file_path):
        try:
            horarios_db = execute_query(get_horarios_for_export, (anio, periodo), fetch=True)
            if not horarios_db:
                return {"estado": "no_horarios", "mensaje": "No hay horarios para exportar"}

            datos_procesados = [self._procesar_fila_horario(dict(row)) for row in horarios_db]
            df = pd.DataFrame(datos_procesados)
            self._exportar_a_excel(df, file_path)
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
                "detalle": error_trace,
            }

    def _procesar_fila_horario(self, fila):
        for campo in ["hora_inicio", "hora_fin"]:
            if campo in fila and isinstance(fila[campo], timedelta):
                total_segundos = fila[campo].total_seconds()
                horas = int(total_segundos // HOUR_IN_SECONDS)
                minutos = int((total_segundos % HOUR_IN_SECONDS) // DIVIDE_TO_GET_MINUTES)
                fila[campo] = f"{horas:02d}:{minutos:02d}"
        return fila

    def _exportar_a_excel(self, df, file_path):
        df_salas = df if "sala_nombre" not in df.columns else df.sort_values(["sala_nombre", "dia", "hora_inicio"])
        df_cursos = df if "curso_codigo" not in df.columns else df.sort_values(["curso_codigo", "seccion_numero", "dia", "hora_inicio"])
        df_profesores = df if "profesor_nombre" not in df.columns else df.sort_values(["profesor_nombre", "dia", "hora_inicio"])

        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Horarios", index=False)
            df_salas.to_excel(writer, sheet_name="Salas", index=False)
            df_cursos.to_excel(writer, sheet_name="Cursos", index=False)
            df_profesores.to_excel(writer, sheet_name="Profesores", index=False)

            workbook = writer.book
            hora_format = workbook.add_format({"num_format": "hh:mm"})
            for sheet_name, worksheet in {
                "Horarios": writer.sheets["Horarios"],
                "Salas": writer.sheets["Salas"],
                "Cursos": writer.sheets["Cursos"],
                "Profesores": writer.sheets["Profesores"],
            }.items():
                for counter, col in enumerate(df.columns):
                    if col in ("hora_inicio", "hora_fin"):
                        worksheet.set_column(counter + ADD_ONE, counter + ADD_ONE, SET_COLUMN_WIDTH, hora_format)
                worksheet.set_column("A:A", SET_COLUMN_WIDTH)
                worksheet.set_column("B:B", SET_COLUMN_WIDTH)
                worksheet.set_column("E:E", SET_COLUMN_WIDTH_30)
                worksheet.set_column("F:F", SET_COLUMN_WIDTH)
                worksheet.set_column("G:G", SET_COLUMN_WIDTH_20)
                worksheet.set_column("H:H", SET_COLUMN_WIDTH)
                worksheet.set_column("I:I", SET_COLUMN_WIDTH_30)
