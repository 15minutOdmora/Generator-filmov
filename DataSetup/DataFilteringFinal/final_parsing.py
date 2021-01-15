import csv
from bisect import *


def pars_all():
    
    def find_elem_in_sorted_list(elem, sorted_list):
        """ https://docs.python.org/3/library/bisect.html
            Locate the leftmost value exactly equal to x"""
        i = bisect_left(sorted_list, elem)
        if i != len(sorted_list) and sorted_list[i] == elem:
            return True
        return False

    movie_ids = []

    def pars_ratings():
        data = []
        i = 0
        print("Reading title.ratings.final")
        with open("title.ratings.final.tsv", 'r', encoding='utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if i == 0:
                    data.append(row)
                    i = 1
                elif int(row[2]) > 100:
                    data.append(row)
                    movie_ids.append(row[0])
                    i += 1
        print("Read {} ratings that fit the parameters from title.ratings".format(i))

        print("Writing title.ratings.end")
        with open("title.ratings.end.tsv", 'w', encoding='utf8', newline='') as f:
            print('Writing title.ratings.end.tsv')
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)

        print("Writing id_mov.test")
        final = open("id_mov.test.txt", "w", encoding='utf8')
        print('Writing... id_mov.test.txt')
        for id_mov in movie_ids:
            final.write(id_mov + "\n")
        final.close()
        print("pars_ratings finished")

    def pars_movies(param=False):
        data = []
        i = 0
        if param:
            # Use if the list is not generated, aka. something went wrong.
            with open("id_mov.test.txt", 'r', encoding='utf8') as f:
                for line in f.readlines():
                    movie_ids.append(line.replace('\n', ''))

        print("Reading title.basicss")
        with open("title.basics.tsv", 'r', encoding='utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if i == 0:
                    data.append(row)
                    i = 1
                elif find_elem_in_sorted_list(row[0], movie_ids):
                    data.append(row)
                    i += 1
        print("Read {} titles that fit the parameters from title.basics".format(i))

        print("Writing title.basics.end")
        with open("title.basics.end.tsv", 'w', encoding='utf8', newline = '') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)
        print("pars_movies finished")
                  
    def pars_crew(param=False):
        data = []
        data2 = []
        i = 0

        if param:
            # Use if the list is not generated, aka. something went wrong.
            with open("id_mov.test.txt", 'r', encoding='utf8') as f:
                for line in f.readlines():
                    movie_ids.append(line.replace('\n', ''))

        print("Reading title.crew")
        with open("title.crew.tsv", 'r', encoding='utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if i == 0:
                    data.append(row)
                    i = 1
                elif find_elem_in_sorted_list(row[0], movie_ids):

                    directors = row[1]
                    writers = row[2]
                    
                    for x in writers.split(','):
                        if x not in data2:
                            data2.append(x)
                    for x in directors.split(','):
                        if x not in data2:
                            data2.append(x)
                    data.append(row)
                    i += 1
        print("Read {} title crews that fit the parameters from title.crew".format(i))
                    
        print('Sorting id_director.end')
        new_data = sorted(data2)
        
        final = open("id_director.end.txt", "w", encoding='utf8')
        print('writing id_director.end')
        for id_director in new_data:
            final.write(id_director + "\n")
        final.close()

        print('Writing title.crew.end')
        with open("title.crew.end.tsv", 'w', encoding='utf8', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)

        print("pars_crew finished")

    def pars_writersdirectors(param=False):
        data = []
        director_ids = []
        i = 0

        print("Reading id_director.end")
        with open("id_director.end.txt", 'r', encoding='utf8') as f:
            for line in f.readlines():
                director_ids.append(line.replace('\n',''))

        print("Reading name.basics")
        with open("name.basics.tsv", 'r', encoding='utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if i == 0:
                    data.append(row)
                    i = 1
                elif find_elem_in_sorted_list(row[0], director_ids):
                    data.append(row)
                    i += 1
        print("Read {} names that fit the parameters from name.basics".format(i))

        print("Writing name.basics.end")
        with open("name.basics.end.tsv", 'w',encoding='utf8', newline='') as f:
            print('writing...name.basics.end.tsv')
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)

        print("pars_writersdirectors finished")

    pars_ratings()      
    pars_movies()
    pars_crew()
    pars_writersdirectors()
    print("All finished correctly")


if __name__ == "__main__":
    pars_all()
