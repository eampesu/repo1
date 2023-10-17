from db import db
from sqlalchemy.sql import text
import messages
import chainz

def get_list():
    sql=db.text('SELECT A.id, A.topic, COUNT(DISTINCT C.id) AS count_chains, COUNT(M.id) AS count_msgs, max(M.created_at) AS max FROM areas A LEFT JOIN chains C ON A.id= C.area_id LEFT JOIN messages M ON M.chain_id=C.id WHERE secret=False GROUP BY A.id')
    result=db.session.execute(sql)
    return result.fetchall()

def get_secret_list():
    sql=text('SELECT A.id, A.topic, S.user_id FROM areas A LEFT JOIN secret_users S ON A.id=S.area_id WHERE secret=True')
    result=db.session.execute(sql)
    return result.fetchall()

def get_secret_topics():
    sql=text('SELECT id, topic FROM areas WHERE secret=True')
    result=db.session.execute(sql)
    return result.fetchall()

def delete(area_id):
    sql=text('SELECT id FROM CHAINS WHERE area_id=:area_id')
    result=db.session.execute(sql, {"area_id":area_id})
    id_list=result.fetchall()
    print(id_list)
    for i in id_list:
        messages.remove_chain(i.id)
        chainz.remove(i.id)
    sql=text('DELETE FROM areas WHERE id=:id')
    db.session.execute(sql, {"id":area_id})
    db.session.commit()
    return

def add(new_topic, truth_value):
    sql=text('INSERT INTO areas (topic, secret) VALUES (:topic, :truth_value)')
    db.session.execute(sql, {"topic":new_topic, "truth_value":truth_value})
    db.session.commit()
    return

def get_area_id(topic):
    sql=text('SELECT id FROM areas WHERE topic=:topic')
    result=db.session.execute(sql, {"topic":topic})
    return result.fetchone()[0]

def is_secret(area_id):
    sql=text('SELECT secret FROM areas WHERE id=:area_id')
    result=db.session.execute(sql, {"area_id":area_id})
    return result.fetchone()[0]
