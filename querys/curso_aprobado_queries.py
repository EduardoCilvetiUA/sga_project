get_cursos_aprobados_by_alumno = """
    SELECT ca.*, c.codigo, c.nombre
    FROM cursos_aprobados ca
    JOIN cursos c ON ca.curso_id = c.id
    WHERE ca.alumno_id = %s
    ORDER BY ca.fecha_aprobacion DESC
"""
get_curso_aprobado_by_id = """
    SELECT ca.*, c.codigo, c.nombre
    FROM cursos_aprobados ca
    JOIN cursos c ON ca.curso_id = c.id
    WHERE ca.id = %s
"""
check_curso_aprobado_by_alumno = """
    SELECT * 
    FROM cursos_aprobados
    WHERE alumno_id = %s AND curso_id = %s AND aprobado = TRUE
"""
check_there_is_record = """
    SELECT id FROM cursos_aprobados
    WHERE alumno_id = %s AND curso_id = %s
"""
update_record = """
    UPDATE cursos_aprobados 
    SET seccion_id = %s, nota_final = %s, aprobado = %s, fecha_aprobacion = %s
    WHERE id = %s
"""
create_record = """
    INSERT INTO cursos_aprobados 
    (alumno_id, curso_id, seccion_id, nota_final, aprobado, fecha_aprobacion)
    VALUES (%s, %s, %s, %s, %s, %s)
"""
delete_curso_aprobado = "DELETE FROM cursos_aprobados WHERE id = %s"
get_curso_id = """
    SELECT ic.curso_id 
    FROM secciones s
    JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
    WHERE s.id = %s
"""
get_alumno_seccion_id = """
    SELECT id FROM alumno_seccion
    WHERE alumno_id = %s AND seccion_id = %s
"""
calculate_nota_final_by_alumno = """
    SELECT COALESCE(AVG(n.nota), 0) AS nota_final
    FROM notas n
    JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
    JOIN topicos_evaluacion te ON ie.topico_id = te.id
    WHERE n.alumno_seccion_id = %s
"""
