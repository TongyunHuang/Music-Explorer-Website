"""Defines all the functions related to the database"""
from app import db
from sqlalchemy import text

def fetch_single_comment(song_id):
    '''
    fetch comment by song_id
    '''
    print(song_id)
    conn = db.connect()
    query = """Select song_id, song_name, comment_link From Comment where song_id LIKE :id;"""
    comment_info = conn.execute(text(query),{"id":song_id}).fetchall()
    conn.close()
    return comment_info


def update_entry(song_id, song_name, comment_link):
    """Updates comment link based on given `song_id`

    Args:
        song_id (str): Targeted song_id
        comment_link (str): Updated comment url

    Returns:
        None
    @STATUS: FINISHED
    """

    conn = db.connect()
    query = """Update Comment set song_name = :song , comment_link = :comment where song_id LIKE :id;"""
    print(query)
    conn.execute(text(query), {"song": song_name, "comment": comment_link, "id":song_id})
    conn.close()


def insert_new_comment(song_id,song_name,comment_link):
    """Insert new comment to table.

    Args:
        song_id,song_name,comment_link: get from form

    Returns: 
        The task ID for the inserted entry
    @STATUS: FINISHED
    """

    conn = db.connect()
    query_sql = """Insert Into Comment (song_id,song_name,comment_link) VALUES ( :song_id , :song_name , :comment_link );"""
    # db is sqlalchemy session object
    query_results = conn.execute(text(query_sql), {"song_id": song_id, "song_name":song_name, "comment_link": comment_link})
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_comment_by_id(song_id):
    """ remove entries based on task ID """
    conn = db.connect()
    query = """Delete From Comment where song_id LIKE :bar_tags;"""
    conn.execute(text(query),{"bar_tags":song_id})
    conn.close()

def find_comment(key):
    ''' Find comment_link of song_name containing the keyword in database 
    @STATUS: FINISHED
    '''
    conn = db.connect()
    # Source: https://stackoverflow.com/questions/3325467/sqlalchemy-equivalent-to-sql-like-statement
    query_sql = """SELECT * FROM Comment WHERE song_name LIKE '%' :bar_tags '%'"""
    # db is sqlalchemy session object
    query_results = conn.execute(text(query_sql), {"bar_tags": key}).fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Comment' ORDER BY ORDINAL_POSITION").fetchall()
    res = []
    count = 0
    res_col = [column_name[0][0],column_name[1][0], column_name[2][0]]
    for result in query_results:
        count += 1
        if count > 15:
            break
        item = [ result[0], result[1], result[2] ]
        res.append(item)
    conn.close()
    return res, res_col

def jinyang_fetch(song_name_1, song_name_2):
    '''
    Return list of songs in same album either with song_name_1 or song_name_2
    '''
    
    conn = db.connect()
    query_sql = """ SELECT *
                    FROM ((SELECT Song.song_name, Song.duration, Song.popularity, Song.artist_name, Song.release_date, Song.song_url, Album.album_name
                    From musicDB.Song As Song JOIN musicDB.Album AS Album USING(album_name)
                    WHERE Album.album_name = (select Song.album_name FROM musicDB.Song As Song WHERE Song.song_name = :song_name_1 LIMIT 1))
                    UNION
                    (SELECT Song.song_name, Song.duration, Song.popularity, Song.artist_name, Song.release_date, Song.song_url, Album.album_name
                    From musicDB.Song As Song JOIN musicDB.Album AS Album USING(album_name)
                    WHERE Album.album_name = (select Song.album_name FROM musicDB.Song As Song WHERE Song.song_name = :song_name_2 LIMIT 1))) AS AllSong
                    ORDER by AllSong.song_name;
    """
    query_results = conn.execute(text(query_sql), {"song_name_1": song_name_1, "song_name_2":song_name_2}).fetchall()
    res_col = ['song_name','duration','popularity','artist_name','release_date','song_url','album_name']
    conn.close()
    return query_results, res_col


    
