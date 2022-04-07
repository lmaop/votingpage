import sqlite3
# from werkzeug.security import check_password_hash


def cr_table():
    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('usersdb.db')
    # create a cursor
    c = conn.cursor()
    # create a table
    c.execute("""CREATE TABLE users(
            user_id integer primary key,
            username text,
            password text,
            voter_id integer, 
            aadhar_no integer,
            vote text)""")

    # commit
    conn.commit()
    # close connection
    conn.close()


def signup(voter_id, hashed_password, aadhar_no, f_name, l_name, age, city, state, pincode, gmail):
    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('users.db')
    # create a cursor
    c = conn.cursor()
    # insert values
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (voter_id, hashed_password, aadhar_no, f_name, l_name, age, city, state, pincode, gmail))
    # commit
    conn.commit()
    # close connection
    conn.close()



def query_val(username, password):
    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('users.db')
    # create a cursor
    c = conn.cursor()
    # query values
    c.execute("SELECT username,password FROM users where username='"+username+"' and password='"+password+"'")
    results = c.fetchall()
    if len(results) == 0:
        return "invalid"
    else:
        return "valid"
