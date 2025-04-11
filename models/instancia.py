from db import execute_query


class Instancia:
    @staticmethod
    def get_all():
        """Get all course instances"""
        query = """
            SELECT ic.*, c.codigo, c.nombre 
            FROM instancias_curso ic
            JOIN cursos c ON ic.curso_id = c.id
            ORDER BY ic.anio DESC, ic.periodo DESC
        """
        return execute_query(query, fetch=True)

    @staticmethod
    def get_by_id(instancia_id):
        """Get a course instance by ID"""
        query = """
            SELECT ic.*, c.codigo, c.nombre 
            FROM instancias_curso ic
            JOIN cursos c ON ic.curso_id = c.id
            WHERE ic.id = %s
        """
        result = execute_query(query, (instancia_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(curso_id, anio, periodo):
        """Create a new course instance"""
        query = (
            "INSERT INTO instancias_curso (curso_id, anio, periodo) VALUES (%s, %s, %s)"
        )
        return execute_query(query, (curso_id, anio, periodo))

    @staticmethod
    def update(instancia_id, curso_id, anio, periodo):
        """Update an existing course instance"""
        query = "UPDATE instancias_curso SET curso_id = %s, anio = %s, periodo = %s WHERE id = %s"
        execute_query(query, (curso_id, anio, periodo, instancia_id))
        return instancia_id

    @staticmethod
    def delete(instancia_id):
        """Delete a course instance"""
        query = "DELETE FROM instancias_curso WHERE id = %s"
        execute_query(query, (instancia_id,))

    @staticmethod
    def get_sections(instancia_id):
        """Get sections for a course instance"""
        query = "SELECT * FROM secciones WHERE instancia_curso_id = %s ORDER BY numero"
        return execute_query(query, (instancia_id,), fetch=True)
