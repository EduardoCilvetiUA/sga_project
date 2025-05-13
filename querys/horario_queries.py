get_all_horarios = """
SELECT h.*, s.nombre as sala_nombre, sec.numero as seccion_numero,
       ic.anio, ic.periodo, c.codigo as codigo_curso
FROM horarios h
JOIN salas s ON h.sala_id = s.id
JOIN secciones sec ON h.seccion_id = sec.id
JOIN instancias_curso ic ON sec.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
ORDER BY h.dia, h.hora_inicio
"""

get_horario_by_id = """
SELECT h.*, s.nombre as sala_nombre, sec.numero as seccion_numero,
       ic.anio, ic.periodo, c.codigo as codigo_curso
FROM horarios h
JOIN salas s ON h.sala_id = s.id
JOIN secciones sec ON h.seccion_id = sec.id
JOIN instancias_curso ic ON sec.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
WHERE h.id = %s
"""

create_horario = """
INSERT INTO horarios (seccion_id, sala_id, dia, hora_inicio, hora_fin)
VALUES (%s, %s, %s, %s, %s)
"""

update_horario = """
UPDATE horarios
SET seccion_id = %s, sala_id = %s, dia = %s, hora_inicio = %s, hora_fin = %s
WHERE id = %s
"""

delete_horario = """
DELETE FROM horarios
WHERE id = %s
"""

get_horario_by_seccion = """
SELECT h.*, s.nombre as sala_nombre, s.capacidad as sala_capacidad
FROM horarios h
JOIN salas s ON h.sala_id = s.id
WHERE h.seccion_id = %s
ORDER BY h.dia, h.hora_inicio
"""

check_disponibilidad_profesor = """
SELECT h.id
FROM horarios h
JOIN profesor_seccion ps ON h.seccion_id = ps.seccion_id
WHERE ps.profesor_id = %s
  AND h.dia = %s
  AND ((h.hora_inicio <= %s AND h.hora_fin > %s) 
       OR (h.hora_inicio < %s AND h.hora_fin >= %s)
       OR (h.hora_inicio >= %s AND h.hora_inicio < %s))
"""

check_disponibilidad_alumno = """
SELECT h.id
FROM horarios h
JOIN alumno_seccion a_s ON h.seccion_id = a_s.seccion_id
WHERE a_s.alumno_id = %s
  AND h.dia = %s
  AND ((h.hora_inicio <= %s AND h.hora_fin > %s) 
       OR (h.hora_inicio < %s AND h.hora_fin >= %s)
       OR (h.hora_inicio >= %s AND h.hora_inicio < %s))
"""

check_conflictos_horario = """
SELECT DISTINCT 'sala' as tipo_conflicto, h.id, s.nombre as sala_nombre, 
       h.dia, h.hora_inicio, h.hora_fin
FROM horarios h
JOIN salas s ON h.sala_id = s.id
WHERE h.sala_id = %s
  AND h.dia = %s
  AND ((h.hora_inicio <= %s AND h.hora_fin > %s) 
       OR (h.hora_inicio < %s AND h.hora_fin >= %s)
       OR (h.hora_inicio >= %s AND h.hora_inicio < %s))
  AND h.seccion_id != %s
      
UNION

SELECT DISTINCT 'profesor' as tipo_conflicto, h.id, p.nombre as profesor_nombre,
       h.dia, h.hora_inicio, h.hora_fin
FROM horarios h
JOIN profesor_seccion ps ON h.seccion_id = ps.seccion_id
JOIN profesores p ON ps.profesor_id = p.id
JOIN profesor_seccion ps2 ON ps.profesor_id = sp2.profesor_id
WHERE ps2.seccion_id = %s
  AND h.dia = %s
  AND ((h.hora_inicio <= %s AND h.hora_fin > %s) 
       OR (h.hora_inicio < %s AND h.hora_fin >= %s)
       OR (h.hora_inicio >= %s AND h.hora_inicio < %s))
  AND h.seccion_id != %s

UNION

SELECT DISTINCT 'alumno' as tipo_conflicto, h.id, a.nombre as alumno_nombre,
       h.dia, h.hora_inicio, h.hora_fin
FROM horarios h
JOIN alumno_seccion a_s ON h.seccion_id = a_s.seccion_id
JOIN alumnos a ON a_s.alumno_id = a.id
JOIN alumno_seccion a_s2 ON a_s.alumno_id = a_s2.alumno_id
WHERE a_s2.seccion_id = %s
  AND h.dia = %s
  AND ((h.hora_inicio <= %s AND h.hora_fin > %s) 
       OR (h.hora_inicio < %s AND h.hora_fin >= %s)
       OR (h.hora_inicio >= %s AND h.hora_inicio < %s))
  AND h.seccion_id != %s
"""

get_horarios_completos = """
SELECT h.id, h.dia, h.hora_inicio, h.hora_fin, 
      s.nombre as sala_nombre, s.capacidad as sala_capacidad,
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
