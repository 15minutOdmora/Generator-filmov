from image_scraping import *
from dbCommunication import Connector
# SQL: UPDATE movie SET imgUrl = %s WHERE movieId = %s;


con = Connector()

con.create_cursor()
code = "SELECT idMovie, title, releaseYear FROM movie;"

con.execute(code, param=None)

data = []
for movie in con.cur:
    data.append({'id': movie['idMovie'], 'title': movie['title'], 'year': movie['releaseYear']})

con.close_cursor()
print("Done reading")

i = 0
for movie in data[::-1]:
    title = movie['title']
    year = movie['year']
    string = title + " " + str(year)
    try:
        url = get_google_image_link(string)
    except:
        i += 1
        print(i, "Failed")
        continue

    con.create_cursor()
    code = "UPDATE movie SET imgUrl = %s WHERE idMovie = %s"
    param = (url, movie['id'])
    con.execute(code, param)
    con.commit()
    con.close_cursor()
    i += 1
    print(i)
