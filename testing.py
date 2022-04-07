import smtplib
import random
import re
# import cryptocode
from werkzeug.security import generate_password_hash, check_password_hash
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def randomnum():
    a = random.randint(1000, 9999)
    return a


def checkgmail(gmail):
    if re.fullmatch(regex, gmail):
        return 'valid'
    return 'invalid'


#  def write(user_name, pass_word):
#   file = open('pass1.txt', 'a')
#     file .write("username: "+user_name+' '+"password: "+pass_word+'')
#
#
# def check(user_name, pass_word):
#     file = open('pass1.txt', 'r')
#     for e in file:
#         if user_name and pass_word in e.split(' '):
#             return 0


def sendmail(gmail, msg):
    from1 = 'jmproject07@gmail.com'
    to = gmail
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("jmproject07@gmail.com", "Project@123")
    # email_id = input("Enter your email: ")
    msg1 = """From: %s\nTo: %s\nSubject: e-chunaav OTP\n\n Dear Sir / Madam,

Your One Time Password(OTP) for your VOTE is :

%s


Do not share your OTP with anyone.


Warm Regards,
E-Chunaav team

           """ % (from1, to, msg)
    # msg1 = "From: \nSubject: e-chunaav OTP\tBody: Please enter the correct OTP and DO NOT SHARE WITH ANYONE %s" % msg
    s.sendmail(from_addr=from1, to_addrs=to, msg=msg1)
    s.quit()


# def encrypt(message, code="hi"):
#     encoded = cryptocode.encrypt(message, code)
#     return encoded
# def decrypt(message, code="hi"):
#     decoded = cryptocode.decrypt(message, code)
#     return decoded


def encrypt(password):
    hashed_password = generate_password_hash(password, method='sha256')
    return hashed_password


def decrypt(hash1, password):
    if check_password_hash(hash1, password):
        return True
    else:
        return False

# decrypt1('sha256$EHQKC7q3gvQrO6Kh$3f74ff6324e1256b64c676a5a1f3a45c67766f66715851ddd312ea6b2659babc', 'hii')
# success



