from matplotlib import pyplot as plt
import numpy as np
from vehicle import Vehicle
from src.trafficSimulator import Simulation
from vehicle_pool import VehiclePool



x = (20,25,30,35,40)
y = (3.8,3.77,3.89,3.8,3.9)
x1 = (20,25,30,35,40)
y1 = (4.33,9,10,13,15)
plt.title("speed-smooth")
plt.xlabel("speed")
plt.ylabel("jerk")
plt.plot(x, y,'-o',label = 'smart intersection')
plt.plot(x1,y1,'-o',label = 'intersection with signal')
plt.legend()
plt.show()