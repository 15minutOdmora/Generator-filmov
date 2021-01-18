import mysql.connector
from image_scraping import *
from auth import AUTH
import json


class Connector:
    def __init__(self):
        self.db = mysql.connector.connect(**AUTH)
        self.cur = None

    def create_cursor(self):
        """
        Function: Creates the cursor in the var. self.cur to operate the database.
        """
        self.cur = self.db.cursor(dictionary=True)

    def close_cursor(self):
        """
        Method: Closes the connection on the cursor cur
        """
        if self.cur is not None:
            self.cur.close()
            self.cur = None
        else:
            print("Cursor does not exist.")
            raise

    def execute(self, code, param):
        """
        Method: Executes the code with the given parameters
        :param code: string containing code to be executed in MySql
        :param param: touple containing values to be used in the string code
        """

        if self.cur is not None:
            if param is None:
                self.cur.execute(code, param)
            else:
                self.cur.execute(code, param)
        else:
            print("Cursor does not exist.")
            raise

    def commit(self):
        """
        Method: Commits changes to the database
        """
        self.db.commit()


class UserDataBase(Connector):

    def add_new_user(self, username, password, email=None, phone=None):
        """ Todo call the function below
        Method: Adds new user into db in the table Uporabnik
        :param username: The username of the user
        :param password: Password of the user
        :param email: Email of the user, if not given is None
        :param phone: Phone number of the user, if not given is None
        :return: (True/False, reason, data_dict)
        """
        # Create cursor
        self.create_cursor()

        # Create liked and watched Json files, dump them into string
        liked = json.dumps({})
        watched = json.dumps({})

        # Check if phone or email was given
        if phone is None and email is not None:
            code = "INSERT INTO User(username, password, email, liked, watched) VALUES (%s, %s, %s, %s, %s)"
            param = (username, password, email, liked, watched)

        elif email is None and phone is not None:
            code = "INSERT INTO User(username, password, phone, liked, watched) VALUES (%s, %s, %s, %s, %S)"
            param = (username, password, phone, liked, watched)

        # Execute the code
        self.cur.execute(code, param)

        # Commit to database
        self.commit()

        # Close cursor
        self.close_cursor()
        
    def check_user_registration_params(self, username='', email='', phone=''):
        """Method checks if username, email, phone are already in the user table
        :param username: users username
        :param email: users email
        :param phone: users phone
        :return: True/False, working/if problem -> where
        """

        def username():
            """Function checks if username is already in the user table
            :return: True/False
            """

            # Create cursor
            self.create_cursor()

            # SQL code
            code = "SELECT idUser FROM User WHERE username = %s"
            param = (username)
            self.cur.execute(code, param)

            # If any user found, returns false
            for user in self.cur:
                self.close_cursor()
                return False

            self.close_cursor()
            return True

        def email():
            """Function checks if email is already in the user table
            :return: True/False
            """

            # Create cursor
            self.create_cursor()

            # SQL code
            code = "SELECT idUser FROM User WHERE email = %s"
            param = (email)
            self.cur.execute(code, param)

            # If any email found, returns false
            for user in self.cur:
                self.close_cursor()
                return False

            self.close_cursor()
            return True

        def phone():
            """Function checks if phone is already in the user table
            :return: True/False
            """

            # Create cursor
            self.create_cursor()

            # SQL code
            code = "SELECT idUser FROM User WHERE phoneNumber = %s"
            param = (phone)
            self.cur.execute(code, param)

            # If any email found, returns false
            for user in self.cur:
                self.close_cursor()
                return False

            self.close_cursor()
            return True

        # If faulty username
        if not username():
            return False, 'username'

        # If faulty email
        if not email():
            return False, 'email'

        # If faulty phone
        if not phone():
            return False, 'phone'

        # If working
        return True, 'working'

    def delete_existing_user(self, id):
        """
        Method: Deletes existing user with the given id.
        :param id: idUporabnik
        :return: True/False if successful or not.
        """
        # Create cursor
        self.create_cursor()

        # Delete user by id
        code = "DELETE FROM User WHERE idUser = %s"
        param = (id,)
        self.cur.execute(code, param)

        # Commit
        self.commit()

        # Close cursor
        self.close_cursor()

    def get_user_by_username(self, username):
        """
        Function checks if user exists, returns True and the users data in a dict.
        :return: Touple (True/False if user exists, {'userId': ,'username': ,'password': ,'email': ,'phone': })
        """
        # Create cursor
        self.create_cursor()

        # Search in database
        code = "SELECT * FROM user WHERE username = %s"
        param = (username,)
        self.cur.execute(code, param)
        # Should only be one username in database
        for user in self.cur:
            id_user = user['idUser']
            password = user['password']
            email = user['email']
            phone = user['phoneNumber']
            liked = json.loads(user['liked'])
            watched = json.loads(user['watched'])

        self.close_cursor()

        data = {'idUser': id_user,
                'username': username,
                'password': password,
                'email': email,
                'phone': phone,
                'liked': liked,
                'watched': watched}

        return True, data

    def get_user_by_id(self, id):
        """Function checks if user exists, returns True and the users data in a dict.
        :return: Touple (True/False if user exists, {'userId': ,'username': ,'email': ,'phone': , 'liked': JSON, 'watched' JSON})
        """
        
        # Create cursor
        self.create_cursor()

        # SQL code
        code = "SELECT * FROM user WHERE idUser = %s"
        param = (id,)
        self.cur.execute(code, param)
        
        # Should only be one username in database
        # Saves user in a dict
        for user in self.cur:
            id_user = user['idUser']
            username = user['username']
            password = user['password']
            email = user['email']
            phone = user['phoneNumber']
            liked = json.loads(user['liked'])
            watched = json.loads(user['watched'])
            self.close_cursor()
            data = {'idUser': id_user,
                    'username': username,
                    'password': password,
                    'email': email,
                    'phone': phone,
                    'liked': liked,
                    'watched': watched}
            
            return True, data
        return False, {}

    def save_watched_to_user(self, username, watched):
        """
        Function saves liked and watched jsons to user in database
        :param username: the id of the user
        :return: True/False if successful
        """
        # Create cursor
        self.create_cursor()

        # Create watched json string
        watched_json = json.dumps(watched)

        # Search in database
        code = "UPDATE user SET watched = %s WHERE username = %s"
        param = (watched_json, username)
        try:
            self.cur.execute(code, param)
            self.commit()
            self.close_cursor()
            return True
        except:
            return False

    def save_liked_to_user(self, username, liked):
        """
        Function saves liked and watched jsons to user in database
        :param username: the id of the user
        :return: True/False if successful
        """
        # Create cursor
        self.create_cursor()

        # Create liked json string
        liked_json = json.dumps(liked)

        # Search in database
        code = "UPDATE user SET liked = %s WHERE username = %s"
        param = (liked_json, username)
        try:
            self.execute(code, param)
            self.commit()
            self.close_cursor()
            return True
        except:
            return False

    def save_opinion_of_movie(self, username, idMovie, opinion, rate):
        """
        Function saves given opinion about the movie to the user opinion table
        :param username: users username
        :param idMovie: id of movie
        :param opinion: str("Luka suvcks balizz")
        :return: True/False if successful
        """
        try:
            opinion_check,rating_check = self.get_all_opinions_of_user(username)
            if opinion_check == {} and rating_check == {}:
                ver, user = self.get_user_by_username(username)
                # Create cursor
                self.create_cursor()
                code = "INSERT INTO opinion(idUser, idMovie, opinion, ocena) VALUES (%s, %s, %s, %s)"
                param = (user['idUser'], idMovie, opinion, rate)
                # Execute the code
                self.execute(code, param)
                # Commit to database
                self.commit()
                # Close cursor
                self.close_cursor()
            else:
                ver, user = self.get_user_by_username(username)
                # Create cursor
                self.create_cursor()
                code = "UPDATE opinion SET opinion = %s, ocena = %s WHERE idUser = %s AND idMovie = %s"
                param = (opinion, rate, user['idUser'], idMovie)
                # Execute the code
                self.execute(code, param)
                # Commit to database
                self.commit()
                # Close cursor
                self.close_cursor()                
        except:
            return False
        return True

    def get_all_opinions_of_user(self, username):
        """
        Function returns a data list of movie ids and opinions the user has saved
        :param username: users username
        :return: {'literally id of movie': 'opinion', 'ex. tt123456': 'I very liked this movie', ...}
        """
        data = {}
        data2 = {}
        self.create_cursor()
        code = "SELECT opinion.idMovie,opinion.opinion, opinion.ocena FROM opinion JOIN user ON opinion.idUser = user.idUser WHERE user.username = %s"
        param = (username,)
        # Execute the code
        self.cur.execute(code, param)

        for opinion in self.cur:
            print(opinion)
            data[opinion['idMovie']] = opinion['opinion']
            data2[opinion['idMovie']] = opinion['ocena']
                    
        self.close_cursor()
        print(data)
        return data, data2


