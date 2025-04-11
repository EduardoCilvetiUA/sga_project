from db import execute_query


class Alumno:
    @staticmethod
    def get_all():
        """Get all students"""
        query = "SELECT * FROM alumnos ORDER BY nombre"
        return execute_query(query, fetch=True)

    @staticmethod
    def get_by_id(alumno_id):
        """Get a student by ID"""
        query = "SELECT * FROM alumnos WHERE id = %s"
        result = execute_query(query, (alumno_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(nombre, correo, fecha_ingreso):
        """Create a new student"""
        query = (
            "INSERT INTO alumnos (nombre, correo, fecha_ingreso) VALUES (%s, %s, %s)"
        )
        return execute_query(query, (nombre, correo, fecha_ingreso))

    @staticmethod
    def update(alumno_id, nombre, correo, fecha_ingreso):
        """Update an existing student"""
        query = "UPDATE alumnos SET nombre = %s, correo = %s, fecha_ingreso = %s WHERE id = %s"
        execute_query(query, (nombre, correo, fecha_ingreso, alumno_id))
        return alumno_id

    @staticmethod
    def delete(alumno_id):
        """Delete a student"""
        query = "DELETE FROM alumnos WHERE id = %s"
        execute_query(query, (alumno_id,))

    @staticmethod
    def get_sections(alumno_id):
        """Get sections where a student is enrolled"""
        query = """
            SELECT s.*, ic.anio, ic.periodo, c.codigo, c.nombre AS curso_nombre
            FROM secciones s
            JOIN alumno_seccion alums ON s.id = alums.seccion_id
            JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            WHERE alums.alumno_id = %s
            ORDER BY ic.anio DESC, ic.periodo DESC
        """
        return execute_query(query, (alumno_id,), fetch=True)
