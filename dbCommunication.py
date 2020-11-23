import mysql.connector


class Connector:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="generator-filmov-1.cay847edpwb1.us-east-2.rds.amazonaws.com",
            user="admin",
            passwd="predmetpb1jezakon",
            database="generator-filmov",
            )
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
            code = "INSERT INTO Uporabnik(uorabniskoIme, geslo, email) VALUES (%s, %s, %s)"
            param = (username, password, email)

        elif email is None and phone is not None:
            code = "INSERT INTO Uporabnik(uorabniskoIme, geslo, tel) VALUES (%s, %s, %s)"
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

        code = "DELETE FROM Uporabnik WHERE idUporabnik = %s"
        param = (id,)
        self.cur.execute(code, param)

        # Commit
        self.commit()

        # Close cursor
        self.close_cursor()


if __name__=="__main__":
    # For testing
    pass
