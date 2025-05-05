from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.curso import Curso

bp = Blueprint("cursos", __name__, url_prefix="/cursos")


@bp.route("/")
def index():
    cursos = Curso.get_all()
    return render_template("cursos/index.html", cursos=cursos)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]

        error = None

        if not codigo:
            error = "El código es requerido."
        elif not nombre:
            error = "El nombre es requerido."

        if error is None:
            try:
                Curso.create(codigo, nombre)
                flash("Curso creado exitosamente!")
                return redirect(url_for("cursos.index"))
            except Exception as e:
                error = f"Error al crear el curso: {e}"

        flash(error)

    return render_template("cursos/create.html")


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    curso = Curso.get_by_id(id)

    if request.method == "POST":
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]

        error = None

        if not codigo:
            error = "El código es requerido."
        elif not nombre:
            error = "El nombre es requerido."

        if error is None:
            try:
                Curso.update(id, codigo, nombre)
                flash("Curso actualizado exitosamente!")
                return redirect(url_for("cursos.index"))
            except Exception as e:
                error = f"Error al actualizar el curso: {e}"

        flash(error)

    return render_template("cursos/edit.html", curso=curso)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    try:
        Curso.delete(id)
        flash("Curso eliminado exitosamente!")
    except Exception as e:
        flash(f"Error al eliminar el curso: {e}")

    return redirect(url_for("cursos.index"))


@bp.route("/<int:id>/view")
def view(id):
    curso = Curso.get_by_id(id)
    prerequisitos = Curso.get_prerequisites(id)
    cursos_disponibles = [c for c in Curso.get_all() if c["id"] != id]

    return render_template(
        "cursos/view.html",
        curso=curso,
        prerequisitos=prerequisitos,
        cursos_disponibles=cursos_disponibles,
    )


@bp.route("/<int:id>/add_prerequisite", methods=("POST",))
def add_prerequisite(id):
    prerequisito_id = request.form["prerequisito_id"]

    try:
        Curso.add_prerequisite(id, prerequisito_id)
        flash("Prerequisito añadido exitosamente!")
    except Exception as e:
        flash(f"Error al añadir el prerequisito: {e}")

    return redirect(url_for("cursos.view", id=id))


@bp.route("/<int:id>/remove_prerequisite/<int:prerequisito_id>", methods=("POST",))
def remove_prerequisite(id, prerequisito_id):
    try:
        Curso.remove_prerequisite(id, prerequisito_id)
        flash("Prerequisito eliminado exitosamente!")
    except Exception as e:
        flash(f"Error al eliminar el prerequisito: {e}")

    return redirect(url_for("cursos.view", id=id))

@bp.route("/<int:id>/close", methods=("POST",))
def close(id):
    try:
        Curso.close(id)
        flash("Curso cerrado exitosamente. No se podrán realizar cambios.")
    except Exception as e:
        flash(f"Error al cerrar el curso: {e}")

    return redirect(url_for("cursos.view", id=id))

@bp.route("/<int:id>/reopen", methods=("POST",))
def reopen(id):
    try:
        Curso.reopen(id)
        flash("Curso reabierto exitosamente. Se podrán realizar cambios.")
    except Exception as e:
        flash(f"Error al reabrir el curso: {e}")

    return redirect(url_for("cursos.view", id=id))
