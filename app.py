from flask import Flask, redirect, url_for, render_template, request, flash, session

import mysql.connector
from passlib.hash import sha256_crypt

import os


# Flask initial setup
app = Flask(__name__)
app.secret_key = os.urandom(24)


# User login
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        if request.form["not_registered"]:
            return redirect(url_for('register'))

        # Get the input of username and password
        username = request.form['username']
        password_candidate = request.form['password']
        password = ''  # Shitty solution to the login system, works for now
        print(username, password_candidate)
        # Create cursor
        # cur = db.cursor(dictionary=True)

        # Get user by username todo usposobi to z databaseom
        """ver = False  # verificator if username exists
        cur.execute("SELECT * FROM users WHERE username = '{}'".format(username))
        for x in cur:
            password = x['password']
            ver = True

        if ver:
            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # app.logger.info("Password matched")
                session['logged_in'] = True
                session['username'] = username

                # Close connection and redirect
                cur.close()
                return redirect(url_for('dashboard'))

            else:
                flash("Incorrect password")
                return render_template("login.html")

        else:
            flash("Username does not exist")
            return render_template("login.html")"""

    else:
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email_phone = request.form["email-phone"]
        username = request.form["username"]
        password = request.form["password"]
        repeat_password = request.form["repeat-password"]

        # Check if passwords match
        if password != repeat_password:
            flash("The passwords don't match.")
            return render_template("register.html")
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)