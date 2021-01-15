import csv
import mysql.connector


def movies_basics():
    # 1st to be run
    print('im in movies')
    tsv_file = open("title.basics.end.tsv",encoding = 'utf8')
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    genres = {}
    count = 1
    ID_movie = []
    i = 0
    for row in read_tsv:
        if i == 0:
            keys = [row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
            dict_id_movies_basics = {}
        if i != 0:
            dict_movies_basics = {keys[2]: row[3],keys[3]: row[4],keys[4]: row[5],keys[6]: row[7],keys[7]: row[8].split(',')}
            dict_id_movies_basics[row[0]] = dict_movies_basics
            for x in row[8].split(','):
                if x not in genres.values() and x != '\\N':
                    genres[count] = x
                    count += 1
            # ID_movie.append(row[0])
        i+= 1

    #print(dict_id_movies_basics)
    #print(genres)
    # return [ID_movie,genres,dict_id_movies_basics]
    return [genres,dict_id_movies_basics]


def title_crew():
    print('im in crew')
    tsv_file = open("title.crew.end.tsv", encoding = "utf8")
    read_tsv = csv.reader(tsv_file,delimiter = "\t")
    potrebni_id = [] # Tega nebova rabla ko bodo podatki urejeni
    i = 0
    dict_crew = {}
    for row in read_tsv:
        if i == 0:
            keys = [row[0],row[1],row[2]]
        else:
            directors = row[1].split(',')
            writers = row[2].split(',')
            dict_crew[row[0]] = {keys[1]:directors,keys[2]:writers}
        i += 1

    return dict_crew


def title_ratings():
    print('im in ratings')
    tsv_file = open("title.ratings.end.tsv", encoding = "utf8")
    read_tsv = csv.reader(tsv_file,delimiter = "\t")
    i = 0
    dict_ratings = {}
    for row in read_tsv:
        if i == 0:
            keys = [row[0], row[1], row[2]]
        else:
            dict_ratings[row[0]] = {keys[1]: row[1], keys[2]: row[2]}
        i += 1
    return dict_ratings


def name_basics():
    print('name_basics')
    tsv_file = open("name.basics.end.tsv",encoding = "utf8")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    i = 0
    for row in read_tsv:
        if i == 0:
            keys = [row[1], row[2], row[3]]
            dict_id_name_basics = {}
        elif i != 0:
            dict_name_basics = {keys[0]: row[1],keys[1]:row[2] ,keys[2]: row[3]}
            dict_id_name_basics[row[0]] = dict_name_basics
        i+= 1
    #print(dict_id_name_basics)
    return(dict_id_name_basics)


genres_data = movies_basics()[0]
movies_data = movies_basics()[1]
title_ratings_data = title_ratings()


def final_table_genres(genres_data):
  return genres_data


def final_table_movies(title_ratings_data,movies_data,genres_data):
    print('im here')
    exceptions = 0
    keys_genres = []
    final_data_movies = {}
    final_table_movies_genres = {}
    for x in title_ratings_data:
        keys_genres = []
        try:
            final_data_movies[x] = {'originalTitle': movies_data[x]['originalTitle'],
                                    'isAdult': movies_data[x]['isAdult'],
                                    'startYear': movies_data[x]['startYear'],
                                    'runtimeMinutes': movies_data[x]['runtimeMinutes'],
                                    'averageRating': title_ratings_data[x]['averageRating'],
                                    'numVotes': title_ratings_data[x]['numVotes']}
            for key in genres_data:
                if genres_data[key] in movies_data[x]['genres']:
                    keys_genres.append(key)
            final_table_movies_genres[x] = keys_genres
        except:
            exceptions += 1
    print("There were ",exceptions, " exceptions.")
    #print(final_data_movies,final_table_movies_genres)
    return [final_data_movies, final_table_movies_genres]



tab_tmp = final_table_movies(title_ratings_data, movies_data, genres_data)
movies = tab_tmp[0]
genresByMovie = tab_tmp[1]
genres = genres_data
writersAndDirectors = name_basics()
team = title_crew()
"""print('Movies tabela: \n', movies)
print('GenresByMovie tabela: \n',genresByMovie)
print('Genres tabela: \n',genres)
print('WritersAndDirectors tabela: \n',writersAndDirectors)
print('Team tabela: \n',team)"""

##cursor = self.tb.cursor(dictionary = True)
##
##cursor.execute("insert into genres (genreName,..) VALUES (%s,%s)",(podatek1,podatek2))
##cursor.execute("insert into genres (genreName,..) VALUES (%s)",(,podatek1))


def beri_movies(movies):
    tb = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='mydb')
    for movieid in movies:
        originalTitle = movies[movieid]['originalTitle']
        isAdult = movies[movieid]['isAdult']
        startYear = movies[movieid]['startYear'] if movies[movieid]['startYear'] != '\\N' else None
        runtimeMinutes = movies[movieid]['runtimeMinutes'] if movies[movieid]['runtimeMinutes'] != '\\N' else None
        averageRating = movies[movieid]['averageRating']
        numVotes = movies[movieid]['numVotes']
        cursor = tb.cursor(dictionary=True)
        cursor.execute("insert into Movie (idMovie,title,isAdult,releaseYear,runtimeMinutes,rating,numVotes) VALUES (%s,%s,%s,%s,%s,%s,%s)",(movieid,originalTitle,isAdult,startYear,runtimeMinutes,averageRating,numVotes))
        cursor.close()
    tb.commit()


