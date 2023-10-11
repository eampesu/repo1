from sqlalchemy.sql import text
from db import db


def add(area_id, lista):
    for user in lista:
        sql=text('INSERT INTO secret_users (area_id, user_id) VALUES (:area_id, :user)')
        db.session.execute(sql, {"area_id":area_id, "user":user})
        db.session.commit()
    return


