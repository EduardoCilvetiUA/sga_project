get_all_courses = """
SELECT id, codigo, nombre, creditos, cerrado
FROM cursos
ORDER BY codigo
"""
get_course_by_id = """
SELECT id, codigo, nombre, creditos, cerrado
FROM cursos
WHERE id = %s
"""
create_course = """
INSERT INTO cursos (codigo, nombre, creditos, cerrado)
VALUES (%s, %s, %s, %s)
"""
update_course = """
UPDATE cursos
SET codigo = %s, nombre = %s, creditos = %s
WHERE id = %s
"""
delete_course = "DELETE FROM cursos WHERE id = %s"
get_course_prerequisites = """
    SELECT c.* FROM cursos c
    JOIN prerequisitos p ON c.id = p.prerequisito_id
    WHERE p.curso_id = %s
"""
add_course_prerequisite = (
    "INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES (%s, %s)"
)
remove_course_prerequisite = (
    "DELETE FROM prerequisitos WHERE curso_id = %s AND prerequisito_id = %s"
)
get_course_eligible_students = """
    SELECT a.* 
    FROM alumnos a
    WHERE NOT EXISTS (
        SELECT 1 FROM prerequisitos p
        WHERE p.curso_id = %s
        AND NOT EXISTS (
            SELECT 1 FROM cursos_aprobados ca
            WHERE ca.alumno_id = a.id
            AND ca.curso_id = p.prerequisito_id
            AND ca.aprobado = TRUE
        )
    )
    ORDER BY a.nombre
"""
close_course = """
UPDATE cursos
SET cerrado = TRUE
WHERE id = %s
"""

reopen_course = """
UPDATE cursos
SET cerrado = FALSE
WHERE id = %s
"""

is_course_closed = """
SELECT cerrado
FROM cursos
WHERE id = %s
"""
