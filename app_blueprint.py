from flask import Blueprint, render_template, redirect, request, session
# flask WebDev framework in python
# Blueprints: they are html route pages linked to the app.py(flaskapp)
# render_templates :  renders the required html page which is called
# redirect: it redirects to the page as and when required
# request: it is to request elements from the web page eg:inputs field, text boxes , radio  button
# session : it is a data structure tool to help authentication of current user
import testing
# this is my predefined function package

app_blueprint = Blueprint('app_blueprint', __name__)

c = []
otp = testing.randomnum()
# gets random 4-digit number - check testing for more
# @app_blueprint takes the blueprint from the templates page and assigns a decorator / or /home or /vote etc


# this is home route or home page
@app_blueprint.route('/', methods=["GET"])
def home():
    session['user'] = 'home'
    return render_template('home.html')
# returns the home html page


# this is the signup page with both modes
@app_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
    msg = ''
    if request.method == "POST":
        # if the method is posted with button signup then user info comes into py code
        fname = request.form.get("fname")
        age = int(request.form.get("age"))
        aadharno = int(request.form.get("aadharno"))
        voter_idno = request.form.get("voterid")
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
        return render_template("signup.html", msg=msg)


# this is the login page route, it has to modes of access get and post
@app_blueprint.route('/login', methods=["GET", "POST"])
def login():

    # user information comes into python code
    msg = ''  # a message to display if any error
    msg1 = str(otp)   # making the otp into a string to send to the user

    if request.method == "POST":
        # if the access mode or request mode is post
        user = request.form.get("userid")
        password = request.form.get("password")
        gmail = request.form.get('gmail')
        if testing.check(user, password) == 0 and testing.checkgmail(gmail) == 'valid':
            # check() checks the file for username and password
            # checks the gmail with a generic regular expression syntax
            session['user'] = 'otp'  # session{user=username} this is a dictionary data structure
            testing.sendmail(gmail, msg1)  # sending mail to user gmail with the otp in string format
            # after checking the user input and if validated. it redirects to otp-verify page
            msg = 'Check gmail for your otp'
            return render_template('otpverify.html', msg=msg)
        else:
            msg = 'Incorrect Username / Password / Gmail!'
            return render_template("login.html", msg=msg)
            # if wrong info then error message with ambiguity
    else:
        if session['user'] == 'otp':
            msg = 'You have already logged in, Please check gmail for otp'
            return render_template('otpverify.html', msg=msg)
        else:
            return render_template("login.html", msg=msg)
    # it either returns to login page with error msg or without error if request mode is GET


# this page is to verify otp with users email address(GMAIL for now) 2 methods
@app_blueprint.route('/otpverify', methods=["GET", "POST"])
def otpverify():
    otp1 = request.form.get("otp")
    # takes users input of OTP through form in html
    # the input comes into python code
    msg = ''
    if request.method == "POST":  # if the method is post ie if the verify button is clicked
        if int(otp1) == otp and session['user'] == 'otp':  # take the OTP input in string form
            # it is converted to integer to verify with global variable otp
            session['user'] = 'vote'
            # the dictionary is updated with his pertaining OTP
            return redirect('/vote')  # only then he/she is redirected to voting page
        else:
            msg = 'Incorrect OTP check Gmail'  # error message
            return render_template('otpverify.html', msg=msg)
    else:
        if session['user'] == 'vote':
            msg = 'please vote and click submit to confirm'
            return render_template('vote.html', msg=msg)
        elif session['user'] == 'voted':
            msg = ' you have already voted , thank you, please logout'
            return render_template('voted.html', msg=msg)
        elif session['user'] == 'logout':
            return redirect("/login")
        elif session['user'] == 'otp':
            return render_template("otpverify.html", msg=msg)  # used in get method and if any error messages
        else:
            return redirect('/login')


# this is the main voting page, has both methods as it has to take a form to get posted
@app_blueprint.route('/vote', methods=["GET", "POST"])
def vote():
    if request.method == "GET":
        if session['user'] == 'vote':  # 'user' is validated with the OTP
            return render_template('vote.html')  # only then he/she can get access to the vote page
        elif session['user'] == 'voted':
            return render_template('voted.html')  # if the 'user' is not the OTP then login page is shown
        else:
            return redirect('/login')
    else:
        option = request.form.get("options")
        print(option)
        session['user'] = 'voted'
        return render_template('voted.html')


# this is about page
@app_blueprint.route('/about')
def about():
    return render_template("about.html")


# this is the logout function which is called when the logout button is clicked
@app_blueprint.route('/logout')
def logout():
    session['user'] = 'logout'  # the 'user' value is changed to log-out
    # as we had validated int previous block
    return redirect("/login")  # after logout it is redirected to the login page


# this a temporary function()
@app_blueprint.route('/error404')
def error():  # it can be used in emergency situations
    return render_template("error.html")
# it is optional and provides a quick backup if anything goes wrong


@app_blueprint.route('/voted')
def voted():
    return render_template("voted.html")
