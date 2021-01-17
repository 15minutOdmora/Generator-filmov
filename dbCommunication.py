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
        """ todo check if username already exists
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
            liked = user['liked']
            watched = user['watched']

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
        pass

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

class MovieDatabase(Connector):

    def search_by_keyword(self, keyword):
        """ todo popravi opis funkcije
            todo SELECT writersanddirectors.*, COUNT(team.idWritersAndDirectors) FROM writersanddirectors join team on writersanddirectors.idWritersAndDirectors = team.idWritersAndDirectors group by (writersanddirectors.name)
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

    def search_by_integer(self, integer):
        """ todo get keyword, search movies, int search by releaseYear(movies and directors)
        Function: Returns movies where search word was an integer, first search by title and then by releaseYear
        :param integer:
        :return: sorted(dict(of movies)), sorted: movies with intiger in title first, then movies by release year
        """
        pass

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
        """
        Function: Returns a movies list containing movie dicts. of the id
        :param id: idMovie
        :return: list[dict('idMovie': , 'title': , ...)]
        """
        # List to save the movie data in
        movies_data = []
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

    def get_movie_by_param(self, parameters):
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
        def get_all_movies():
            """Searches movies"""

            # List to save the movie data in based on id, used for interjection
            movies_data = {}
            # Create cursor
            self.create_cursor()
            code = "SELECT * FROM movie"
            param = (None)
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

                movies_dict = {'title': title,
                               'isAdult': isAdult,
                               'releaseYear': releaseYear,
                               'runtimeMinutes': runtimeMinutes,
                               'rating': rating,
                               'numVotes': numVotes}
                movies_data[idMovie] = movies_dict
            return movies_data

        all_movies = get_all_movies()
        print("Done get_all movies")

        def get_movie_by_genre(genre):
            '''Searches movies by genres'''

            # List to save the movie data in based on id, used for interjection
            movies_data = {}
            # Create cursor
            self.create_cursor()
            code = "SELECT movie.* FROM movie JOIN genresbymovie ON genresbymovie.idMovie = movie.idMovie JOIN genre ON genresbymovie.idGenre = genre.idGenre WHERE genre.genreName = %s"
            param = (genre,)
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

                movies_dict = {'title': title,
                               'isAdult': isAdult,
                               'releaseYear': releaseYear,
                               'runtimeMinutes': runtimeMinutes,
                               'rating': rating,
                               'numVotes': numVotes}
                movies_data[idMovie] = movies_dict

            if movies_data == {}:
                return all_movies
            return movies_data
        
        def get_movie_by_director(name):
            '''Searches movies by director'''

            # List to save the movie data in based on id, used for interjection
            movies_data = {}
            # Create cursor
            self.create_cursor()
            code = "SELECT movie.* FROM movie JOIN team ON team.idMovie = movie.idMovie JOIN writersanddirectors ON team.idWritersAndDirectors = writersanddirectors.idWritersAndDirectors WHERE writersanddirectors.name = %s"
            param = (name,)
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

                movies_dict = {'title': title,
                               'isAdult': isAdult,
                               'releaseYear': releaseYear,
                               'runtimeMinutes': runtimeMinutes,
                               'rating': rating,
                               'numVotes': numVotes}
                movies_data[idMovie] = movies_dict
            if movies_data == {}:
                return all_movies
            return movies_data

        def join_all():
             """dict('release_year': dict('from': , 'to': ),
                            'genre': str(),
                            'duration': dict('from': , 'to': ),
                            'directed_by': str(),
                            'number_of_votes': dict('from': , 'to': ),
                            'rating': dict('from': , 'to': ))"""
             data = []
             print("Done d2")
             d3 = get_movie_by_director(parameters['directed_by'])
             print("Done d3")
             d5 = get_movie_by_genre(parameters['genre'])
             print("Done d5")

            
             common_ids = d3.keys() & d5.keys()
             for mov_id in all_movies:
                 if mov_id in common_ids:
                     data.append(all_movies[mov_id])
             return data
        
        return join_all()


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
    param = {'release_year': {'from': 1990, 'to': 2000},
            'genre': "Romance",
            'duration': {'from': 50, 'to': 120},
            'directed_by': "0",
            'number_of_votes': {'from': 200, 'to': 10000},
            'rating': {'from': 6, 'to': 10}}
    print(mdb.get_movie_by_param(param))
    pass
