from db import db
from sqlalchemy.sql import text
from flask import session

def check_group(group_name):
    sql = text("SELECT id FROM groups WHERE group_name=:group_name")
    result = db.session.execute(sql, {"group_name":group_name})
    group_id = result.fetchone()
    return group_id[0] if group_id else False

def new_group(group_name):
    try:
        sql = text("""INSERT INTO groups (user_id, group_name) 
                   VALUES (:user_id, :group_name) RETURNING id""")
        result = db.session.execute(sql, {"user_id": session["id"], "group_name": group_name})
        group_id = result.fetchone()[0]
        sql = text("INSERT INTO user_info (user_id, group_id) VALUES (:user_id, :group_id)")
        db.session.execute(sql, {"user_id": session["id"], "group_id": group_id})
        db.session.commit()
        return True
    except:
        return False

def join_group(group_id):
    try:
        sql = text("INSERT INTO user_info (group_id, user_id) VALUES (:group_id, :user_id)")
        db.session.execute(sql, {"group_id": group_id, "user_id": session["id"]})
        db.session.commit()
        return True
    except:
        return False
    
def all_groups():
    sql = text("""SELECT u.group_id, g.group_name 
               FROM user_info u INNER JOIN groups g
               ON u.group_id = g.id 
               WHERE u.user_id=:user_id""")
    result = db.session.execute(sql, {"user_id":session["id"]})
    return result.fetchall()

def list_users(group_id):
    sql = text("""SELECT u.id, u.username, g.group_name
               FROM groups g INNER JOIN user_info u
               ON g.user_id = u.user_id
               WHERE u.group_id=:group_id""")
    result = db.session.execute(sql, {"group_id": group_id})
    return result.fetchall()
