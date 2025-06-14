get_all_intancias_curso = """
    SELECT ic.*, c.codigo, c.nombre 
    FROM instancias_curso ic
    JOIN cursos c ON ic.curso_id = c.id
    ORDER BY ic.anio DESC, ic.periodo DESC
"""
get_instancias_curso_by_id = """
    SELECT ic.*, c.codigo, c.nombre 
    FROM instancias_curso ic
    JOIN cursos c ON ic.curso_id = c.id
    WHERE ic.id = %s
"""
create_instancias_curso = (
    "INSERT INTO instancias_curso (curso_id, anio, periodo) VALUES (%s, %s, %s)"
)
update_instancias_curso = (
    "UPDATE instancias_curso SET curso_id = %s, anio = %s, periodo = %s WHERE id = %s"
)
delete_instancias_curso = "DELETE FROM instancias_curso WHERE id = %s"
get_secciones_by_instancia_curso_id = (
    "SELECT * FROM secciones WHERE instancia_curso_id = %s ORDER BY numero"
)
is_instancia_cerrada = "SELECT cerrado FROM instancias_curso WHERE id = %s"