class MovieDatabase(Connector):

    def search_by_keyword(self, keyword):
        """Function gets a keyword that was typed in the search box, returns all the results.
        Search by keyword on main page
        :param keyword: string
        :return: int(number_of_matches), sorted(list[dict("movieId": , "title": , "year": , ...)]),
        """
        
        # Lists for saving data
        movies_data = []
        writers_and_directors_data = []
        
        # Add % for keyword search
        keyword = '%' + keyword + '%'
        
        # Create cursor
        self.create_cursor()

        # SQL code
        code = "SELECT * FROM movie WHERE title LIKE %s ORDER BY (numVotes) DESC"
        param = (keyword,)
        self.cur.execute(code, param)

        # Save all of the data for movies
        for movie in self.cur:
            idMovie = movie['idMovie']
            title = movie['title']
            isAdult = movie['isAdult']
            releaseYear = movie['releaseYear']
            runtimeMinutes = movie['runtimeMinutes']
            rating = movie['rating']
            numVotes = movie['numVotes']

            movies_dict = {'idMovie': idMovie,
                           'title': title,
                           'isAdult': isAdult,
                           'releaseYear': releaseYear,
                           'runtimeMinutes': runtimeMinutes,
                           'rating': rating,
                           'numVotes': numVotes}
            movies_data.append(movies_dict)
            
        self.close_cursor()

        # Saves number of matches
        number_of_matches = len(movies_data)

        return number_of_matches, movies_data

    def random_new_movies(self):
        """
        Function returns a dict containing a list of 5 random movies.
        :return: dict("movies": sorted(list["movieId": , ...]))
        """
        
        # List to save the movie data in
        movies_data = []
        
        # Create cursor
        self.create_cursor()

        # SQL code
        code = "SELECT * FROM movie ORDER BY RAND() LIMIT 5"
        self.cur.execute(code)

        # Save all of the data for movies
        for movie in self.cur:
            idMovie = movie['idMovie']
            title = movie['title']
            isAdult = movie['isAdult']
            releaseYear = movie['releaseYear']
            runtimeMinutes = movie['runtimeMinutes']
            rating = movie['rating']
            numVotes = movie['numVotes']

            img_url = get_google_image_link(title + " " + str(releaseYear))
            movies_dict = {'idMovie': idMovie, 'title': title, 'isAdult': isAdult, 'releaseYear': releaseYear, 'runtimeMinutes': runtimeMinutes, 'rating': rating, 'numVotes': numVotes, 'img_url': img_url}
            movies_data.append(movies_dict)

        self.close_cursor()
        return {"movies": movies_data}

    def search_movie_by_id(self, id):
        """Function: Returns a movies list containing movie dicts, also has genres
        :param id: idMovie
        :return: list[dict('idMovie': , 'title': , ...)]
        """
        
        def search_all_genres_for_movie(mov_id):
            """Function: Returns a genre list for movie id
            :param id: idMovie
            :return: list[dict('idMovie': , 'title': , ...)]
            """

            # Saves all genres
            genres_data = []

            # Creates cursor
            self.create_cursor()
    
            # SQL code
            code = "SELECT genreName FROM Genre JOIN GenresByMovie ON Genre.idGenre = GenresByMovie.idGenre JOIN GenresByMovie ON Movie.idMovie = GenresByMovie.idMovie  WHERE Movie.title = %s"
            param = (mov_id,)
            self.cur.execute(code, param)

            # Saves genres
            for genre in self.cur:
                genres_data.append(genre['genreName'])
                
            return genres_data
            
        # List to save the movie data in, should only be one
        movies_data = []
        
        # Create cursor
        self.create_cursor()
        # SQL code
        code = "SELECT * FROM movie WHERE idMovie = %s"
        param = (id,)
        self.cur.execute(code, param)

        # Save all of the data for movies, should only be one
        for movie in self.cur:
            idMovie = movie['idMovie']
            title = movie['title']
            isAdult = movie['isAdult']
            releaseYear = movie['releaseYear']
            runtimeMinutes = movie['runtimeMinutes']
            rating = movie['rating']
            numVotes = movie['numVotes']

            # genre = search_all_genres_for_movie(idMovie)
            img_url = get_google_image_link(title + " " + str(releaseYear))
            additional_data = get_movie_details(id)

            movies_dict = {'idMovie': idMovie,
                           'title': title,
                           'isAdult': isAdult,
                           'releaseYear': releaseYear,
                           'runtimeMinutes': runtimeMinutes,
                           'rating': rating,
                           'numVotes': numVotes,
                           'img_url': img_url,
                           'description': additional_data['description']}
                          #  'genre': genre}
            movies_data.append(movies_dict)

        return movies_data

    def get_movie_by_param(self, parameters, rand=False):
        """Function: Returns a movies list containing movie dicts
        :parameters: dict('release_year': dict('from': , 'to': ),
                            'genre': str(),
                            'duration': dict('from': , 'to': ),
                            'directed_by': str(),
                            'number_of_votes': dict('from': , 'to': ),
                            'rating': dict('from': , 'to': ))
        :return: list[dict("movieId": , "title": , "year": , ...)]
        """

        def get_all_movie_by_idstring(id_string):
            """Function: Returns a movies list based on idMovie.
            :parameters: str('idMovie1','idMovie2', ...)
            :return: list[dict("movieId": , "title": , "year": , ...)]
            """

            # For saving movies
            data = []

            # Create cursor
            self.create_cursor()

            # SQL code
            code = "SELECT * FROM movie WHERE idMovie IN (" + id_string + ")"
            self.execute(code, None)

            # Saves all movies in a list
            for movie in self.cur:
                idMovie = movie['idMovie']
                title = movie['title']
                isAdult = movie['isAdult']
                releaseYear = movie['releaseYear']
                runtimeMinutes = movie['runtimeMinutes']
                rating = movie['rating']
                numVotes = movie['numVotes']

                # Gets movie image
                """img_url = get_google_image_link(title + " " + str(releaseYear))
                additional_data = get_movie_details(id)"""

                movies_dict = {'idMovie': idMovie,
                               'title': title,
                               'isAdult': isAdult,
                               'releaseYear': releaseYear,
                               'runtimeMinutes': runtimeMinutes,
                               'rating': rating,
                               'numVotes': numVotes}
                data.append(movies_dict)

            return data

        def get_all_movie_by_idstring_rand(id_string):
            """Function: Returns a 3 random movies list based on idMovie.
            :parameters: str('idMovie1','idMovie2', ...)
            :return: list[dict("movieId": , "title": , "year": , ...)]
            """

            # For saving movies
            data = []

            # Create cursor
            self.create_cursor()

            # SQL code
            code = "SELECT * FROM movie WHERE idMovie IN (" + id_string + ") ORDER BY RAND() LIMIT 3"
            self.execute(code, None)

            # Saves all movies in a list
            for movie in self.cur:
                idMovie = movie['idMovie']
                title = movie['title']
                isAdult = movie['isAdult']
                releaseYear = movie['releaseYear']
                runtimeMinutes = movie['runtimeMinutes']
                rating = movie['rating']
                numVotes = movie['numVotes']

                """img_url = get_google_image_link(title + " " + str(releaseYear))
                additional_data = get_movie_details(id)"""

                movies_dict = {'idMovie': idMovie,
                               'title': title,
                               'isAdult': isAdult,
                               'releaseYear': releaseYear,
                               'runtimeMinutes': runtimeMinutes,
                               'rating': rating,
                               'numVotes': numVotes}
                data.append(movies_dict)

            return data

        def get_all_movie_ids():
            """Function: Returns idMovie for all movies in the database, is used for interjection
            :parameters: None
            :return: dict(idMovie1: None, ... )
            """

            # Dict to save the movie data in based on id, used for interjection / should use set()
            movies_ids_tmp = {}

            # Create cursor
            self.create_cursor()

            # SQL code
            code = "SELECT idMovie FROM movie"
            param = (None)
            self.cur.execute(code, param)

            # Saves all idMovie for movies
            for movie in self.cur:
                idMovie = movie['idMovie']
                movies_ids_tmp[idMovie] = None

            return movies_ids_tmp

        def get_movieid_by_genre(genres_str):
            """Function: Returns idMovie for all movies in selected genres
            :parameters: str('Romance','Horror',...)
            :return: dict(idMovie1: None, ... )
            """

            # Dict to save the movie data in based on id, used for interjection / should use set()
            genre_movies_ids_tmp = {}

            # Create cursor
            self.create_cursor()

            # SQL code
            code = "SELECT movie.idMovie FROM movie JOIN genresbymovie ON genresbymovie.idMovie = movie.idMovie JOIN genre ON genresbymovie.idGenre = genre.idGenre WHERE genre.genreName IN (" + genres_str + ")"
            self.cur.execute(code, None)

            # Saves all idMovie for movies
            for movie in self.cur:
                idMovie = movie['idMovie']
                genre_movies_ids_tmp[idMovie] = None

            return genre_movies_ids_tmp

        def get_movieid_by_director(name):
            """Function: Returns idMovie for all movies directed by a one person
            :parameters: Directors name
            :return: dict(idMovie1: None, ... )
            """

            # Dict to save the movie data in based on id, used for interjection / should use set()
            director_movies_ids_tmp = {}

            # Create cursor
            self.create_cursor()

            # SQL code
            code = "SELECT movie.* FROM movie JOIN team ON team.idMovie = movie.idMovie JOIN writersanddirectors ON team.idWritersAndDirectors = writersanddirectors.idWritersAndDirectors WHERE writersanddirectors.name = %s"
            param = (name,)
            self.cur.execute(code, param)

            # Saves all idMovie for movies
            for movie in self.cur:
                idMovie = movie['idMovie']
                director_movies_ids_tmp[idMovie] = None

            return director_movies_ids_tmp

        def get_movieid_by_all_else(code, param):
            """Function: Returns idMovie for all movies fitting from,to parameters
            :parameters: code = str(SQL code), param = tuple(int('from this year'),int('to this year'),...)
            :return: dict(idMovie1: None, ... )
            """

            # Dict to save the movie data in based on id, used for interjection / should use set()
            other_movies_ids_tmp = {}

            # Create cursor
            self.create_cursor()

            # Executes cursor, code is provided in params
            self.cur.execute(code, param)

            # Saves all idMovie for movies
            for movie in self.cur:
                idMovie = movie['idMovie']
                other_movies_ids_tmp[idMovie] = None

            return other_movies_ids_tmp

        def join_all_return_ids(directors_ids, genres_ids, other_ids):
            """Function: Returns a list of idMovie for searched parameters
            :parameters: directors_ids is a dictionary of idMovie for director searched
                            genres_ids is a dictionary of idMovie for genres searched
                            other_ids is a dictionary of idMovie for other parameters
            :return: list(idMovie1,...)
            """

            # List to save all final parsed idMovie
            movie_ids = []

            # Makes an intersection
            common_ids = directors_ids.keys() & genres_ids.keys() & other_ids.keys()

            # Saves all idMovie in a list
            for id in common_ids:
                movie_ids.append(id)

            return movie_ids

        def call(parameters, rand):
            """Function: calls stuff does stuff makes stuff we need
            :parameters: parameters = dict('release_year': dict('from': , 'to': ),
                            'genre': str(),
                            'duration': dict('from': , 'to': ),
                            'directed_by': str(),
                            'number_of_votes': dict('from': , 'to': ),
                            'rating': dict('from': , 'to': ))
                        rand = True/False
            :return: list[dict("movieId": , "title": , "year": , ...)]
            """

            # List for saving all dicts with idMovie
            join_this = []

            # SQL code used for searching movies based on integer parameters
            code = 'SELECT idMovie FROM movie WHERE'

            # Saves from and to parameters
            param = []

            # Check if any integer parameters were given
            i_did_it = False

            # Saves idMovie for all parameters, will be used for intersection
            other_ids = {}
            genres_ids = {}
            directors_ids = {}

            # Prepares code if release year parameter was given
            if 'release_year' in parameters.keys():

                # Adds a condition line to the SQL code
                code += ' releaseYear > %s AND releaseYear < %s AND'

                # Saves parameters
                param.append(parameters['release_year']['from'])
                param.append(parameters['release_year']['to'])

                # Integer parameters were given
                i_did_it = True

            # Prepares code if duration parameter was given
            if 'duration' in parameters.keys():

                # Adds a condition line to the SQL code
                code += ' runtimeMinutes > %s AND runtimeMinutes < %s AND'

                # Saves parameters
                param.append(parameters['duration']['from'])
                param.append(parameters['duration']['to'])

                # Integer parameters were given
                i_did_it = True

            # Prepares code if number of votes parameter was given
            if 'number_of_votes' in parameters.keys():

                # Adds a condition line to the SQL code
                code += ' numVotes > %s AND numVotes < %s AND'

                # Saves parameters
                param.append(parameters['number_of_votes']['from'])
                param.append(parameters['number_of_votes']['to'])

                # Integer parameters were given
                i_did_it = True

            # Prepares code if rating parameter was given
            if 'rating' in parameters.keys():

                # Adds a condition line to the SQL code
                code += ' rating > %s AND rating < %s AND'

                # Saves parameters
                param.append(parameters['rating']['from'])
                param.append(parameters['rating']['to'])

                # Integer parameters were given
                i_did_it = True

            # If integer parameters were given, finds all idMovie for those
            if i_did_it:

                # Adds 1 to the end of code
                # Code end now looks like:  SELECT ... WHERE case1 AND case2 ... AND 1
                code += ' 1'

                # Saves all idMovie for integer parameters
                other_ids = get_movieid_by_all_else(code, tuple(param))

                # If none were found -> no movie fits the parameters given
                if other_ids == {}:
                    return {}

            # If genre parameters is geven, finds all idMovie for those
            if 'genre' in parameters.keys():

                # Saves string for genres, will be SQL parameter
                genre_str = ''

                i = 0
                # Creates genre string used for code, string described in function parameters
                for some_genre in parameters['genre']:
                    if i == 0:
                        genre_str += "'" + some_genre + "'"
                        i = 1
                    else:
                        genre_str = genre_str + ",'" + some_genre + "'"

                # Saves all idMovie for given genres
                genres_ids = get_movieid_by_genre(genre_str)

                # If none were found -> no movie fits the parameters given
                if genres_ids == {}:
                    return {}
            # If director parameter is geven, finds all idMovie for those
            if 'directed_by' in parameters.keys():

                # Saves all idMovie for given genres
                directors_ids = get_movieid_by_director(parameters['directed_by'])

                # If none were found -> no movie fits the parameters given
                if directors_ids == {}:
                    return {}

            # Checks if user didnt select some parameters
            join_this.append(other_ids)
            join_this.append(directors_ids)
            join_this.append(genres_ids)
            if {} in join_this:

                # Saves all movie ids, runs only if user did not specify some parameters
                all_ids = get_all_movie_ids()

                # Fills empty dicts with idMovie for all movies
                # used for intersection
                if directors_ids == {}:
                    directors_ids = all_ids
                if genres_ids == {}:
                    genres_ids = all_ids
                if other_ids == {}:
                    other_ids = all_ids

            # Saves joined idMovie
            mov_ids = join_all_return_ids(directors_ids, genres_ids, other_ids)

            # Saves string for the ids, used for SQL code
            string_of_ids = ''

            # Creates string for ids, used for SQL code
            i = 0
            for id in mov_ids:
                if i == 0:
                    string_of_ids += "'" + id + "'"
                    i = 1
                else:
                    string_of_ids = string_of_ids + ",'" + id + "'"

            # If random is True, saves random movies based on parameters,
            # otherwise, save all movies based on parameters.
            if rand:
                final_squad = get_all_movie_by_idstring_rand(string_of_ids)
            else:
                final_squad = get_all_movie_by_idstring(string_of_ids)

            # Returns a movies dict
            return final_squad

        # Return the call
        return call(parameters, rand)


    def search_movie_by_multiple_ids(self, id_list):
        """
        Function: Returns a movies list containing movie dicts. of the ids in the id_list
        :param id: list containing movie ids
        :return: list[dict('idMovie': , 'title': , ...)]
        """
        
        # List to save the movie data in
        movies_data = []

        # For each id
        for id in id_list:
            
            # Create cursor
            self.create_cursor()
            code = "SELECT * FROM movie WHERE idMovie = %s"
            param = (id,)
            self.cur.execute(code, param)

            # Save all of the data for movies, one at a time
            for movie in self.cur:
                idMovie = movie['idMovie']
                title = movie['title']
                isAdult = movie['isAdult']
                releaseYear = movie['releaseYear']
                runtimeMinutes = movie['runtimeMinutes']
                rating = movie['rating']
                numVotes = movie['numVotes']

                img_url = get_google_image_link(title + " " + str(releaseYear))
                additional_data = get_movie_details(id)

                movies_dict = {'idMovie': idMovie,
                               'title': title,
                               'isAdult': isAdult,
                               'releaseYear': releaseYear,
                               'runtimeMinutes': runtimeMinutes,
                               'rating': rating,
                               'numVotes': numVotes,
                               'img_url': img_url,
                               'description': additional_data['description']}
                movies_data.append(movies_dict)

        return movies_data
        

if __name__ == "__main__":
    # For testing
    mdb = MovieDatabase()
    udb = UserDataBase()
    opinion = udb.get_all_opinions_of_user("test3")
    """print(mdb.random_new_movies())"""
    """param = {'release_year': {'from': 1990, 'to': 2020},
             'genre': 'Romance',
             'duration': {'from': 60, 'to': 120},
             'directed_by': "0",
             'number_of_votes': {'from': 200, 'to': 10000},
             'rating': {'from': 8, 'to': 10}}
    print(mdb.get_movie_by_param(param))"""
    pass
