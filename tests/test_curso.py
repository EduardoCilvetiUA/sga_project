import pytest
from models.curso import Curso
from db import execute_query, get_db_connection

# ID global para usar en las pruebas
curso_id_test = None


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Prepara la base de datos para las pruebas"""
    # Limpia la tabla de cursos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Eliminar datos existentes para evitar duplicados
    try:
        cursor.execute("DELETE FROM prerequisitos")
        cursor.execute("DELETE FROM cursos")
        connection.commit()
    except Exception as e:
        print(f"Error al limpiar datos: {e}")
    finally:
        cursor.close()
        connection.close()


def test_create_curso():
    """Prueba la creación de un curso"""
    global curso_id_test

    # Crear un curso de prueba
    curso_id = Curso.create("TST123", "Curso de Prueba")
    curso_id_test = curso_id

    # Verificar que se creó correctamente
    assert curso_id is not None
    assert curso_id > 0


def test_get_all_cursos():
    """Prueba obtener todos los cursos"""
    # Obtener todos los cursos
    cursos = Curso.get_all()

    # Verificar que la lista no está vacía y contiene el curso de prueba
    assert cursos is not None
    assert len(cursos) > 0

    # Buscar el curso creado en la prueba anterior
    curso_encontrado = False
    for curso in cursos:
        if curso["codigo"] == "TST123":
            curso_encontrado = True
            assert curso["nombre"] == "Curso de Prueba"
            break

    assert curso_encontrado


def test_get_curso_by_id():
    """Prueba obtener un curso por ID"""
    global curso_id_test

    # Verificar que tenemos un ID válido para probar
    assert curso_id_test is not None

    # Obtener el curso por ID
    curso = Curso.get_by_id(curso_id_test)

    # Verificar que se encontró el curso y tiene los datos correctos
    assert curso is not None
    assert curso["codigo"] == "TST123"
    assert curso["nombre"] == "Curso de Prueba"


def test_update_curso():
    """Prueba actualizar un curso"""
    global curso_id_test

    # Actualizar el curso
    Curso.update(curso_id_test, "TST456", "Curso Actualizado")

    # Verificar que se actualizó correctamente
    curso = Curso.get_by_id(curso_id_test)
    assert curso["codigo"] == "TST456"
    assert curso["nombre"] == "Curso Actualizado"


def test_prerequisitos():
    """Prueba la gestión de prerequisitos"""
    global curso_id_test

    # Crear otro curso para usar como prerequisito
    prereq_id = Curso.create("PRE123", "Prerequisito de Prueba")

    # Añadir el prerequisito
    Curso.add_prerequisite(curso_id_test, prereq_id)

    # Verificar que se añadió correctamente
    prereqs = Curso.get_prerequisites(curso_id_test)
    assert len(prereqs) > 0

    prereq_encontrado = False
    for prereq in prereqs:
        if prereq["codigo"] == "PRE123":
            prereq_encontrado = True
            break

    assert prereq_encontrado

    # Eliminar el prerequisito
    Curso.remove_prerequisite(curso_id_test, prereq_id)

    # Verificar que se eliminó correctamente
    prereqs = Curso.get_prerequisites(curso_id_test)
    assert prereqs is not None

    # Si prereqs es None, cambiarlo a una lista vacía
    prereqs = [] if prereqs is None else prereqs

    prereq_encontrado = False
    for prereq in prereqs:
        if prereq["codigo"] == "PRE123":
            prereq_encontrado = True
            break

    assert not prereq_encontrado


def test_delete_curso():
    """Prueba la eliminación de un curso"""
    global curso_id_test

    # Eliminar el curso
    Curso.delete(curso_id_test)

    # Verificar que se eliminó correctamente
    curso = Curso.get_by_id(curso_id_test)
    assert curso is None
