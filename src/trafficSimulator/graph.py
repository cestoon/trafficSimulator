from matplotlib import pyplot as plt
import numpy as np
from vehicle import Vehicle
from src.trafficSimulator import Simulation
from vehicle_pool import VehiclePool



x = (8,9,10,11,12)
y = (0.00183,0.00686,0.02338,0.04557,0.0907)
x1 = (8,9,10,11,12)
y1 = (0.1912,0.4735,0.7357,1.053,1.202)
plt.title("speed-smooth")
plt.xlabel("speed")
plt.ylabel("jerk")
plt.plot(x, y,'-o',label = 'smart intersection')
plt.plot(x1,y1,'-o',label = 'intersection with signal')
plt.legend()
plt.show()