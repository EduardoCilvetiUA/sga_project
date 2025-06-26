from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.sala import Sala
from querys.sala_queries import get_horario_sala
from db import execute_query

bp = Blueprint("salas", __name__, url_prefix="/salas")


@bp.route("/")
def index():
    salas = Sala.get_all()
    return render_template("salas/index.html", salas=salas)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        return _handle_create_post()
    return render_template("salas/create.html")


def _handle_create_post():
    nombre = request.form["nombre"]
    capacidad = request.form["capacidad"]
    error = _validate_sala_data(nombre, capacidad)
    
    if error is None:
        try:
            Sala.create(nombre, int(capacidad))
            flash("Sala creada exitosamente!")
            return redirect(url_for("salas.index"))
        except Exception as e:
            error = f"Error al crear la sala: {e}"
    
    flash(error)
    return render_template("salas/create.html")


def _validate_sala_data(nombre, capacidad):
    if not nombre:
        return "El nombre es requerido."
    if not capacidad:
        return "La capacidad es requerida."
    try:
        capacidad_int = int(capacidad)
        if capacidad_int <= 0:
            return "La capacidad debe ser un número entero positivo."
    except ValueError:
        return "La capacidad debe ser un número entero."
    return None


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    sala = Sala.get_by_id(id)
    
    if request.method == "POST":
        return _handle_edit_post(id, sala)
    return render_template("salas/edit.html", sala=sala)


def _handle_edit_post(id, sala):
    nombre = request.form["nombre"]
    capacidad = request.form["capacidad"]
    error = _validate_sala_data(nombre, capacidad)
    
    if error is None:
        try:
            Sala.update(id, nombre, int(capacidad))
            flash("Sala actualizada exitosamente!")
            return redirect(url_for("salas.index"))
        except Exception as e:
            error = f"Error al actualizar la sala: {e}"
    
    flash(error)
    return render_template("salas/edit.html", sala=sala)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    try:
        Sala.delete(id)
        flash("Sala eliminada exitosamente!")
    except Exception as e:
        flash(f"Error al eliminar la sala: {e}")

    return redirect(url_for("salas.index"))


@bp.route("/<int:id>/view")
def view(id):
    sala = Sala.get_by_id(id)

    horarios = []
    try:
        horarios = execute_query(get_horario_sala, (id,), fetch=True)
    except Exception:
        pass

    return render_template("salas/view.html", sala=sala, horarios=horarios)
