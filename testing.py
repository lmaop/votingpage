import smtplib
import random
import re
import cryptocode
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def randomnum():
    a = random.randint(1000, 9999)
    return a


def checkgmail(gmail):
    if re.fullmatch(regex, gmail):
        return 'valid'
    return 'invalid'


def write(user_name, pass_word):
    file = open('pass1.txt', 'a')
    file .write("username: "+user_name+' '+"password: "+pass_word+'')


def check(user_name, pass_word):
    file = open('pass1.txt', 'r')
    for e in file:
        if user_name and pass_word in e.split(' '):
            return 0


def sendmail(gmail, msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("e.chunaav.gov.jproject@gmail.com", "Project@123")
    # email_id = input("Enter your email: ")
    s.sendmail('&&&&&&&&&&&', gmail, msg)


def encrypt(message, code="hi"):
    encoded = cryptocode.encrypt(message, code)
    return encoded


def decrypt(message, code="hi"):
    decoded = cryptocode.decrypt(message, code)
    return decoded
