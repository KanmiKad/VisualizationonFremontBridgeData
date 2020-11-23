import seaborn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as ani

fremont_data = pd.read_csv('fremont.csv',index_col='Date', parse_dates=True)
fremont_data.columns = ["West", "East"]

#introducing a total column
fremont_data["Total"] = fremont_data["West"] + fremont_data["East"]

#VISUALIZATION

#Plot display of the Total Column only
seaborn.set()
fremont_data.plot()
plt.ylabel("Hourly count")
plt.show()

#Plot display of all the Columns
daily = fremont_data.resample('D').sum()
daily.rolling(30, center=True, win_type='gaussian').sum(std=10).plot(style=[':', '--', '-'])
plt.ylabel('mean hourly count')
plt.show()


#Moving Graph Display
color = ['blue', 'orange', 'green']
fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
plt.subplots_adjust(bottom=0.2, top=0.9) #ensuring the dates (on the x-axis) fit in the screen
plt.ylabel('Bicycle Rides')
plt.xlabel('Dates')

def buildmebarchart(i=int):
    plt.legend(fremont_data.columns)
    p = plt.plot(fremont_data[:i].index, fremont_data[:i].values) #note it only returns the dataset, up to the point i
    for i in range(0,3):
        p[i].set_color(color[i]) #set the colour of each curve

animator = ani.FuncAnimation(fig, buildmebarchart, interval = 100)
plt.show()

#Moving Bar Chart
fig = plt.figure()
bar = ''
def buildmebarchart(i=int):
    iv = min(i, len(fremont_data.index)-1)
    objects = fremont_data.max().index
    y_pos = np.arange(len(objects))
    performance = fremont_data.iloc[[iv]].values.tolist()[0]
    if bar == 'vertical':
        plt.bar(y_pos, performance, align='center', color=['blue', 'orange', 'green'])
        plt.xticks(y_pos, objects)
        plt.ylabel('Numbers')
        plt.xlabel('Geo')
        plt.title('Number by Geo\n' + str(fremont_data.index[iv].strftime('%y-%m-%d')))
    else:
        plt.barh(y_pos, performance, align='center', color=['red', 'green', 'blue', 'orange'])
        plt.yticks(y_pos, objects)
        plt.xlabel('Numbers')
        plt.ylabel('Geo')

animator = ani.FuncAnimation(fig, buildmebarchart, interval=500)
plt.show()

#Moving Pie Chart
fig,ax = plt.subplots()
explode=[0.01,0.01,0.01] #pop out each slice from the pie
def getmepie(i):
    def absolute_value(val): #turn % back to a number
        a = np.round(val/100.*fremont_data.head(i).max().sum(), 0)
        return int(a)
    ax.clear()
    plot = fremont_data.head(i).max().plot.pie(y=fremont_data.columns,autopct=absolute_value, label='',explode=explode, shadow = True)
    plot.set_title('Total Number of Hours\n' + str(fremont_data.index[min( i, len(fremont_data.index)-1 )].strftime('%y-%m-%d')), fontsize=12)
import matplotlib.animation as ani
animator = ani.FuncAnimation(fig, getmepie, interval=1000)
plt.show()