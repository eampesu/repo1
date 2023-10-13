from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from sqlalchemy.sql import text

def login(username, password):
    print("Päästiin users.loginiin!")
    sql=db.text("SELECT id, password FROM users WHERE username=:username")
    result=db.session.execute(sql, {"username" :username})
    user=result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"]=user.id
            session["username"]=username
            return True
        else:
            return False

def register(username, password, answer):
    hash_value = generate_password_hash(password)
    if answer=="Kyllä":

        try:
            sql=text('INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)')
            db.session.execute(sql, {"username":username, "password":hash_value, "admin":True})
            db.session.commit()
        except:
            return False
    elif answer=="Ei":
        try:
            sql=text('INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)')
            db.session.execute(sql, {"username":username, "password":hash_value, "admin":False})
            db.session.commit()
        except:
            return False
    else:
        return False

    return login(username, password)

def user_id():
    return session.get("user_id",0)

def logout():
    del session["user_id"]
    return

def is_admin(user_id):
    sql=text('SELECT admin FROM users WHERE id=:id')
    result=db.session.execute(sql, {"id":user_id})
    return result.fetchone()[0]

def get_users():
    sql=text('SELECT id, username FROM users')
    result=db.session.execute(sql)
    return result.fetchall()

def get_username(user_id):
    sql=text('SELECT username FROM users WHERE id=:id')
    result=db.session.execute(sql, {"id":user_id})
    return result.fetchone()[0]

def is_user(username):
    sql=text('SELECT username from users WHERE username=:username')
    result=db.session.execute(sql, {"username":username})
    print("haettu username ja saatu:", result.fetchone())
    return result.fetchone()
