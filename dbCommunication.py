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
        """ Todo
        Function checks if username, email, phone are already in the user table
        :param username: users username
        :param email: users email
        :param phone: users phone
        :return: True/False, working/if problem -> where
        """
        def username():
            
            # Create cursor
            self.create_cursor()
            code = "SELECT idUser FROM User WHERE username = %s"
            param = (username)
            self.cur.execute(code, param)
            for user in self.cur:
                self.close_cursor()
                return False
            
            self.close_cursor()
            return True
        
        def email():
            
            # Create cursor
            self.create_cursor()
            code = "SELECT idUser FROM User WHERE email = %s"
            param = (email)
            self.cur.execute(code, param)
            for user in self.cur:
                self.close_cursor()
                return False
            
            self.close_cursor()
            return True
        
        def phone():
            
            # Create cursor
            self.create_cursor()
            code = "SELECT idUser FROM User WHERE phoneNumber = %s"
            param = (phone)
            self.cur.execute(code, param)
            for user in self.cur:
                self.close_cursor()
                return False
            
            self.close_cursor()
            return True
        
        if not username():
            return False, 'username'
        
        if not email():
            return False, 'email'

        if not phone():
            return False, 'phone'

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
        """ TODO
        Function checks if user exists, returns True and the users data in a dict.
        :return: Touple (True/False if user exists, {'userId': ,'username': ,'email': ,'phone': , 'liked': JSON, 'watched' JSON})
        """
        # Create cursor
        self.create_cursor()

        # Search in database
        code = "SELECT * FROM user WHERE idUser = %s"
        param = (id,)
        self.cur.execute(code, param)
        # Should only be one username in database
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

    def save_opinion_of_movie(self, username, idMovie, opinion):
        """
        Function saves given opinion about the movie to the user opinion table
        :param username: users username
        :param idMovie: id of movie
        :param opinion: str("Luka suvcks balizz")
        :return: True/False if successful
        """
        try:
            # Create cursor
            self.create_cursor()
            code = "INSERT INTO opinion(idUser, idMovie, opinion) VALUES (%s, %s, %s )"
            param = (self.get_user_by_username(username)[1]['idUser'], idMovie, opinion)
            # Execute the code
            self.cur.execute(code, param)
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
        self.create_cursor()
        code = "SELECT opinion.idMovie,opinion.opinion FROM opinion JOIN user ON opinion.idUser = user.idUser WHERE user.username = %s"
        param = (username,)
        # Execute the code
        self.cur.execute(code, param)

        for opinion in self.cur:
            data[opinion['idMovie']] = opinion['opinion']
                    
        self.close_cursor()
        return data


