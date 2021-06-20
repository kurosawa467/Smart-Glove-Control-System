import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(3,1,1)
ax2 = fig.add_subplot(3,1,2)
ax3 = fig.add_subplot(3,1,3)

def animate(i):
    #lines = []
    with open('data.txt', 'r') as fin:
        lines = fin.read().splitlines(True)
        fin.close()
    with open('data.txt', 'w') as fout:
        if len(lines)>100:
            fout.writelines(lines[1:])
            fout.close()
    #head, tail = fin.read().split('\n', 1); ...; fout.write(tail)
    
    #graph_data = open('data.txt','r').read()
    #lines = graph_data.split('\n')
    #if len(lines)>50:
    #    lines = lines[1:]
    times = []
    xs = []
    ys = []
    zs = []
    for line in lines:
        if len(line) > 1:
            time, status, x, y, z= line.split(',')
            times.append(float(time))
            xs.append(float(x))
            ys.append(float(y))
            zs.append(float(z))
    ax1.clear()
    ax1.plot(times, xs)
    ax2.clear()
    ax2.plot(times, ys)
    ax3.clear()
    ax3.plot(times, zs)
    
    
    
    
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()