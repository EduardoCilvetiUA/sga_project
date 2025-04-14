get_all_students = "SELECT * FROM alumnos ORDER BY nombre"
get_student_by_id = "SELECT * FROM alumnos WHERE id = %s"
create_student = (
    "INSERT INTO alumnos (nombre, correo, fecha_ingreso) VALUES (%s, %s, %s)"
)
update_student_data = (
    "UPDATE alumnos SET nombre = %s, correo = %s, fecha_ingreso = %s WHERE id = %s"
)
delete_student = "DELETE FROM alumnos WHERE id = %s"
get_student_sections = """
        SELECT s.*, ic.anio, ic.periodo, c.codigo, c.nombre AS curso_nombre
        FROM secciones s
        JOIN alumno_seccion alums ON s.id = alums.seccion_id
        JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
        JOIN cursos c ON ic.curso_id = c.id
        WHERE alums.alumno_id = %s
        ORDER BY ic.anio DESC, ic.periodo DESC
    """