class MovieDatabase(Connector):

    def search_by_keyword(self, keyword):
        """ ONLY MOVIE NAMES
        Function gets a keyword that was typed in the search box, returns all the results.
        Search by keyword on main page(could be actor, movie, genre...)
        :param keyword: string
        :return: int(number_of_matches), dict("movies": sorted(list[dict("movieId": , "title": , "year": , ...)]),
                                              "directors": sorted(list[dict("actorId": , "age": , ...))])
        List should be sorted decreasing by number of votes for movies, decreasing by number of roles for actor
        """
        # we only have directors / writers
        # Finished, check returns and comments

        # Lists for saving data
        movies_data = []
        writers_and_directors_data = []
        # Add % for keyword search
        keyword = '%' + keyword + '%'
        # Create cursor for movies
        self.create_cursor()

        # Search in movie database
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
        Function returns a dict containing a sorted list of 5 random new-er movies.
        :return: dict("movies": sorted(list["movieId": , ...]))
        Newer movies have a higher chance of being selected, so the random returned dict should be mostly movies
        made between 2010 - 2020, with a small chance of older movies. //
        Sorted by number of votes.
        """
        # List to save the movie data in
        movies_data = []
        # Create cursor
        self.create_cursor()
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
        """ TODO add genres of movie
        Function: Returns a movies list containing movie dicts. of the id
        :param id: idMovie
        :return: list[dict('idMovie': , 'title': , ...)]
        """
        def search_all_genres_for_movie(mov_id):
            genres_data = []
            self.create_cursor()

            
            code = "SELECT genreName FROM Genre JOIN Genre ON Genre.idGenre = GenresByMovie.idGenre JOIN GenresByMovie ON Movie.idMovie = GenresByMovie.idMovie  WHERE Movie.title = %s"
            param = (mov_id,)
            self.cur.execute(code, param)
            for genre in self.cur:
                genres_data.append(genre['genreName'])
            return genres_data
            
        # List to save the movie data in
        movies_data = []
        # Create cursor
        self.create_cursor()
        # TODO add genre
        code = "SELECT * FROM movie WHERE idMovie = %s"
        param = (id,)
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
            # todo add genre

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
                           'genre': search_all_genres_for_movie(idMovie)
            movies_data.append(movies_dict)

        return movies_data

    def get_movie_by_param(self, parameters, rand=False):
        """ todo Function that returns movie/director data based on search inputs saved in dict param
            todo should add: If key not in param, user did not select that
        :param param: dict('release_year': dict('from': , 'to': ),
                            'genre': str(),
                            'duration': dict('from': , 'to': ),
                            'directed_by': str(),
                            'number_of_votes': dict('from': , 'to': ),
                            'rating': dict('from': , 'to': ))
                if from/to == -1, do all
        :return: the same
        """
        print(rand)

        def get_all_movie_by_idstring(id_string):
            """Searches movies"""
            data = []
            # Create cursor
            self.create_cursor()
            code = "SELECT * FROM movie WHERE idMovie IN (" + id_string + ")"
            self.execute(code, None)
            print(self.cur)
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

            print("data", data)
            return data

        def get_all_movie_by_idstring_rand(id_string):
            """Searches movies"""
            print("Malora")
            data = []
            # Create cursor
            self.create_cursor()
            code = "SELECT * FROM movie WHERE idMovie IN (" + id_string + ") ORDER BY RAND() LIMIT 3"
            self.execute(code, None)
            print(self.cur)
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

            print("data", data)
            return data
        
        def get_all_movie_ids():
            """Searches movies"""

            # List to save the movie data in based on id, used for interjection
            movies_ids_tmp = {}
            # Create cursor
            self.create_cursor()
            code = "SELECT idMovie FROM movie"
            param = (None)
            self.cur.execute(code, param)

            # Save all of the data for movies
            for movie in self.cur:
                idMovie = movie['idMovie']
                movies_ids_tmp[idMovie] = None

            # print("movie_ids_tmp", movies_ids_tmp)
            print("Im here")
            return movies_ids_tmp

        def get_movieid_by_genre(genres_str):
            '''Searches movies by genres'''

            # List to save the movie data in based on id, used for interjection
            genre_movies_ids_tmp = {}
            # Create cursor
            self.create_cursor()
            code = "SELECT movie.idMovie FROM movie JOIN genresbymovie ON genresbymovie.idMovie = movie.idMovie JOIN genre ON genresbymovie.idGenre = genre.idGenre WHERE genre.genreName IN ("+ genres_str + ")"
            self.cur.execute(code, None)

            # Save all of the data for movies
            for movie in self.cur:
                idMovie = movie['idMovie']
                genre_movies_ids_tmp[idMovie] = None

            print("genre_movies_ids_tmp", genre_movies_ids_tmp)
            return genre_movies_ids_tmp
        
        def get_movieid_by_director(name):
            '''Searches movies by director'''

            # List to save the movie data in based on id, used for interjection
            director_movies_ids_tmp = {}
            # Create cursor
            self.create_cursor()
            code = "SELECT movie.* FROM movie JOIN team ON team.idMovie = movie.idMovie JOIN writersanddirectors ON team.idWritersAndDirectors = writersanddirectors.idWritersAndDirectors WHERE writersanddirectors.name = %s"
            param = (name,)
            self.cur.execute(code, param)

            # Save all of the data for movies
            for movie in self.cur:
                idMovie = movie['idMovie']
                director_movies_ids_tmp[idMovie] = None

            print("director_movies_ids_tmp", director_movies_ids_tmp)
            return director_movies_ids_tmp

        def get_movieid_by_all_else(code, param):
            
            other_movies_ids_tmp = {}
            # Create cursor
            self.create_cursor()
            self.cur.execute(code, param)

            # Save all of the data for movies
            for movie in self.cur:
                idMovie = movie['idMovie']
                other_movies_ids_tmp[idMovie] = None

            print("other_movies_ids_tmp", other_movies_ids_tmp)
            return other_movies_ids_tmp

        def join_all_return_ids(directors_ids,genres_ids,other_ids):

            movie_ids = []
            common_ids = directors_ids.keys() & genres_ids.keys() & other_ids.keys()
            for id in common_ids:
                movie_ids.append(id)

            print("movie_ids", movie_ids)
            return movie_ids

        def call(parameters, rand):
            """ calls stuff does stuff makes stuff we need """
            
            join_this = []
            code = 'SELECT idMovie FROM movie WHERE'
            param = []
            i_did_it = False
            other_ids = {}
            genres_ids = {}
            directors_ids = {}
            if 'release_year' in parameters.keys():
                code += ' releaseYear > %s AND releaseYear < %s AND'
                param.append(parameters['release_year']['from'])
                param.append(parameters['release_year']['to'])
                i_did_it = True

            if 'duration' in parameters.keys():
                code += ' runtimeMinutes > %s AND runtimeMinutes < %s AND'
                param.append(parameters['duration']['from'])
                param.append(parameters['duration']['to'])
                i_did_it = True

            if 'number_of_votes' in parameters.keys():
                code += ' numVotes > %s AND numVotes < %s AND'
                param.append(parameters['number_of_votes']['from'])
                param.append(parameters['number_of_votes']['to'])
                i_did_it = True
                
            if 'rating' in parameters.keys():
                code += ' rating > %s AND rating < %s AND'
                param.append(parameters['rating']['from'])
                param.append(parameters['rating']['to'])
                i_did_it = True
                
            if i_did_it:
                code += ' 1'
                other_ids = get_movieid_by_all_else(code, tuple(param))
                if other_ids == {}:
                    return {}
                
            if 'genre' in parameters.keys():
                genre_str = ''
                i = 0
                for some_genre in parameters['genre']:
                    if i == 0:
                        genre_str += "'" + some_genre + "'"
                        i = 1
                    else:
                        genre_str = genre_str + ",'" + some_genre + "'"  
                genres_ids = get_movieid_by_genre(genre_str)
                
                if genres_ids == {}:
                    return {}
                
            if 'directed_by' in parameters.keys():
                directors_ids = get_movieid_by_director(parameters['directed_by'])
                if directors_ids == {}:
                    return {}
                
            join_this.append(other_ids)
            join_this.append(directors_ids)
            join_this.append(genres_ids)

            if {} in join_this:
                all_ids = get_all_movie_ids()
                
            if directors_ids == {}:
                directors_ids = all_ids
                
            if genres_ids == {}:
                genres_ids = all_ids
                
            if other_ids == {}:
                other_ids = all_ids
                
            mov_ids = join_all_return_ids(directors_ids, genres_ids, other_ids)
            string_of_ids = ''
            i = 0
            for id in mov_ids:
                if i == 0:
                    string_of_ids += "'" + id + "'"
                    i = 1
                else:
                    string_of_ids = string_of_ids + ",'" + id + "'"

            print(rand)
            if rand:
                final_squad = get_all_movie_by_idstring_rand(string_of_ids)
            else:
                final_squad = get_all_movie_by_idstring(string_of_ids)
                
            return final_squad
      
        return call(parameters, rand)

    def get_movie_by_param_randomized(self, param):
        """ todo Function that returns one movie based on param, randomized from all the movies that fit param measures
            todo call get_movie_by_param(self, param):
            todo should add: If key not in param, user did not select that
        :param param: dict('release_year': dict('from': , 'to': ),
                            'genre': str(),
                            'duration': dict('from': , 'to': ),
                            'directed_by': str(),
                            'number_of_votes': dict('from': , 'to': ),
                            'rating': dict('from': , 'to': ))
                if from/to == -1, do all
        :return: the same
        """
        pass

    def search_movie_by_multiple_ids(self, id_list):
        """
        Function: Returns a movies list containing movie dicts. of the ids in the id_list
        :param id: list containing movie ids
        :return: list[dict('idMovie': , 'title': , ...)]
        """
        # List to save the movie data in
        movies_data = []
        for id in id_list:
            # Create cursor
            self.create_cursor()
            code = "SELECT * FROM movie WHERE idMovie = %s"
            param = (id,)
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
    """print(mdb.random_new_movies())"""
    param = {'release_year': {'from': 1990, 'to': 2020},
             'genre': 'Romance',
             'duration': {'from': 60, 'to': 120},
             'directed_by': "0",
             'number_of_votes': {'from': 200, 'to': 10000},
             'rating': {'from': 8, 'to': 10}}
    print(mdb.get_movie_by_param(param))
    pass
