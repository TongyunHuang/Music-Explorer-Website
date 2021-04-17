"""Defines all the functions related to the database"""
from app import db
from sqlalchemy import text

def fetch_single_artist(artist_id):
    '''
    fetch single artist by artist_id
    '''
    conn = db.connect()
    query = """Select artist_id, artist_name, num_followers, artist_url From Artist where artist_id LIKE :id;"""
    artist_info = conn.execute(text(query),{"id":artist_id}).fetchall()
    conn.close()
    return artist_info


def update_artist_entry(artist_id, artist_name, num_followers, artist_url):
    """Updates artist popularity based on given `task_id`

    Args:
        artist_id (str): Targeted artist_id
        num (int): Updated popularity

    Returns:
        None
        @todo
    """
    conn = db.connect()
    query = """Update Artist set artist_name = :artist, num_followers = :followers, artist_url = :url where artist_id LIKE :id;"""
    print(query)
    conn.execute(text(query), {"artist": artist_name, "followers": num_followers, "url":artist_url, "id":artist_id})
    print(query)
    conn.close()


def insert_new_artist(artist_id,artist_name, num_followers, artist_url):
    """Insert new artist to table.

    Args:
        artist_name,artist,duration,popularity: get from form

    Returns: The task ID for the inserted entry
    @STATUS: FINISHED
    """

    conn = db.connect()
    query_sql = """Insert Into Artist (artist_id, artist_name, num_followers, artist_url) VALUES ( :artist_id , :artist_name , :num_followers , :artist_url);"""
    query_results = conn.execute(text(query_sql), {"artist_id": artist_id, "artist_name":artist_name, "num_followers": num_followers,"artist_url":artist_url})
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()
    return task_id


def remove_artist_by_id(artist_id):
    """ remove entries based on task ID """
    conn = db.connect()
    query = """Delete From Artist where artist_id LIKE :bar_tags;"""
    conn.execute(text(query),{"bar_tags":artist_id})
    conn.close()

def find_artist(key):
    ''' Find artist_name containing the keyword in database 
    @STATUS: FINISHED
    '''
    conn = db.connect()
    # Source: https://stackoverflow.com/questions/3325467/sqlalchemy-equivalent-to-sql-like-statement
    query_sql = """SELECT * FROM Artist WHERE artist_name LIKE '%' :bar_tags '%'"""
    query_results = conn.execute(text(query_sql), {"bar_tags": key}).fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Artist' ORDER BY ORDINAL_POSITION").fetchall()
    res = []
    count = 0
    res_col = [column_name[1][0], column_name[0][0], column_name[3][0], column_name[4][0]]
    for result in query_results:
        count += 1
        if count > 15:
            break
        item = [
                result[1],
                result[0],
                result[3],
                result[4]
        ]
        res.append(item)
    conn.close()
    return res, res_col

'''
SELECT s.artist_name, AVG(s.popularity) AS avg_pop, a.num_followers 
FROM Artist a NATURAL JOIN Song s 
GROUP BY a.artist_id, a.num_followers 
ORDER BY a.num_followers DESC;
'''

def adv_sql(num_followers):
    sql_query = "SELECT s.artist_name, AVG(s.popularity) AS avg_pop, a.num_followers FROM Artist a NATURAL JOIN Song s WHERE a.num_followers > :num_followers GROUP BY a.artist_id, a.num_followers ORDER BY a.num_followers DESC;"
    conn = db.connect()
    print(text(sql_query))
    query_results = conn.execute(text(sql_query), {"num_followers": num_followers}).fetchall()
    conn.close()
    res_col = ['Artist name', 'Average popularity', 'Number of followers']
    return query_results, res_col