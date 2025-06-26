import pytest
import os
import json
import tempfile
from flask import Flask
from routes.cargas import bp
from unittest.mock import patch, MagicMock
from utils.json_loader import JsonLoader


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-key'
    app.template_folder = 'templates'
    app.register_blueprint(bp)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def temp_json_file(tmp_path):
    def _create_temp_file(data):
        temp_file = tmp_path / "test_file.json"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return str(temp_file)
    return _create_temp_file


class TestCargasRoutes:
    
    @patch('routes.cargas.render_template')
    def test_index_route(self, mock_render, client):
        mock_render.return_value = 'test response'
        response = client.get('/cargas/')
        assert response.status_code == 200

    @patch('routes.cargas.render_template')
    def test_cargar_alumnos_get(self, mock_render, client):
        mock_render.return_value = 'test response'
        response = client.get('/cargas/alumnos')
        assert response.status_code == 200

    @patch('routes.cargas.render_template')
    def test_cargar_profesores_get(self, mock_render, client):
        mock_render.return_value = 'test response'
        response = client.get('/cargas/profesores')
        assert response.status_code == 200

    @patch('routes.cargas.render_template')
    def test_cargar_cursos_get(self, mock_render, client):
        mock_render.return_value = 'test response'
        response = client.get('/cargas/cursos')
        assert response.status_code == 200

    @patch('routes.cargas.render_template')
    def test_cargar_salas_get(self, mock_render, client):
        mock_render.return_value = 'test response'
        response = client.get('/cargas/salas')
        assert response.status_code == 200

    @patch('routes.cargas.render_template')
    def test_cargar_instancias_get(self, mock_render, client):
        mock_render.return_value = 'test response'
        response = client.get('/cargas/instancias')
        assert response.status_code == 200

    @patch('routes.cargas.render_template')
    def test_cargar_secciones_get(self, mock_render, client):
        mock_render.return_value = 'test response'
        response = client.get('/cargas/secciones')
        assert response.status_code == 200

    @patch('routes.cargas.render_template')
    def test_cargar_alumnos_seccion_get(self, mock_render, client):
        mock_render.return_value = 'test response'
        response = client.get('/cargas/alumnos_seccion')
        assert response.status_code == 200

    @patch('routes.cargas.render_template')
    def test_cargar_notas_get(self, mock_render, client):
        mock_render.return_value = 'test response'
        response = client.get('/cargas/notas')
        assert response.status_code == 200

    def test_cargar_alumnos_post_no_file(self, client):
        response = client.post('/cargas/alumnos', data={})
        assert response.status_code == 302

    def test_cargar_alumnos_post_empty_filename(self, client):
        response = client.post('/cargas/alumnos', data={'archivo': (open(__file__, 'rb'), '')})
        assert response.status_code == 302

    def test_cargar_alumnos_post_non_json_file(self, client):
        response = client.post('/cargas/alumnos', data={'archivo': (open(__file__, 'rb'), 'test.txt')})
        assert response.status_code == 302

    @patch('routes.cargas.render_template')
    @patch('routes.cargas.JsonLoader.load_alumnos')
    @patch('os.remove')
    def test_cargar_alumnos_post_success(self, mock_remove, mock_load_alumnos, mock_render, client, temp_json_file):
        test_data = {
            "alumnos": [
                {"id": 1, "nombre": "Test Student", "correo": "test@test.com", "anio_ingreso": 2024}
            ]
        }
        temp_file = temp_json_file(test_data)
        
        mock_load_alumnos.return_value = {"exitosos": 1, "fallidos": 0, "errores": []}
        mock_render.return_value = 'success response'
        
        with open(temp_file, 'rb') as f:
            response = client.post('/cargas/alumnos', data={'archivo': (f, 'test.json')})
        
        assert response.status_code == 200
        mock_load_alumnos.assert_called_once()
        mock_remove.assert_called_once()

    @patch('routes.cargas.JsonLoader.load_alumnos')
    @patch('os.remove')
    def test_cargar_alumnos_post_exception(self, mock_remove, mock_load_alumnos, client, temp_json_file):
        test_data = {"alumnos": []}
        temp_file = temp_json_file(test_data)
        
        mock_load_alumnos.side_effect = Exception("Test error")
        
        with open(temp_file, 'rb') as f:
            response = client.post('/cargas/alumnos', data={'archivo': (f, 'test.json')})
        
        assert response.status_code == 302

    @patch('routes.cargas.render_template')
    @patch('routes.cargas.JsonLoader.load_profesores')
    @patch('os.remove')
    def test_cargar_profesores_post_success(self, mock_remove, mock_load_profesores, mock_render, client, temp_json_file):
        test_data = {
            "profesores": [
                {"id": 1, "nombre": "Test Professor", "correo": "prof@test.com"}
            ]
        }
        temp_file = temp_json_file(test_data)
        
        mock_load_profesores.return_value = {"exitosos": 1, "fallidos": 0, "errores": []}
        mock_render.return_value = 'success response'
        
        with open(temp_file, 'rb') as f:
            response = client.post('/cargas/profesores', data={'archivo': (f, 'test.json')})
        
        assert response.status_code == 200
        mock_load_profesores.assert_called_once()

    @patch('routes.cargas.render_template')
    @patch('routes.cargas.JsonLoader.load_cursos')
    @patch('os.remove')
    def test_cargar_cursos_post_success(self, mock_remove, mock_load_cursos, mock_render, client, temp_json_file):
        test_data = {
            "cursos": [
                {"id": 1, "codigo": "TEST101", "descripcion": "Test Course", "creditos": 3}
            ]
        }
        temp_file = temp_json_file(test_data)
        
        mock_load_cursos.return_value = {"exitosos": 1, "fallidos": 0, "errores": []}
        mock_render.return_value = 'success response'
        
        with open(temp_file, 'rb') as f:
            response = client.post('/cargas/cursos', data={'archivo': (f, 'test.json')})
        
        assert response.status_code == 200
        mock_load_cursos.assert_called_once()

    @patch('routes.cargas.render_template')
    @patch('routes.cargas.JsonLoader.load_salas')
    @patch('os.remove')
    def test_cargar_salas_post_success(self, mock_remove, mock_load_salas, mock_render, client, temp_json_file):
        test_data = {
            "salas": [
                {"id": 1, "nombre": "Test Room", "capacidad": 30}
            ]
        }
        temp_file = temp_json_file(test_data)
        
        mock_load_salas.return_value = {"exitosos": 1, "fallidos": 0, "errores": []}
        mock_render.return_value = 'success response'
        
        with open(temp_file, 'rb') as f:
            response = client.post('/cargas/salas', data={'archivo': (f, 'test.json')})
        
        assert response.status_code == 200
        mock_load_salas.assert_called_once()

    @patch('routes.cargas.render_template')
    @patch('routes.cargas.JsonLoader.load_instancias_cursos')
    @patch('os.remove')
    def test_cargar_instancias_post_success(self, mock_remove, mock_load_instancias, mock_render, client, temp_json_file):
        test_data = {
            "año": 2024,
            "semestre": 1,
            "instancias": [
                {"id": 1, "curso_id": 1}
            ]
        }
        temp_file = temp_json_file(test_data)
        
        mock_load_instancias.return_value = {"exitosos": 1, "fallidos": 0, "errores": []}
        mock_render.return_value = 'success response'
        
        with open(temp_file, 'rb') as f:
            response = client.post('/cargas/instancias', data={'archivo': (f, 'test.json')})
        
        assert response.status_code == 200
        mock_load_instancias.assert_called_once()

    @patch('routes.cargas.render_template')
    @patch('routes.cargas.JsonLoader.load_secciones')
    @patch('os.remove')
    def test_cargar_secciones_post_success(self, mock_remove, mock_load_secciones, mock_render, client, temp_json_file):
        test_data = {
            "secciones": [
                {
                    "id": 1,
                    "instancia_curso": 1,
                    "profesor_id": 1,
                    "evaluacion": {
                        "tipo": "porcentaje",
                        "combinacion_topicos": [],
                        "topicos": {}
                    }
                }
            ]
        }
        temp_file = temp_json_file(test_data)
        
        mock_load_secciones.return_value = {"exitosos": 1, "fallidos": 0, "errores": []}
        mock_render.return_value = 'success response'
        
        with open(temp_file, 'rb') as f:
            response = client.post('/cargas/secciones', data={'archivo': (f, 'test.json')})
        
        assert response.status_code == 200
        mock_load_secciones.assert_called_once()

    @patch('routes.cargas.render_template')
    @patch('routes.cargas.JsonLoader.load_alumnos_seccion')
    @patch('os.remove')
    def test_cargar_alumnos_seccion_post_success(self, mock_remove, mock_load_alumnos_seccion, mock_render, client, temp_json_file):
        test_data = {
            "alumnos_seccion": [
                {"alumno_id": 1, "seccion_id": 1}
            ]
        }
        temp_file = temp_json_file(test_data)
        
        mock_load_alumnos_seccion.return_value = {"exitosos": 1, "fallidos": 0, "errores": []}
        mock_render.return_value = 'success response'
        
        with open(temp_file, 'rb') as f:
            response = client.post('/cargas/alumnos_seccion', data={'archivo': (f, 'test.json')})
        
        assert response.status_code == 200
        mock_load_alumnos_seccion.assert_called_once()

    @patch('routes.cargas.render_template')
    @patch('routes.cargas.JsonLoader.load_notas')
    @patch('os.remove')
    def test_cargar_notas_post_success(self, mock_remove, mock_load_notas, mock_render, client, temp_json_file):
        test_data = {
            "notas": [
                {"alumno_id": 1, "topico_id": 1, "instancia": 1, "nota": 6.5}
            ]
        }
        temp_file = temp_json_file(test_data)
        
        mock_load_notas.return_value = {"exitosos": 1, "fallidos": 0, "errores": []}
        mock_render.return_value = 'success response'
        
        with open(temp_file, 'rb') as f:
            response = client.post('/cargas/notas', data={'archivo': (f, 'test.json')})
        
        assert response.status_code == 200
        mock_load_notas.assert_called_once()

    def test_all_post_routes_without_file(self, client):
        routes = [
            'profesores', 'cursos', 'salas', 'instancias', 
            'secciones', 'alumnos_seccion', 'notas'
        ]
        
        for route in routes:
            response = client.post(f'/cargas/{route}', data={})
            assert response.status_code == 302

    def test_all_post_routes_with_non_json(self, client):
        routes = [
            'profesores', 'cursos', 'salas', 'instancias', 
            'secciones', 'alumnos_seccion', 'notas'
        ]
        
        for route in routes:
            response = client.post(f'/cargas/{route}', data={'archivo': (open(__file__, 'rb'), 'test.txt')})
            assert response.status_code == 302

    @patch('routes.cargas.JsonLoader.load_profesores')
    @patch('os.remove')
    def test_error_handling_cleanup(self, mock_remove, mock_load_profesores, client, temp_json_file):
        test_data = {"profesores": []}
        temp_file = temp_json_file(test_data)
        
        mock_load_profesores.side_effect = Exception("Database error")
        
        with open(temp_file, 'rb') as f:
            response = client.post('/cargas/profesores', data={'archivo': (f, 'test.json')})
        
        assert response.status_code == 302
        mock_load_profesores.assert_called_once()