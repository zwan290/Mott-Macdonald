import pandas as pd
import numpy as np
import copy

#database connection
#import pyodbc

#conn = pyodbc.connect('Driver={SQL Server};'
#                      'Server=server_name;'
#                      'Database=db_name;'
#                      'Trusted_Connection=yes;')

#cursor = conn.cursor()
#cursor.execute('SELECT * FROM accumRainfall')

#Transfer 1 hour Time into 3600s and caculate total value into (mm)
data = pd.read_csv('accumRainfall.csv')
data = np.array(data)
start_time = data[:,0].min()
end_time = data[:,0].max()
time_span = -start_time + end_time
second_span = time_span/3600

orign_time = copy.deepcopy(data[:,0])

time = (data[:,0] - start_time)/second_span
data[:,0] = time
accu_value =np.sum(data[:,1])
print('The accumated rainfall is %.4f mm'%(accu_value*10/1000))

# Find the peak 30 minute period within the supplied time range
cal = 1
i = 0
max_value = 0
bestspan = []
while cal:
    start_time = data[i,0]
    max_time = start_time+1800
    if  max_time<= data[-1,0]:
        # find every 30-min timespan
#             cal_span1 = np.where((data[:,0]>=start_time))
        index1 = (data[:,0]>=start_time)
        index2 = (data[:,0]<=max_time)

        index1 = (np.array(index1)).astype(int)
        index2 = (np.array(index2)).astype(int)

        index = index1 + index2
        cal_span = np.where(index == 2)
        value30 = np.sum(data[cal_span,1])
        i = i+1
#         print(i)
        if value30 > max_value:
            max_value = value30
            bestspan = data[cal_span,0]
            ori_span = cal_span
    else:
        cal = 0

index = ori_span[0].tolist()

best_start = orign_time[min(index)]
best_end =  orign_time[max(index)]
print('The maximum accumulated value in 30-min interval is %.4f mm'%(max_value*10/1000))
print('The maximum time interval is from %s to %s'%(best_start, best_end))

