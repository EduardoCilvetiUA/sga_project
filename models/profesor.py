from db import execute_query

class Profesor:
    @staticmethod
    def get_all():
        """Get all professors"""
        query = "SELECT * FROM profesores ORDER BY nombre"
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(profesor_id):
        """Get a professor by ID"""
        query = "SELECT * FROM profesores WHERE id = %s"
        result = execute_query(query, (profesor_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def create(nombre, correo):
        """Create a new professor"""
        query = "INSERT INTO profesores (nombre, correo) VALUES (%s, %s)"
        return execute_query(query, (nombre, correo))
    
    @staticmethod
    def update(profesor_id, nombre, correo):
        """Update an existing professor"""
        query = "UPDATE profesores SET nombre = %s, correo = %s WHERE id = %s"
        execute_query(query, (nombre, correo, profesor_id))
        return profesor_id
    
    @staticmethod
    def delete(profesor_id):
        """Delete a professor"""
        query = "DELETE FROM profesores WHERE id = %s"
        execute_query(query, (profesor_id,))
    
    @staticmethod
    def get_sections(profesor_id):
        """Get sections taught by a professor"""
        query = """
            SELECT s.*, ic.anio, ic.periodo, c.codigo, c.nombre AS curso_nombre
            FROM secciones s
            JOIN profesor_seccion ps ON s.id = ps.seccion_id
            JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            WHERE ps.profesor_id = %s
            ORDER BY ic.anio DESC, ic.periodo DESC
        """
        return execute_query(query, (profesor_id,), fetch=True)