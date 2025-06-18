from db import execute_query
from querys.reporte_queries import (
    get_notas_instancia_topico,
    get_notas_finales_seccion,
    check_curso_cerrado_by_seccion,
    get_certificado_notas_alumno,
    get_instancias_evaluacion_for_report,
    get_secciones_cursos_cerrados,
    get_alumnos_for_certificado,
    get_estadisticas_certificado,
)

MIN_START = 0
MIN_NOTA_APROBACION = 4.0
START_INDEX = 0
ROUND_BY_TWO = 2

class Reporte:
    @staticmethod
    def get_notas_instancia_topico(instancia_evaluacion_id):
        Reporte._validate_id(instancia_evaluacion_id, "ID de instancia de evaluación es requerido")
        notas = execute_query(get_notas_instancia_topico, (instancia_evaluacion_id,), fetch=True)
        if not notas:
            return None
        info_reporte = Reporte._build_info_reporte_instancia_topico(notas)
        return {"info": info_reporte, "notas": notas}

    @staticmethod
    def _build_info_reporte_instancia_topico(notas):
        return {
            "curso_codigo": notas[START_INDEX]["curso_codigo"],
            "curso_nombre": notas[START_INDEX]["curso_nombre"],
            "anio": notas[START_INDEX]["anio"],
            "periodo": notas[START_INDEX]["periodo"],
            "seccion_numero": notas[START_INDEX]["seccion_numero"],
            "topico_nombre": notas[START_INDEX]["topico_nombre"],
            "instancia_nombre": notas[START_INDEX]["instancia_nombre"],
            "total_alumnos": len(notas),
            "promedio": round(sum(nota["nota"] for nota in notas) / len(notas), ROUND_BY_TWO),
            "nota_maxima": max(nota["nota"] for nota in notas),
            "nota_minima": min(nota["nota"] for nota in notas),
            "aprobados": len([nota for nota in notas if nota["nota"] >= MIN_NOTA_APROBACION]),
            "reprobados": len([nota for nota in notas if nota["nota"] < MIN_NOTA_APROBACION]),
        }

    @staticmethod
    def get_notas_finales_seccion(seccion_id):
        Reporte._validate_id(seccion_id, "ID de sección es requerido")
        Reporte._validate_curso_cerrado(seccion_id)
        notas = execute_query(get_notas_finales_seccion, (seccion_id,), fetch=True)
        if not notas:
            return None
        info_reporte = Reporte._build_info_reporte_finales_seccion(notas)
        return {"info": info_reporte, "notas": notas}

    @staticmethod
    def _build_info_reporte_finales_seccion(notas):
        return {
            "curso_codigo": notas[START_INDEX]["curso_codigo"],
            "curso_nombre": notas[START_INDEX]["curso_nombre"],
            "anio": notas[START_INDEX]["anio"],
            "periodo": notas[START_INDEX]["periodo"],
            "seccion_numero": notas[START_INDEX]["seccion_numero"],
            "total_alumnos": len(notas),
            "promedio": round(sum(nota["nota_final"] for nota in notas) / len(notas), ROUND_BY_TWO),
            "nota_maxima": max(nota["nota_final"] for nota in notas),
            "nota_minima": min(nota["nota_final"] for nota in notas),
            "aprobados": len([nota for nota in notas if nota["aprobado"]]),
            "reprobados": len([nota for nota in notas if not nota["aprobado"]]),
        }

    @staticmethod
    def _validate_curso_cerrado(seccion_id):
        instancia_cerrada = execute_query(check_curso_cerrado_by_seccion, (seccion_id,), fetch=True)
        if not instancia_cerrada or not instancia_cerrada[START_INDEX]["cerrado"]:
            raise ValueError("La instancia del curso debe estar cerrada para generar este reporte")

    @staticmethod
    def get_certificado_notas_alumno(alumno_id):
        Reporte._validate_id(alumno_id, "ID de alumno es requerido")
        cursos = execute_query(get_certificado_notas_alumno, (alumno_id,), fetch=True)
        if not cursos:
            return None
        estadisticas = execute_query(get_estadisticas_certificado, (alumno_id,), fetch=True)
        info_alumno = Reporte._build_info_alumno(cursos)
        stats = Reporte._build_stats_certificado(estadisticas)
        return {"alumno": info_alumno, "estadisticas": stats, "cursos": cursos}

    @staticmethod
    def _build_info_alumno(cursos):
        return {
            "nombre": cursos[START_INDEX]["alumno_nombre"] if cursos else "",
            "correo": cursos[START_INDEX]["alumno_correo"] if cursos else "",
        }

    @staticmethod
    def _build_stats_certificado(estadisticas):
        if estadisticas:
            return estadisticas[START_INDEX]
        return {
            "total_cursos": MIN_START,
            "cursos_aprobados": MIN_START,
            "cursos_reprobados": MIN_START,
            "promedio_general": MIN_START,
            "total_creditos": MIN_START,
            "creditos_aprobados": MIN_START,
        }

    @staticmethod
    def get_instancias_evaluacion_disponibles():
        return execute_query(get_instancias_evaluacion_for_report, fetch=True)

    @staticmethod
    def get_secciones_cursos_cerrados():
        return execute_query(get_secciones_cursos_cerrados, fetch=True)

    @staticmethod
    def get_alumnos_disponibles():
        return execute_query(get_alumnos_for_certificado, fetch=True)

    @staticmethod
    def validate_reporte_inputs(tipo_reporte, **kwargs):
        if tipo_reporte == "instancia_topico":
            Reporte._validate_numeric_input(kwargs.get("instancia_evaluacion_id"), "Debe seleccionar una instancia de evaluación", "ID de instancia de evaluación debe ser un número válido")
        elif tipo_reporte == "notas_finales":
            Reporte._validate_numeric_input(kwargs.get("seccion_id"), "Debe seleccionar una sección", "ID de sección debe ser un número válido")
        elif tipo_reporte == "certificado":
            Reporte._validate_numeric_input(kwargs.get("alumno_id"), "Debe seleccionar un alumno", "ID de alumno debe ser un número válido")
        else:
            raise ValueError("Tipo de reporte no válido")

    @staticmethod
    def _validate_id(value, error_message):
        if not value:
            raise ValueError(error_message)

    @staticmethod
    def _validate_numeric_input(value, empty_msg, invalid_msg):
        if not value:
            raise ValueError(empty_msg)
        try:
            int(value)
        except (ValueError, TypeError):
            raise ValueError(invalid_msg)
