from db import execute_query


class Nota:
    @staticmethod
    def get_all():
        """Get all grades"""
        query = """
            SELECT n.*, a.nombre as alumno_nombre, a.correo as alumno_correo,
                   ie.nombre as instancia_nombre, ie.opcional,
                   te.nombre as topico_nombre, te.valor as topico_valor,
                   s.numero as seccion_numero, s.usa_porcentaje,
                   ic.anio, ic.periodo,
                   c.codigo, c.nombre as curso_nombre
            FROM notas n
            JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
            JOIN alumnos a ON als.alumno_id = a.id
            JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
            JOIN topicos_evaluacion te ON ie.topico_id = te.id
            JOIN secciones s ON te.seccion_id = s.id
            JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            ORDER BY c.codigo, ic.anio DESC, ic.periodo DESC, s.numero, te.nombre, ie.nombre, a.nombre
        """
        return execute_query(query, fetch=True)

    @staticmethod
    def get_by_id(nota_id):
        """Get a grade by ID"""
        query = """
            SELECT n.*, a.id as alumno_id, a.nombre as alumno_nombre, a.correo as alumno_correo,
                   ie.id as instancia_id, ie.nombre as instancia_nombre, ie.opcional, ie.valor,
                   te.id as topico_id, te.nombre as topico_nombre, te.valor as topico_valor,
                   s.id as seccion_id, s.numero as seccion_numero, s.usa_porcentaje,
                   ic.anio, ic.periodo,
                   c.codigo, c.nombre as curso_nombre
            FROM notas n
            JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
            JOIN alumnos a ON als.alumno_id = a.id
            JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
            JOIN topicos_evaluacion te ON ie.topico_id = te.id
            JOIN secciones s ON te.seccion_id = s.id
            JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            WHERE n.id = %s
        """
        result = execute_query(query, (nota_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(alumno_seccion_id, instancia_evaluacion_id, nota):
        """Create a new grade"""
        query = "INSERT INTO notas (alumno_seccion_id, instancia_evaluacion_id, nota) VALUES (%s, %s, %s)"
        return execute_query(query, (alumno_seccion_id, instancia_evaluacion_id, nota))

    @staticmethod
    def update(nota_id, nota_valor):
        """Update an existing grade"""
        query = "UPDATE notas SET nota = %s WHERE id = %s"
        execute_query(query, (nota_valor, nota_id))
        return nota_id

    @staticmethod
    def delete(nota_id):
        """Delete a grade"""
        query = "DELETE FROM notas WHERE id = %s"
        execute_query(query, (nota_id,))

    @staticmethod
    def get_grades_by_section(seccion_id):
        """Get all grades for a section"""
        query = """
            SELECT n.*, a.nombre as alumno_nombre, a.correo as alumno_correo,
                   ie.nombre as instancia_nombre, ie.opcional, ie.valor,
                   te.nombre as topico_nombre, te.valor as topico_valor
            FROM notas n
            JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
            JOIN alumnos a ON als.alumno_id = a.id
            JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
            JOIN topicos_evaluacion te ON ie.topico_id = te.id
            WHERE te.seccion_id = %s
            ORDER BY a.nombre, te.nombre, ie.nombre
        """
        return execute_query(query, (seccion_id,), fetch=True)

    @staticmethod
    def get_grades_by_student_section(alumno_id, seccion_id):
        """Get all grades for a student in a section"""
        query = """
            SELECT n.*, ie.nombre as instancia_nombre, ie.opcional, ie.valor,
                   te.nombre as topico_nombre, te.valor as topico_valor,
                   s.usa_porcentaje
            FROM notas n
            JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
            JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
            JOIN topicos_evaluacion te ON ie.topico_id = te.id
            JOIN secciones s ON te.seccion_id = s.id
            WHERE als.alumno_id = %s AND te.seccion_id = %s
            ORDER BY te.nombre, ie.nombre
        """
        return execute_query(query, (alumno_id, seccion_id), fetch=True)

    @staticmethod
    def get_student_section_id(alumno_id, seccion_id):
        """Get the alumno_seccion_id for a student and section"""
        query = """
            SELECT id FROM alumno_seccion
            WHERE alumno_id = %s AND seccion_id = %s
        """
        result = execute_query(query, (alumno_id, seccion_id), fetch=True)
        return result[0]["id"] if result else None

    @staticmethod
    def get_pending_evaluations(alumno_id, seccion_id):
        """Get evaluation instances that don't have a grade for a student"""
        query = """
            SELECT ie.*, te.nombre as topico_nombre
            FROM instancias_evaluacion ie
            JOIN topicos_evaluacion te ON ie.topico_id = te.id
            WHERE te.seccion_id = %s
            AND ie.id NOT IN (
                SELECT n.instancia_evaluacion_id
                FROM notas n
                JOIN alumno_seccion als ON n.alumno_seccion_id = als.id
                WHERE als.alumno_id = %s AND als.seccion_id = %s
            )
            ORDER BY te.nombre, ie.nombre
        """
        return execute_query(query, (seccion_id, alumno_id, seccion_id), fetch=True)

    @staticmethod
    def calculate_final_grade(alumno_id, seccion_id):
        """Calculate the final grade for a student in a section"""
        # Get all grades for the student in the section
        grades = Nota.get_grades_by_student_section(alumno_id, seccion_id)

        if not grades:
            return None

        # Check if the section uses percentage or weight
        usa_porcentaje = grades[0]["usa_porcentaje"] if grades else True

        # Group grades by topic
        topics = {}
        for grade in grades:
            topico_nombre = grade["topico_nombre"]
            if topico_nombre not in topics:
                topics[topico_nombre] = {
                    "valor": grade["topico_valor"],
                    "instancias": [],
                }

            topics[topico_nombre]["instancias"].append(
                {
                    "nombre": grade["instancia_nombre"],
                    "valor": grade["valor"],
                    "opcional": grade["opcional"],
                    "nota": grade["nota"],
                }
            )

        # Calculate weighted average for each topic
        topic_grades = {}
        for topico, data in topics.items():
            total_valor = sum(inst["valor"] for inst in data["instancias"])
            weighted_sum = sum(
                inst["nota"] * inst["valor"] for inst in data["instancias"]
            )

            if total_valor > 0:
                topic_grades[topico] = weighted_sum / total_valor
            else:
                topic_grades[topico] = 0

        # Calculate final weighted average
        if usa_porcentaje:
            # Using percentages (should sum to 100)
            total_percentage = sum(data["valor"] for data in topics.values())

            if total_percentage <= 0:
                return None

            final_grade = 0
            for topico, nota in topic_grades.items():
                valor = topics[topico]["valor"]
                final_grade += nota * (valor / total_percentage)
        else:
            # Using weights
            total_weight = sum(data["valor"] for data in topics.values())

            if total_weight <= 0:
                return None

            final_grade = 0
            for topico, nota in topic_grades.items():
                valor = topics[topico]["valor"]
                final_grade += nota * (valor / total_weight)

        return round(final_grade, 1)
