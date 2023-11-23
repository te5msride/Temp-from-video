import matplotlib.pyplot as plt 
import numpy as np
import csv 

x = [] 
y = [] 
  
with open('output.csv','r') as csvfile: 
    next(csvfile)
    lines = csv.reader(csvfile, delimiter=',') 
    for row in lines: 
        x.append(float(row[0])) 
        y.append(float(row[1]))

plt.plot(x, y, color = 'g', linestyle = 'dashed', 
         marker = 'o',label = "Output") 
# plt.plot(x, y)        # plot x and y using default line style and color
plt.xticks(np.arange(min(x), max(x)+1, 1.0))
# plt.xticks(rotation = 25)
plt.yticks(np.arange(int(min(y)), int(max(y)+1), 1.0))
plt.xlabel('time') 
plt.ylabel('Temperature(°C)') 
plt.title('Output', fontsize = 20) 
plt.grid() 
plt.legend() 
plt.show() 
