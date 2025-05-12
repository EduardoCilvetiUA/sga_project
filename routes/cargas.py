from flask import Blueprint, render_template, request, redirect, flash
from utils.json_loader import JsonLoader
import os

bp = Blueprint("cargas", __name__, url_prefix="/cargas")


@bp.route("/")
def index():
    return render_template("cargas/index.html")


@bp.route("/alumnos", methods=["GET", "POST"])
def cargar_alumnos():
    if request.method == "POST":
        if "archivo" not in request.files:
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        archivo = request.files["archivo"]

        if archivo.filename == "":
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        if archivo and archivo.filename.endswith(".json"):
            temp_path = os.path.join("/tmp", archivo.filename)
            archivo.save(temp_path)

            try:
                resultados = JsonLoader.load_alumnos(temp_path)

                os.remove(temp_path)

                flash(
                    f"Carga completada: {resultados['exitosos']} exitosos, {resultados['fallidos']} fallidos"
                )
                return render_template(
                    "cargas/resultados.html", resultados=resultados, tipo="alumnos"
                )
            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}")
                return redirect(request.url)
        else:
            flash("El archivo debe tener formato JSON")
            return redirect(request.url)

    return render_template("cargas/alumnos.html")


@bp.route("/profesores", methods=["GET", "POST"])
def cargar_profesores():
    if request.method == "POST":
        if "archivo" not in request.files:
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        archivo = request.files["archivo"]

        if archivo.filename == "":
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        if archivo and archivo.filename.endswith(".json"):
            temp_path = os.path.join("/tmp", archivo.filename)
            archivo.save(temp_path)

            try:
                resultados = JsonLoader.load_profesores(temp_path)

                os.remove(temp_path)

                flash(
                    f"Carga completada: {resultados['exitosos']} exitosos, {resultados['fallidos']} fallidos"
                )
                return render_template(
                    "cargas/resultados.html", resultados=resultados, tipo="profesores"
                )
            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}")
                return redirect(request.url)
        else:
            flash("El archivo debe tener formato JSON")
            return redirect(request.url)

    return render_template("cargas/profesores.html")


@bp.route("/cursos", methods=["GET", "POST"])
def cargar_cursos():
    if request.method == "POST":
        if "archivo" not in request.files:
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        archivo = request.files["archivo"]

        if archivo.filename == "":
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        if archivo and archivo.filename.endswith(".json"):
            temp_path = os.path.join("/tmp", archivo.filename)
            archivo.save(temp_path)

            try:
                resultados = JsonLoader.load_cursos(temp_path)

                os.remove(temp_path)

                flash(
                    f"Carga completada: {resultados['exitosos']} exitosos, {resultados['fallidos']} fallidos"
                )
                return render_template(
                    "cargas/resultados.html", resultados=resultados, tipo="cursos"
                )
            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}")
                return redirect(request.url)
        else:
            flash("El archivo debe tener formato JSON")
            return redirect(request.url)

    return render_template("cargas/cursos.html")


@bp.route("/salas", methods=["GET", "POST"])
def cargar_salas():
    if request.method == "POST":
        if "archivo" not in request.files:
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        archivo = request.files["archivo"]

        if archivo.filename == "":
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        if archivo and archivo.filename.endswith(".json"):
            temp_path = os.path.join("/tmp", archivo.filename)
            archivo.save(temp_path)

            try:
                resultados = JsonLoader.load_salas(temp_path)

                os.remove(temp_path)

                flash(
                    f"Carga completada: {resultados['exitosos']} exitosos, {resultados['fallidos']} fallidos"
                )
                return render_template(
                    "cargas/resultados.html", resultados=resultados, tipo="salas"
                )
            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}")
                return redirect(request.url)
        else:
            flash("El archivo debe tener formato JSON")
            return redirect(request.url)

    return render_template("cargas/salas.html")


@bp.route("/instancias", methods=["GET", "POST"])
def cargar_instancias():
    if request.method == "POST":
        if "archivo" not in request.files:
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        archivo = request.files["archivo"]

        if archivo.filename == "":
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        if archivo and archivo.filename.endswith(".json"):
            temp_path = os.path.join("/tmp", archivo.filename)
            archivo.save(temp_path)

            try:
                resultados = JsonLoader.load_instancias_cursos(temp_path)

                os.remove(temp_path)

                flash(
                    f"Carga completada: {resultados['exitosos']} exitosos, {resultados['fallidos']} fallidos"
                )
                return render_template(
                    "cargas/resultados.html", resultados=resultados, tipo="instancias"
                )
            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}")
                return redirect(request.url)
        else:
            flash("El archivo debe tener formato JSON")
            return redirect(request.url)

    return render_template("cargas/instancias.html")


@bp.route("/secciones", methods=["GET", "POST"])
def cargar_secciones():
    if request.method == "POST":
        if "archivo" not in request.files:
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        archivo = request.files["archivo"]

        if archivo.filename == "":
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        if archivo and archivo.filename.endswith(".json"):
            temp_path = os.path.join("/tmp", archivo.filename)
            archivo.save(temp_path)

            try:
                resultados = JsonLoader.load_secciones(temp_path)

                os.remove(temp_path)

                flash(
                    f"Carga completada: {resultados['exitosos']} exitosos, {resultados['fallidos']} fallidos"
                )
                return render_template(
                    "cargas/resultados.html", resultados=resultados, tipo="secciones"
                )
            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}")
                return redirect(request.url)
        else:
            flash("El archivo debe tener formato JSON")
            return redirect(request.url)

    return render_template("cargas/secciones.html")


@bp.route("/alumnos_seccion", methods=["GET", "POST"])
def cargar_alumnos_seccion():
    if request.method == "POST":
        if "archivo" not in request.files:
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        archivo = request.files["archivo"]

        if archivo.filename == "":
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        if archivo and archivo.filename.endswith(".json"):
            temp_path = os.path.join("/tmp", archivo.filename)
            archivo.save(temp_path)

            try:
                resultados = JsonLoader.load_alumnos_seccion(temp_path)

                os.remove(temp_path)

                flash(
                    f"Carga completada: {resultados['exitosos']} exitosos, {resultados['fallidos']} fallidos"
                )
                return render_template(
                    "cargas/resultados.html",
                    resultados=resultados,
                    tipo="alumnos_seccion",
                )
            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}")
                return redirect(request.url)
        else:
            flash("El archivo debe tener formato JSON")
            return redirect(request.url)

    return render_template("cargas/alumnos_seccion.html")


@bp.route("/notas", methods=["GET", "POST"])
def cargar_notas():
    if request.method == "POST":
        if "archivo" not in request.files:
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        archivo = request.files["archivo"]

        if archivo.filename == "":
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)

        if archivo and archivo.filename.endswith(".json"):
            temp_path = os.path.join("/tmp", archivo.filename)
            archivo.save(temp_path)

            try:
                resultados = JsonLoader.load_notas(temp_path)

                os.remove(temp_path)

                flash(
                    f"Carga completada: {resultados['exitosos']} exitosos, {resultados['fallidos']} fallidos"
                )
                return render_template(
                    "cargas/resultados.html", resultados=resultados, tipo="notas"
                )
            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}")
                return redirect(request.url)
        else:
            flash("El archivo debe tener formato JSON")
            return redirect(request.url)

    return render_template("cargas/notas.html")
