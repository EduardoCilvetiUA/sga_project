get_all_grades = """
    SELECT n.*, a.nombre as alumno_nombre, a.correo as alumno_correo,
            ie.nombre as instancia_nombre, ie.opcional,
            te.nombre as topico_nombre, te.valor as topico_valor,
            s.numero as seccion_numero, s.usa_porcentaje,
            ic.anio, ic.periodo,
            c.codigo, c.nombre as curso_nombre
    FROM notas n
    JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
    JOIN alumnos a ON als.alumno_id = a.id
    JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
    JOIN topicos_evaluacion te ON ie.topico_id = te.id
    JOIN secciones s ON te.seccion_id = s.id
    JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
    JOIN cursos c ON ic.curso_id = c.id
    ORDER BY c.codigo, ic.anio DESC, ic.periodo DESC, s.numero, te.nombre, ie.nombre, a.nombre
"""
get_grade_by_id = """
    SELECT n.*, a.id as alumno_id, a.nombre as alumno_nombre, a.correo as alumno_correo,
            ie.id as instancia_id, ie.nombre as instancia_nombre, ie.opcional, ie.valor,
            te.id as topico_id, te.nombre as topico_nombre, te.valor as topico_valor,
            s.id as seccion_id, s.numero as seccion_numero, s.usa_porcentaje,
            ic.anio, ic.periodo,
            c.codigo, c.nombre as curso_nombre
    FROM notas n
    JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
    JOIN alumnos a ON als.alumno_id = a.id
    JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
    JOIN topicos_evaluacion te ON ie.topico_id = te.id
    JOIN secciones s ON te.seccion_id = s.id
    JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
    JOIN cursos c ON ic.curso_id = c.id
    WHERE n.id = %s
"""
create_grade = "INSERT INTO notas (alumno_seccion_id, instancia_evaluacion_id, nota) VALUES (%s, %s, %s)"
update_grade = "UPDATE notas SET nota = %s WHERE id = %s"
delete_grade = "DELETE FROM notas WHERE id = %s"
get_all_grades_by_section = """
    SELECT n.*, a.nombre as alumno_nombre, a.correo as alumno_correo,
            ie.nombre as instancia_nombre, ie.opcional, ie.valor,
            te.nombre as topico_nombre, te.valor as topico_valor
    FROM notas n
    JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
    JOIN alumnos a ON als.alumno_id = a.id
    JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
    JOIN topicos_evaluacion te ON ie.topico_id = te.id
    WHERE te.seccion_id = %s
    ORDER BY a.nombre, te.nombre, ie.nombre
"""
get_student_grades_in_section = """
    SELECT n.*, ie.nombre as instancia_nombre, ie.opcional, ie.valor,
            te.nombre as topico_nombre, te.valor as topico_valor,
            s.usa_porcentaje
    FROM notas n
    JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
    JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
    JOIN topicos_evaluacion te ON ie.topico_id = te.id
    JOIN secciones s ON te.seccion_id = s.id
    WHERE als.alumno_id = %s AND te.seccion_id = %s
    ORDER BY te.nombre, ie.nombre
"""
get_student_section_id = """
    SELECT id FROM alumno_seccion
    WHERE alumno_id = %s AND seccion_id = %s
"""
get_missing_grades_for_student = """
    SELECT ie.*, te.nombre as topico_nombre
    FROM instancias_evaluacion ie
    JOIN topicos_evaluacion te ON ie.topico_id = te.id
    WHERE te.seccion_id = %s
    AND ie.id NOT IN (
        SELECT n.instancia_evaluacion_id
        FROM notas n
        JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
        WHERE als.alumno_id = %s AND als.seccion_id = %s
    )
    ORDER BY te.nombre, ie.nombre
"""
