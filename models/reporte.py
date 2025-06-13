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


class Reporte:
    @staticmethod
    def get_notas_instancia_topico(instancia_evaluacion_id):
        """
        Reporte A: Obtiene las notas de una instancia de tópico específica
        """
        if not instancia_evaluacion_id:
            raise ValueError("ID de instancia de evaluación es requerido")
        
        notas = execute_query(
            get_notas_instancia_topico, 
            (instancia_evaluacion_id,), 
            fetch=True
        )
        
        if not notas:
            return None
        
        # Información general del reporte
        info_reporte = {
            'curso_codigo': notas[0]['curso_codigo'],
            'curso_nombre': notas[0]['curso_nombre'],
            'anio': notas[0]['anio'],
            'periodo': notas[0]['periodo'],
            'seccion_numero': notas[0]['seccion_numero'],
            'topico_nombre': notas[0]['topico_nombre'],
            'instancia_nombre': notas[0]['instancia_nombre'],
            'total_alumnos': len(notas),
            'promedio': round(sum(nota['nota'] for nota in notas) / len(notas), 2),
            'nota_maxima': max(nota['nota'] for nota in notas),
            'nota_minima': min(nota['nota'] for nota in notas),
            'aprobados': len([n for n in notas if n['nota'] >= 4.0]),
            'reprobados': len([n for n in notas if n['nota'] < 4.0])
        }
        
        return {
            'info': info_reporte,
            'notas': notas
        }
    
    @staticmethod
    def get_notas_finales_seccion(seccion_id):
        """
        Reporte B: Obtiene las notas finales de una sección (solo cursos cerrados)
        """
        if not seccion_id:
            raise ValueError("ID de sección es requerido")
        
        # Verificar que el curso esté cerrado
        curso_cerrado = execute_query(
            check_curso_cerrado_by_seccion, 
            (seccion_id,), 
            fetch=True
        )
        
        if not curso_cerrado or not curso_cerrado[0]['cerrado']:
            raise ValueError("El curso debe estar cerrado para generar este reporte")
        
        notas = execute_query(
            get_notas_finales_seccion, 
            (seccion_id,), 
            fetch=True
        )
        
        if not notas:
            return None
        
        # Información general del reporte
        info_reporte = {
            'curso_codigo': notas[0]['curso_codigo'],
            'curso_nombre': notas[0]['curso_nombre'],
            'anio': notas[0]['anio'],
            'periodo': notas[0]['periodo'],
            'seccion_numero': notas[0]['seccion_numero'],
            'total_alumnos': len(notas),
            'promedio': round(sum(nota['nota_final'] for nota in notas) / len(notas), 2),
            'nota_maxima': max(nota['nota_final'] for nota in notas),
            'nota_minima': min(nota['nota_final'] for nota in notas),
            'aprobados': len([n for n in notas if n['aprobado']]),
            'reprobados': len([n for n in notas if not n['aprobado']])
        }
        
        return {
            'info': info_reporte,
            'notas': notas
        }
    
    @staticmethod
    def get_certificado_notas_alumno(alumno_id):
        """
        Reporte C: Obtiene el certificado de notas de un alumno (todos los cursos cerrados)
        """
        if not alumno_id:
            raise ValueError("ID de alumno es requerido")
        
        cursos = execute_query(
            get_certificado_notas_alumno, 
            (alumno_id,), 
            fetch=True
        )
        
        if not cursos:
            return None
        
        # Obtener estadísticas
        estadisticas = execute_query(
            get_estadisticas_certificado, 
            (alumno_id,), 
            fetch=True
        )
        
        info_alumno = {
            'nombre': cursos[0]['alumno_nombre'] if cursos else '',
            'correo': cursos[0]['alumno_correo'] if cursos else ''
        }
        
        stats = estadisticas[0] if estadisticas else {
            'total_cursos': 0,
            'cursos_aprobados': 0,
            'cursos_reprobados': 0,
            'promedio_general': 0,
            'total_creditos': 0,
            'creditos_aprobados': 0
        }
        
        return {
            'alumno': info_alumno,
            'estadisticas': stats,
            'cursos': cursos
        }
    
    @staticmethod
    def get_instancias_evaluacion_disponibles():
        """
        Obtiene todas las instancias de evaluación para el selector del reporte A
        """
        return execute_query(get_instancias_evaluacion_for_report, fetch=True)
    
    @staticmethod
    def get_secciones_cursos_cerrados():
        """
        Obtiene todas las secciones de cursos cerrados para el reporte B
        """
        return execute_query(get_secciones_cursos_cerrados, fetch=True)
    
    @staticmethod
    def get_alumnos_disponibles():
        """
        Obtiene todos los alumnos para el reporte C
        """
        return execute_query(get_alumnos_for_certificado, fetch=True)
    
    @staticmethod
    def validate_reporte_inputs(tipo_reporte, **kwargs):
        """
        Valida las entradas para los diferentes tipos de reporte
        """
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