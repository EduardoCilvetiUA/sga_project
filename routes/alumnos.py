from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.alumno import Alumno

bp = Blueprint("alumnos", __name__, url_prefix="/alumnos")


@bp.route("/")
def index():
    alumnos = Alumno.get_all()
    return render_template("alumnos/index.html", alumnos=alumnos)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        fecha_ingreso = request.form["fecha_ingreso"]

        error = None

        if not nombre:
            error = "El nombre es requerido."
        elif not correo:
            error = "El correo es requerido."
        elif not fecha_ingreso:
            error = "La fecha de ingreso es requerida."

        if error is None:
            try:
                Alumno.create(nombre, correo, fecha_ingreso)
                flash("Alumno creado exitosamente!")
                return redirect(url_for("alumnos.index"))
            except Exception as e:
                error = f"Error al crear el alumno: {e}"

        flash(error)

    return render_template("alumnos/create.html")


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    alumno = Alumno.get_by_id(id)

    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        fecha_ingreso = request.form["fecha_ingreso"]

        error = None

        if not nombre:
            error = "El nombre es requerido."
        elif not correo:
            error = "El correo es requerido."
        elif not fecha_ingreso:
            error = "La fecha de ingreso es requerida."

        if error is None:
            try:
                Alumno.update(id, nombre, correo, fecha_ingreso)
                flash("Alumno actualizado exitosamente!")
                return redirect(url_for("alumnos.index"))
            except Exception as e:
                error = f"Error al actualizar el alumno: {e}"

        flash(error)

    return render_template("alumnos/edit.html", alumno=alumno)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    try:
        Alumno.delete(id)
        flash("Alumno eliminado exitosamente!")
    except Exception as e:
        flash(f"Error al eliminar el alumno: {e}")

    return redirect(url_for("alumnos.index"))


@bp.route("/<int:id>/view")
def view(id):
    alumno = Alumno.get_by_id(id)
    secciones = Alumno.get_secciones(id)

    return render_template("alumnos/view.html", alumno=alumno, secciones=secciones)
