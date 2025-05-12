import pytest
from models.curso import Curso
from db import get_db_connection

curso_id_test = None


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    connection = get_db_connection()
    cursor = connection.cursor()

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
    global curso_id_test

    curso_id = Curso.create("TST123", "Curso de Prueba")
    curso_id_test = curso_id

    assert curso_id is not None
    assert curso_id > 0


def test_get_all_cursos():
    cursos = Curso.get_all()

    assert cursos is not None
    assert len(cursos) > 0

    curso_encontrado = False
    for curso in cursos:
        if curso["codigo"] == "TST123":
            curso_encontrado = True
            assert curso["nombre"] == "Curso de Prueba"
            break

    assert curso_encontrado


def test_get_curso_by_id():
    global curso_id_test

    assert curso_id_test is not None

    curso = Curso.get_by_id(curso_id_test)

    assert curso is not None
    assert curso["codigo"] == "TST123"
    assert curso["nombre"] == "Curso de Prueba"


def test_update_curso():
    global curso_id_test

    Curso.update(curso_id_test, "TST456", "Curso Actualizado")

    curso = Curso.get_by_id(curso_id_test)
    assert curso["codigo"] == "TST456"
    assert curso["nombre"] == "Curso Actualizado"


def test_prerequisitos():
    global curso_id_test

    prereq_id = Curso.create("PRE123", "Prerequisito de Prueba")

    Curso.add_prerequisite(curso_id_test, prereq_id)

    prereqs = Curso.get_prerequisites(curso_id_test)
    assert len(prereqs) > 0

    prereq_encontrado = False
    for prereq in prereqs:
        if prereq["codigo"] == "PRE123":
            prereq_encontrado = True
            break

    assert prereq_encontrado

    Curso.remove_prerequisite(curso_id_test, prereq_id)

    prereqs = Curso.get_prerequisites(curso_id_test)
    assert prereqs is not None

    prereqs = [] if prereqs is None else prereqs

    prereq_encontrado = False
    for prereq in prereqs:
        if prereq["codigo"] == "PRE123":
            prereq_encontrado = True
            break

    assert not prereq_encontrado


def test_delete_curso():
    global curso_id_test

    Curso.delete(curso_id_test)

    curso = Curso.get_by_id(curso_id_test)
    assert curso is None
