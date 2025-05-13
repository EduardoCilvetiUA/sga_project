from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.profesor import Profesor

bp = Blueprint("profesores", __name__, url_prefix="/profesores")


@bp.route("/")
def index():
    profesores = Profesor.get_all()
    return render_template("profesores/index.html", profesores=profesores)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]

        error = None

        if not nombre:
            error = "El nombre es requerido."
        elif not correo:
            error = "El correo es requerido."

        if error is None:
            try:
                Profesor.create(nombre, correo)
                flash("Profesor creado exitosamente!")
                return redirect(url_for("profesores.index"))
            except Exception as e:
                error = f"Error al crear el profesor: {e}"

        flash(error)

    return render_template("profesores/create.html")


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    profesor = Profesor.get_by_id(id)

    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]

        error = None

        if not nombre:
            error = "El nombre es requerido."
        elif not correo:
            error = "El correo es requerido."

        if error is None:
            try:
                Profesor.update(id, nombre, correo)
                flash("Profesor actualizado exitosamente!")
                return redirect(url_for("profesores.index"))
            except Exception as e:
                error = f"Error al actualizar el profesor: {e}"

        flash(error)

    return render_template("profesores/edit.html", profesor=profesor)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    try:
        Profesor.delete(id)
        flash("Profesor eliminado exitosamente!")
    except Exception as e:
        flash(f"Error al eliminar el profesor: {e}")

    return redirect(url_for("profesores.index"))


@bp.route("/<int:id>/view")
def view(id):
    profesor = Profesor.get_by_id(id)
    secciones = Profesor.get_secciones(id)

    return render_template(
        "profesores/view.html", profesor=profesor, secciones=secciones
    )
