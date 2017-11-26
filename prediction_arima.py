'''
Created on 27 Oct 2017

@author: stack
'''
import csv

from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

import random

def parser(x):
    #print datetime.strptime('190'+x, '%Y-%m')
    return datetime.strptime('1'+x, '%Y-%m')
 



def generate_pps_thp():
    data = []
    x = []
    for i in range(1000):
        x.append(i)
        #flow_name = 'f'+str(i)
        pps = random.randint(100, 600) # pps
        thp = round(random.uniform(1, 15),2) # Mbps
        data.append(('f1', i, pps, thp))
        pps = random.randint(100, 600) # pps
        thp = round(random.uniform(1, 15),2) # Mbps
        data.append(('f2', i, pps, thp))
        pps = random.randint(100, 600) # pps
        thp = round(random.uniform(1, 15),2) # Mbps
        data.append(('f3', i, pps, thp))
    return data

'''
if 1==2:
    data = generate_pps_thp()
    f = open('/opt/stack/data_rtt.csv', 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    writer.writerow(['month rate'])
    i = 0 
    for d in data:
        y = i//12 + 1
        m = i%12 + 1
        date_ = str(y).zfill(3)+'-'+str(m).zfill(2)
        if d[0] == 'f1':
            row = '\"'+date_+'\"'+' '+str(float(d[2]))
            writer.writerow([row])
            print date_, d[2]
            i = i + 1 
            
    f.close()        
    #print data
'''

'''
data = []

if 1==1:
    
    f = open('/opt/stack/data_pred.csv', 'rb')
    reader = csv.reader(f, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='')
    for row in reader:
        data.append(['f1', row[0], row[1]])
        #sources[row[0]] = {'ip' : row[1], 'flavor' : row[2], 'name' : row[3]}
    f.close() 
    
    

    
    
    
    f = open('/opt/stack/data_rtt.csv', 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    writer.writerow(['month rate'])
    i = 0 
    for d in data:
        y = i//12 + 1
        m = i%12 + 1
        date_ = str(y).zfill(3)+'-'+str(m).zfill(2)
        if d[0] == 'f1':
            row = '\"'+date_+'\"'+' '+str(float(d[1]))
            writer.writerow([row])
            print date_, d[1]
            i = i + 1 
            
    f.close() 
           
    f = open('/opt/stack/data_t.csv', 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    writer.writerow(['month t'])
    i = 0 
    for d in data:
        y = i//12 + 1
        m = i%12 + 1
        date_ = str(y).zfill(3)+'-'+str(m).zfill(2)
        if d[0] == 'f1':
            row = '\"'+date_+'\"'+' '+str(float(d[2]))
            writer.writerow([row])
            print date_, d[2]
            i = i + 1 
            
    f.close()  
       
'''   




series = read_csv('/opt/stack/data_t.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
X = series.values

size = int(len(X) * 0.9)
print X, size

train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()

        
'''
#series.plot()
#pyplot.show()

#print y1
#print data


df_y1 = pd.DataFrame(y1)
df_y1.columns = ['pps', 'thp']


#df_y1.set_index([0,1])

#print df_y1

#df_y1.plot(figsize=(15, 6))
#plt.show()
'''





