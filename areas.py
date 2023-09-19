from db import db
from sqlalchemy.sql import text
def get_list():
    sql=text("SELECT A.id, A.topic, COUNT(DISTINCT C.id), COUNT(An.id), min(An.created_at) FROM areas A LEFT JOIN chains C ON A.id= A.area_id LEFT JOIN answers An ON An.chains_id=chains.id GROUP BY A.id")
    result=db.session.execute(sql)
    return result.fetchall()
