from flask import Blueprint, render_template, redirect, request, session
# from werkzeug.security import generate_password_hash, check_password_hash
# flask WebDev framework in python
# Blueprints: they are html route pages linked to the app.py(flaskapp)
# render_templates :  renders the required html page which is called
# redirect: it redirects to the page as and when required
# request: it is to request elements from the web page eg:inputs field, text boxes , radio  button
# session : it is a data structure tool to help authentication of current user
import testing
import sql
# this is my predefined function package

app_blueprint = Blueprint('app_blueprint', __name__)

otp = testing.randomnum()
msg1 = str(otp)
# gets random 4-digit number - check testing for more
# @app_blueprint takes the blueprint from the templates page and assigns a decorator / or /home or /vote etc


# this is home route or home page
@app_blueprint.route('/', methods=["GET"])
def home():
    return render_template('home.html')
# returns the home html page


# this is the signup page with both modes
@app_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # if the method is posted with button signup then user info comes into py code
        voter_id = request.form.get("voterid")
        aadhar_no = request.form.get("aadharno")

        f_name = request.form.get("fname")
        l_name = request.form.get("lname")
        age = int(request.form.get("age"))
        city = request.form.get("city")
        state = request.form.get("state")
        pincode = int(request.form.get("pincode"))

        gmail = request.form.get("gmail")
        pass_word = request.form.get("password")
        pass_word2 = request.form.get("password1")

        if len(voter_id) == 12 and len(aadhar_no) == 12 and voter_id == aadhar_no:
            if age > 18 and pass_word == pass_word2 and testing.checkgmail(gmail) == 'valid':
                if len(f_name) > 2 and len(l_name) > 2 and len(city) > 2 and len(state) > 2 and len(str(pincode)) > 2:
                    hashed_password = testing.encrypt(pass_word)
                    if sql.signup(voter_id, hashed_password, aadhar_no,
                                  f_name, l_name, age, city, state, pincode, gmail) != 'error':
                        msg = 'Sign Up Successful, Login and confirm OTP'  # success message
                        return render_template('login.html', msg=msg)
                    else:
                        msg = 'Sign Up Unsuccessful, Voter ID already exists'
                        return render_template('signup.html', msg=msg)
                else:
                    msg = 'Sign Up Unsuccessful, please enter a valid firstname/lastname/state/city/pincode'
                    return render_template('signup.html', msg=msg)
            else:
                msg = 'Sign Up Unsuccessful, you are underage or passwords do not match or gmail invalid'
                return render_template('signup.html', msg=msg)
        else:
            msg = 'Sign Up Unsuccessful, invalid Voter_ID/Aadhar number'
            return render_template('signup.html', msg=msg)
    else:
        return render_template("signup.html")


# this is the login page route, it has to modes of access get and post
@app_blueprint.route('/login', methods=["GET", "POST"])
def login():
    # making the otp into a string to send to the user
    # user information comes into python code
    if request.method == "POST":
        # if the access mode or request mode is post
        voter_id = request.form.get("voterid")
        password = request.form.get("password")
        if sql.query_voter(voter_id):
            if testing.decrypt(sql.query_val(voter_id), password):
                session['user'] = voter_id
                session['page'] = 'vote'   # session{user=username} this is a dictionary data structure
                gmail = sql.query_gmail(session['user'])
                testing.sendmail(gmail, msg1)  # sending mail to user gmail with the otp in string format
                return render_template('vote.html', voterid=voter_id)

            else:
                msg = 'Incorrect Credentials'
                return render_template("login.html", msg=msg)
        else:
            msg = 'Incorrect Credentials'
            return render_template("login.html", msg=msg)

    else:
        if 'user' in session:
            msg = 'You are logged in ' + session['user']
            return render_template('vote.html', msg=msg)
        elif 'page' in session:
            return render_template('login.html')
        else:
            return render_template('login.html')
    # it either returns to login page with error msg or without error if request mode is GET


# this is the main voting page, has both methods as it has to take a form to get posted
@app_blueprint.route('/vote', methods=["GET", "POST"])
def vote():
    otp1 = request.form.get("otp")
    if request.method == "GET":
        print(session)
        if 'user' in session and session['page'] == 'vote' and sql.query_vote(session['user']) is False:
            return render_template('vote.html')  # only then he/she can get access to the vote page
        elif sql.query_vote(session['user']) is not False:
            return redirect("/voted")
        else:
            msg = 'Please Login'
            return render_template('login.html', msg=msg)
    else:
        if int(otp1) == otp and 'user' in session and sql.query_vote(session['user']) is False:
            option = request.form.get("options")
            sql.vote(session['user'], option)
            session['page'] = 'vote'
            return redirect("/voted")
        elif sql.query_vote(session['user']) is not False:
            return redirect("/voted")
        else:
            msg = 'Wrong OTP entered please check gmail or try again'
            return render_template('vote.html', msg=msg)


# this is about page
@app_blueprint.route('/about')
def about():
    return render_template("about.html")


# this is the logout function which is called when the logout button is clicked
@app_blueprint.route('/logout')
def logout():
    print(session)
    session.pop('user', None)
    print(session)
    return redirect("login")  # after logout it is redirected to the login page


# this a temporary function()
@app_blueprint.route('/error404')
def error():  # it can be used in emergency situations
    return render_template("error.html")
# it is optional and provides a quick backup if anything goes wrong


@app_blueprint.route('/voted')
def voted():
    if session['page'] == 'vote':
        return render_template("voted.html")
    else:
        return redirect('/vote')
