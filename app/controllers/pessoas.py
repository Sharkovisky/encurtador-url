from app import app, db, login_manager
from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
from flask_login import login_user, logout_user
from sqlalchemy import func
from datetime import date, datetime
from app.models.tables import Usuario
from validate_docbr import CPF
import sys, uuid
from datetime import datetime
import bcrypt

@login_manager.user_loader
def get_usuario(usuario_id):
    return Usuario.query.filter_by(id=usuario_id).first()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        mensagem = request.args.get("mensagem")
        return render_template("login.html", mensagem=mensagem)

    if request.method == "POST":
        email = request.form["inputEmail"]
        senha = request.form["inputPassword"]

        usuario = Usuario.query.filter_by(email=email).first()
        auth = False
        
        if usuario:
            auth = bcrypt.checkpw(senha.encode("utf-8"), usuario.senha.encode("utf-8"))
            session['logged_in'] = True
            session['user_id'] = usuario.id
            login_user(usuario)
            if not usuario or not auth:
                mensagem = "E-mail ou senha inválidos"
                return render_template("login.html", mensagem=mensagem)
        else:
            #login_user(usuario)
            #usuario = usuario.id
            mensagem = "E-mail ou senha inválidos"
            return render_template("login.html", mensagem=mensagem)
            
    return redirect("/")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        mensagem = request.args.get("mensagem")
        return render_template("cadastro.html")

    if request.method == "POST":
        nome = request.form["inputName"]
        if len(nome) <= 3:
            mensagem = "Seu nome completo deve conter ao menos 3 caracteres"
            return render_template("cadastro.html", mensagem=mensagem)

        cpf = CPF()
        if cpf.validate(request.form["inputCPF"]):
            existe_cpf = Usuario.query.filter_by(cpf=request.form["inputCPF"]).first()
            if existe_cpf:
                mensagem = "CPF já cadastrado."
                return render_template("cadastro.html", mensagem=mensagem)
            else:
                cpf = request.form["inputCPF"]

        else:
            mensagem = "Insira um CPF válido"
            return render_template("cadastro.html", mensagem=mensagem)

        email = request.form["inputEmail"]
        existe_email = Usuario.query.filter_by(email=email).first()
        if existe_email:
            mensagem = "Email já cadastrado"
            return render_template("cadastro.html", mensagem=mensagem)

        if len(request.form["inputPassword"]) >= 8:
            if request.form["inputPassword"] == request.form["inputPasswordConfirm"]:
                senha = request.form["inputPassword"]
            else:
                mensagem = "As senhas não correspondem"
                return render_template("cadastro.html", mensagem=mensagem)

        else:
            mensagem = "Sua senha deve conter ao menos 8 caracteres"
            return render_template("cadastro.html", mensagem=mensagem)

        senhaEncriptada = bcrypt.hashpw(senha.encode("UTF-8"), bcrypt.gensalt())
        data_cadastro = datetime.now()

        usuario = Usuario(
            nome=nome,
            cpf=cpf,
            email=email,
            senha=senhaEncriptada,
            data_cadastro=data_cadastro,
        )
        db.session.add(usuario)
        db.session.commit()

    return redirect("/login")

@app.route("/logout")
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect("/")