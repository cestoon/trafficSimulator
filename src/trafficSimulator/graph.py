from matplotlib import pyplot as plt
import numpy as np
from vehicle import Vehicle
from src.trafficSimulator import Simulation
from vehicle_pool import VehiclePool



x = (1.9475,11.377,14.433,15.049,16.557,17.116)
y = (0,0,0.0002,0.0016,0.0070,0.0182)
x1 = (10.787,56.627,64.456,81.26,91.561,95.09)
y1 = (0.243,0.252,0.271,0.251,0.24,0.24)
plt.title("speed-smooth")
plt.xlabel("speed")
plt.ylabel("jerk")
plt.plot(x, y,'-o',label = 'smart intersection')
plt.plot(x1,y1,'-o',label = 'intersection with signal')
plt.legend()
plt.show()
