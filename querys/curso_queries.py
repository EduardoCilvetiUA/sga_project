get_all_cursos = """
SELECT id, codigo, nombre, creditos, cerrado
FROM cursos
ORDER BY codigo
"""
get_curso_by_id = """
SELECT id, codigo, nombre, creditos, cerrado
FROM cursos
WHERE id = %s
"""
create_curso = """
INSERT INTO cursos (codigo, nombre, creditos, cerrado)
VALUES (%s, %s, %s, %s)
"""
update_curso = """
UPDATE cursos
SET codigo = %s, nombre = %s, creditos = %s
WHERE id = %s
"""
delete_curso = "DELETE FROM cursos WHERE id = %s"
get_curso_prerequisitos = """
    SELECT c.* FROM cursos c
    JOIN prerequisitos p ON c.id = p.prerequisito_id
    WHERE p.curso_id = %s
"""
add_curso_prerequisitos = (
    "INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES (%s, %s)"
)
remove_curso_prerequisitos = (
    "DELETE FROM prerequisitos WHERE curso_id = %s AND prerequisito_id = %s"
)
get_alumnos_eligibles_by_curso = """
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
close_curso = """
UPDATE cursos
SET cerrado = TRUE
WHERE id = %s
"""

reopen_curso = """
UPDATE cursos
SET cerrado = FALSE
WHERE id = %s
"""

is_curso_closed = """
SELECT cerrado
FROM cursos
WHERE id = %s
"""
