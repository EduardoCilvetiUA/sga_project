import pytest
from models.alumno import Alumno
from db import get_db_connection
from datetime import date

alumno_id_test = None


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    connection = get_db_connection()
    cursor = connection.cursor()

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
    global alumno_id_test

    fecha_ingreso = date(2024, 3, 1)
    alumno_id = Alumno.create(
        "Alumno Test", "alumno.test@universidad.cl", fecha_ingreso
    )
    alumno_id_test = alumno_id

    assert alumno_id is not None
    assert alumno_id > 0


def test_get_all_alumnos():
    alumnos = Alumno.get_all()

    assert alumnos is not None
    assert len(alumnos) > 0

    alumno_encontrado = False
    for alumno in alumnos:
        if alumno["correo"] == "alumno.test@universidad.cl":
            alumno_encontrado = True
            assert alumno["nombre"] == "Alumno Test"
            break

    assert alumno_encontrado


def test_get_alumno_by_id():
    global alumno_id_test

    assert alumno_id_test is not None

    alumno = Alumno.get_by_id(alumno_id_test)

    assert alumno is not None
    assert alumno["correo"] == "alumno.test@universidad.cl"
    assert alumno["nombre"] == "Alumno Test"


def test_update_alumno():
    global alumno_id_test

    fecha_ingreso = date(2024, 3, 1)

    Alumno.update(
        alumno_id_test,
        "Alumno Actualizado",
        "alumno.test@universidad.cl",
        fecha_ingreso,
    )

    alumno = Alumno.get_by_id(alumno_id_test)
    assert alumno["nombre"] == "Alumno Actualizado"
    assert alumno["correo"] == "alumno.test@universidad.cl"


def test_delete_alumno():
    global alumno_id_test

    Alumno.delete(alumno_id_test)

    alumno = Alumno.get_by_id(alumno_id_test)
    assert alumno is None