def beri_genresByMovie(genresByMovie):
    # 3rd to run
    print('Im in genresbymovie')
    tb = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='mydb')
    for movieid in genresByMovie:
        for genreid in genresByMovie[movieid]:
            cursor = tb.cursor(dictionary = True)
            cursor.execute("insert into GenresByMovie (idGenre,idMovie) VALUES (%s,%s)",(genreid,movieid))
            cursor.close()
    tb.commit()
      

def beri_genres(genres):
    # 2nd to run
    print('Im in genres')
    tb = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='mydb')
    print(genres)
    for genreid in genres:
        genreName = genres[genreid]
        # insert je tle za genreid in genreName
        cursor = tb.cursor(dictionary=True)
        cursor.execute("insert into Genre (idGenre,genreName) VALUES (%s,%s)", (genreid, genreName))
        cursor.close()
    tb.commit()


def beri_writersAndDirectors(writersAndDirectors):
    # 4th to run
    print('Im in writers')
    tb = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='mydb')
    for writersAndDirectorsID in writersAndDirectors:
        name = writersAndDirectors[writersAndDirectorsID]['primaryName']
        birthYear = writersAndDirectors[writersAndDirectorsID]['birthYear'] if writersAndDirectors[writersAndDirectorsID]['birthYear'] != '\\N' else None
        deathYear = writersAndDirectors[writersAndDirectorsID]['deathYear'] if writersAndDirectors[writersAndDirectorsID]['deathYear'] != '\\N' else None
        # insert je tle za writersAndDirectorsid in ostalo
        cursor = tb.cursor(dictionary=True)
        cursor.execute("insert into writersAndDirectors (idWritersAndDirectors,name,birthYear,deathYear) VALUES (%s,%s,%s,%s)",(writersAndDirectorsID, name, birthYear, deathYear))
        cursor.close()
    tb.commit()


def beri_team(team):
    # 5th to run
    tb = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='mydb')
    for movieID in team:
        directors = team[movieID]['directors']
        writers = team[movieID]['writers']
        for WritersAndDirectorsID in directors:
            if WritersAndDirectorsID in writers:
                writer = 1
                director = 1
            else:
                writer = 0
                director = 1
            try:
                cursor = tb.cursor(dictionary = True)
                cursor.execute("insert into team (idWritersAndDirectors,idMovie,director,writer) VALUES (%s,%s,%s,%s)",(WritersAndDirectorsID,movieID,director,writer))
                cursor.close()
            except:
                pass
        tb.commit()
        # insert je tuki za writer = bool, director = 1, movieID,writersAndDirectorsID
        for WritersAndDirectorsID in writers:
            if WritersAndDirectorsID not in directors:
                writer = 1
                director = 0
                try:
                    cursor = tb.cursor(dictionary = True)
                    cursor.execute("insert into team (idWritersAndDirectors,idMovie,director,writer) VALUES (%s,%s,%s,%s)",(WritersAndDirectorsID,movieID,director,writer))
                    cursor.close()
                except:
                    pass
        tb.commit()


if __name__ == "__main__":
    # beri_movies(movies)
    # beri_genres(genres)
    # beri_genresByMovie(genresByMovie)
    # beri_writersAndDirectors(writersAndDirectors)
    beri_team(team)
