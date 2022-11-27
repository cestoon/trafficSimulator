from .road import Road
from copy import deepcopy
from .vehicle_generator import VehicleGenerator
from .traffic_signal import TrafficSignal
from .vehicle_pool import VehiclePool
from .vehicle import Vehicle
from matplotlib import pyplot as plt
import numpy as np


class Simulation:

    def __init__(self, a=2):
        # Set default configuration
        self.vehicle_pool = VehiclePool(self)
        self.set_default_config()
        self.paths = []
        self.a=a
        self.have_traffic_signal = False
        self.waittime = 0
        self.throughput = 0
        self.final_waittime = 0
        self.final_jerk = 0
        self.final_co2 = 0

    def set_default_config(self):
        self.t = 0.0  # Time keeping
        self.frame_count = 0  # Frame count keeping
        self.dt = 1 / 60  # Simulation time step
        self.roads = []  # Array to store roads
        self.generators = []
        self.traffic_signals = []
        self.waittime = 0
        self.besttime=0
        self.crashtime = 0
        self.throughput =0
        self.currentusage=0
        self.passingcars=0

    def create_road(self, start, end, road_count):
        road = Road(start, end, road_count)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        road_count = 0
        for road in road_list:
            self.create_road(*road, road_count)
            road_count += 1



    def create_signal(self, roads, config={}):
        roads = [[self.roads[i] for i in road_group] for road_group in roads]
        sig = TrafficSignal(roads, config)
        self.traffic_signals.append(sig)
        self.have_traffic_signal = True
        return sig

    def create_intersection(self, roads, config={}):
        roads = [[self.roads[i] for i in road_group] for road_group in roads]
        sig = TrafficSignal(roads, config)
        self.traffic_signals.append(sig)
        return sig

    def update(self):

        for signal in self.traffic_signals:
            signal.update(self)

        if len(self.paths) > 0:
            # update vehicle pool after updated roads
            self.vehicle_pool.update(self.dt)

        self.t += self.dt
        self.frame_count += 1

        # if 200 <= self.t <= 200 + self.dt:
        #     self.final_waittime = self.waittime/self.throughput

        if self.throughput == 100:
            self.final_waittime = self.waittime / (self.passingcars + 1)
            self.final_jerk = self.vehicle_pool.total_jerk
            self.final_co2 = self.vehicle_pool.total_co2
    def run(self, steps):
        for _ in range(steps):
            self.update()
