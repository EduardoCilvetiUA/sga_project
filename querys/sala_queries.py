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