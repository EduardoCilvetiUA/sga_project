from db import execute_query
from datetime import date


class CursoAprobado:
    @staticmethod
    def get_all_by_alumno(alumno_id):
        """Get all courses completed by a student"""
        query = """
            SELECT ca.*, c.codigo, c.nombre
            FROM cursos_aprobados ca
            JOIN cursos c ON ca.curso_id = c.id
            WHERE ca.alumno_id = %s
            ORDER BY ca.fecha_aprobacion DESC
        """
        return execute_query(query, (alumno_id,), fetch=True)

    @staticmethod
    def get_by_id(curso_aprobado_id):
        """Get a specific approved course record"""
        query = """
            SELECT ca.*, c.codigo, c.nombre
            FROM cursos_aprobados ca
            JOIN cursos c ON ca.curso_id = c.id
            WHERE ca.id = %s
        """
        result = execute_query(query, (curso_aprobado_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def is_curso_aprobado(alumno_id, curso_id):
        """Check if a student has passed a specific course"""
        query = """
            SELECT * 
            FROM cursos_aprobados
            WHERE alumno_id = %s AND curso_id = %s AND aprobado = TRUE
        """
        result = execute_query(query, (alumno_id, curso_id), fetch=True)
        return bool(result)

    @staticmethod
    def register_curso_aprobado(alumno_id, curso_id, seccion_id, nota_final, aprobado):
        """Register a course as completed for a student"""
        # Check if there's already a record for this course
        query = """
            SELECT id FROM cursos_aprobados
            WHERE alumno_id = %s AND curso_id = %s
        """
        existing = execute_query(query, (alumno_id, curso_id), fetch=True)

        if existing:
            # Update existing record
            query = """
                UPDATE cursos_aprobados 
                SET seccion_id = %s, nota_final = %s, aprobado = %s, fecha_aprobacion = %s
                WHERE id = %s
            """
            execute_query(
                query,
                (seccion_id, nota_final, aprobado, date.today(), existing[0]["id"]),
            )
            return existing[0]["id"]
        else:
            # Create new record
            query = """
                INSERT INTO cursos_aprobados 
                (alumno_id, curso_id, seccion_id, nota_final, aprobado, fecha_aprobacion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            return execute_query(
                query,
                (alumno_id, curso_id, seccion_id, nota_final, aprobado, date.today()),
            )

    @staticmethod
    def delete(curso_aprobado_id):
        """Delete an approved course record"""
        query = "DELETE FROM cursos_aprobados WHERE id = %s"
        execute_query(query, (curso_aprobado_id,))

    @staticmethod
    def calculate_and_register_final_grade(alumno_id, seccion_id):
        """Calculate final grade for a student in a section and register as completed course"""
        # First get the course_id for this section
        curso_id_query = """
            SELECT ic.curso_id 
            FROM secciones s
            JOIN instancias_curso ic ON s.instancia_curso_id = ic.id
            WHERE s.id = %s
        """
        curso_result = execute_query(curso_id_query, (seccion_id,), fetch=True)
        if not curso_result:
            raise Exception("Seccion no encontrada")

        curso_id = curso_result[0]["curso_id"]

        # Get the student's grade in this section
        alumno_seccion_query = """
            SELECT id FROM alumno_seccion
            WHERE alumno_id = %s AND seccion_id = %s
        """
        alumno_seccion = execute_query(
            alumno_seccion_query, (alumno_id, seccion_id), fetch=True
        )
        if not alumno_seccion:
            raise Exception("Alumno no encontrado en la sección")

        alumno_seccion_id = alumno_seccion[0]["id"]

        # Calculate final grade (this is a simplified calculation)
        # A complete implementation would need to account for the grading scheme of the section
        final_grade_query = """
            SELECT COALESCE(AVG(n.nota), 0) AS nota_final
            FROM notas n
            JOIN instancias_evaluacion ie ON n.instancia_evaluacion_id = ie.id
            JOIN topicos_evaluacion te ON ie.topico_id = te.id
            WHERE n.alumno_seccion_id = %s
        """
        grade_result = execute_query(
            final_grade_query, (alumno_seccion_id,), fetch=True
        )
        nota_final = grade_result[0]["nota_final"] if grade_result else 0

        # In Chile, the passing grade is usually 4.0 out of 7.0
        aprobado = nota_final >= 4.0

        # Register the completed course
        return CursoAprobado.register_curso_aprobado(
            alumno_id, curso_id, seccion_id, nota_final, aprobado
        )
