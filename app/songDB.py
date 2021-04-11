"""Defines all the functions related to the database"""
from app import db
from sqlalchemy import text

def fetch_single_song(song_id):
    '''
    fetch single song by song_id
    '''
    conn = db.connect()
    query = """Select song_id, song_name, artist_name From Song where song_id LIKE :id;"""
    # print(query)
    song_info = conn.execute(text(query),{"id":song_id}).fetchall()
    conn.close()
    return song_info


def update_entry(song_id, song_name, artist_name):
    """Updates song popularity based on given `task_id`

    Args:
        song_id (str): Targeted song_id
        num (int): Updated popularity

    Returns:
        None
        @todo
    """

    conn = db.connect()
    query = """Update Song set song_name = :song , artist_name = :artist where song_id LIKE :id;"""
    print(query)
    conn.execute(text(query), {"song": song_name, "artist": artist_name, "id":song_id})
    conn.close()


def insert_new_song(song_id,song_name,artist,duration,popularity):
    """Insert new song to table.

    Args:
        song_name,artist,duration,popularity: get from form

    Returns: The task ID for the inserted entry
    @STATUS: FINISHED
    """

    conn = db.connect()
    # query_sql = 'Insert Into Song (song_id,song_name,artist_name,duration,popularity) VALUES (" '
    # +song_id+' ","'+song_name+' ","'+artist_name+' ","'+duration+' ",'+str(popularity)+');'
    # query_sql = """Insert Into Song (song_id,song_name,artist_name,duration,popularity) VALUES (" :song_id' ","'+song_name+' ","'+artist_name+' ","'+duration+' ",'+str(popularity)+');"""
    query_sql = """Insert Into Song (song_id,song_name,artist_name,duration,popularity) VALUES ( :song_id , :song_name , :artist_name , :duration , :popularity  );"""
    # db is sqlalchemy session object
    query_results = conn.execute(text(query_sql), {"song_id": song_id, "song_name":song_name, "artist_name":artist, "duration":duration, "popularity":popularity})
    # .format(song_id,song_name,artist,duration,popularity)
    # conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_song_by_id(song_id):
    """ remove entries based on task ID """
    conn = db.connect()
    query = """Delete From Song where song_id LIKE :bar_tags;"""
    # print(query)
    conn.execute(text(query),{"bar_tags":song_id})
    conn.close()

def find_song(key):
    ''' Find song_name containing the keyword in database 
    @STATUS: FINISHED
    '''
    conn = db.connect()
    # Source: https://stackoverflow.com/questions/3325467/sqlalchemy-equivalent-to-sql-like-statement
    query_sql = """SELECT * FROM Song WHERE song_name LIKE '%' :bar_tags '%'"""
    # db is sqlalchemy session object
    query_results = conn.execute(text(query_sql), {"bar_tags": key}).fetchall()
    #  = conn.execute("SELECT * from Song WHERE song_name LIKE %{}% ;").format(key).fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Song' ORDER BY ORDINAL_POSITION").fetchall()
    res = []
    count = 0
    res_col = [column_name[6][0],column_name[0][0], column_name[2][0], column_name[4][0], column_name[5][0]]
    for result in query_results:
        count += 1
        if count > 15:
            break
        item = [ result[6],result[0], result[2],result[4],result[5] ]
        res.append(item)
    conn.close()
    return res, res_col

def tongyun_fetch(decade):
    '''
    Return table of artists that is popular in some range of time
    '''
    if decade == '90':
        start_year,end_year = '9%','00'
    elif decade == '00':
        start_year,end_year = '0%','10'
    else:
        start_year,end_year = '1%','20'

    conn = db.connect()
    query_sql = """ SELECT a.artist_name, a.num_followers, s.song_name, s.album_name, s.release_date, s.popularity
    FROM musicDB.Artist a NATURAL JOIN musicDB.Song s
    WHERE (s.release_date LIKE '%/%/' :start OR s.release_date LIKE '%/%/' :end  ) AND a.num_followers > (SELECT AVG(num_followers) FROM musicDB.Artist)
    ORDER BY s.popularity;
    """
    query_results = conn.execute(text(query_sql), {"start": start_year, "end":end_year}).fetchall()
    res_col = ['artist_name', 'num_followers', 'song_name', 'album_name', 'release_date', 'popularity']
    conn.close()
    return query_results, res_col