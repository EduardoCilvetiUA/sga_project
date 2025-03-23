from flask import Flask, render_template
from db import init_db
from routes import cursos, profesores, alumnos, instancias, secciones, evaluaciones, notas

app = Flask(__name__)
app.config.from_object('config.Config')

# Register blueprints
app.register_blueprint(cursos.bp)
app.register_blueprint(profesores.bp)
app.register_blueprint(alumnos.bp)
app.register_blueprint(instancias.bp)
app.register_blueprint(secciones.bp)
app.register_blueprint(evaluaciones.bp)
app.register_blueprint(notas.bp)

@app.route('/')
def index():
    return render_template('index.html')

# Initialize database
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')