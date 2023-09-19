import db from db

def get_list(area_id):
    sql=text("SELECT U.username, C.topic, C.created_at, C.id FROM users U LEFT JOIN chains C ON U.id=C.user_id WHERE C.area_id=area_id ORDER BY C.created_at DESC")
    result=db.session.execute(sql)
    return result.fetchall()

def get_topic(chain_id):
    sql=text("SELECT topic FROM chains WHERE id=chain_id")
    result=db.session.execute(sql)
    return result.fetchone()

def get_messages(chain_id):
    sql=text("SELECT U.username, M.content, M.created_at FROM users U LEFT JOIN messages M ON U.id=M.user_id WHERE M.chain_id=chain_id ORDER BY M.created_at")
    result=db.session.execute(sql)
    return result.fetchall()

def add(user_id, topic, area_id):
    sql=text("INSRET INTO chains VALUES (area_id, user_id, topic, NOW()")
    db.session.execute(sql)
    db.session.commit()

