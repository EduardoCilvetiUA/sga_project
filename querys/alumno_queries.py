get_all_alumnos = "SELECT * FROM alumnos ORDER BY nombre"
get_alumno_by_id = "SELECT * FROM alumnos WHERE id = %s"
create_alumno = (
    "INSERT INTO alumnos (nombre, correo, fecha_ingreso) VALUES (%s, %s, %s)"
)
update_data_alumno = (
    "UPDATE alumnos SET nombre = %s, correo = %s, fecha_ingreso = %s WHERE id = %s"
)
delete_alumno = "DELETE FROM alumnos WHERE id = %s"
get_seccion_alumno = """
        SELECT s.*, ic.anio, ic.periodo, c.codigo, c.nombre AS curso_nombre
        FROM secciones s
        JOIN alumno_seccion alums ON s.id = alums.seccion_id
        JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
        JOIN cursos c ON ic.curso_id = c.id
        WHERE alums.alumno_id = %s
        ORDER BY ic.anio DESC, ic.periodo DESC
    """
