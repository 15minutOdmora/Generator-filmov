import mysql.connector

# Naredi database instance
db = mysql.connector.connect(
    host='localhost',
    user='',
    passwd='',
)


# Naredi cursor
cur = db.cursor()

# Execute commands
cur.execute("neki ukazi bla bla bla")

# Če vstavljaš, shraniš z
db.commit()

# Na koncu vedno končaš povezavo
db.close()


# Primeri od liama

# Branje iz databasea
# username = liam
# cur.execute("SELECT * FROM users WHERE username = '%s'".format(username))

# Vstavljanje v database
# cur.execute("INSERT INTO users(ime, username, password) VALUES (%s,%s,%s)", ("neko_ime", "nek_username", nek_password))
