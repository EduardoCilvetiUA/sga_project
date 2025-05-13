from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.instancia import Instancia
from models.curso import Curso

bp = Blueprint("instancias", __name__, url_prefix="/instancias")


@bp.route("/")
def index():
    instancias = Instancia.get_all()
    return render_template("instancias/index.html", instancias=instancias)


@bp.route("/create", methods=("GET", "POST"))
def create():
    cursos = Curso.get_all()

    if request.method == "POST":
        curso_id = request.form["curso_id"]
        anio = request.form["anio"]
        periodo = request.form["periodo"]

        error = None

        if not curso_id:
            error = "El curso es requerido."
        elif not anio:
            error = "El año es requerido."
        elif not periodo:
            error = "El periodo es requerido."

        if error is None:
            try:
                Instancia.create(curso_id, anio, periodo)
                flash("Instancia de curso creada exitosamente!")
                return redirect(url_for("instancias.index"))
            except Exception as e:
                error = f"Error al crear la instancia de curso: {e}"

        flash(error)

    return render_template("instancias/create.html", cursos=cursos)


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    instancia = Instancia.get_by_id(id)
    cursos = Curso.get_all()

    if request.method == "POST":
        curso_id = request.form["curso_id"]
        anio = request.form["anio"]
        periodo = request.form["periodo"]

        error = None

        if not curso_id:
            error = "El curso es requerido."
        elif not anio:
            error = "El año es requerido."
        elif not periodo:
            error = "El periodo es requerido."

        if error is None:
            try:
                Instancia.update(id, curso_id, anio, periodo)
                flash("Instancia de curso actualizada exitosamente!")
                return redirect(url_for("instancias.index"))
            except Exception as e:
                error = f"Error al actualizar la instancia de curso: {e}"

        flash(error)

    return render_template("instancias/edit.html", instancia=instancia, cursos=cursos)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    try:
        Instancia.delete(id)
        flash("Instancia de curso eliminada exitosamente!")
    except Exception as e:
        flash(f"Error al eliminar la instancia de curso: {e}")

    return redirect(url_for("instancias.index"))


@bp.route("/<int:id>/view")
def view(id):
    instancia = Instancia.get_by_id(id)
    secciones = Instancia.get_secciones(id)

    return render_template(
        "instancias/view.html", instancia=instancia, secciones=secciones
    )
