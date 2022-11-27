from src.trafficSimulator import Vehicle
from numpy.random import randint


class VehiclePool:
    def __init__(self, sim):
        self.inroadtime = 0
        self.sim = sim
        self.vehicle_pool_list = []
        self.vehicles_in_buffer =[]
        self.vehicles_in_collision = []
        self.vehicles_in_buffer_west = []
        self.vehicles_in_buffer_south = []
        self.vehicles_in_buffer_east = []
        self.vehicles_in_buffer_north = []
        self.last_added_time = 0
        self.last_pass_time = 0
        self.vehicle_rate = 30
        self.vehicle_count = 0
        self.v_max = 7
        self.total_co2 = 0
        self.total_jerk = 0
        self.final_jerk = 0
        self.v_realspeed=self.v_max*5
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
        if len(self.vehicle_pool_list)<40:
            self.vehicle_generator()

        # update vehicle's status
        for vehicle in self.vehicle_pool_list:
            # find which road the vehicle is on
            road = self.sim.roads[vehicle.road_id]
            if vehicle.x >= road.length:
                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path['roads']):
                    if vehicle.current_road_index == 0:
                        vehicle.inroadtime=self.sim.t
                    # Add it to the next road
                    vehicle.current_road_index += 1
                    vehicle.road_id = vehicle.path['roads'][vehicle.current_road_index]
                    if vehicle.current_road_index == (len(vehicle.path['roads'])-1):
                        self.sim.throughput += 1
                    vehicle.x = 0
                else:
                    self.vehicle_pool_list.remove(vehicle)
                    vehicle.outroadtime=self.sim.t
                    self.sim.currentusage = (vehicle.outroadtime - vehicle.inroadtime)
                    self.sim.waittime += (self.sim.currentusage - self.sim.besttime)
                    # self.sim.waittime+=self.sim.currentusage
                    if self.sim.besttime==0:
                        self.sim.besttime = self.sim.currentusage
                    if self.sim.currentusage<=self.sim.besttime:
                        self.sim.besttime=self.sim.currentusage
                    self.sim.passingcars+=1

            # update vehicles_in_buffer
            if (vehicle.already_in_buffer==False) & (vehicle.is_in_buffer == True):
                self.vehicles_in_buffer.append(vehicle)
                if(vehicle.from_which_direction == 'WEST'):
                    self.vehicles_in_buffer_west.append(vehicle)
                elif (vehicle.from_which_direction == 'SOUTH'):
                    self.vehicles_in_buffer_south.append(vehicle)
                elif (vehicle.from_which_direction == 'EAST'):
                    self.vehicles_in_buffer_east.append(vehicle)
                elif (vehicle.from_which_direction == 'NORTH'):
                    self.vehicles_in_buffer_north.append(vehicle)

                vehicle.already_in_buffer = True

                vehicle.color = (255,255,0)
                vehicle.time_reach_buffer = self.sim.t
                vehicle.time_reach_collision = self.sim.t + 60
                vehicle.time_out_collision = self.sim.t + 200
            elif(vehicle.already_in_buffer==True) & (vehicle.is_in_buffer == False):
                self.vehicles_in_buffer.remove(vehicle)
                if (vehicle.from_which_direction == 'WEST'):
                    self.vehicles_in_buffer_west.remove(vehicle)
                elif (vehicle.from_which_direction == 'SOUTH'):
                    self.vehicles_in_buffer_south.remove(vehicle)
                elif (vehicle.from_which_direction == 'EAST'):
                    self.vehicles_in_buffer_east.remove(vehicle)
                elif (vehicle.from_which_direction == 'NORTH'):
                    self.vehicles_in_buffer_north.remove(vehicle)
                vehicle.already_in_buffer = False
                vehicle.is_in_collision = True
                vehicle.color = (255,0,0)

                # vehicle.time_reach_collision = self.sim.t
            elif (vehicle.already_in_buffer == True) & (vehicle.is_in_buffer == True):
                # update priority
                if (vehicle.from_which_direction == 'WEST'):
                    vehicle.priority = 2 * self.vehicles_in_buffer_west.index(vehicle)
                elif (vehicle.from_which_direction == 'SOUTH'):
                    vehicle.priority = 2 * self.vehicles_in_buffer_south.index(vehicle)
                elif (vehicle.from_which_direction == 'EAST'):
                    vehicle.priority = 2 * self.vehicles_in_buffer_east.index(vehicle) + 1
                elif (vehicle.from_which_direction == 'NORTH'):
                    vehicle.priority = 2 * self.vehicles_in_buffer_north.index(vehicle) + 1

            # update vehicles_in_collision
            if (vehicle.already_in_collision == False) & (vehicle.is_in_collision == True):
                self.vehicles_in_collision.append(vehicle)
                vehicle.already_in_collision = True
                self.last_pass_time = self.sim.t
                self.total_jerk += abs(vehicle.jerk)
            elif (vehicle.already_in_collision == True) & (vehicle.is_in_collision == False):
                self.vehicles_in_collision.remove(vehicle)
                vehicle.already_in_collision = False
                vehicle.already_out_collision = True
                vehicle.color = (0, 255, 0)
                # vehicle.time_out_collision = self.sim.t


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
                    if vehicle.current_road_index == 0:
                        counter = 0
                        for buffered_vehicle in self.vehicles_in_buffer:
                            if buffered_vehicle.path['roads'][0] == vehicle.path['roads'][0]:
                                counter = counter + 1
                        if (counter >= 4) & (vehicle.current_road_index == 0):
                            vehicle.slow(0.1 * vehicle._v_max)
                        elif (counter < 4) & (vehicle.current_road_index == 0):
                            vehicle.slow(0.4 * vehicle._v_max)
                        else:
                            vehicle.unslow()
                            vehicle.unstop()
                    elif vehicle in self.vehicles_in_buffer:
                        vehicle_index = self.vehicles_in_buffer.index(vehicle)
                        if (vehicle_index == 0 and len(self.vehicles_in_collision) <= 1 and (self.sim.t - self.last_pass_time > 10)):
                            vehicle.unstop()
                            vehicle.unslow()
                        elif (self.vehicles_in_buffer[0].stopped==True ) and (lead is None) and (vehicle.current_road_index>0) and (self.sim.t - self.last_pass_time > 6):
                            self.vehicles_in_collision.append(vehicle)
                            self.last_pass_time = self.sim.t
                            # self.vehicles_in_buffer.remove(vehicle)
                            vehicle.unstop()
                            vehicle.unslow()
                        else:
                            vehicle.slow(0.4 * vehicle._v_max)

                    elif (vehicle.already_in_collision == True) or (vehicle.already_out_collision == True):
                        vehicle.unstop()
                        vehicle.unslow()
                    else:
                        #bug
                        vehicle.slow(0.4 * vehicle._v_max)
                        # print('wrong state')
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
        for vehicle in self.vehicle_pool_list:
            self.total_co2 = self.total_co2 + vehicle.co2em
            last = vehicle.jerk
        # i = 0
        # for i in range(len(self.vehicle_pool_list)-1):
        #     t = self.vehicle_pool_list[i].jerk
        #     if self.vehicle_pool_list[i+1].jerk > self.vehicle_pool_list[i].jerk:
        #         self.total_jerk += self.vehicle_pool_list[i+1].jerk




