"""Defines all the functions related to the database"""
from app import db
from sqlalchemy import text

def update_popularity_entry(song_id, num):
    """Updates song popularity based on given `task_id`

    Args:
        song_id (str): Targeted song_id
        num (int): Updated popularity

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set popularity = "{}" where id = {};'.format(num, song_id)
    conn.execute(query)
    conn.close()


def insert_new_song(song_id,song_name,artist,duration,popularity):
    """Insert new song to table.

    Args:
        song_name,artist,duration,popularity: get from form

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query_sql = 'Insert Into Song (song_id,song_name,artist_name,duration,popularity) VALUES (%(_id)s,%(_name)s,"{}","{}",{});'.format(
        song_id,song_name,artist,duration,popularity)
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_song_by_id(song_id):
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From Song where song_name={};'.format(song_id)
    conn.execute(query)
    conn.close()

def find_song(key):
    ''' Find song_name containing the keyword in database '''
    conn = db.connect()
    # Source: https://stackoverflow.com/questions/3325467/sqlalchemy-equivalent-to-sql-like-statement
    query_sql = """SELECT * FROM Song WHERE song_name LIKE '%' :bar_tags '%'"""
    # db is sqlalchemy session object
    query_results = conn.execute(text(query_sql), {"bar_tags": key}).fetchall()
    #  = conn.execute("SELECT * from Song WHERE song_name LIKE %{}% ;").format(key).fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Song' ORDER BY ORDINAL_POSITION").fetchall()
    res = []
    count = 0
    res_col = [column_name[0][0], column_name[2][0], column_name[4][0], column_name[5][0]]
    for result in query_results:
        count += 1
        if count > 15:
            break
        item = [ result[0], result[2],result[4],result[5] ]
        res.append(item)
    conn.close()
    return res, res_col