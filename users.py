import secrets
from sqlalchemy.sql import text
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def login(username, password):
    sql = text("""SELECT id, password FROM users
               WHERE username=:username""")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False


def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("csrf_token", None)


def register(username, password):
    hash_value = generate_password_hash(password)
    username_lower = username.lower()
    try:
        sql = text("""INSERT INTO users (username, password)
                   VALUES (:username, :password)""")
        db.session.execute(
            sql, {"username": username_lower, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username_lower, password)


def user_id():
    return session.get("user_id", 0)


def check_token(csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)


def check_username(username):
    sql = text("""SELECT username FROM users
               WHERE username=:username""")
    result = db.session.execute(sql, {"username": username})
    if result.fetchone():
        return False
    return True


def is_logged_in():
    return "user_id" in session
