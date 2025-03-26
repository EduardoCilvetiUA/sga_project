from db import execute_query

class Seccion:
    @staticmethod
    def get_all():
        """Get all sections"""
        query = """
            SELECT s.*, ic.anio, ic.periodo, c.codigo, c.nombre as curso_nombre
            FROM secciones s
            JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            ORDER BY ic.anio DESC, ic.periodo DESC, s.numero
        """
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(seccion_id):
        """Get a section by ID"""
        query = """
            SELECT s.*, ic.anio, ic.periodo, ic.curso_id, c.codigo, c.nombre as curso_nombre
            FROM secciones s
            JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            WHERE s.id = %s
        """
        result = execute_query(query, (seccion_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def create(instancia_curso_id, numero, usa_porcentaje=True):
        """Create a new section"""
        try:
            # Convert parameters to appropriate data types
            instancia_curso_id = int(instancia_curso_id)
            numero = int(numero)
            usa_porcentaje = bool(usa_porcentaje)
            
            print(f"Creating section with: {instancia_curso_id}, {numero}, {usa_porcentaje}")
            
            query = "INSERT INTO secciones (instancia_curso_id, numero, usa_porcentaje) VALUES (%s, %s, %s)"
            result = execute_query(query, (instancia_curso_id, numero, usa_porcentaje))
            
            print(f"Section creation result: {result}")
            return result
        except Exception as e:
            print(f"Error in Seccion.create: {str(e)}")
            raise
    
    @staticmethod
    def update(seccion_id, instancia_curso_id, numero, usa_porcentaje=True):
        """Update an existing section"""
        try:
            # Convert parameters to appropriate data types
            seccion_id = int(seccion_id)
            instancia_curso_id = int(instancia_curso_id)
            numero = int(numero)
            usa_porcentaje = bool(usa_porcentaje)
            
            query = "UPDATE secciones SET instancia_curso_id = %s, numero = %s, usa_porcentaje = %s WHERE id = %s"
            execute_query(query, (instancia_curso_id, numero, usa_porcentaje, seccion_id))
            return seccion_id
        except Exception as e:
            print(f"Error in Seccion.update: {str(e)}")
            raise
    
    @staticmethod
    def delete(seccion_id):
        """Delete a section"""
        query = "DELETE FROM secciones WHERE id = %s"
        execute_query(query, (seccion_id,))
    
    @staticmethod
    def get_professors(seccion_id):
        """Get professors assigned to a section"""
        query = """
            SELECT p.* 
            FROM profesores p
            JOIN profesor_seccion ps ON p.id = ps.profesor_id
            WHERE ps.seccion_id = %s
        """
        return execute_query(query, (seccion_id,), fetch=True)
    
    @staticmethod
    def get_students(seccion_id):
        """Get students enrolled in a section"""
        query = """
            SELECT a.* 
            FROM alumnos a
            JOIN alumno_seccion als ON a.id = als.alumno_id
            WHERE als.seccion_id = %s
            ORDER BY a.nombre
        """
        return execute_query(query, (seccion_id,), fetch=True)
    
    @staticmethod
    def assign_professor(seccion_id, profesor_id):
        """Assign a professor to a section"""
        query = "INSERT INTO profesor_seccion (profesor_id, seccion_id) VALUES (%s, %s)"
        return execute_query(query, (profesor_id, seccion_id))
    
    @staticmethod
    def remove_professor(seccion_id, profesor_id):
        """Remove a professor from a section"""
        query = "DELETE FROM profesor_seccion WHERE profesor_id = %s AND seccion_id = %s"
        execute_query(query, (profesor_id, seccion_id))
    
    @staticmethod
    def enroll_student(seccion_id, alumno_id):
        """Enroll a student in a section"""
        query = "INSERT INTO alumno_seccion (alumno_id, seccion_id) VALUES (%s, %s)"
        return execute_query(query, (alumno_id, seccion_id))
    
    @staticmethod
    def unenroll_student(seccion_id, alumno_id):
        """Unenroll a student from a section"""
        query = "DELETE FROM alumno_seccion WHERE alumno_id = %s AND seccion_id = %s"
        execute_query(query, (alumno_id, seccion_id))
    
    @staticmethod
    def get_available_professors(seccion_id):
        """Get professors not assigned to this section"""
        query = """
            SELECT p.* 
            FROM profesores p
            WHERE p.id NOT IN (
                SELECT profesor_id FROM profesor_seccion WHERE seccion_id = %s
            )
            ORDER BY p.nombre
        """
        return execute_query(query, (seccion_id,), fetch=True)
    
    @staticmethod
    def get_available_students(seccion_id):
        """Get students not enrolled in this section"""
        query = """
            SELECT a.* 
            FROM alumnos a
            WHERE a.id NOT IN (
                SELECT alumno_id FROM alumno_seccion WHERE seccion_id = %s
            )
            ORDER BY a.nombre
        """
        return execute_query(query, (seccion_id,), fetch=True)