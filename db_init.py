import sqlite3 as lite

users = (
    ('00000000','password'),
    ('00000010','password2'),
    ('00000011','password3')
    )

if __name__ == '__main__':
    con = lite.connect('base.db')
    with con:
        cur = con.cursor()

        # CREATE USERS DATA BASE
        cur.execute("DROP TABLE IF EXISTS Users")
        cur.execute("CREATE TABLE Users(Phone TEXT, Password TEXT)")
        cur.executemany("INSERT INTO Users VALUES(?, ?)", users)
