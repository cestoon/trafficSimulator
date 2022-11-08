from .road import Road
from copy import deepcopy
from .vehicle_generator import VehicleGenerator
from .traffic_signal import TrafficSignal
from .vehicle_pool import VehiclePool


class Simulation:
    def __init__(self, config={}):
        # Set default configuration
        self.vehicle_pool = VehiclePool(self)
        self.set_default_config()
        self.paths = []

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0  # Time keeping
        self.frame_count = 0  # Frame count keeping
        self.dt = 1 / 60  # Simulation time step
        self.roads = []  # Array to store roads
        self.generators = []
        self.traffic_signals = []

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
        return sig

    def update(self):
        for signal in self.traffic_signals:
            signal.update(self)

        if len(self.paths) > 0:
            # update vehicle pool after updated roads
            self.vehicle_pool.update(self.dt)

        # Increment time
        self.t += self.dt
        self.frame_count += 1

    def run(self, steps):
        for _ in range(steps):
            self.update()
