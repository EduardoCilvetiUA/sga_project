from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.sala import Sala
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
    
    # Obtener los horarios asignados a esta sala
    horarios = []
    try:
        horarios = execute_query(
            """
            SELECT h.*, sec.numero as seccion_numero, c.codigo as curso_codigo, c.nombre as curso_nombre
            FROM horarios h
            JOIN secciones sec ON h.seccion_id = sec.id
            JOIN instancias_curso ic ON sec.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            WHERE h.sala_id = %s
            ORDER BY h.dia, h.hora_inicio
            """,
            (id,),
            fetch=True
        )
    except Exception:
        pass

    return render_template("salas/view.html", sala=sala, horarios=horarios)