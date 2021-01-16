from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
import os
from passlib.hash import sha256_crypt
from functools import wraps

from dbCommunication import Connector, UserDataBase, MovieDatabase
# Create instances UserDatabase and MovieDatatbase
udb = UserDataBase()
mdb = MovieDatabase()


# Flask initial setup
app = Flask(__name__)
app.secret_key = os.urandom(24)


# User login
@app.route("/login", methods=["POST", "GET"])
def login():
    # todo Access user liked, watched jsons and save to session user
    if request.method == "POST":
        # If register button was clicked, redirect
        if request.form.get("submit_button", False) == "not_registered":
            return redirect(url_for('register'))

        # Get the input of username and password
        username = request.form['username']
        if username == '':
            flash("No username given.")
            return render_template("login.html")
        password_candidate = request.form['password']
        if password_candidate == '':
            flash("No password given.")
            return render_template("login.html")

        # Check if user in database, get user_dict
        is_in_database, user_dict = udb.get_user_by_username(username)

        # Check if username exists
        if is_in_database:
            # Check if password matches the saved hashed password
            if sha256_crypt.verify(password_candidate, user_dict["password"]):
                session['logged_in'] = True
                email = user_dict['email']
                phone = user_dict['phone']
                session['user'] = {'username': username, 'email': email, 'phone': phone}
                # Rederect to main page
                return redirect(url_for('main_page'))
            else:
                flash("Incorrect password.")
                return render_template("login.html")
        else:
            flash("Username does not exist.")
            return render_template("login.html")

    else:
        return render_template("login.html")


@app.route("/log_out", methods=["POST", "GET"])
def log_out():
    session.pop('logged_in')
    session.pop('user')
    return redirect(url_for('main_page'))


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
    # todo Access user liked, watched json data and save to session user
    # todo Writing an email already written returns MySql error
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

        # If everything passes, encrypt password in hash
        hashed_pass = sha256_crypt.hash(password)
        # Save user to db
        udb.add_new_user(username, hashed_pass, email=email, phone=phone)

        # Set logged in session to true, create user dict.
        session['logged_in'] = True
        session['user'] = {'username': username, 'email': email, 'phone': phone}

        # Rederect to main page
        return redirect(url_for('main_page'))

    else:
        return render_template("register.html")


@app.route("/movie/<id>", methods=["POST", "GET"])
def movie(id):
    movie_data = mdb.search_movie_by_id(id)[0]
    return render_template("movie_page.html", movie=movie_data)


@app.route("/", methods=["POST", "GET"])
def main_page():
    # todo v main_page.html ne dela isAdult
    if request.method == "POST":
        # Get search_button pressed
        if request.form.get("search_button", False) == 'submit':
            # Get text from search box
            search_text = request.form["search"]
            # Check if not empty string
            if search_text == '':
                pass
                # return render_template("main_page.html")
            else:
                # Get movies from db
                search_resoults, movie_data = mdb.search_by_keyword(search_text)
                movies = movie_data
                return render_template("main_page.html", movies=movies, search_resoults=search_resoults)

    movie_data = mdb.random_new_movies()
    movies = movie_data['movies']

    return render_template("main_page.html", movies=movies, search_resoults=-1)


@app.route("/random_generator", methods=["POST", "GET"])
def random_generator():
    return render_template("random_generator.html")



if __name__ == "__main__":
    app.run(debug=True)
