from db import execute_query


class Evaluacion:
    @staticmethod
    def get_all_topics():
        """Get all evaluation topics"""
        query = """
            SELECT te.*, s.numero, s.instancia_curso_id, s.usa_porcentaje as seccion_usa_porcentaje, 
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
            SELECT te.*, s.numero, s.instancia_curso_id, s.usa_porcentaje as seccion_usa_porcentaje,
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
    def create_topic(seccion_id, nombre, valor, usa_porcentaje):
        """Create a new evaluation topic"""
        query = "INSERT INTO topicos_evaluacion (seccion_id, nombre, valor, usa_porcentaje) VALUES (%s, %s, %s, %s)"
        return execute_query(query, (seccion_id, nombre, valor, usa_porcentaje))

    @staticmethod
    def update_topic(topic_id, nombre, valor, usa_porcentaje):
        """Update an existing evaluation topic"""
        query = "UPDATE topicos_evaluacion SET nombre = %s, valor = %s, usa_porcentaje = %s WHERE id = %s"
        execute_query(query, (nombre, valor, usa_porcentaje, topic_id))
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
            SELECT ie.*, te.usa_porcentaje 
            FROM instancias_evaluacion ie
            JOIN topicos_evaluacion te ON ie.topico_id = te.id
            WHERE ie.topico_id = %s
            ORDER BY ie.nombre
        """
        return execute_query(query, (topic_id,), fetch=True)

    @staticmethod
    def get_instance_by_id(instance_id):
        """Get an evaluation instance by ID"""
        query = """
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
        result = execute_query(query, (instance_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create_instance(topico_id, nombre, valor, opcional):
        """Create a new evaluation instance"""
        query = """
            INSERT INTO instancias_evaluacion 
            (topico_id, nombre, valor, opcional) 
            VALUES (%s, %s, %s, %s)
        """
        return execute_query(query, (topico_id, nombre, valor, opcional))

    @staticmethod
    def update_instance(instance_id, nombre, valor, opcional):
        """Update an existing evaluation instance"""
        query = """
            UPDATE instancias_evaluacion 
            SET nombre = %s, valor = %s, opcional = %s 
            WHERE id = %s
        """
        execute_query(query, (nombre, valor, opcional, instance_id))
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
            SELECT te.*, s.usa_porcentaje as seccion_usa_porcentaje 
            FROM topicos_evaluacion te
            JOIN secciones s ON te.seccion_id = s.id
            WHERE te.seccion_id = %s
            ORDER BY te.nombre
        """
        return execute_query(query, (seccion_id,), fetch=True)

    @staticmethod
    def get_section_total_percentage(seccion_id):
        """Get total value of evaluation topics for a section"""
        # First check if section uses percentage
        section_query = """
            SELECT usa_porcentaje FROM secciones
            WHERE id = %s
        """
        section_result = execute_query(section_query, (seccion_id,), fetch=True)

        if not section_result:
            return 0

        usa_porcentaje = section_result[0]["usa_porcentaje"]

        # If using percentages, total should not exceed 100
        if usa_porcentaje:
            query = """
                SELECT SUM(valor) as total
                FROM topicos_evaluacion
                WHERE seccion_id = %s
            """
            result = execute_query(query, (seccion_id,), fetch=True)

            if not result or result[0]["total"] is None:
                return 0

            return result[0]["total"]

        return None  # Return None for weight-based sections

    @staticmethod
    def get_topic_total_percentage(topic_id):
        """Get total value of evaluation instances for a topic"""
        # First check if topic uses percentage
        topic_query = """
            SELECT usa_porcentaje FROM topicos_evaluacion
            WHERE id = %s
        """
        topic_result = execute_query(topic_query, (topic_id,), fetch=True)

        if not topic_result:
            return 0

        usa_porcentaje = topic_result[0]["usa_porcentaje"]

        # If using percentages, total should not exceed 100
        if usa_porcentaje:
            query = """
                SELECT SUM(valor) as total
                FROM instancias_evaluacion
                WHERE topico_id = %s
            """
            result = execute_query(query, (topic_id,), fetch=True)

            if not result or result[0]["total"] is None:
                return 0

            return result[0]["total"]

        return None  # Return None for weight-based topics
