from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
import os
from passlib.hash import sha256_crypt
from functools import wraps
import json

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
                liked = user_dict['liked']
                watched = user_dict['watched']
                session['user'] = {'username': username,
                                   'email': email,
                                   'phone': phone,
                                   'liked': liked,
                                   'watched': watched}
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
        session['user'] = {'username': username, 'email': email, 'phone': phone, 'liked': {}, 'watched': {}}

        # Rederect to main page
        return redirect(url_for('main_page'))

    else:
        return render_template("register.html")


@app.route("/movie/<id>", methods=["POST", "GET"])
def movie(id):
    if request.method == "POST":
        if request.form["save_button"].split(" ")[0] == "liked":
            # Add to session liked
            session['user']['liked'][id] = "Test"
            ver = udb.save_liked_to_user(session['user']['username'], session['user']['liked'])

        elif request.form["save_button"].split(" ")[0] == "unliked":
            if id in session['user']['liked'].keys():
                del session['user']['liked'][id]
                ver = udb.save_liked_to_user(session['user']['username'], session['user']['liked'])
                print(ver)

        if request.form["save_button"].split(" ")[0] == "watched":
            # Add to session liked
            session['user']['watched'][id] = "Test"
            ver = udb.save_watched_to_user(session['user']['username'], session['user']['watched'])
            print(ver)
        elif request.form["save_button"].split(" ")[0] == "unwatched":
            if id in session['user']['watched'].keys():
                del session['user']['watched'][id]
                ver = udb.save_watched_to_user(session['user']['username'], session['user']['watched'])
                print(ver)

        if request.form["save_button"] == "save_opinion":
            opinion = request.form["opinion"]
            rate = request.form["rate"]
            ver = udb.save_opinion_of_movie(session['user']['username'], id, opinion, int(rate))
            print(ver)

        # Have to update session otherwise liked/watched gets f****d
        username = session['user']['username']
        is_in_database, user_dict = udb.get_user_by_username(username)
        email = user_dict['email']
        phone = user_dict['phone']
        liked = user_dict['liked']
        watched = user_dict['watched']
        session['user'] = {'username': username,
                           'email': email,
                           'phone': phone,
                           'liked': liked,
                           'watched': watched}

    movie_data = mdb.search_movie_by_id(id)[0]

    if 'logged_in' in session:
        opinion, opinion_rating = udb.get_all_opinions_of_user(session['user']['username'])
        # Save opinion in movie_data
        if id in opinion.keys():
            movie_data['opinion'] = opinion[id]
            movie_data['opinion_rating'] = int(opinion_rating[id])

    return render_template("movie_page.html", movie=movie_data)


@app.route("/users/<username>", methods=["POST", "GET"])
def user_profile(username):
    is_in_database, user_data = udb.get_user_by_username(username)
    if is_in_database:
        # Get all opinions
        opinions, ratings = udb.get_all_opinions_of_user(username)
        # Get liked and watched movies data
        liked_movies = []
        for key, value in user_data['liked'].items():
            liked_movies.append(mdb.search_movie_by_id(key)[0])
        watched_movies = []
        for key, value in user_data['watched'].items():
            searched_movie = mdb.search_movie_by_id(key)[0]
            # Shitty solution
            if key in opinions.keys():
                searched_movie['opinion'] = opinions[key]
                searched_movie['opinion_rating'] = ratings[key]
            watched_movies.append(searched_movie)
        return render_template("user_profile.html",
                               user_data=user_data,
                               liked=liked_movies,
                               watched=watched_movies,
                               opinions=opinions)
    else:
        return "<h2>This user does not exist</h2>"


def param_to_string(param):
    """
    Helper function for random_generator, creates a string from the param dict
    :param param_dict: param_dict from random_generator
    :return: string of params
    """
    string = "<p>Search results for these parameters: </p>"
    if param == {}:
        return "<p></p>"
    for key, value in param.items():
        if isinstance(value, dict):
            string += "<p>  " + key + ": " + "from " + str(value['from']) + " to " + str(value["to"]) + "</p>"
        else:
            if not isinstance(value, list):
                string += "<p>  " + key + ": " + " ".join(value) + "</p>"
            else:
                string += "<p>  " + key + ": " + str(value) + "</p>"
    return string


