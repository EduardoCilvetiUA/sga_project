from db import execute_query

class Curso:
    @staticmethod
    def get_all():
        """Get all courses"""
        query = "SELECT * FROM cursos ORDER BY codigo"
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(curso_id):
        """Get a course by ID"""
        query = "SELECT * FROM cursos WHERE id = %s"
        result = execute_query(query, (curso_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def create(codigo, nombre):
        """Create a new course"""
        query = "INSERT INTO cursos (codigo, nombre) VALUES (%s, %s)"
        return execute_query(query, (codigo, nombre))
    
    @staticmethod
    def update(curso_id, codigo, nombre):
        """Update an existing course"""
        query = "UPDATE cursos SET codigo = %s, nombre = %s WHERE id = %s"
        execute_query(query, (codigo, nombre, curso_id))
        return curso_id
    
    @staticmethod
    def delete(curso_id):
        """Delete a course"""
        query = "DELETE FROM cursos WHERE id = %s"
        execute_query(query, (curso_id,))
    
    @staticmethod
    def get_prerequisites(curso_id):
        """Get prerequisites for a course"""
        query = """
            SELECT c.* FROM cursos c
            JOIN prerequisitos p ON c.id = p.prerequisito_id
            WHERE p.curso_id = %s
        """
        return execute_query(query, (curso_id,), fetch=True)
    
    @staticmethod
    def add_prerequisite(curso_id, prerequisito_id):
        """Add a prerequisite to a course"""
        query = "INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES (%s, %s)"
        return execute_query(query, (curso_id, prerequisito_id))
    
    @staticmethod
    def remove_prerequisite(curso_id, prerequisito_id):
        """Remove a prerequisite from a course"""
        query = "DELETE FROM prerequisitos WHERE curso_id = %s AND prerequisito_id = %s"
        execute_query(query, (curso_id, prerequisito_id))