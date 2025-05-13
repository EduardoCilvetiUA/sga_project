get_all_sections = """
    SELECT s.*, ic.anio, ic.periodo, c.codigo, c.nombre as curso_nombre
    FROM secciones s
    JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
    JOIN cursos c ON ic.curso_id = c.id
    ORDER BY ic.anio DESC, ic.periodo DESC, s.numero
"""
get_section_by_id = """
    SELECT s.*, ic.anio, ic.periodo, ic.curso_id, c.codigo, c.nombre as curso_nombre
    FROM secciones s
    JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
    JOIN cursos c ON ic.curso_id = c.id
    WHERE s.id = %s
"""
create_section = "INSERT INTO secciones (instancia_curso_id, numero, usa_porcentaje) VALUES (%s, %s, %s)"
update_section = "UPDATE secciones SET instancia_curso_id = %s, numero = %s, usa_porcentaje = %s WHERE id = %s"
delete_section = "DELETE FROM secciones WHERE id = %s"
get_profesores_by_seccion = """
    SELECT p.* 
    FROM profesores p
    JOIN profesor_seccion ps ON p.id = ps.profesor_id
    WHERE ps.seccion_id = %s
"""
get_students_enrolled_in_section = """
    SELECT a.* 
    FROM alumnos a
    JOIN alumno_seccion als ON a.id = als.alumno_id
    WHERE als.seccion_id = %s
    ORDER BY a.nombre
"""
assign_professor_to_section = (
    "INSERT INTO profesor_seccion (profesor_id, seccion_id) VALUES (%s, %s)"
)
remove_professor_from_section = (
    "DELETE FROM profesor_seccion WHERE profesor_id = %s AND seccion_id = %s"
)
get_curso_id_for_section = """
    SELECT ic.curso_id 
    FROM secciones s
    JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
    WHERE s.id = %s
"""
enroll_student_in_section = (
    "INSERT INTO alumno_seccion (alumno_id, seccion_id) VALUES (%s, %s)"
)
unenroll_student_from_section = (
    "DELETE FROM alumno_seccion WHERE alumno_id = %s AND seccion_id = %s"
)
get_not_enrolled_professors = """
    SELECT p.* 
    FROM profesores p
    WHERE p.id NOT IN (
        SELECT profesor_id FROM profesor_seccion WHERE seccion_id = %s
    )
    ORDER BY p.nombre
"""
get_not_enrolled_students = """
    SELECT a.* 
    FROM alumnos a
    WHERE a.id NOT IN (
        SELECT alumno_id FROM alumno_seccion WHERE seccion_id = %s
    )
    ORDER BY a.nombre
"""
check_student_prerequisites_for_course = """
    SELECT prerequisito_id 
    FROM prerequisitos
    WHERE curso_id = %s
"""
