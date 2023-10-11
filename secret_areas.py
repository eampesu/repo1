from db import db
from sqlalchemy import text

def add(slist, topic):
    for user in slist:
        sql=text('INSERT INTO secret_areas (topic, username) VALUES (:topic, :username)')
        db.session.execute(sql, {"topic":topic, "username":user})
        db.session.commit()
    return 
def get_list():
    sql=text('SELECT topic, username FROM secret_areas')
    result=db.session.execute(sql)
    return result.fetchall()
