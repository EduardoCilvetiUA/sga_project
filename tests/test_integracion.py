from models.curso import Curso
from models.profesor import Profesor
from models.alumno import Alumno
from models.instancia import Instancia
from models.seccion import Seccion
from models.evaluacion import Evaluacion
from models.nota import Nota
from db import get_db_connection
from datetime import date
import random
import string


class TestIntegracion:

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
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM notas")
            cursor.execute("DELETE FROM instancias_evaluacion")
            cursor.execute("DELETE FROM topicos_evaluacion")
            cursor.execute("DELETE FROM alumno_seccion WHERE 1=1")
            cursor.execute("DELETE FROM profesor_seccion WHERE 1=1")
            cursor.execute("DELETE FROM secciones WHERE 1=1")
            cursor.execute("DELETE FROM instancias_curso WHERE 1=1")
            cursor.execute("DELETE FROM prerequisitos WHERE 1=1")
            cursor.execute(
                "DELETE FROM profesores WHERE correo LIKE 'prof.integracion%'"
            )
            cursor.execute(
                "DELETE FROM alumnos WHERE correo LIKE 'alumno.integracion%'"
            )
            cursor.execute("DELETE FROM cursos WHERE codigo='INT100'")
            connection.commit()
        except Exception as e:
            print(f"Error al limpiar tablas: {e}")
        finally:
            cursor.close()
            connection.close()

    def test_01_crear_entidades_basicas(self):
        random_suffix = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=6)
        )

        TestIntegracion.curso_id = Curso.create("INT100", "Curso de Integración")
        assert TestIntegracion.curso_id is not None

        profesor_correo = f"prof.integracion.{random_suffix}@universidad.cl"
        TestIntegracion.profesor_id = Profesor.create(
            "Profesor Integración", profesor_correo
        )
        assert TestIntegracion.profesor_id is not None

        alumno_correo = f"alumno.integracion.{random_suffix}@universidad.cl"
        fecha_ingreso = date(2024, 3, 1)
        TestIntegracion.alumno_id = Alumno.create(
            "Alumno Integración", alumno_correo, fecha_ingreso
        )
        assert TestIntegracion.alumno_id is not None

    def test_02_crear_instancia_curso(self):
        TestIntegracion.instancia_id = Instancia.create(
            TestIntegracion.curso_id, 2024, "1"
        )
        assert TestIntegracion.instancia_id is not None

        instancia = Instancia.get_by_id(TestIntegracion.instancia_id)
        assert instancia["curso_id"] == TestIntegracion.curso_id
        assert instancia["anio"] == 2024
        assert instancia["periodo"] == "1"

    def test_03_crear_seccion(self):
        TestIntegracion.seccion_id = Seccion.create(TestIntegracion.instancia_id, 1)
        assert TestIntegracion.seccion_id is not None

        seccion = Seccion.get_by_id(TestIntegracion.seccion_id)
        assert seccion["instancia_curso_id"] == TestIntegracion.instancia_id
        assert seccion["numero"] == 1

    def test_04_asignar_profesor(self):
        Seccion.assign_profesor(TestIntegracion.seccion_id, TestIntegracion.profesor_id)

        profesores = Seccion.get_profesores(TestIntegracion.seccion_id)
        assert len(profesores) > 0
        profesor_encontrado = False
        for profesor in profesores:
            if profesor["id"] == TestIntegracion.profesor_id:
                profesor_encontrado = True
                break
        assert profesor_encontrado

    def test_05_inscribir_alumno(self):
        Seccion.enroll_alumno(TestIntegracion.seccion_id, TestIntegracion.alumno_id)

        alumnos = Seccion.get_alumnos(TestIntegracion.seccion_id)
        assert len(alumnos) > 0
        alumno_encontrado = False
        for alumno in alumnos:
            if alumno["id"] == TestIntegracion.alumno_id:
                alumno_encontrado = True
                break
        assert alumno_encontrado

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id FROM alumno_seccion WHERE alumno_id = %s AND seccion_id = %s",
            (TestIntegracion.alumno_id, TestIntegracion.seccion_id),
        )
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        TestIntegracion.alumno_seccion_id = result["id"]

    def test_06_crear_topico_evaluacion(self):
        TestIntegracion.topico_id = Evaluacion.create_topico(
            TestIntegracion.seccion_id, "Controles", 60.0
        )
        assert TestIntegracion.topico_id is not None

        topico = Evaluacion.get_topico_by_id(TestIntegracion.topico_id)
        assert topico["seccion_id"] == TestIntegracion.seccion_id
        assert topico["nombre"] == "Controles"
        assert float(topico["porcentaje"]) == 60.0

    def test_07_crear_instancia_evaluacion(self):
        TestIntegracion.instancia_evaluacion_id = Evaluacion.create_instancia(
            TestIntegracion.topico_id, "Control 1", 1.0, False
        )
        assert TestIntegracion.instancia_evaluacion_id is not None

        instancia = Evaluacion.get_instancia_by_id(
            TestIntegracion.instancia_evaluacion_id
        )
        assert instancia["topico_id"] == TestIntegracion.topico_id
        assert instancia["nombre"] == "Control 1"
        assert float(instancia["peso"]) == 1.0
        assert instancia["opcional"] == 0

    def test_08_registrar_nota(self):
        nota_id = Nota.create(
            TestIntegracion.alumno_seccion_id,
            TestIntegracion.instancia_evaluacion_id,
            5.5,
        )
        assert nota_id is not None

        notas = Nota.get_notas_by_alumno_seccion(
            TestIntegracion.alumno_id, TestIntegracion.seccion_id
        )
        assert len(notas) > 0
        nota_encontrada = False
        for nota in notas:
            if (
                nota["instancia_evaluacion_id"]
                == TestIntegracion.instancia_evaluacion_id
            ):
                nota_encontrada = True
                assert float(nota["nota"]) == 5.5
                break
        assert nota_encontrada

    def test_09_calcular_nota_final(self):
        nota_final = Nota.calculate_nota_final(
            TestIntegracion.alumno_id, TestIntegracion.seccion_id
        )

        assert nota_final is not None
        assert nota_final == 5.5
