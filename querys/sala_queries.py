get_all_classrooms = """
SELECT *
FROM salas
ORDER BY nombre
"""

get_classroom_by_id = """
SELECT *
FROM salas
WHERE id = %s
"""

create_classroom = """
INSERT INTO salas (nombre, capacidad)
VALUES (%s, %s)
"""

update_classroom = """
UPDATE salas
SET nombre = %s, capacidad = %s
WHERE id = %s
"""

delete_classroom = """
DELETE FROM salas
WHERE id = %s
"""

get_classroom_availability = """
SELECT *
FROM horarios 
WHERE sala_id = %s AND dia = %s AND 
((hora_inicio <= %s AND hora_fin > %s) OR
 (hora_inicio < %s AND hora_fin >= %s) OR
 (hora_inicio >= %s AND hora_inicio < %s))
"""

get_classroom_schedule = """
SELECT h.*, sec.numero as seccion_numero, c.codigo as curso_codigo, c.nombre as curso_nombre
FROM horarios h
JOIN secciones sec ON h.seccion_id = sec.id
JOIN instancias_curso ic ON sec.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
WHERE h.sala_id = %s
ORDER BY h.dia, h.hora_inicio
"""
