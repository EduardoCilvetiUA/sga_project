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

class Reporte:
    @staticmethod
    def get_notas_instancia_topico(instancia_evaluacion_id):
        if not instancia_evaluacion_id:
            raise ValueError("ID de instancia de evaluación es requerido")
        
        notas = execute_query(
            get_notas_instancia_topico, 
            (instancia_evaluacion_id,), 
            fetch=True
        )
        
        if not notas:
            return None
        
        info_reporte = {
            'curso_codigo': notas[START_INDEX]['curso_codigo'],
            'curso_nombre': notas[START_INDEX]['curso_nombre'],
            'anio': notas[START_INDEX]['anio'],
            'periodo': notas[START_INDEX]['periodo'],
            'seccion_numero': notas[START_INDEX]['seccion_numero'],
            'topico_nombre': notas[START_INDEX]['topico_nombre'],
            'instancia_nombre': notas[START_INDEX]['instancia_nombre'],
            'total_alumnos': len(notas),
            'promedio': round(sum(nota['nota'] for nota in notas) / len(notas), 2),
            'nota_maxima': max(nota['nota'] for nota in notas),
            'nota_minima': min(nota['nota'] for nota in notas),
            'aprobados': len([nota for nota in notas if nota['nota'] >= MIN_NOTA_APROBACION]),
            'reprobados': len([nota for nota in notas if nota['nota'] < MIN_NOTA_APROBACION])
        }
        
        return {
            'info': info_reporte,
            'notas': notas
        }
    
    @staticmethod
    def get_notas_finales_seccion(seccion_id):
        if not seccion_id:
            raise ValueError("ID de sección es requerido")
        
        instancia_cerrada = execute_query(
            check_curso_cerrado_by_seccion, 
            (seccion_id,), 
            fetch=True
        )
        
        if not instancia_cerrada or not instancia_cerrada[START_INDEX]['cerrado']:
            raise ValueError("La instancia del curso debe estar cerrada para generar este reporte")
        
        notas = execute_query(
            get_notas_finales_seccion, 
            (seccion_id,), 
            fetch=True
        )
        
        if not notas:
            return None
        
        info_reporte = {
            'curso_codigo': notas[START_INDEX]['curso_codigo'],
            'curso_nombre': notas[START_INDEX]['curso_nombre'],
            'anio': notas[START_INDEX]['anio'],
            'periodo': notas[START_INDEX]['periodo'],
            'seccion_numero': notas[START_INDEX]['seccion_numero'],
            'total_alumnos': len(notas),
            'promedio': round(sum(nota['nota_final'] for nota in notas) / len(notas), 2),
            'nota_maxima': max(nota['nota_final'] for nota in notas),
            'nota_minima': min(nota['nota_final'] for nota in notas),
            'aprobados': len([nota for nota in notas if nota['aprobado']]),
            'reprobados': len([nota for nota in notas if not nota['aprobado']])
        }
        
        return {
            'info': info_reporte,
            'notas': notas
        }
    
    @staticmethod
    def get_certificado_notas_alumno(alumno_id):
        if not alumno_id:
            raise ValueError("ID de alumno es requerido")
        
        cursos = execute_query(
            get_certificado_notas_alumno, 
            (alumno_id,), 
            fetch=True
        )
        
        if not cursos:
            return None
        
        estadisticas = execute_query(
            get_estadisticas_certificado, 
            (alumno_id,), 
            fetch=True
        )
        
        info_alumno = {
            'nombre': cursos[START_INDEX]['alumno_nombre'] if cursos else '',
            'correo': cursos[START_INDEX]['alumno_correo'] if cursos else ''
        }
        
        stats = estadisticas[START_INDEX] if estadisticas else {
            'total_cursos': MIN_START,
            'cursos_aprobados': MIN_START,
            'cursos_reprobados': MIN_START,
            'promedio_general': MIN_START,
            'total_creditos': MIN_START,
            'creditos_aprobados': MIN_START,
        }
        
        return {
            'alumno': info_alumno,
            'estadisticas': stats,
            'cursos': cursos
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
        if tipo_reporte == 'instancia_topico':
            instancia_id = kwargs.get('instancia_evaluacion_id')
            if not instancia_id:
                raise ValueError("Debe seleccionar una instancia de evaluación")
            try:
                int(instancia_id)
            except (ValueError, TypeError):
                raise ValueError("ID de instancia de evaluación debe ser un número válido")
        
        elif tipo_reporte == 'notas_finales':
            seccion_id = kwargs.get('seccion_id')
            if not seccion_id:
                raise ValueError("Debe seleccionar una sección")
            try:
                int(seccion_id)
            except (ValueError, TypeError):
                raise ValueError("ID de sección debe ser un número válido")
        
        elif tipo_reporte == 'certificado':
            alumno_id = kwargs.get('alumno_id')
            if not alumno_id:
                raise ValueError("Debe seleccionar un alumno")
            try:
                int(alumno_id)
            except (ValueError, TypeError):
                raise ValueError("ID de alumno debe ser un número válido")
        
        else:
            raise ValueError("Tipo de reporte no válido")