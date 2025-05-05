from flask import Flask, render_template
from db import init_db
from routes import cursos, profesores, alumnos, instancias, secciones, evaluaciones, notas, cargas, horarios, salas

app = Flask(__name__)
app.config.from_object('config.Config')

app.register_blueprint(cursos.bp)
app.register_blueprint(profesores.bp)
app.register_blueprint(alumnos.bp)
app.register_blueprint(instancias.bp)
app.register_blueprint(secciones.bp)
app.register_blueprint(evaluaciones.bp)
app.register_blueprint(notas.bp)
app.register_blueprint(cargas.bp)
app.register_blueprint(horarios.bp)
app.register_blueprint(salas.bp)
@app.route('/')
def index():
    return render_template('index.html')

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')