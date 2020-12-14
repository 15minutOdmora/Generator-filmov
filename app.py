from flask import Flask, redirect, url_for, render_template, request, flash, session

from passlib.hash import sha256_crypt
from functools import wraps

from dbCommunication import Connector, UserDataBase
# Create instances
udb = UserDataBase()

import os


# Flask initial setup
app = Flask(__name__)
app.secret_key = os.urandom(24)


# User login
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # Nedela
        """if request.form["not_registered"]:
            return redirect(url_for('register'))"""

        # Get the input of username and password
        username = request.form['username']
        password_candidate = request.form['password']

        # Check if user in database, get user_dict
        ver, user_dict = udb.get_user_by_username(username)
        print(user_dict)

        # Check if username exists
        if ver is True:
            # Check if password matches
            if password_candidate == user_dict["password"]:
                # todo, log the user in
                pass
            else:
                flash("Incorrect password.")
                return render_template("login.html")
        else:
            flash("Username does not exist.")
            return render_template("login.html")

    else:
        return render_template("login.html")


# Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Log in to access profile.')
            return redirect(url_for('login'))
    return wrap


# User registration
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email_phone = request.form["email-phone"]
        username = request.form["username"]
        password = request.form["password"]
        repeat_password = request.form["repeat-password"]

        # Check if passwords match, if not flash error
        if password != repeat_password:
            flash("The passwords do not match.")
            return render_template("register.html")

        # Check if email or phone number
        if "@" in email_phone:
            email = email_phone
            phone = None
        # Should be phone number
        else:
            # Check if phone number has only digits
            if email_phone.replace(" ", "").isdigit():
                phone = email_phone
                email = None
            else:
                flash("Email or phone number is incorrect")
                return render_template("register.html")

        # If everything passes, save user to db
        udb.add_new_user(username, password, email=email, phone=phone)

        # Set logged in session to true, create user dict.
        session['logged_in'] = True
        session['user'] = {'username': username, 'email': email, 'phone': phone}

    else:
        return render_template("register.html")


@app.route("/", methods=["POST", "GET"])
# @is_logged_in
def main_page():
    return render_template("main_page.html")


if __name__ == "__main__":
    app.run(debug=True)
