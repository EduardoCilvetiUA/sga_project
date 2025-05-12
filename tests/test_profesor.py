import pytest
from models.profesor import Profesor
from db import get_db_connection

profesor_id_test = None


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    connection = get_db_connection()
    cursor = connection.cursor()

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
    global profesor_id_test

    profesor_id = Profesor.create("Profesor Test", "profesor.test@universidad.cl")
    profesor_id_test = profesor_id

    assert profesor_id is not None
    assert profesor_id > 0


def test_get_all_profesores():
    profesores = Profesor.get_all()

    assert profesores is not None
    assert len(profesores) > 0

    profesor_encontrado = False
    for profesor in profesores:
        if profesor["correo"] == "profesor.test@universidad.cl":
            profesor_encontrado = True
            assert profesor["nombre"] == "Profesor Test"
            break

    assert profesor_encontrado


def test_get_profesor_by_id():
    global profesor_id_test

    assert profesor_id_test is not None

    profesor = Profesor.get_by_id(profesor_id_test)

    assert profesor is not None
    assert profesor["correo"] == "profesor.test@universidad.cl"
    assert profesor["nombre"] == "Profesor Test"


def test_update_profesor():
    global profesor_id_test

    Profesor.update(
        profesor_id_test, "Profesor Actualizado", "profesor.test@universidad.cl"
    )

    profesor = Profesor.get_by_id(profesor_id_test)
    assert profesor["nombre"] == "Profesor Actualizado"
    assert profesor["correo"] == "profesor.test@universidad.cl"


def test_delete_profesor():
    global profesor_id_test

    Profesor.delete(profesor_id_test)

    profesor = Profesor.get_by_id(profesor_id_test)
    assert profesor is None
