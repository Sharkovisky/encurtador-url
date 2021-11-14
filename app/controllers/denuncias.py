from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link, LinksProibidos
import string, random, requests

@app.route('/denuncias', methods=["GET"])
def denuncia():
    return render_template("denuncias.html")