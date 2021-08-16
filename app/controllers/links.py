from app import app, db
from flask import render_template
from app.models.tables import Usuario, Link

@app.route('/', methods=["GET", "POST"])
def inicio():
    return render_template("base.html")