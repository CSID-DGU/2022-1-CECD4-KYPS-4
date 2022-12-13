import time
import datetime
import numpy as np

ftr=[3600,60,1]

now = time.localtime()
timestr = time.strftime('%X', now)
timeSecond = sum([a*b for a,b in zip(ftr,map(int, timestr.split(':')))])
print(timeSecond)   

data=[]
data.append('8')
data.append(timeSecond)
print(data)

X=np.array(data,dtype=float)

print(X)
