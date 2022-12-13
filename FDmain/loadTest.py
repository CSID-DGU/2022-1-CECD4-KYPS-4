import csv
import re
import joblib
import time
import rrcfModel as rf
def load_test_model(input):
    
    input_2D=[input]
    sc = joblib.load('standard.pkl')
    X_std = sc.transform(input_2D)
    lr = joblib.load('Logistic.pkl')
    new_row = []
    new_realtime = []
    y_pred = lr.predict(X_std)
    rf.rrcfModel_run(y_pred)

    # if y_pred :
    #     fcv = open('NEWCORD.csv', 'a', newline='')
    #     wr = csv.writer(fcv)
        
    #     new_row.append(y_pred)
    #     new_row.append(time.strftime('%c'))
    #     wr.writerow(new_row)
    #     fcv.close()
    

   










