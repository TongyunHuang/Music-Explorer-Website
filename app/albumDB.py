"""Defines all the functions related to the database"""
from app import db
from sqlalchemy import text

def fetch_single_album(album_id):
    '''
    fetch single album by album_id
    '''
    conn = db.connect()
    query = """Select album_id, album_name, album_type, album_release_date From Album where album_id LIKE :id;"""
    # print(query)
    album_info = conn.execute(text(query),{"id":album_id}).fetchall()
    conn.close()
    return album_info


def update_album_entry(album_id, album_name, album_type):
    """Updates album popularity based on given `task_id`

    Args:
        album_id (str): Targeted album_id
        album_name (str) : Updated album name
        album_type (str): Updated album type 

    Returns:
        None
        @todo
    """

    conn = db.connect()
    query = """Update Album set album_name = :album , album_type = :type where album_id LIKE :id;"""
    print(query)
    conn.execute(text(query), {"album": album_name, "type": album_type, "id":album_id})
    conn.close()


def insert_new_album(album_id, album_name, album_type, album_release_date):
    """Insert new album to table.

    Args:
        album_id, album_name, album_type, album_release_date

    Returns: The task ID for the inserted entry
    @STATUS: FINISHED
    """

    conn = db.connect()
    query_sql = """Insert Into Album (album_id,album_name,album_type, album_release_date) VALUES ( :album_id , :album_name , :album_type , :album_release_date  );"""
    # db is sqlalchemy session object
    query_results = conn.execute(text(query_sql), {"album_id": album_id, "album_name":album_name, "album_type":album_type, "album_release_date":album_release_date})
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_album_by_id(album_id):
    """ remove entries based on task ID """
    conn = db.connect()
    query = """Delete From Album where album_id LIKE :bar_tags;"""
    conn.execute(text(query),{"bar_tags":album_id})
    conn.close()

def find_album(key):
    ''' Find album_name containing the keyword in database 
    @STATUS: FINISHED
    '''
    conn = db.connect()
    # Source: https://stackoverflow.com/questions/3325467/sqlalchemy-equivalent-to-sql-like-statement
    query_sql = """SELECT * FROM Album WHERE album_name LIKE '%' :bar_tags '%'"""
    # db is sqlalchemy session object
    query_results = conn.execute(text(query_sql), {"bar_tags": key}).fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Album' ORDER BY ORDINAL_POSITION").fetchall()
    res = []
    count = 0
    res_col = [column_name[1][0],column_name[0][0], column_name[2][0], column_name[4][0]]
    for result in query_results:
        count += 1
        if count > 15:
            break
        item = [ result[1],result[0], result[2],result[4] ]
        res.append(item)
    conn.close()
    return res, res_col

def shirley_fetch(popularity):
    '''
    Return table of albums with popularities greater than an indicated value
    '''

    conn = db.connect()
    query_sql = """ SELECT A.album_name, AVG(S.popularity) AS avg_popularity, A.album_id, A.album_type, A.album_release_date
    FROM Album A JOIN Song S ON A.album_name = S.album_name
    GROUP BY A.album_name, A.album_id
    HAVING avg_popularity >= %s
    ORDER BY avg_popularity DESC, A.album_name
    """ %(popularity)
    query_results = conn.execute(text(query_sql), {"popularity": popularity}).fetchall()
    res_col = ['album_name', 'avg_popularity', 'album_id', 'album_type', 'album_release_date']
    conn.close()
    return query_results, res_col