get_all_student_topics = """
SELECT te.*, s.numero, s.instancia_curso_id, s.usa_porcentaje as seccion_usa_porcentaje, 
        ic.anio, ic.periodo, c.codigo, c.nombre as curso_nombre
FROM topicos_evaluacion te
JOIN secciones s ON te.seccion_id = s.id
JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
ORDER BY c.codigo, ic.anio DESC, ic.periodo DESC, s.numero
"""
get_evaluation_topic_by_id = """
SELECT te.*, s.numero, s.instancia_curso_id, s.usa_porcentaje as seccion_usa_porcentaje,
        ic.anio, ic.periodo, c.codigo, c.nombre as curso_nombre
FROM topicos_evaluacion te
JOIN secciones s ON te.seccion_id = s.id
JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
WHERE te.id = %s
"""
create_evaluation_topic = "INSERT INTO topicos_evaluacion (seccion_id, nombre, valor, usa_porcentaje) VALUES (%s, %s, %s, %s)"
update_evaluation_topic = "UPDATE topicos_evaluacion SET nombre = %s, valor = %s, usa_porcentaje = %s WHERE id = %s"
delete_evaluation_topic = "DELETE FROM topicos_evaluacion WHERE id = %s"
get_evaluation_instances_by_topic = """
SELECT ie.*, te.usa_porcentaje 
FROM instancias_evaluacion ie
JOIN topicos_evaluacion te ON ie.topico_id = te.id
WHERE ie.topico_id = %s
ORDER BY ie.nombre
"""
get_evaluation_instance_by_id = """
SELECT ie.*, te.nombre as topico_nombre, te.seccion_id, te.usa_porcentaje,
        s.numero, s.usa_porcentaje as seccion_usa_porcentaje, ic.anio, ic.periodo,
        c.codigo, c.nombre as curso_nombre
FROM instancias_evaluacion ie
JOIN topicos_evaluacion te ON ie.topico_id = te.id
JOIN secciones s ON te.seccion_id = s.id
JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
JOIN cursos c ON ic.curso_id = c.id
WHERE ie.id = %s
"""
create_evaluation_instance = """
INSERT INTO instancias_evaluacion 
(topico_id, nombre, valor, opcional) 
VALUES (%s, %s, %s, %s)
"""
update_evaluation_instance = """
UPDATE instancias_evaluacion 
SET nombre = %s, valor = %s, opcional = %s 
WHERE id = %s
"""
delete_evaluation_instance = "DELETE FROM instancias_evaluacion WHERE id = %s"
get_evaluation_topic_by_section = """
SELECT te.*, s.usa_porcentaje as seccion_usa_porcentaje 
FROM topicos_evaluacion te
JOIN secciones s ON te.seccion_id = s.id
WHERE te.seccion_id = %s
ORDER BY te.nombre
"""
get_section_percentage = """
SELECT usa_porcentaje FROM secciones
WHERE id = %s
"""
get_total_score_by_section = """
    SELECT SUM(valor) as total
    FROM topicos_evaluacion
    WHERE seccion_id = %s
"""
get_topic_percentage = """
SELECT usa_porcentaje FROM topicos_evaluacion
WHERE id = %s
"""
get_total_score_by_topic = """
    SELECT SUM(valor) as total
    FROM instancias_evaluacion
    WHERE topico_id = %s
"""
