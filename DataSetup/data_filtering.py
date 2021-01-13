import csv

i = 0
# Create novo.tsv from movie.basics.tsv downloaded
"""id_file = open("id_data.tsv", "w", encoding='utf8')
with open("title.basics.tsv",'r',encoding = 'utf8') as f:
    with open("novo.tsv", 'w', encoding='utf8') as file:
        reader = csv.reader(f, delimiter='\t')
        ct = 0
        for row in reader:
            ct += 1
            print(ct)
            if i == 0:
                i = 1
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(row)
            elif row[1] == 'movie':
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(row)

                writer_id = csv.writer(id_file, delimiter='\t')
                writer_id.writerow(row[0])"""

# Create final title.basics.tsv from novo.tsv
"""data = list()
ct = 0
with open("novo.tsv", "r", encoding = 'utf8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if len(row) == 0:
            pass
        else:
            ct += 1
            print(ct)
            data.append(row)

final = open("title.basics.tsv", "w", encoding='utf8', newline="")
writer = csv.writer(final, delimiter='\t')
writer.writerows(data)"""

# Create id_data.txt from title.basics.tsv
"""data = list()
ct = 0
with open("title.basics.tsv", "r", encoding='utf8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if ct == 0:
            ct += 1
            pass
        else:
            ct += 1
            print(ct)
            data.append(str(row[0]))

final = open("id_data.txt", "w", encoding='utf8')
for id in data:
    final.write(id + "\n")
final.close()"""
