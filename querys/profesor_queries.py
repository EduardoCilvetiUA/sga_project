get_all_profesores = "SELECT * FROM profesores ORDER BY nombre"
get_profesor_by_id = "SELECT * FROM profesores WHERE id = %s"
create_profesor = "INSERT INTO profesores (nombre, correo) VALUES (%s, %s)"
update_profesor = "UPDATE profesores SET nombre = %s, correo = %s WHERE id = %s"
delete_profesor = "DELETE FROM profesores WHERE id = %s"
get_secciones_by_profesor = """
    SELECT s.*, ic.anio, ic.periodo, c.codigo, c.nombre AS curso_nombre
    FROM secciones s
    JOIN profesor_seccion ps ON s.id = ps.seccion_id
    JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
    JOIN cursos c ON ic.curso_id = c.id
    WHERE ps.profesor_id = %s
    ORDER BY ic.anio DESC, ic.periodo DESC
"""
