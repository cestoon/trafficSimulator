from matplotlib import pyplot as plt
import numpy as np
from vehicle import Vehicle
from src.trafficSimulator import Simulation
from vehicle_pool import VehiclePool

x = []
y = []
data = [(100, 265.7394806927325), (200, 538.2662820775407), (300, 809.9240172488057), (400, 1082.3385584663345), (500, 1353.631148928334), (600, 1626.3024325042147), (700, 1898.6223507298912), (800, 2170.4263979148714)]

for d in data:
    x.append(d[0])
    y.append(d[1])

data2 = [(100, 625.914372341167), (200, 1411.922155771473), (300, 2189.209583567679), (400, 2877.091380343546), (500, 3586.023244969436), (600, 4370.843059499383), (700, 5125.991518382448), (800, 5878.891473690374)]
x2 = []
y2 = []

for d in data2:
    x2.append(d[0])
    y2.append(d[1])

# y = 2 * x + 5
plt.title("CO2 emission graph")
plt.xlabel("number of vehicle crossed intersect")
plt.ylabel("CO2 (kg)")
plt.plot(x, y, 'o-', label='smart intersect')
plt.plot(x2, y2, 'o-', label='intersect with signal')
plt.legend()
plt.show()
