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
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (voter_id, hashed_password, aadhar_no, f_name, l_name, age, city, state, pincode, gmail))
    except sqlite3.IntegrityError:
        return "error"
    # commit
    conn.commit()
    # close connection
    conn.close()


def query_val(voter_id):  # returns pass if voter id exists
    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('users.db')
    # create a cursor
    c = conn.cursor()
    # query values
    c.execute("SELECT hash_pass FROM users where voter_id='"+voter_id+"'")
    result = c.fetchone()
    # commit
    conn.commit()
    # close connection
    conn.close()
    return result[0]


def query_gmail(voter_id):
    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('users.db')
    # create a cursor
    c = conn.cursor()
    # query values
    c.execute("SELECT gmail FROM users where voter_id='"+voter_id+"'")
    result = c.fetchone()
    # commit
    conn.commit()
    # close connection
    conn.close()
    return result[0]


def query_voter(voter_id):
    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('users.db')
    # create a cursor
    c = conn.cursor()
    # query values
    c.execute("SELECT voter_id FROM users where voter_id='"+voter_id+"'")
    result = c.fetchone()
    # commit
    if result:
        return True
    return False


def vote(voter_id, vote_option):
    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('users.db')
    # create a cursor
    c = conn.cursor()
    # insert values
    try:
        c.execute("INSERT INTO votes VALUES (?, ?)",
                  (voter_id, vote_option))
    except sqlite3.IntegrityError:
        return "error"
    # commit
    conn.commit()
    # close connection
    conn.close()


def query_vote(voter_id):
    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect('users.db')
    # create a cursor
    c = conn.cursor()
    # query values
    c.execute("SELECT voter_id FROM votes where voter_id='"+voter_id+"'")
    result = c.fetchone()
    # commit
    if result:
        return True
    return False



