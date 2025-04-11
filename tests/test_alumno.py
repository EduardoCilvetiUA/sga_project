import pytest
from models.alumno import Alumno
from db import execute_query, get_db_connection
from datetime import date

# ID global para usar en las pruebas
alumno_id_test = None


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Prepara la base de datos para las pruebas"""
    # Limpia la tabla de alumnos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Eliminar datos existentes para evitar duplicados
    try:
        cursor.execute("DELETE FROM alumno_seccion")
        cursor.execute(
            "DELETE FROM alumnos WHERE correo = 'alumno.test@universidad.cl'"
        )
        connection.commit()
    except Exception as e:
        print(f"Error al limpiar datos: {e}")
    finally:
        cursor.close()
        connection.close()


def test_create_alumno():
    """Prueba la creación de un alumno"""
    global alumno_id_test

    # Crear un alumno de prueba
    fecha_ingreso = date(2024, 3, 1)
    alumno_id = Alumno.create(
        "Alumno Test", "alumno.test@universidad.cl", fecha_ingreso
    )
    alumno_id_test = alumno_id

    # Verificar que se creó correctamente
    assert alumno_id is not None
    assert alumno_id > 0


def test_get_all_alumnos():
    """Prueba obtener todos los alumnos"""
    # Obtener todos los alumnos
    alumnos = Alumno.get_all()

    # Verificar que la lista no está vacía y contiene el alumno de prueba
    assert alumnos is not None
    assert len(alumnos) > 0

    # Buscar el alumno creado en la prueba anterior
    alumno_encontrado = False
    for alumno in alumnos:
        if alumno["correo"] == "alumno.test@universidad.cl":
            alumno_encontrado = True
            assert alumno["nombre"] == "Alumno Test"
            break

    assert alumno_encontrado


def test_get_alumno_by_id():
    """Prueba obtener un alumno por ID"""
    global alumno_id_test

    # Verificar que tenemos un ID válido para probar
    assert alumno_id_test is not None

    # Obtener el alumno por ID
    alumno = Alumno.get_by_id(alumno_id_test)

    # Verificar que se encontró el alumno y tiene los datos correctos
    assert alumno is not None
    assert alumno["correo"] == "alumno.test@universidad.cl"
    assert alumno["nombre"] == "Alumno Test"


def test_update_alumno():
    """Prueba actualizar un alumno"""
    global alumno_id_test

    # Fecha para la actualización
    fecha_ingreso = date(2024, 3, 1)

    # Actualizar el alumno
    Alumno.update(
        alumno_id_test,
        "Alumno Actualizado",
        "alumno.test@universidad.cl",
        fecha_ingreso,
    )

    # Verificar que se actualizó correctamente
    alumno = Alumno.get_by_id(alumno_id_test)
    assert alumno["nombre"] == "Alumno Actualizado"
    assert alumno["correo"] == "alumno.test@universidad.cl"


def test_delete_alumno():
    """Prueba la eliminación de un alumno"""
    global alumno_id_test

    # Eliminar el alumno
    Alumno.delete(alumno_id_test)

    # Verificar que se eliminó correctamente
    alumno = Alumno.get_by_id(alumno_id_test)
    assert alumno is None
