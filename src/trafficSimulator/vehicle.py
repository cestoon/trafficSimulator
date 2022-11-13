import numpy as np


class Vehicle:
    def __init__(self, config={}, v_max=8.6):
        # Set default configuration
        self.set_default_config(v_max)

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self, v_max):
        self.l = 4
        self.s0 = 7
        self.T = 1
        self.v_max = v_max
        self.a_max = 4
        self.b_max = 5
        self.color = (0,255,0)
        # self.position = position
        self.inroadtime = 0
        self.outroadtime = 0
        self.co2em1=0
        self.co2em2=0
        self.co2em = 0
        self.lastp=0
        self.jerk = 0

        self.path = []
        self.current_road_index = 0
        self.priority = 999
        self.from_which_direction =''
        self.jerk_every_time = 0

        self.rollingRes = 0.018  # wheelonroad
        self.engineEff = 0.35  # fuel2force
        self.oil2co2 = 0.785  # kg/L
        self.fuelheat = 9.3278  # L/kWh

        self.x = 0
        self.total_x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False
        self.already_in_buffer = False
        self.already_in_collision = False
        self.is_in_buffer = False
        self.is_in_collision = False
        self.time_reach_buffer = 0
        self.time_reach_collision = 55555555
        self.time_out_collision = 999999999
        self.already_out_collision = False

    def init_properties(self):
        self.sqrt_ab = 2 * np.sqrt(self.a_max * self.b_max)
        self._v_max = self.v_max

    def update(self, lead, dt):
        if self.path['roads'][0] == 0:
            self.from_which_direction = 'WEST'
        elif self.path['roads'][0] == 1:
            self.from_which_direction = 'SOUTH'
        elif self.path['roads'][0] == 2:
            self.from_which_direction = 'EAST'
        elif self.path['roads'][0] == 3:
            self.from_which_direction = 'NORTH'


        #update is_in_buffer
        if self.current_road_index == 1:
            self.is_in_buffer = True
        else:
            self.is_in_buffer = False
        #update is_in_collision
        if (self.current_road_index >1) & (self.current_road_index < len(self.path['roads'])-1)  :
            self.is_in_collision = True
        else:
            self.is_in_collision = False

        a0 = self.a
        # Update position and velocity
        self.lastp = self.x
        self.lastjerk = self.jerk_every_time
        if self.v + self.a * dt < 0:
            self.x -= 1 / 2 * self.v * self.v / self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * dt * dt / 2
        # Update acceleration
        alpha = 0
        if (lead is not None) & (self.already_out_collision == False) & (self.have_traffic_signal == True) :
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v
            alpha = (self.s0 + max(0, self.T * self.v + delta_v * self.v / self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1 - (self.v / self.v_max) ** 4 - alpha ** 2)

        if self.stopped:
            self.a = -self.b_max * self.v / self.v_max

        self.jerk_every_time = (self.a - a0) / dt

        if self.jerk_every_time > self.lastjerk:
            self.jerk = self.jerk_every_time

        self.co2em1 = 0
        self.co2em2 = 0
        if self.a == 0:
            self.co2em1 = self.rollingRes * 1250 * 0.98 * (self.x - self.lastp) /3600/ 1000 / self.fuelheat / self.oil2co2
        elif self.a > 0:
            self.co2em2 = 1250 * self.a * 0.98 * (self.x - self.lastp)/ 3600 / 1000 / self.fuelheat / self.oil2co2

        self.co2em += self.co2em1 + self.co2em2

    def stop(self):
        self.stopped = True

    def unstop(self):
        self.stopped = False

    def slow(self, v):
        self.v_max = v

    def unslow(self):
        self.v_max = self._v_max

