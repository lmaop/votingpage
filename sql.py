import sqlite3

# conn = sqlite3.connect(':memory:')

conn = sqlite3.connect('users.db')

# create a cursor
c = conn.cursor()

# create a table
c.execute("""CREATE TABLE users(
    
)

""")

# commit
conn.commit()

# close connection
conn.close()
