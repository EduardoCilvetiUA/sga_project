from db import execute_query

class Evaluacion:
    @staticmethod
    def get_all_topics():
        """Get all evaluation topics"""
        query = """
            SELECT te.*, s.numero, s.instancia_curso_id, 
                   ic.anio, ic.periodo, c.codigo, c.nombre as curso_nombre
            FROM topicos_evaluacion te
            JOIN secciones s ON te.seccion_id = s.id
            JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            ORDER BY c.codigo, ic.anio DESC, ic.periodo DESC, s.numero
        """
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_topic_by_id(topic_id):
        """Get an evaluation topic by ID"""
        query = """
            SELECT te.*, s.numero, s.instancia_curso_id, 
                   ic.anio, ic.periodo, c.codigo, c.nombre as curso_nombre
            FROM topicos_evaluacion te
            JOIN secciones s ON te.seccion_id = s.id
            JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            WHERE te.id = %s
        """
        result = execute_query(query, (topic_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def create_topic(seccion_id, nombre, porcentaje):
        """Create a new evaluation topic"""
        query = "INSERT INTO topicos_evaluacion (seccion_id, nombre, porcentaje) VALUES (%s, %s, %s)"
        return execute_query(query, (seccion_id, nombre, porcentaje))
    
    @staticmethod
    def update_topic(topic_id, nombre, porcentaje):
        """Update an existing evaluation topic"""
        query = "UPDATE topicos_evaluacion SET nombre = %s, porcentaje = %s WHERE id = %s"
        execute_query(query, (nombre, porcentaje, topic_id))
        return topic_id
    
    @staticmethod
    def delete_topic(topic_id):
        """Delete an evaluation topic"""
        query = "DELETE FROM topicos_evaluacion WHERE id = %s"
        execute_query(query, (topic_id,))
    
    @staticmethod
    def get_instances(topic_id):
        """Get evaluation instances for a topic"""
        query = """
            SELECT * FROM instancias_evaluacion
            WHERE topico_id = %s
            ORDER BY nombre
        """
        return execute_query(query, (topic_id,), fetch=True)
    
    @staticmethod
    def get_instance_by_id(instance_id):
        """Get an evaluation instance by ID"""
        query = """
            SELECT ie.*, te.nombre as topico_nombre, te.seccion_id,
                   s.numero, ic.anio, ic.periodo,
                   c.codigo, c.nombre as curso_nombre
            FROM instancias_evaluacion ie
            JOIN topicos_evaluacion te ON ie.topico_id = te.id
            JOIN secciones s ON te.seccion_id = s.id
            JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            WHERE ie.id = %s
        """
        result = execute_query(query, (instance_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def create_instance(topico_id, nombre, peso, opcional):
        """Create a new evaluation instance"""
        query = """
            INSERT INTO instancias_evaluacion 
            (topico_id, nombre, peso, opcional) 
            VALUES (%s, %s, %s, %s)
        """
        return execute_query(query, (topico_id, nombre, peso, opcional))
    
    @staticmethod
    def update_instance(instance_id, nombre, peso, opcional):
        """Update an existing evaluation instance"""
        query = """
            UPDATE instancias_evaluacion 
            SET nombre = %s, peso = %s, opcional = %s 
            WHERE id = %s
        """
        execute_query(query, (nombre, peso, opcional, instance_id))
        return instance_id
    
    @staticmethod
    def delete_instance(instance_id):
        """Delete an evaluation instance"""
        query = "DELETE FROM instancias_evaluacion WHERE id = %s"
        execute_query(query, (instance_id,))
    
    @staticmethod
    def get_topics_by_section(seccion_id):
        """Get evaluation topics for a section"""
        query = """
            SELECT te.* 
            FROM topicos_evaluacion te
            WHERE te.seccion_id = %s
            ORDER BY te.nombre
        """
        return execute_query(query, (seccion_id,), fetch=True)
    
    @staticmethod
    def get_section_total_percentage(seccion_id):
        """Get total percentage of evaluation topics for a section"""
        query = """
            SELECT SUM(porcentaje) as total
            FROM topicos_evaluacion
            WHERE seccion_id = %s
        """
        result = execute_query(query, (seccion_id,), fetch=True)
        return result[0]['total'] if result and result[0]['total'] else 0