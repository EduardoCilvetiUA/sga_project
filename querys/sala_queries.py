get_all_salas = """
SELECT *
FROM salas
ORDER BY nombre
"""

get_sala_by_id = """
SELECT *
FROM salas
WHERE id = %s
"""

create_sala = """
INSERT INTO salas (nombre, capacidad)
VALUES (%s, %s)
"""

update_sala = """
UPDATE salas
SET nombre = %s, capacidad = %s
WHERE id = %s
"""

delete_sala = """
DELETE FROM salas
WHERE id = %s
"""

get_disponibilidad_sala = """
SELECT *
FROM horarios 
WHERE sala_id = %s AND dia = %s AND 
((hora_inicio <= %s AND hora_fin > %s) OR
 (hora_inicio < %s AND hora_fin >= %s) OR
 (hora_inicio >= %s AND hora_inicio < %s))
"""

get_horario_sala = """
SELECT h.*, sec.numero as seccion_numero, c.codigo as curso_codigo, c.nombre as curso_nombre
FROM horarios h
JOIN secciones sec ON h.seccion_id = sec.id
JOIN instancias_curso ic ON sec.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
WHERE h.sala_id = %s
ORDER BY h.dia, h.hora_inicio
"""
