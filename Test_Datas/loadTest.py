import csv
import re
from sklearn.model_selection import train_test_split
import joblib

data = []

# f = open('new_Mix_Edit.csv', 'r', encoding='UTF8')
f = open('C:/Users/july_6/Desktop/Test_Datas/Mix.csv', 'r', encoding='UTF8')

rdr = csv.reader(f)

X = []
y = []

tmp=0

for line in rdr:
    X.append(line[:28])
    arr=line[29].replace('[','').replace(']','').replace('\'FALSE\'','0').replace('\'TRUE\'','1').replace(',','')
    y.append(int(''.join(arr.split()),2))
    # y.append(int(''.join(line[29].split()),2))


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05,random_state=1,stratify=y)

sc = joblib.load('standard.pkl')
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

lr = joblib.load('Logistic.pkl')

y_pred = lr.predict(X_test_std)
y_pred

print('Training accuracy: %.2f' % lr.score(X_train_std,y_train))
print('Test accuracy: %.2f' % lr.score(X_test_std,y_test))







