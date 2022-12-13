import csv
f = open('Mix.csv', 'r', encoding='UTF8')
rdr = csv.reader(f)

lines = []

i=0

cur = None
for line in rdr:
    if line[-2] != cur and len(line[-2])>0:
        lines.append(line) 

f = open('new_Mix_Edit.csv', 'w', newline='', encoding='UTF8')

wr = csv.writer(f)
wr.writerows(lines)

f.close()
