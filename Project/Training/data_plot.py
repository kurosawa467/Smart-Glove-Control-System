import matplotlib.pyplot as plt
import pandas
import numpy as np
import seaborn as sns

def plot_for_one_csv(filename):
    sensor_data = pandas.read_csv(filename, header = 0)
    x = np.array(sensor_data['timestamp']).T
    y1 = np.array(sensor_data['yaw']).T
    y2 = np.array(sensor_data['pitch']).T
    y3 = np.array(sensor_data['row']).T
    plt.plot(x, y1, label = "yaw")
    plt.plot(x, y2, label = "pitch")
    plt.plot(x, y3, label = "row")
    plt.title (filename)
    plt.xlabel('time')
    plt.legend()
    plt.show()
    

#plot_for_one_csv('user/user34.csv')
#plot_for_one_csv('user/user35.csv')
#plot_for_one_csv('user/user36.csv')
#plot_for_one_csv('user/user37.csv')
#plot_for_one_csv('user/user38.csv')
    
gestures = pandas.read_csv('all_data.csv')
sns.set_style("whitegrid")
sns.pairplot(gestures, hue = "species", height = 3)
plt.show()
