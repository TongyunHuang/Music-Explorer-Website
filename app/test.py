import os
import sqlalchemy
from yaml import load, Loader
from flask import Flask
from sqlalchemy import text
'''
connect to GCP database
'''
def init_connect_engine():
    # Detect if the server is running on a GCP instance or on a local computer
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open("../app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]
    
    # GCP instance feature: reads in the yaml file and sets the defined string right into its os env
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST')
        )
    )
    return pool

db = init_connect_engine()

# testing function
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

getRecSong("test")
