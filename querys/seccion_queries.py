get_all_secciones = """
    SELECT s.*, ic.anio, ic.periodo, c.codigo, c.nombre as curso_nombre
    FROM secciones s
    JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
    JOIN cursos c ON ic.curso_id = c.id
    ORDER BY ic.anio DESC, ic.periodo DESC, s.numero
"""
get_seccion_by_id = """
    SELECT s.*, ic.anio, ic.periodo, ic.curso_id, c.codigo, c.nombre as curso_nombre
    FROM secciones s
    JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
    JOIN cursos c ON ic.curso_id = c.id
    WHERE s.id = %s
"""
create_seccion = "INSERT INTO secciones (instancia_curso_id, numero, usa_porcentaje) VALUES (%s, %s, %s)"
update_seccion = "UPDATE secciones SET instancia_curso_id = %s, numero = %s, usa_porcentaje = %s WHERE id = %s"
delete_seccion = "DELETE FROM secciones WHERE id = %s"
get_profesores_by_seccion = """
    SELECT p.* 
    FROM profesores p
    JOIN profesor_seccion ps ON p.id = ps.profesor_id
    WHERE ps.seccion_id = %s
"""
get_enrolled_alumnos_in_seccion = """
    SELECT a.* 
    FROM alumnos a
    JOIN alumno_seccion als ON a.id = als.alumno_id
    WHERE als.seccion_id = %s
    ORDER BY a.nombre
"""
insert_profesor_in_seccion = (
    "INSERT INTO profesor_seccion (profesor_id, seccion_id) VALUES (%s, %s)"
)
remove_profesor_from_seccion = (
    "DELETE FROM profesor_seccion WHERE profesor_id = %s AND seccion_id = %s"
)
get_curso_id_for_seccion = """
    SELECT ic.curso_id 
    FROM secciones s
    JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
    WHERE s.id = %s
"""
insert_alumno_in_seccion = (
    "INSERT INTO alumno_seccion (alumno_id, seccion_id) VALUES (%s, %s)"
)
delete_alumno_from_seccion = (
    "DELETE FROM alumno_seccion WHERE alumno_id = %s AND seccion_id = %s"
)
get_not_enrolled_profesores = """
    SELECT p.* 
    FROM profesores p
    WHERE p.id NOT IN (
        SELECT profesor_id FROM profesor_seccion WHERE seccion_id = %s
    )
    ORDER BY p.nombre
"""
get_not_enrolled_alumnos = """
    SELECT a.* 
    FROM alumnos a
    WHERE a.id NOT IN (
        SELECT alumno_id FROM alumno_seccion WHERE seccion_id = %s
    )
    ORDER BY a.nombre
"""
check_prerequisitos_for_curso = """
    SELECT prerequisito_id 
    FROM prerequisitos
    WHERE curso_id = %s
"""
