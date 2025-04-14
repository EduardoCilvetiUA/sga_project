get_all_courses = "SELECT * FROM cursos ORDER BY codigo"
get_course_by_id = "SELECT * FROM cursos WHERE id = %s"
create_course = "INSERT INTO cursos (codigo, nombre) VALUES (%s, %s)"
update_course = "UPDATE cursos SET codigo = %s, nombre = %s WHERE id = %s"
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
