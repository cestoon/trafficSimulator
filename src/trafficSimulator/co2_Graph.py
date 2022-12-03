from matplotlib import pyplot as plt
import numpy as np
from vehicle import Vehicle
from src.trafficSimulator import Simulation
from vehicle_pool import VehiclePool



#smart: long: wt 14.4853 acc:3.89, co2:78.45
        #middle: wt:7.38 acc:3.83, co2:86.36
        #short: wt:3.35 acc:3.83, co2:91.42
        #60:wt:10.43,acc:3.89,co2:91.31
        #100:wt:19.2,acc:3.89,co2:97.65
x = []
y = []
data =  [(1, 6.48), (5, 7.27), (10, 7.20)]


for d in data:
    x.append(d[0])
    y.append(d[1])
#long traffic wt:49,acc:10.17, co2:63.87
#middle       wt:30.23,acc:8.8, co2:83.11
#short        wt:28.07, acc:3.53, co2:77.43
#60:          wt:20.74,acc:14.3, co2:88.3
#100:         wt:55.04,acc:8.87,co2:80.11
data2 = [(1, 18.41), (5, 31.37), (10, 33.36)]
x2 = []
y2 = []

for d in data2:
    x2.append(d[0])
    y2.append(d[1])

# y = 2 * x + 5
plt.title("ImbalanceDegree-WaitingTime")
plt.xlabel("Imbalance")
plt.ylabel("WaitingTime(t)")
plt.plot(x, y, 'o-', label='smart intersect')
plt.plot(x2, y2, 'o-', label='intersect with signal')
plt.legend()
plt.show()
