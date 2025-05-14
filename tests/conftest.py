import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(scope="session", autouse=True)
def setup_testing_environment():
    print("Iniciando pruebas del Sistema de Gestión Académica")
    yield
    print("Finalizando pruebas del Sistema de Gestión Académica")
