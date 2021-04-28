from app import db
from sqlalchemy import text

def change_password(username, new_password):
    '''
    Change user's password
    '''
    conn = db.connect()
    update_password_query = """UPDATE User SET password = :new_password WHERE user = :username"""
    conn.execute(text(update_password_query), {"new_password": new_password, "username": username})
    conn.close()

def getLikeSong(username):
    '''
    Fetch list of like song from GCP
    '''
    conn = db.connect()
    query_text = """SELECT f.liked_song_name,s.song_name, s.artist_name FROM musicDB.Favorite f JOIN musicDB.Song s ON f.liked_song_name=s.song_id 
    WHERE username LIKE :username ; """
    liked_song_list = conn.execute(text(query_text), {"username": username}).fetchall()
    conn.close()
    return liked_song_list

def delete_like_song(username,song_id):
    """
    Delete like relation in databse.
        @Args: username, song_id
        @Returns: The task ID for the inserted entry
    """
    conn = db.connect()
    conn.execute("SET SQL_SAFE_UPDATES = 0;")
    query = """Delete From Favorite where liked_song_name LIKE :song_id AND username LIKE :username ;"""
    # print(query)
    conn.execute(text(query),{"song_id":song_id, "username":username})
    conn.execute("SET SQL_SAFE_UPDATES = 1;")
    conn.close()
    return 1

def getRecSong(username):
    '''
    Fetch list of recommended "playlist" from GCP
    '''
    conn = db.connect()
    query = """SELECT ours.username, theirs.username, count(*) as `score`
FROM Favorite as `theirs`, (SELECT f.username, f.liked_song_name FROM Favorite f JOIN Song s ON f.liked_song_name=s.song_id
                              WHERE f.username = :username ) as `ours`
WHERE theirs.username != :username AND theirs.liked_song_name = ours.liked_song_name
GROUP BY theirs.username ORDER BY score DESC;"""
    playlist_list = conn.execute(text(query),{ "username":username}).fetchall()
    print(playlist_list)
    conn.close()
    return playlist_list

def getDiffSong(recName, username):
    '''
    Get set difference between choosen playlist and user playlist
    '''
    conn = db.connect()
    query = """SELECT theirs.liked_song_name, theirs.song_name, theirs.artist_name
FROM (SELECT f.username, f.liked_song_name, s.song_name, s.artist_name
    FROM Favorite f JOIN Song s ON f.liked_song_name=s.song_id WHERE f.username = :recName ) as `theirs`
WHERE theirs.liked_song_name not in (SELECT f.liked_song_name
    FROM Favorite f JOIN Song s ON f.liked_song_name=s.song_id WHERE f.username = :username ) ; """
    diffSongs = conn.execute(text(query),{ "recName":recName ,"username":username}).fetchall()
    conn.close()
    return diffSongs