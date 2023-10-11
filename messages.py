from db import db
from sqlalchemy import text

def add(content, chain_id, user_id):
    sql=text('INSERT INTO messages (content, chain_id, user_id, created_at) VALUES (:content, :chain_id, :user_id, NOW())')
    db.session.execute(sql, {"content":content, "chain_id":chain_id, "user_id": user_id})
    db.session.commit()
    return

def edit(message_id, new_content):
    print("TULOSTUS:", message_id, new_content)
    sql=text('UPDATE messages SET content=:content WHERE id=:id')
    db.session.execute(sql, {"content":new_content, "id":message_id})
    db.session.commit()
    return

def remove(message_id):
    sql=text('DELETE FROM messages WHERE id=:id')
    db.session.execute(sql, {"id":message_id})
    db.session.commit()
    return

def remove_chain(chain_id):
    sql=text('DELETE FROM messages WHERE chain_id=:id')
    db.session.execute(sql, {"id":chain_id})
    db.session.commit()
    return

def find_normal(query):
    sql=text('SELECT M.chain_id, M.content FROM areas A LEFT JOIN chains C ON A.id=C.area_id LEFT JOIN messages M ON C.id=M.chain_id WHERE M.content LIKE :query AND secret=False')
    result=db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def find_secret(query):
    sql=text('SELECT C.id, M.content, S.user_id AS user_id FROM areas A LEFT JOIN chains C ON A.id=C.area_id LEFT JOIN messages M ON C.id=M.chain_id LEFT JOIN secret_users S ON A.id=S.area_id WHERE M.content LIKE :query AND A.secret=True')
    result=db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()
