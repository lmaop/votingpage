from flask import Blueprint, render_template, redirect, request, session
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

c = []
otp = testing.randomnum()
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
        fname = request.form.get("fname")
        age = int(request.form.get("age"))
        aadharno = int(request.form.get("aadharno"))
        voter_idno = int(request.form.get("voterid"))
        pass_word = request.form.get("password")
        pass_word2 = request.form.get("password1")
        # all details come into code for verification
        # will validate voter-id and aadhar-no at some point, right now it is NOT validated
        c.extend([fname, age, aadharno, voter_idno])  # just using the variables by storing them
        if age > 18 and pass_word == pass_word2:
            # if aadhar_no > 1 and voter_id_no >1:
            # this checks age of user and confirms 2 passwords and( the length of password)
            testing.write(fname, pass_word)  # it writes the user input into file to check during login
            msg = 'Sign Up Successful, Login and confirm OTP'  # success message
            return render_template('login.html', msg=msg)
        else:
            msg = 'Not Eligible to vote/ passwords do not match'  # Error message
            return render_template('signup.html', msg=msg)
    else:
        return render_template("signup.html")


# this is the login page route, it has to modes of access get and post
@app_blueprint.route('/login', methods=["GET", "POST"])
def login():

    # user information comes into python code
    # a message to display if any error
    msg1 = str(otp)   # making the otp into a string to send to the user

    if request.method == "POST":
        # if the access mode or request mode is post
        user = str(request.form.get("userid"))
        password = str(request.form.get("password"))
        gmail = request.form.get('gmail')
        if sql.query_val(user, password) == 'valid' and testing.checkgmail(gmail) == 'valid':
            # check() checks the file for username and password
            # checks the gmail with a generic regular expression syntax
            session['user'] = user
            session['pg'] = 'verified'  # session{user=username} this is a dictionary data structure
            testing.sendmail(gmail, msg1)  # sending mail to user gmail with the otp in string format
            # after checking the user input and if validated. it redirects to otp-verify page
            return redirect('/vote')
        else:
            msg = 'Incorrect Username / Password / Gmail!'
            return render_template("login.html", msg=msg)
            # if wrong info then error message with ambiguity
    else:
        if 'user' in session:
            return redirect('/vote')
        return render_template("login.html")
    # it either returns to login page with error msg or without error if request mode is GET


# this is the main voting page, has both methods as it has to take a form to get posted
@app_blueprint.route('/vote', methods=["GET", "POST"])
def vote():
    otp1 = request.form.get("otp")
    if request.method == "GET":
        if 'user' in session and session['pg'] == 'verified':
            # 'user' is validated with the OTP
            session['pg'] = 'vote'
            return render_template('vote.html')  # only then he/she can get access to the vote page
        else:
            msg = 'Please Login'
            return render_template('login.html', msg=msg)
    else:
        if int(otp1) == otp and 'user' in session and session['pg'] == 'vote':
            option = request.form.get("options")
            print(option)
            session['pg'] = 'voted'
            return redirect("/voted")
        else:
            return render_template('login.html')


# this is about page
@app_blueprint.route('/about')
def about():
    return render_template("about.html")


# this is the logout function which is called when the logout button is clicked
@app_blueprint.route('/logout')
def logout():
    session.pop('user', None)
    # as we had validated int previous block
    return redirect("login")  # after logout it is redirected to the login page


# this a temporary function()
@app_blueprint.route('/error404')
def error():  # it can be used in emergency situations
    return render_template("error.html")
# it is optional and provides a quick backup if anything goes wrong


@app_blueprint.route('/voted')
def voted():
    if session['pg'] == 'voted':
        return render_template("voted.html")
    else:
        return redirect('/vote')
