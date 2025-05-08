from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.sala import Sala
from querys.sala_queries import get_classroom_schedule
from db import execute_query

bp = Blueprint("salas", __name__, url_prefix="/salas")


@bp.route("/")
def index():
    salas = Sala.get_all()
    return render_template("salas/index.html", salas=salas)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        nombre = request.form["nombre"]
        capacidad = request.form["capacidad"]

        error = None

        if not nombre:
            error = "El nombre es requerido."
        elif not capacidad:
            error = "La capacidad es requerida."
        else:
            try:
                capacidad = int(capacidad)
                if capacidad <= 0:
                    error = "La capacidad debe ser un número entero positivo."
            except ValueError:
                error = "La capacidad debe ser un número entero."

        if error is None:
            try:
                Sala.create(nombre, capacidad)
                flash("Sala creada exitosamente!")
                return redirect(url_for("salas.index"))
            except Exception as e:
                error = f"Error al crear la sala: {e}"

        flash(error)

    return render_template("salas/create.html")


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    sala = Sala.get_by_id(id)

    if request.method == "POST":
        nombre = request.form["nombre"]
        capacidad = request.form["capacidad"]

        error = None

        if not nombre:
            error = "El nombre es requerido."
        elif not capacidad:
            error = "La capacidad es requerida."
        else:
            try:
                capacidad = int(capacidad)
                if capacidad <= 0:
                    error = "La capacidad debe ser un número entero positivo."
            except ValueError:
                error = "La capacidad debe ser un número entero."

        if error is None:
            try:
                Sala.update(id, nombre, capacidad)
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
        horarios = execute_query(get_classroom_schedule, (id,), fetch=True)
    except Exception:
        pass

    return render_template("salas/view.html", sala=sala, horarios=horarios)
