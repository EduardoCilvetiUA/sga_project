# Reporte A: Notas de una instancia de tópico específica
get_notas_instancia_topico = """
SELECT 
    a.nombre as alumno_nombre,
    a.correo as alumno_correo,
    n.nota,
    c.codigo as curso_codigo,
    c.nombre as curso_nombre,
    ic.anio,
    ic.periodo,
    s.numero as seccion_numero,
    te.nombre as topico_nombre,
    ie.nombre as instancia_nombre
FROM notas n
JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
JOIN alumnos a ON als.alumno_id = a.id
JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
JOIN topicos_evaluacion te ON ie.topico_id = te.id
JOIN secciones s ON te.seccion_id = s.id
JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
WHERE ie.id = %s
ORDER BY a.nombre;
"""

# Reporte B: Notas finales de una sección (solo cursos cerrados)
get_notas_finales_seccion = """
SELECT 
    a.id as alumno_id,
    a.nombre as alumno_nombre,
    a.correo as alumno_correo,
    ca.nota_final,
    ca.aprobado,
    ca.fecha_aprobacion,
    c.codigo as curso_codigo,
    c.nombre as curso_nombre,
    ic.anio,
    ic.periodo,
    s.numero as seccion_numero
FROM cursos_aprobados ca
JOIN alumnos a ON ca.alumno_id = a.id
JOIN cursos c ON ca.curso_id = c.id
JOIN secciones s ON ca.seccion_id = s.id
JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
WHERE s.id = %s AND c.cerrado = 1
ORDER BY a.nombre;
"""

# Verificar si un curso está cerrado
check_curso_cerrado_by_seccion = """
SELECT c.cerrado
FROM cursos c
JOIN instancias_curso ic ON c.id = ic.curso_id
JOIN secciones s ON ic.id = s.instancia_curso_id
WHERE s.id = %s;
"""

# Reporte C: Certificado de notas de un alumno (todos los cursos cerrados)
get_certificado_notas_alumno = """
SELECT 
    c.codigo as curso_codigo,
    c.nombre as curso_nombre,
    c.creditos,
    ic.anio,
    ic.periodo,
    s.numero as seccion_numero,
    ca.nota_final,
    ca.aprobado,
    ca.fecha_aprobacion,
    CASE 
        WHEN ic.periodo = '1' THEN CONCAT(ic.anio, ' - Primer Semestre')
        WHEN ic.periodo = '2' THEN CONCAT(ic.anio, ' - Segundo Semestre')
        WHEN ic.periodo = '3' THEN CONCAT(ic.anio, ' - Verano')
        ELSE CONCAT(ic.anio, ' - Periodo ', ic.periodo)
    END as periodo_nombre
FROM cursos_aprobados ca
JOIN cursos c ON ca.curso_id = c.id
JOIN secciones s ON ca.seccion_id = s.id
JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
WHERE ca.alumno_id = %s AND c.cerrado = 1
ORDER BY ic.anio DESC, ic.periodo DESC, c.codigo;
"""

# Obtener todas las instancias de evaluación para el selector del reporte A
get_instancias_evaluacion_for_report = """
SELECT 
    ie.id,
    ie.nombre as instancia_nombre,
    te.nombre as topico_nombre,
    c.codigo as curso_codigo,
    c.nombre as curso_nombre,
    ic.anio,
    ic.periodo,
    s.numero as seccion_numero,
    CONCAT(c.codigo, ' - ', te.nombre, ' - ', ie.nombre, ' (', ic.anio, '-', ic.periodo, ' Sec.', s.numero, ')') as display_name
FROM instancias_evaluacion ie
JOIN topicos_evaluacion te ON ie.topico_id = te.id
JOIN secciones s ON te.seccion_id = s.id
JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
ORDER BY c.codigo, ic.anio DESC, ic.periodo DESC, s.numero, te.nombre, ie.nombre;
"""

# Obtener todas las secciones de cursos cerrados para el reporte B
get_secciones_cursos_cerrados = """
SELECT 
    s.id,
    s.numero as seccion_numero,
    c.codigo as curso_codigo,
    c.nombre as curso_nombre,
    ic.anio,
    ic.periodo,
    CONCAT(c.codigo, ' - ', c.nombre, ' (', ic.anio, '-', ic.periodo, ' Sec.', s.numero, ')') as display_name
FROM secciones s
JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
WHERE c.cerrado = 1
ORDER BY c.codigo, ic.anio DESC, ic.periodo DESC, s.numero;
"""

# Obtener todos los alumnos para el reporte C
get_alumnos_for_certificado = """
SELECT 
    a.id,
    a.nombre,
    a.correo,
    CONCAT(a.nombre, ' (', a.correo, ')') as display_name
FROM alumnos a
ORDER BY a.nombre;
"""

# Estadísticas del certificado de notas
get_estadisticas_certificado = """
SELECT 
    COUNT(*) as total_cursos,
    COUNT(CASE WHEN ca.aprobado = 1 THEN 1 END) as cursos_aprobados,
    COUNT(CASE WHEN ca.aprobado = 0 THEN 1 END) as cursos_reprobados,
    ROUND(AVG(ca.nota_final), 2) as promedio_general,
    SUM(c.creditos) as total_creditos,
    SUM(CASE WHEN ca.aprobado = 1 THEN c.creditos ELSE 0 END) as creditos_aprobados
FROM cursos_aprobados ca
JOIN cursos c ON ca.curso_id = c.id
WHERE ca.alumno_id = %s AND c.cerrado = 1;
"""