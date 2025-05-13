get_all_course_instances = """
    SELECT ic.*, c.codigo, c.nombre 
    FROM instancias_curso ic
    JOIN cursos c ON ic.curso_id = c.id
    ORDER BY ic.anio DESC, ic.periodo DESC
"""
get_course_instance_by_id = """
    SELECT ic.*, c.codigo, c.nombre 
    FROM instancias_curso ic
    JOIN cursos c ON ic.curso_id = c.id
    WHERE ic.id = %s
"""
create_curso _instance = (
    "INSERT INTO instancias_curso (curso_id, anio, periodo) VALUES (%s, %s, %s)"
)
update_curso_instance = (
    "UPDATE instancias_curso SET curso_id = %s, anio = %s, periodo = %s WHERE id = %s"
)
delete_curso_instance = "DELETE FROM instancias_curso WHERE id = %s"
get_sections_by_course_instance_id = (
    "SELECT * FROM secciones WHERE instancia_curso_id = %s ORDER BY numero"
)
