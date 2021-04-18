"""Defines all the functions related to the database"""
from app import db
from sqlalchemy import text

def fetch_single_cover(song_id):
    '''
    fetch single cover by song_id
    '''
    conn = db.connect()
    query = """Select song_id, song_name, Cover_link From Cover where song_id LIKE :id;"""
    # print(query)
    cover_info = conn.execute(text(query),{"id":song_id}).fetchall()
    conn.close()
    return cover_info


def update_cover_entry(song_id, song_name, Cover_link):
    """Updates cover info based on given `task_id`

    Args:
        song_id (str): Targeted song_id
        song_name (str) : Updated song name
        Cover_link (str): Updated cover link

    Returns:
        None
        @todo
    """

    conn = db.connect()
    query = """Update Cover set Cover_link = :link , song_name = :name where song_id LIKE :id;"""
    print(query)
    conn.execute(text(query), {"link": Cover_link, "name": song_name, "id":song_id})
    conn.close()


def insert_new_cover(song_id, song_name, Cover_link):
    """Insert new cover to table.

    Args:
        song_id, song_name, Cover_link

    Returns: The task ID for the inserted entry
    @STATUS: FINISHED
    """

    conn = db.connect()
    query_sql = """Insert Into Cover (song_id,song_name,Cover_link) VALUES ( :song_id , :song_name , :Cover_link  );"""
    # db is sqlalchemy session object
    query_results = conn.execute(text(query_sql), {"song_id": song_id, "song_name":song_name, "Cover_link":Cover_link})
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_cover_by_id(song_id):
    """ remove entries based on task ID """
    conn = db.connect()
    query = """Delete From Cover where song_id LIKE :bar_tags;"""
    conn.execute(text(query),{"bar_tags":song_id})
    conn.close()

def find_cover(key):
    ''' Find song_name containing the keyword in database 
    @STATUS: FINISHED
    '''
    conn = db.connect()
    # Source: https://stackoverflow.com/questions/3325467/sqlalchemy-equivalent-to-sql-like-statement
    query_sql = """SELECT * FROM Cover WHERE song_name LIKE '%' :bar_tags '%'"""
    # db is sqlalchemy session object
    query_results = conn.execute(text(query_sql), {"bar_tags": key}).fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Cover' ORDER BY ORDINAL_POSITION").fetchall()
    res = []
    count = 0
    res_col = [column_name[0][0],column_name[1][0], column_name[2][0]]
    for result in query_results:
        count += 1
        if count > 15:
            break
        item = [ result[0],result[1], result[2] ]
        res.append(item)
    conn.close()
    return res, res_col

