import sqlite3

dbName_Bible = "bible_20230102.db"

# 1. connect
sqlite_bible = sqlite3.connect( dbName_Bible )

# 2. get cursor
cur = sqlite_bible.cursor()

# 3. query and show  -- tbibleContK4
if False :
    cur.execute("select * from tbibleContK4")
    rows = cur.fetchall()
    for row in rows :
        print( row )
    sqlite_bible.close()

# 4. query and show -- tBibleBook
if True :
    cur.execute("select * from tbibleBook")
    rows = cur.fetchall()
    for row in rows :
        print( row )
    sqlite_bible.close()

