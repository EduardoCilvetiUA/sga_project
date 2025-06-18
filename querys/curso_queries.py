get_all_cursos = "SELECT id, codigo, nombre, creditos FROM cursos ORDER BY codigo"

get_curso_by_id = "SELECT id, codigo, nombre, creditos FROM cursos WHERE id = %s"

create_curso = "INSERT INTO cursos (codigo, nombre, creditos) VALUES (%s, %s, %s)"

update_curso = "UPDATE cursos SET codigo = %s, nombre = %s, creditos = %s WHERE id = %s"

delete_curso = "DELETE FROM cursos WHERE id = %s"

get_curso_prerequisitos = """
SELECT p.id, p.codigo, p.nombre 
FROM cursos p
JOIN prerequisitos cp ON p.id = cp.prerequisito_id
WHERE cp.curso_id = %s
ORDER BY p.codigo
"""

add_curso_prerequisitos = "INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES (%s, %s)"

remove_curso_prerequisitos = "DELETE FROM prerequisitos WHERE curso_id = %s AND prerequisito_id = %s"

get_alumnos_eligibles_by_curso = """
SELECT a.id, a.nombre, a.correo
FROM alumnos a
WHERE NOT EXISTS (
    SELECT 1 FROM prerequisitos cp
    WHERE cp.curso_id = %s
    AND cp.prerequisito_id NOT IN (
        SELECT ca.curso_id FROM cursos_aprobados ca
        WHERE ca.alumno_id = a.id AND ca.aprobado = 1
    )
)
ORDER BY a.nombre
"""

get_instancias_by_curso = """
SELECT ic.*, 
       CASE 
           WHEN ic.periodo = '01' THEN CONCAT(ic.anio, ' - Primer Semestre')
           WHEN ic.periodo = '02' THEN CONCAT(ic.anio, ' - Segundo Semestre') 
           WHEN ic.periodo = '03' THEN CONCAT(ic.anio, ' - Verano')
           ELSE CONCAT(ic.anio, ' - Periodo ', ic.periodo)
       END as periodo_nombre
FROM instancias_curso ic
WHERE ic.curso_id = %s
ORDER BY ic.anio DESC, ic.periodo DESC
"""

close_instancia_curso = "UPDATE instancias_curso SET cerrado = TRUE WHERE id = %s"

reopen_instancia_curso = "UPDATE instancias_curso SET cerrado = FALSE WHERE id = %s"

is_instancia_cerrada = "SELECT cerrado FROM instancias_curso WHERE id = %s"

check_seccion_instancia_cerrada = """
SELECT ic.cerrado 
FROM instancias_curso ic
JOIN secciones s ON ic.id = s.instancia_curso_id
WHERE s.id = %s
"""
get_secciones_by_instancia = """
SELECT id FROM secciones WHERE instancia_curso_id = %s
"""

get_alumnos_by_seccion = """
SELECT alumno_id FROM alumno_seccion WHERE seccion_id = %s
"""

secciones_query = """
SELECT id FROM secciones WHERE instancia_curso_id = %s
"""

alumnos_query = """
SELECT alumno_id FROM alumno_seccion WHERE seccion_id = %s
"""