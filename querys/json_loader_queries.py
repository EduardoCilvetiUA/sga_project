check_alumno_exists = "SELECT id FROM alumnos WHERE id = %s"
update_alumno = (
    "UPDATE alumnos SET nombre = %s, correo = %s, fecha_ingreso = %s WHERE id = %s"
)
insert_alumno = (
    "INSERT INTO alumnos (id, nombre, correo, fecha_ingreso) VALUES (%s, %s, %s, %s)"
)
check_profesor_exists = "SELECT id FROM profesores WHERE id = %s"
update_profesor = "UPDATE profesores SET nombre = %s, correo = %s WHERE id = %s"
insert_profesor = "INSERT INTO profesores (id, nombre, correo) VALUES (%s, %s, %s)"
check_curso_exists = "SELECT id FROM cursos WHERE id = %s"
update_curso = "UPDATE cursos SET codigo = %s, nombre = %s, creditos = %s WHERE id = %s"
insert_curso = "INSERT INTO cursos (id, codigo, nombre, creditos) VALUES (%s, %s, %s, %s)"
delete_prerequisitos = "DELETE FROM prerequisitos WHERE curso_id = %s"
insert_prerequisito = (
    "INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES (%s, %s)"
)
check_sala_exists = "SELECT id FROM salas WHERE id = %s"
update_sala = "UPDATE salas SET nombre = %s, capacidad = %s WHERE id = %s"
insert_sala = "INSERT INTO salas (id, nombre, capacidad) VALUES (%s, %s, %s)"
check_instancia_exists = "SELECT id FROM instancias_curso WHERE id = %s"
update_instancia = (
    "UPDATE instancias_curso SET curso_id = %s, anio = %s, periodo = %s WHERE id = %s"
)
insert_instancia = (
    "INSERT INTO instancias_curso (id, curso_id, anio, periodo) VALUES (%s, %s, %s, %s)"
)
check_curso_exists_by_id = "SELECT id FROM cursos WHERE id = %s"
check_seccion_exists = "SELECT id FROM secciones WHERE id = %s"
update_seccion = "UPDATE secciones SET instancia_curso_id = %s, numero = %s, usa_porcentaje = %s WHERE id = %s"
insert_seccion = "INSERT INTO secciones (id, instancia_curso_id, numero, usa_porcentaje) VALUES (%s, %s, %s, %s)"
check_profesor_seccion_exists = (
    "SELECT id FROM profesor_seccion WHERE profesor_id = %s AND seccion_id = %s"
)
insert_profesor_seccion = (
    "INSERT INTO profesor_seccion (profesor_id, seccion_id) VALUES (%s, %s)"
)
check_topico_exists = "SELECT id FROM topicos_evaluacion WHERE id = %s"
update_topico = """
UPDATE topicos_evaluacion 
SET seccion_id = %s, nombre = %s, valor = %s, usa_porcentaje = %s 
WHERE id = %s
"""
insert_topico = """
INSERT INTO topicos_evaluacion 
(id, seccion_id, nombre, valor, usa_porcentaje) 
VALUES (%s, %s, %s, %s, %s)
"""
delete_instancias_evaluacion = "DELETE FROM instancias_evaluacion WHERE topico_id = %s"
insert_instancia_evaluacion = """
INSERT INTO instancias_evaluacion 
(topico_id, nombre, valor, opcional) 
VALUES (%s, %s, %s, %s)
"""
check_seccion_exists_by_id = "SELECT id FROM secciones WHERE id = %s"
check_alumno_exists_by_id = "SELECT id FROM alumnos WHERE id = %s"
check_alumno_seccion_exists = (
    "SELECT id FROM alumno_seccion WHERE alumno_id = %s AND seccion_id = %s"
)
insert_alumno_seccion = (
    "INSERT INTO alumno_seccion (alumno_id, seccion_id) VALUES (%s, %s)"
)

check_topico_exists_by_id = "SELECT id FROM topicos_evaluacion WHERE id = %s"
get_seccion_id_from_topico = "SELECT seccion_id FROM topicos_evaluacion WHERE id = %s"
check_alumno_seccion_by_seccion = (
    "SELECT id FROM alumno_seccion WHERE alumno_id = %s AND seccion_id = %s"
)
get_instancia_evaluacion_by_offset = """
SELECT id FROM instancias_evaluacion 
WHERE topico_id = %s 
ORDER BY id 
LIMIT 1 OFFSET %s
"""
check_nota_exists = (
    "SELECT id FROM notas WHERE alumno_seccion_id = %s AND instancia_evaluacion_id = %s"
)
update_nota = "UPDATE notas SET nota = %s WHERE id = %s"
insert_nota = "INSERT INTO notas (alumno_seccion_id, instancia_evaluacion_id, nota) VALUES (%s, %s, %s)"

get_max_numero_seccion = (
    "SELECT MAX(numero) as max_num FROM secciones WHERE instancia_curso_id = %s"
)
