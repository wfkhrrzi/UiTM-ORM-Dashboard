# from app import db
import os
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy import Table, create_engine, select

from env.config import DB_NAME

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

User_tbl = Table('user', User.metadata)

from app import server

engine = create_engine(f"sqlite:///{os.path.join(server.instance_path, DB_NAME)}.db")

def add_user(username, password, email):
    hashed_password = generate_password_hash(password, method='sha256')

    ins = User_tbl.insert().values(
        username=username, email=email, password=hashed_password)

    conn = engine.connect()
    conn.execute(ins)
    conn.close()


def del_user(username):
    delete = User_tbl.delete().where(User_tbl.c.username == username)

    conn = engine.connect()
    conn.execute(delete)
    conn.close()


def show_users():
    select_st = select([User_tbl.c.username, User_tbl.c.email])

    conn = engine.connect()
    rs = conn.execute(select_st)

    for row in rs:
        print(row)

    conn.close()