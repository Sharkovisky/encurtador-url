from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import os, logging

logging.basicConfig(
    filename="access.log", format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nelson:SuportE99@localhost/encurtador'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.models.tables import Usuario
from app.models.tables import Link

from app.controllers import links
from app.controllers import descricao
from app.controllers import denuncias