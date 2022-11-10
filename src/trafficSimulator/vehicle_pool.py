from src.trafficSimulator import Vehicle
from numpy.random import randint


class VehiclePool:
    def __init__(self, sim):
        self.sim = sim
        self.vehicle_pool_list = []
        self.vehicles_in_buffer =[]
        self.vehicles_in_collision = []
        self.last_added_time = 0
        self.vehicle_rate = 20
        self.vehicle_count = 0
        self.v_max = 8
        # self.postion = []


    def vehicle_generator(self):
        if self.sim.t - self.last_added_time >= 60 / self.vehicle_rate:
            # 1. create vehicle, assign id to each vehicle
            self.vehicle_count += 1
            vehicle = Vehicle({'id': self.vehicle_count,'have_traffic_signal':self.sim.have_traffic_signal},self.v_max)
            # 2. assign a path to the vehicle base on weight
            total_weight = sum(path['weight'] for path in self.sim.paths)
            r = randint(1, total_weight + 1)
            for pa in self.sim.paths:
                r -= pa['weight']
                if r <= 0:
                    vehicle.path = pa
                    vehicle.road_id = pa['roads'][0]
                    vehicle.current_road_index = 0
                    break
            # 3. add to list
            self.vehicle_pool_list.append(vehicle)
            # 4.Reset last_added_time
            self.last_added_time = self.sim.t


    def find_lead(self, vehicle):
        ve_list = [ve for ve in self.vehicle_pool_list if ve.road_id == vehicle.road_id
                   and ve.id < vehicle.id]
        if len(ve_list) > 0:
            return ve_list[len(ve_list)-1]
        else:
            return None

    def update(self, dt):
        # add vehicle
        self.vehicle_generator()

        # update vehicle's status
        for vehicle in self.vehicle_pool_list:
            # find which road the vehicle is on
            road = self.sim.roads[vehicle.road_id]
            if vehicle.x >= road.length:
                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path['roads']):
                    # Add it to the next road
                    vehicle.current_road_index += 1
                    vehicle.road_id = vehicle.path['roads'][vehicle.current_road_index]
                    vehicle.x = 0
                else:
                    self.vehicle_pool_list.remove(vehicle)

            # update vehicles_in_buffer
            if (vehicle.already_in_buffer==False) & (vehicle.is_in_buffer == True):
                self.vehicles_in_buffer.append(vehicle)
                vehicle.already_in_buffer = True
                vehicle.color = (255,255,0)
                vehicle.time_reach_buffer = self.sim.t
                vehicle.time_reach_collision = self.sim.t + 5 + 30
                vehicle.time_out_collision = self.sim.t + 10 + 30
            elif(vehicle.already_in_buffer==True) & (vehicle.is_in_buffer == False):
                self.vehicles_in_buffer.remove(vehicle)
                vehicle.already_in_buffer = False
                vehicle.is_in_collision = True
                vehicle.color = (255,0,0)

            # update vehicles_in_collision
            if (vehicle.already_in_collision == False) & (vehicle.is_in_collision == True):
                self.vehicles_in_collision.append(vehicle)
                vehicle.already_in_collision = True
            elif (vehicle.already_in_collision == True) & (vehicle.is_in_collision == False):
                self.vehicles_in_collision.remove(vehicle)
                vehicle.already_in_collision = False
                vehicle.already_out_collision = True
                vehicle.color = (0, 255, 0)

            # # find the lead car
            lead = self.find_lead(vehicle)
            vehicle.update(lead, dt)

            if self.sim.have_traffic_signal:
                # Check for traffic signal
                signal_state = True
                if road.has_traffic_signal:
                    # If traffic signal is green or doesn't exist, then let vehicles pass
                    i = road.traffic_signal_group
                    signal_state = road.traffic_signal.current_cycle[i]

                # green or no signal
                if signal_state:

                    #detect buffer is full
                    counter = 0
                    for buffered_vehicle in self.vehicles_in_buffer:
                        if buffered_vehicle.path['roads'][0] == vehicle.path['roads'][0]:
                            counter = counter + 1
                    # if (counter > 6):
                    #     vehicle.slow(0.1 * vehicle._v_max)
                    # elif (counter < 6):
                    #     vehicle.slow(0.5 * vehicle._v_max)
                    if (counter > 4) & (vehicle.current_road_index==0):
                        vehicle.slow(0.1 * vehicle._v_max)
                    elif (counter < 4) & (vehicle.current_road_index==0):
                        vehicle.slow(0.5 * vehicle._v_max)
                    else:
                        vehicle.unslow()
                        vehicle.unstop()
                    counter = 0
                    if vehicle in self.vehicles_in_buffer:
                        vehicle_index = self.vehicles_in_buffer.index(vehicle)
                        if (lead is None) & (vehicle_index == 0):
                            vehicle.unstop()
                            vehicle.unslow()
                        elif (lead is None) & (vehicle_index == 1):
                            vehicle.unstop()
                            t0 = self.vehicles_in_buffer[0].time_out_collision
                            t1 = vehicle.time_reach_collision
                            if t1 < t0:
                                vehicle.slow(0.4 * vehicle._v_max)
                            else:
                                vehicle.unslow()
                        else:
                            vehicle.slow(0.4 * vehicle._v_max)
                    if vehicle in self.vehicles_in_collision:
                        vehicle.unstop()
                        vehicle.unslow()
                else:
                    if lead is None:
                        if vehicle.x >= road.length - road.traffic_signal.slow_distance:
                            vehicle.slow(road.traffic_signal.slow_factor * vehicle._v_max)
                            # vehicle.stop()
                        if road.length - road.traffic_signal.stop_distance <= vehicle.x <= road.length - road.traffic_signal.stop_distance / 2:
                            vehicle.stop()
            else:
                if lead is None:
                    vehicle.unstop()
                vehicle.unslow()
                if vehicle in self.vehicles_in_buffer:
                    vehicle_index = self.vehicles_in_buffer.index(vehicle)
                    if (lead is None)&(vehicle_index==0):
                        vehicle.unstop()
                        vehicle.unslow()
                    elif (lead is None)&(vehicle_index==1):
                        vehicle.unstop()
                        t0 = self.vehicles_in_buffer[0].time_out_collision
                        t1 = vehicle.time_reach_collision
                        if t1<t0:
                            vehicle.slow(0.4 * vehicle._v_max)
                        else:
                            vehicle.unslow()
                    else:
                        vehicle.slow(0.4 * vehicle._v_max)
                if vehicle in self.vehicles_in_collision:
                    vehicle.unstop()
                    vehicle.unslow()
