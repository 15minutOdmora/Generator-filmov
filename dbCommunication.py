import mysql.connector
from auth import AUTH


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

        # Check if phone or email was given
        if phone is None and email is not None:
            code = "INSERT INTO User(username, password, email) VALUES (%s, %s, %s)"
            param = (username, password, email)

        elif email is None and phone is not None:
            code = "INSERT INTO User(username, password, phone) VALUES (%s, %s, %s)"
            param = (username, password, phone)

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
        code = "SELECT * FROM User WHERE username = '%s'"
        param = (username,)
        self.cur.execute(code, param)
        # Should only be one username in database
        for user in self.cur:
            id_user = user['idUser']
            password = user['password']
            email = user['email']
            phone = user['phone']

        self.close_cursor()

        return True, {'idUser': id_user, 'username': username, 'password': password, 'email': email, 'phone': phone}


class MovieDatabase(Connector):

    def search_by_keyword(self, keyword):
        """ todo Create whole function
        Function gets a keyword that was typed in the search box, returns all the results.
        Search by keyword on main page(could be actor, movie, genre...)
        :param keyword: string
        :return: int(number_of_matches), dict("movies": sorted(list[dict("movieId": , "title": , "year": , ...)]),
                                              "actor": sorted(list[dict("actorId": , "age": , ...))])
        List should be sorted decreasing by number of votes for movies, decreasing by number of roles for actor
        (num. of roles = num. of movies played in)
        number_of_matches is an integer number of all results found (movies + actors)
        """
        pass

    def random_new_movies(self):
        """ todo Create whole function
        Function returns a dict containing a sorted list of 20 random new-er movies.
        :return: dict("movies": sorted(list["movieId": , ...]))
        Newer movies have a higher chance of being selected, so the random returned dict should be mostly movies
        made between 2010 - 2020, with a small chance of older movies.
        Sorted by number of votes.
        """
        pass


if __name__=="__main__":
    # For testing
    udb = UserDataBase()
    udb.add_new_user("test", "test", "test@gmail.com", phone=None)
    pass
