from matplotlib import pyplot as plt
import numpy as np
from vehicle import Vehicle
from src.trafficSimulator import Simulation
from vehicle_pool import VehiclePool

x = np.arange(1, 11)
y = 2 * x + 5
plt.title("Matplotlib demo")
plt.xlabel("x axis caption")
plt.ylabel("y axis caption")
plt.plot(x, y)
plt.show()