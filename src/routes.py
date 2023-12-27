from flask import Blueprint, render_template, url_for

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route('/chat')
def chat():
    return render_template('chat.html')

@main.route('/registration')
def registration():
    return render_template('registration.html')

@main.route('/next_registration')
def next_registration():
    return render_template('next_registration.html')


@main.route('/forgot_psw')
def forgot_psw():
    return render_template('forgot_psw.html')
