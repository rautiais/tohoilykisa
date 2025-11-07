from flask import session
from sqlalchemy.sql import text
from db import db


def check_event_cat(event_cat_name):
    event_cat_name_lower = event_cat_name.lower()
    sql = text("""SELECT id FROM event_cat
               WHERE (LOWER(event_cat_name)=:event_cat_name)""")
    result = db.session.execute(sql, {"event_cat_name": event_cat_name_lower})
    event_cat_id = result.fetchone()
    return event_cat_id[0] if event_cat_id else False

    
def new_event_cat(event_cat_name):
    event_cat_name_lower = event_cat_name.lower()
    try:
        sql = text("""INSERT INTO event_cat (event_cat_name)
                   VALUES (:event_cat_name)""")
        db.session.execute(sql, {"event_cat_name": event_cat_name_lower})
        db.session.commit()
        return True
    except:
        return False


def get_category_name(cat_id):
    sql = text("""SELECT event_cat_name
               FROM event_cat WHERE id=:cat_id""")
    result = db.session.execute(sql, {"cat_id": cat_id})
    name = result.fetchone()
    return name[0] if name else None


def all_event_cats():
    sql = text("""SELECT id, event_cat_name
               FROM event_cat ORDER BY event_cat_name""")
    result = db.session.execute(sql)
    return result.fetchall()


def list_events_in_cat(cat_id):
    sql = text("""SELECT e.id, e.event_name, e.points, c.event_cat_name
               FROM events e JOIN event_cat c ON e.event_cat_id = c.id
               WHERE c.id=:cat_id""")
    result = db.session.execute(sql, {"cat_id": cat_id})
    return result.fetchall()


def check_event(event_name):
    event_name_lower = event_name.lower()
    sql = text("""SELECT id FROM events
               WHERE (LOWER(event_name)=:event_name)""")
    result = db.session.execute(sql, {"event_name": event_name_lower})
    event_id = result.fetchone()
    return event_id[0] if event_id else False

    
def new_event(event_name, event_points, cat_id):
    event_name_lower = event_name.lower()
    try:
        sql = text("""INSERT INTO events (event_name, points, event_cat_id)
                   VALUES (:event_name, :points, :cat_id)""")
        db.session.execute(sql, {
            "event_name": event_name_lower,
            "points": event_points,
            "cat_id": cat_id})
        db.session.commit()
        return True
    except:
        return False


def get_events_by_cateogry(cat_id):
    sql = text("""SELECT id, event_name
               FROM events WHERE event_cat_id=:cat_id
               ORDER BY event_name""")
    result = db.session.execute(sql, {"cat_id": cat_id})
    events = [{"id": event.id, "event_name": event.event_name}
              for event in result]
    return events
