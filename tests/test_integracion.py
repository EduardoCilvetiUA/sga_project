import pytest
from models.curso import Curso
from models.profesor import Profesor
from models.alumno import Alumno
from models.instancia import Instancia
from models.seccion import Seccion
from models.evaluacion import Evaluacion
from models.nota import Nota
from db import execute_query, get_db_connection
from datetime import date

class TestIntegracion:
    """Pruebas de integración para el Sistema de Gestión Académica"""
    
    # Variables para almacenar IDs de prueba
    curso_id = None
    profesor_id = None
    alumno_id = None
    instancia_id = None
    seccion_id = None
    topico_id = None
    instancia_evaluacion_id = None
    alumno_seccion_id = None
    
    @classmethod
    def setup_class(cls):
        """Configuración inicial para las pruebas de integración"""
        # Limpiar tablas para evitar conflictos
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM notas")
            cursor.execute("DELETE FROM instancias_evaluacion")
            cursor.execute("DELETE FROM topicos_evaluacion")
            cursor.execute("DELETE FROM alumno_seccion")
            cursor.execute("DELETE FROM profesor_seccion")
            cursor.execute("DELETE FROM secciones")
            cursor.execute("DELETE FROM instancias_curso")
            cursor.execute("DELETE FROM prerequisitos")
            connection.commit()
        except Exception as e:
            print(f"Error al limpiar tablas: {e}")
        finally:
            cursor.close()
            connection.close()
    
    def test_01_crear_entidades_basicas(self):
        """Crear curso, profesor y alumno"""
        # Crear curso
        TestIntegracion.curso_id = Curso.create("INT100", "Curso de Integración")
        assert TestIntegracion.curso_id is not None
        
        # Crear profesor
        TestIntegracion.profesor_id = Profesor.create("Profesor Integración", "prof.integracion@universidad.cl")
        assert TestIntegracion.profesor_id is not None
        
        # Crear alumno
        fecha_ingreso = date(2024, 3, 1)
        TestIntegracion.alumno_id = Alumno.create("Alumno Integración", "alumno.integracion@universidad.cl", fecha_ingreso)
        assert TestIntegracion.alumno_id is not None
    
    def test_02_crear_instancia_curso(self):
        """Crear instancia de curso"""
        # Crear instancia de curso
        TestIntegracion.instancia_id = Instancia.create(TestIntegracion.curso_id, 2024, "01")
        assert TestIntegracion.instancia_id is not None
        
        # Verificar que se creó correctamente
        instancia = Instancia.get_by_id(TestIntegracion.instancia_id)
        assert instancia['curso_id'] == TestIntegracion.curso_id
        assert instancia['anio'] == 2024
        assert instancia['periodo'] == "01"
    
    def test_03_crear_seccion(self):
        """Crear sección para la instancia de curso"""
        # Crear sección
        TestIntegracion.seccion_id = Seccion.create(TestIntegracion.instancia_id, 1)
        assert TestIntegracion.seccion_id is not None
        
        # Verificar que se creó correctamente
        seccion = Seccion.get_by_id(TestIntegracion.seccion_id)
        assert seccion['instancia_curso_id'] == TestIntegracion.instancia_id
        assert seccion['numero'] == 1
    
    def test_04_asignar_profesor(self):
        """Asignar profesor a la sección"""
        # Asignar profesor
        Seccion.assign_professor(TestIntegracion.seccion_id, TestIntegracion.profesor_id)
        
        # Verificar asignación
        profesores = Seccion.get_professors(TestIntegracion.seccion_id)
        assert len(profesores) > 0
        profesor_encontrado = False
        for profesor in profesores:
            if profesor['id'] == TestIntegracion.profesor_id:
                profesor_encontrado = True
                break
        assert profesor_encontrado
    
    def test_05_inscribir_alumno(self):
        """Inscribir alumno en la sección"""
        # Inscribir alumno
        Seccion.enroll_student(TestIntegracion.seccion_id, TestIntegracion.alumno_id)
        
        # Verificar inscripción
        alumnos = Seccion.get_students(TestIntegracion.seccion_id)
        assert len(alumnos) > 0
        alumno_encontrado = False
        for alumno in alumnos:
            if alumno['id'] == TestIntegracion.alumno_id:
                alumno_encontrado = True
                break
        assert alumno_encontrado
        
        # Obtener alumno_seccion_id para usar en pruebas de notas
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id FROM alumno_seccion WHERE alumno_id = %s AND seccion_id = %s",
            (TestIntegracion.alumno_id, TestIntegracion.seccion_id)
        )
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        TestIntegracion.alumno_seccion_id = result['id']
    
    def test_06_crear_topico_evaluacion(self):
        """Crear tópico de evaluación para la sección"""
        # Crear tópico
        TestIntegracion.topico_id = Evaluacion.create_topic(TestIntegracion.seccion_id, "Controles", 60.0)
        assert TestIntegracion.topico_id is not None
        
        # Verificar creación
        topico = Evaluacion.get_topic_by_id(TestIntegracion.topico_id)
        assert topico['seccion_id'] == TestIntegracion.seccion_id
        assert topico['nombre'] == "Controles"
        assert float(topico['porcentaje']) == 60.0
    
    def test_07_crear_instancia_evaluacion(self):
        """Crear instancia de evaluación para el tópico"""
        # Crear instancia de evaluación
        TestIntegracion.instancia_evaluacion_id = Evaluacion.create_instance(
            TestIntegracion.topico_id, "Control 1", 1.0, False
        )
        assert TestIntegracion.instancia_evaluacion_id is not None
        
        # Verificar creación
        instancia = Evaluacion.get_instance_by_id(TestIntegracion.instancia_evaluacion_id)
        assert instancia['topico_id'] == TestIntegracion.topico_id
        assert instancia['nombre'] == "Control 1"
        assert float(instancia['peso']) == 1.0
        assert instancia['opcional'] == 0  # False en MySQL es 0
    
    def test_08_registrar_nota(self):
        """Registrar nota para el alumno"""
        # Registrar nota
        nota_id = Nota.create(TestIntegracion.alumno_seccion_id, TestIntegracion.instancia_evaluacion_id, 5.5)
        assert nota_id is not None
        
        # Verificar registro
        notas = Nota.get_grades_by_student_section(TestIntegracion.alumno_id, TestIntegracion.seccion_id)
        assert len(notas) > 0
        nota_encontrada = False
        for nota in notas:
            if nota['instancia_evaluacion_id'] == TestIntegracion.instancia_evaluacion_id:
                nota_encontrada = True
                assert float(nota['nota']) == 5.5
                break
        assert nota_encontrada
    
    def test_09_calcular_nota_final(self):
        """Calcular nota final del alumno"""
        # Calcular nota final
        nota_final = Nota.calculate_final_grade(TestIntegracion.alumno_id, TestIntegracion.seccion_id)
        
        # Como solo hay una nota, la nota final debe ser igual
        assert nota_final is not None
        assert nota_final == 5.5