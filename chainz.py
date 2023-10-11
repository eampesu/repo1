from db import db
from sqlalchemy import text

def get_list(areaid):
    sql=text('SELECT U.username, C.topic, C.content, C.created_at, C.id FROM users U LEFT JOIN chains C ON U.id=C.user_id WHERE C.area_id=:areaid ORDER BY C.created_at DESC')
    result=db.session.execute(sql, {"areaid":areaid})
    return result.fetchall()

def get_chain(chain_id):
    sql=text('SELECT U.username, C.id, C.topic, C.content, C.created_at FROM users U LEFT JOIN chains C ON U.id=C.user_id WHERE C.id=:chain_id')
    result=db.session.execute(sql, {"chain_id":chain_id})
    return result.fetchone()

def get_topic(chain_id):
    sql=text('SELECT topic FROM chains WHERE id=:chain_id')
    result=db.session.execute(sql, {"chain_id":chain_id})
    return result.fetchone()

def get_messages(chain_id):
    sql=text('SELECT U.username, M.content, M.created_at, M.id AS M_id FROM users U LEFT JOIN messages M ON U.id=M.user_id WHERE M.chain_id=:chain_id ORDER BY M.created_at')
    result=db.session.execute(sql, {"chain_id":chain_id})
    return result.fetchall()

def add(user_id, topic, content, area_id):
    sql=text('INSERT INTO chains (user_id, area_id,topic, content, created_at) VALUES (:user_id, :area_id, :topic, :content, NOW())')
    db.session.execute(sql, {"user_id":user_id, "topic":topic, "content":content, "area_id":area_id})
    db.session.commit()
    return

def get_username(chain_id):
    sql=text('SELECT U.username FROM users U LEFT JOIN chains C on U.id=C.user_id WHERE C.id=:chain_id')
    result=db.session.execute(sql, {"chain_id":chain_id})
    return result.fetchone()[0]

def change_topic(chain_id, new_topic):
    sql=text('UPDATE chains SET topic=:new_topic WHERE id=:chain_id')
    db.session.execute(sql, {"new_topic": new_topic, "chain_id":chain_id})
    db.session.commit()
    return

def edit_message(chain_id, new_content):
    sql=text('UPDATE chains SET content=:new_content WHERE id=:chain_id')
    db.session.execute(sql, {"chain_id":chain_id, "new_content":new_content})
    db.session.commit()
    return

def remove(chain_id):
    sql=text('DELETE FROM chains WHERE id=:chain_id')
    db.session.execute(sql, {"chain_id":chain_id})
    db.session.commit()
    return

def get_area(chain_id):
    sql=text('SELECT DISTINCT area_id FROM chains WHERE id=:chain_id')
    result=db.session.execute(sql, {"chain_id":chain_id})
    return result.fetchone()[0]

def find_normal(query):
    sql = text('SELECT C.id, C.content FROM areas A LEFT JOIN chains C ON A.id=C.area_id WHERE content LIKE :query AND A.secret=False')
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def find_secret(query):
    sql = text('SELECT C.id, C.content, S.user_id AS user_id FROM areas A LEFT JOIN chains C ON A.id=C.area_id LEFT JOIN secret_users S ON A.id=S.area_id WHERE content LIKE :query AND A.secret=True')
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()
