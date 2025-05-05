# Consulta para obtener los créditos de un curso
get_course_credits = """
SELECT creditos FROM cursos WHERE id = %s
"""

# Consulta para obtener secciones sin horario asignado
get_sections_without_schedule = """
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

# Consulta para obtener profesores de una sección
get_professors_for_section = """
SELECT p.id, p.nombre
FROM profesores p
JOIN profesor_seccion ps ON p.id = ps.profesor_id
WHERE ps.seccion_id = %s
"""

# Consulta para obtener alumnos de una sección
get_students_for_section = """
SELECT a.id, a.nombre
FROM alumnos a
JOIN alumno_seccion as_1 ON a.id = as_1.alumno_id
WHERE as_1.seccion_id = %s
"""

# Consulta para verificar disponibilidad de sala
check_room_availability = """
SELECT COUNT(*) as count
FROM horarios
WHERE sala_id = %s AND dia = %s AND 
((hora_inicio <= %s AND hora_fin > %s) OR
 (hora_inicio < %s AND hora_fin >= %s) OR
 (hora_inicio >= %s AND hora_inicio < %s))
"""

# Consulta para verificar disponibilidad de profesor
check_professor_availability = """
SELECT COUNT(*) as count
FROM horarios h
JOIN profesor_seccion ps ON h.seccion_id = ps.seccion_id
WHERE ps.profesor_id = %s AND h.dia = %s AND 
((h.hora_inicio <= %s AND h.hora_fin > %s) OR
 (h.hora_inicio < %s AND h.hora_fin >= %s) OR
 (h.hora_inicio >= %s AND h.hora_inicio < %s))
"""

# Consulta para verificar disponibilidad de alumno
check_student_availability = """
SELECT COUNT(*) as count
FROM horarios h
JOIN alumno_seccion as_1 ON h.seccion_id = as_1.seccion_id
WHERE as_1.alumno_id = %s AND h.dia = %s AND 
((h.hora_inicio <= %s AND h.hora_fin > %s) OR
 (h.hora_inicio < %s AND h.hora_fin >= %s) OR
 (h.hora_inicio >= %s AND h.hora_inicio < %s))
"""

# Consulta para asignar horario
assign_schedule = """
INSERT INTO horarios (seccion_id, sala_id, dia, hora_inicio, hora_fin)
VALUES (%s, %s, %s, %s, %s)
"""

# Consulta para obtener horarios para exportar
get_schedules_for_export = """
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