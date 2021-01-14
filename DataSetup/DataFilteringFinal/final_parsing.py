import csv
from bisect import *

def pars_all():
    
    def find_elem_in_sorted_list(elem, sorted_list):
    # https://docs.python.org/3/library/bisect.html
    # 'Locate the leftmost value exactly equal to x'
        i = bisect_left(sorted_list, elem)
        if i != len(sorted_list) and sorted_list[i] == elem:
            return True
        return False

    
    movie_ids = []
    def pars_ratings():
        data = []
        i = 0
        with open("title.ratings.tsv",'r',encoding = 'utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if i == 0:
                    data.append(row)
                    i = 1
                elif int(row[2]) > 100:
                    data.append(row)
                    movie_ids.append(row[0])
                    i += 1
                    print(i)
                
                  
        with open("title.ratings.end.tsv",'w',encoding = 'utf8',newline = '') as f:
            print('writing')
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)
            
        final = open("id_mov.test.txt", "w", encoding='utf8')
        print('writing ids')
        for id_mov in movie_ids:
            final.write(id_mov + "\n")
        final.close()
        

    def pars_movies():
        data = []
        i = 0
        # Uporabis samo imas ze zgenerirano
        with open("id_mov.test.txt",'r',encoding = 'utf8') as f:
            for line in f.readlines():
                movie_ids.append(line.replace('\n',''))
        
        with open("title.basics.tsv",'r',encoding = 'utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if i == 0:
                    data.append(row)
                    i = 1
                elif find_elem_in_sorted_list(row[0], movie_ids):
                    data.append(row)
                    i += 1
                    print(i)
            
        with open("title.basics.end.tsv",'w',encoding = 'utf8',newline = '') as f:
            print('writing')
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)
                  
    def pars_crew():
        data = []
        i = 0
        data2 = []

        with open("id_mov.test.txt",'r',encoding = 'utf8') as f:
            for line in f.readlines():
                movie_ids.append(line.replace('\n',''))
        
        with open("title.crew.tsv",'r',encoding = 'utf8') as f:
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
                    print(i)
                    
        print('sorting liam')
        new_data = sorted(data2)
        
        final = open("id_director.test.txt", "w", encoding='utf8')
        print('writing ids')
        for id_director in new_data:
            final.write(id_director + "\n")
        final.close()
        
        with open("title.crew.end.tsv",'w',encoding = 'utf8',newline = '') as f:
            print('writing')
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)

    def pars_writersdirectors():
        data = []
        director_ids = []
        i = 0

        with open("id_director.test.txt",'r',encoding = 'utf8') as f:
            for line in f.readlines():
                director_ids.append(line.replace('\n',''))
        
        with open("name.basics.tsv",'r',encoding = 'utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if i == 0:
                    data.append(row)
                    i = 1
                elif find_elem_in_sorted_list(row[0], director_ids):
                    data.append(row)
                    i += 1
                    print(i)
            
        with open("name.basics.end.tsv",'w',encoding = 'utf8',newline = '') as f:
            print('writing')
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(data)
            
    pars_ratings()      
    pars_movies()
    pars_crew()
    pars_writersdirectors()
    
pars_all()
