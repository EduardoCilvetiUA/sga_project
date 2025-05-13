get_creditos_curso = """
SELECT creditos FROM cursos WHERE id = %s
"""
get_secciones_sin_horario_by_periodo = """
SELECT s.id, s.numero, ic.id as instancia_curso_id, c.id as curso_id, 
       c.codigo, c.nombre, c.creditos
FROM secciones s
JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
WHERE ic.anio = %s AND ic.periodo = %s
AND NOT EXISTS (
    SELECT 1 FROM horarios h WHERE h.seccion_id = s.id
)
ORDER BY c.creditos DESC, s.id
"""
get_profesores_by_seccion = """
SELECT p.id, p.nombre
FROM profesores p
JOIN profesor_seccion ps ON p.id = ps.profesor_id
WHERE ps.seccion_id = %s
"""
get_alumnos_by_seccion = """
SELECT a.id, a.nombre
FROM alumnos a
JOIN alumno_seccion as_1 ON a.id = as_1.alumno_id
WHERE as_1.seccion_id = %s
"""
check_disponibilidad_sala = """
SELECT COUNT(*) as count
FROM horarios
WHERE sala_id = %s AND dia = %s AND 
((hora_inicio <= %s AND hora_fin > %s) OR
 (hora_inicio < %s AND hora_fin >= %s) OR
 (hora_inicio >= %s AND hora_inicio < %s))
"""
check_disponibilidad_profesor = """
SELECT COUNT(*) as count
FROM horarios h
JOIN profesor_seccion ps ON h.seccion_id = ps.seccion_id
WHERE ps.profesor_id = %s AND h.dia = %s AND 
((h.hora_inicio <= %s AND h.hora_fin > %s) OR
 (h.hora_inicio < %s AND h.hora_fin >= %s) OR
 (h.hora_inicio >= %s AND h.hora_inicio < %s))
"""
check_disponibilidad_alumno = """
SELECT COUNT(*) as count
FROM horarios h
JOIN alumno_seccion as_1 ON h.seccion_id = as_1.seccion_id
WHERE as_1.alumno_id = %s AND h.dia = %s AND 
((h.hora_inicio <= %s AND h.hora_fin > %s) OR
 (h.hora_inicio < %s AND h.hora_fin >= %s) OR
 (h.hora_inicio >= %s AND h.hora_inicio < %s))
"""
create_horario = """
INSERT INTO horarios (seccion_id, sala_id, dia, hora_inicio, hora_fin)
VALUES (%s, %s, %s, %s, %s)
"""
get_horarios_for_export = """
SELECT h.dia, h.hora_inicio, h.hora_fin, s.nombre as sala_nombre,
       c.codigo as curso_codigo, c.nombre as curso_nombre,
       sec.numero as seccion_numero, p.nombre as profesor_nombre
FROM horarios h
JOIN salas s ON h.sala_id = s.id
JOIN secciones sec ON h.seccion_id = sec.id
JOIN instancias_curso ic ON sec.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
LEFT JOIN profesor_seccion ps ON sec.id = ps.seccion_id
LEFT JOIN profesores p ON ps.profesor_id = p.id
WHERE ic.anio = %s AND ic.periodo = %s
ORDER BY h.dia, h.hora_inicio, s.nombre
"""
get_salas_ordered_by_capacidad = (
    "SELECT id, nombre, capacidad FROM salas ORDER BY capacidad DESC"
)
