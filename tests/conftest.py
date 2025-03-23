import pytest
import os
import sys

# Añadir el directorio raíz al path para poder importar los módulos de la aplicación
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuración global para las pruebas
@pytest.fixture(scope="session", autouse=True)
def setup_testing_environment():
    # Aquí puedes colocar cualquier configuración que afecte a todas las pruebas
    print("Iniciando pruebas del Sistema de Gestión Académica")
    yield
    print("Finalizando pruebas del Sistema de Gestión Académica")