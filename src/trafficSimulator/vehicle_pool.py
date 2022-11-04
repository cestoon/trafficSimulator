from src.trafficSimulator import Vehicle
from copy import deepcopy
from numpy.random import randint


class VehiclePool:
    def __init__(self, sim):
        self.sim = sim
        self.vehicle_pool_list = []
        self.last_added_time = 0
        self.vehicle_rate = 20
        self.vehicle_count = 0

    def vehicle_generator(self):
        if self.sim.t - self.last_added_time >= 60 / self.vehicle_rate:
            # 1. create vehicle, assign id to each vehicle
            self.vehicle_count += 1
            vehicle = Vehicle({'id': self.vehicle_count})
            # 2. assign a path to the vehicle base on weight
            total_weight = sum(path['weight'] for path in self.sim.paths)
            r = randint(1, total_weight + 1)
            for pa in self.sim.paths:
                r -= pa['weight']
                if r <= 0:
                    vehicle.path = pa
                    vehicle.road_id = pa['path'][0]
                    vehicle.current_road_index = 0
                    break
            # 3. add to list
            self.vehicle_pool_list.append(vehicle)
            # 4.Reset last_added_time
            self.last_added_time = self.sim.t

    def update(self, dt):
        # add vehicle
        self.vehicle_generator()

        # update vehicle's status
        for vehicle in self.vehicle_pool_list:
            # find which road the vehicle is on
            road = self.sim.roads[vehicle.road_id]
            if vehicle.x >= road.length:
                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path['path']):
                    # Add it to the next road
                    vehicle.current_road_index += 1
                    vehicle.road_id = vehicle.path['path'][vehicle.current_road_index]
                    vehicle.x = 0
                else:
                    self.vehicle_pool_list.remove(vehicle)
            # find the lead car
            vehicle.update(None, dt)

