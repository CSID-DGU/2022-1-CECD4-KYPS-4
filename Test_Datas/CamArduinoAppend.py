import csv
from datetime import datetime

Cam_Lines = []
Ard_Lines = []

f = open('C:/Users/july_6/Desktop/Test_Datas/sensor.csv', 'r', encoding='UTF8')
rdr = csv.reader(f)

for line in rdr:
    Ard_Lines.append(line)

Ard_Lines.pop(0)

f = open('C:/Users/july_6/Desktop/Test_Datas/skeleton.csv', 'r', encoding='UTF8')
rdr = csv.reader(f)


for line in rdr:
    if line[-1]=='':
        continue
    Cam_Lines.append(line)
        
cam_start_idx=0 

start_time = datetime.strptime(Cam_Lines[cam_start_idx][-1], '%c') 

while(start_time<datetime.strptime(Ard_Lines[0][-1], '%Y. %m. %d. %H:%M:%S')):
    cam_start_idx=cam_start_idx+1
    start_time=datetime.strptime(Cam_Lines[cam_start_idx][-1], '%c') 


i = 0
for line in Ard_Lines:
    if(datetime.strptime(line[-1], '%Y. %m. %d. %H:%M:%S') == start_time):
        break
    i=i+1

MixLines=[]

j = i

finished=False
for t in range(cam_start_idx, len(Cam_Lines)):
    if j>len(Ard_Lines) - 1:
        break
    while(datetime.strptime(Cam_Lines[t][-1], '%c') != datetime.strptime(Ard_Lines[j][-1], '%Y. %m. %d. %H:%M:%S')):
        j=j+1
        if j>len(Ard_Lines) - 1:
            finished=True
            break
    if(finished==False):
        MixLine = Cam_Lines[t]
        MixLine.append(Ard_Lines[j][0:4])
        MixLines.append(MixLine)

f = open('C:/Users/july_6/Desktop/Test_Datas/Mix.csv', 'w', newline='', encoding='UTF8')

wr = csv.writer(f)
wr.writerows(MixLines)

f.close()









