from app import db

number_of_results_displayed = 15
# num_column = "No."

def fetch_song():
    conn = db.connect()
    query_results = conn.execute("Select * from Song;").fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Song' ORDER BY ORDINAL_POSITION").fetchall()
    res = []
    count = 0
    res_col = [column_name[0][0], column_name[2][0], column_name[4][0], column_name[5][0]]
    for result in query_results:
        count += 1
        if count > number_of_results_displayed:
            break
        item = [
                result[0],
                result[2],
                result[4],
                result[5]
        ]
        res.append(item)
    conn.close()
    return res, res_col

def fetch_album():
    conn = db.connect()
    query_results = conn.execute("Select * from Album;").fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Album' ORDER BY ORDINAL_POSITION").fetchall()
    res_col = [column_name[0][0], column_name[2][0], column_name[3][0], column_name[4][0], column_name[5][0]]
    res = []
    count = 0
    for result in query_results:
        count += 1
        if count > number_of_results_displayed:
            break
        item = [
                result[0],
                result[2],
                result[3],
                result[4],
                result[5]
        ]
        res.append(item)
    conn.close()
    return res, res_col

def fetch_cover():
    conn = db.connect()
    query_results = conn.execute("Select * from Cover;").fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Cover' ORDER BY ORDINAL_POSITION").fetchall()
    res_col = [column_name[1][0], column_name[2][0]]
    res = []
    count = 0
    for result in query_results:
        count += 1
        if count > number_of_results_displayed:
            break
        item = [
                result[1],
                result[2],
        ]
        res.append(item)
    conn.close()
    return res, res_col

def fetch_artist():
    conn = db.connect()
    query_results = conn.execute("Select * from Artist;").fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Artist' ORDER BY ORDINAL_POSITION").fetchall()
    res_col = [column_name[0][0], column_name[3][0], column_name[4][0]]
    res = []
    count = 0
    for result in query_results:
        count += 1
        if count > number_of_results_displayed:
            break
        item = [
                result[0],
                result[3],
                result[4]
        ]
        res.append(item)
    conn.close()
    return res, res_col

def fetch_comment():
    conn = db.connect()
    query_results = conn.execute("Select * from Comment;").fetchall()
    column_name = conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Comment' ORDER BY ORDINAL_POSITION").fetchall()
    res_col = [column_name[1][0], column_name[2][0]]
    res = []
    count = 0
    for result in query_results:
        count += 1
        if count > number_of_results_displayed:
            break
        item = [
                result[1],
                result[2]
        ]
        res.append(item)
    conn.close()
    return res, res_col