def param_cleaner(param_dict):
    """
    Helper function for random_generator, cleans the given param_dict of 'empty' values
    :param param_dict: param_dict from random_generator
    :return: param_dict_cleaned
    """
    def generate_number_from_type(type, to_from, value):
        if value == 0 or value == '':
            if type == 'release_year':
                if to_from == 'from':
                    return 1900
                elif to_from == 'to':
                    return 2020
            if type == 'duration':
                if to_from == 'from':
                    return 0
                elif to_from == 'to':
                    return 1000
            if type == 'number_of_votes':
                if to_from == 'from':
                    return 0
                elif to_from == 'to':
                    return 10000000
            if type == 'rating':
                if to_from == 'from':
                    return 0
                elif to_from == 'to':
                    return 11
        return value

    cleaned = dict()
    for key, value in param_dict.items():
        if isinstance(value, dict):
            if value['to'] == '' and value['from'] == '':
                pass
            else:
                cleaned[key] = {'from': 0, 'to': 0}
                cleaned[key]['from'] = generate_number_from_type(key, 'from', param_dict[key]['from'])
                cleaned[key]['to'] = generate_number_from_type(key, 'to', param_dict[key]['to'])
        else:
            if value == '' or value == 0:
                pass
            else:
                cleaned[key] = value

    return cleaned


@app.route("/random_generator", methods=["POST", "GET"])
def random_generator():
    if request.method == "POST":
        params_dict = {'release_year': {'from': 0, 'to': 0},
                        'genre': '',
                        'duration': {'from': 0, 'to': 0},
                        'directed_by': '',
                        'number_of_votes': {'from': 0, 'to': 0},
                        'rating': {'from': 0, 'to': 0}}

        # If Search button was clicked
        if request.form.get("search_button", False) == 'search':
            params_dict["release_year"]["from"] = request.form["release_year_from"]
            params_dict["release_year"]["to"] = request.form["release_year_to"]
            # params_dict["genre"] = request.form["select_genre"]
            params_dict["duration"]["from"] = request.form["duration_from"]
            params_dict["duration"]["to"] = request.form["duration_to"]
            params_dict["directed_by"] = request.form["directed_by"]
            params_dict["number_of_votes"]["from"] = request.form["num_of_votes_from"]
            params_dict["number_of_votes"]["to"] = request.form["num_of_votes_to"]
            params_dict["rating"]["from"] = request.form["rating_from"]
            params_dict["rating"]["to"] = request.form["rating_to"]
            if "select_genre" in request.form.keys():
                params_dict["genre"] = request.form.getlist('select_genre')

            param = param_cleaner(params_dict)
            movies = mdb.get_movie_by_param(param)
            search_results = str(len(movies))
            return render_template("random_generator.html", movies=movies,
                                   param=param_to_string(param),
                                   search_results=search_results)

        # If Generate button was clicked
        if request.form.get("search_button", False) == 'generate':
            params_dict["release_year"]["from"] = request.form["release_year_from"]
            params_dict["release_year"]["to"] = request.form["release_year_to"]
            params_dict["duration"]["from"] = request.form["duration_from"]
            params_dict["duration"]["to"] = request.form["duration_to"]
            params_dict["directed_by"] = request.form["directed_by"]
            params_dict["number_of_votes"]["from"] = request.form["num_of_votes_from"]
            params_dict["number_of_votes"]["to"] = request.form["num_of_votes_to"]
            params_dict["rating"]["from"] = request.form["rating_from"]
            params_dict["rating"]["to"] = request.form["rating_to"]
            if "select_genre" in request.form.keys():
                params_dict["genre"] = request.form.getlist('select_genre')

            param = param_cleaner(params_dict)
            print(param_to_string(param))
            movies = mdb.get_movie_by_param(param, rand=True)
            search_results = str(len(movies))
            return render_template("random_generator.html", movies=movies,
                                   param=param_to_string(param),
                                   search_results=search_results)

    return render_template("random_generator.html", movies=[], param="", search_results="0")


@app.route("/", methods=["POST", "GET"])
def main_page():
    if request.method == "POST":
        # Get search_button pressed
        if request.form.get("search_button", False) == 'submit':
            # Get text from search box
            search_text = request.form["search"]
            # Check if not empty string
            if search_text == '':
                pass
            else:
                # Get movies from db
                search_resoults, movie_data = mdb.search_by_keyword(search_text)
                movies = movie_data
                return render_template("main_page.html", movies=movies, search_resoults=search_resoults)

    movie_data = mdb.random_new_movies()
    movies = movie_data['movies']

    return render_template("main_page.html", movies=movies, search_resoults=-1)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
