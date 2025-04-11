import pytest
from models.profesor import Profesor
from db import execute_query, get_db_connection

# ID global para usar en las pruebas
profesor_id_test = None


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Prepara la base de datos para las pruebas"""
    # Limpia la tabla de profesores
    connection = get_db_connection()
    cursor = connection.cursor()

    # Eliminar datos existentes para evitar duplicados
    try:
        cursor.execute("DELETE FROM profesor_seccion")
        cursor.execute(
            "DELETE FROM profesores WHERE correo = 'profesor.test@universidad.cl'"
        )
        connection.commit()
    except Exception as e:
        print(f"Error al limpiar datos: {e}")
    finally:
        cursor.close()
        connection.close()


def test_create_profesor():
    """Prueba la creación de un profesor"""
    global profesor_id_test

    # Crear un profesor de prueba
    profesor_id = Profesor.create("Profesor Test", "profesor.test@universidad.cl")
    profesor_id_test = profesor_id

    # Verificar que se creó correctamente
    assert profesor_id is not None
    assert profesor_id > 0


def test_get_all_profesores():
    """Prueba obtener todos los profesores"""
    # Obtener todos los profesores
    profesores = Profesor.get_all()

    # Verificar que la lista no está vacía y contiene el profesor de prueba
    assert profesores is not None
    assert len(profesores) > 0

    # Buscar el profesor creado en la prueba anterior
    profesor_encontrado = False
    for profesor in profesores:
        if profesor["correo"] == "profesor.test@universidad.cl":
            profesor_encontrado = True
            assert profesor["nombre"] == "Profesor Test"
            break

    assert profesor_encontrado


def test_get_profesor_by_id():
    """Prueba obtener un profesor por ID"""
    global profesor_id_test

    # Verificar que tenemos un ID válido para probar
    assert profesor_id_test is not None

    # Obtener el profesor por ID
    profesor = Profesor.get_by_id(profesor_id_test)

    # Verificar que se encontró el profesor y tiene los datos correctos
    assert profesor is not None
    assert profesor["correo"] == "profesor.test@universidad.cl"
    assert profesor["nombre"] == "Profesor Test"


def test_update_profesor():
    """Prueba actualizar un profesor"""
    global profesor_id_test

    # Actualizar el profesor
    Profesor.update(
        profesor_id_test, "Profesor Actualizado", "profesor.test@universidad.cl"
    )

    # Verificar que se actualizó correctamente
    profesor = Profesor.get_by_id(profesor_id_test)
    assert profesor["nombre"] == "Profesor Actualizado"
    assert profesor["correo"] == "profesor.test@universidad.cl"


def test_delete_profesor():
    """Prueba la eliminación de un profesor"""
    global profesor_id_test

    # Eliminar el profesor
    Profesor.delete(profesor_id_test)

    # Verificar que se eliminó correctamente
    profesor = Profesor.get_by_id(profesor_id_test)
    assert profesor is None
