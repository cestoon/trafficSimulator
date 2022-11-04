import numpy as np
import pygame
from src.trafficSimulator.button import traffic_flow_button, vehicle_velocity_button, scene_light_2lane_button, scence_round_button, scence_light_4lane_button, scence_smart_4lane_button,scence_smart_2lane_button
from src.trafficSimulator import Simulation, TURN_LEFT, TURN_RIGHT, turn_road, curve_road
from pygame import gfxdraw
import os


class Window:
    def __init__(self, sim, config={}):
        # create buttons

        # load button images
        # get the directory of this file
        sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        # join the filepath and the filename
        start_btn_path = os.path.join(sourceFileDir, './button/start_btn.png')
        exit_btn_path = os.path.join(sourceFileDir, './button/exit_btn.png')
        plus_btn_path = os.path.join(sourceFileDir, './button/plus_btn.png')
        minus_btn_path = os.path.join(sourceFileDir, './button/minus_btn.png')
        light_2lane_btn_path = os.path.join(sourceFileDir, 'button/traffic2lanes.jpg')
        light_4lane_btn_path = os.path.join(sourceFileDir, 'button/traffic4lanes.jpg')
        smart_2lane_btn_path = os.path.join(sourceFileDir, 'button/smart2lanes.jpg')
        smart_4lane_btn_path = os.path.join(sourceFileDir, 'button/smart4lanes.jpg')
        smart_round_btn_path = os.path.join(sourceFileDir, 'button/roundroad.jpg')

        self.plus_img = pygame.image.load(plus_btn_path)
        self.minus_img = pygame.image.load(minus_btn_path)
        self.light_2lane_img = pygame.image.load(light_2lane_btn_path)
        self.light_4lane_img = pygame.image.load(light_4lane_btn_path)
        self.smart_2lane_img = pygame.image.load(smart_2lane_btn_path)
        self.smart_4lane_img = pygame.image.load(smart_4lane_btn_path)
        self.round_img = pygame.image.load(smart_round_btn_path)

        # create button instances
        self.traffic_flow_button = traffic_flow_button.Button(0, 20, self.plus_img, self.minus_img, 0.01, 0.01)
        self.vehicle_velocity_button = vehicle_velocity_button.Button(0, 40, self.plus_img, self.minus_img, 0.01, 0.01)
        self.light_2lane_button = scene_light_2lane_button.Button(100, 60, self.light_2lane_img, 0.4)
        self.smart_2lane_button = scence_smart_2lane_button.Button(100, 110, self.smart_2lane_img, 0.4)
        self.light_4lane_button = scence_light_4lane_button.Button(100, 160, self.light_4lane_img, 0.4)
        self.smart_4lane_button = scence_smart_4lane_button.Button(100, 210, self.smart_4lane_img, 0.4)
        self.round_button = scence_round_button.Button(100, 260, self.round_img, 0.4)
        # Simulation to draw

        # Simulation to draw

        self.sim = sim

        # Set default configurations
        self.set_default_config()

        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        """Set default configuration"""
        self.width = 1400
        self.height = 900
        self.bg_color = (250, 250, 250)

        self.fps = 60
        self.zoom = 5
        self.offset = (0, 0)

        self.mouse_last = (0, 0)
        self.mouse_down = False

    def loop(self, loop=None):
        """Shows a window visualizing the simulation and runs the loop function."""

        # Create a pygame window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()

        # Fixed fps
        clock = pygame.time.Clock()

        # To draw text
        pygame.font.init()
        self.text_font = pygame.font.SysFont('Lucida Console', 16)

        # Draw loop
        running = True
        while running:
            # Update simulation
            if loop: loop(self.sim)

            # Draw simulation
            self.draw()

            # Update window
            pygame.display.update()
            clock.tick(self.fps)

            # Handle all events
            for event in pygame.event.get():
                # Quit program if window is closed
                if event.type == pygame.QUIT:
                    running = False
                # Handle mouse events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If mouse button down
                    if event.button == 1:
                        # Left click
                        x, y = pygame.mouse.get_pos()
                        x0, y0 = self.offset
                        self.mouse_last = (x - x0 * self.zoom, y - y0 * self.zoom)
                        self.mouse_down = True
                    if event.button == 4:
                        # Mouse wheel up
                        self.zoom *= (self.zoom ** 2 + self.zoom / 4 + 1) / (self.zoom ** 2 + 1)
                    if event.button == 5:
                        # Mouse wheel down
                        self.zoom *= (self.zoom ** 2 + 1) / (self.zoom ** 2 + self.zoom / 4 + 1)
                elif event.type == pygame.MOUSEMOTION:
                    # Drag content
                    if self.mouse_down:
                        x1, y1 = self.mouse_last
                        x2, y2 = pygame.mouse.get_pos()
                        self.offset = ((x2 - x1) / self.zoom, (y2 - y1) / self.zoom)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False

    def run(self, steps_per_update=1):
        """Runs the simulation by updating in every loop."""

        def loop(sim):
            sim.run(steps_per_update)

        self.loop(loop)

    def convert(self, x, y=None):
        """Converts simulation coordinates to screen coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(self.width / 2 + (x + self.offset[0]) * self.zoom),
            int(self.height / 2 + (y + self.offset[1]) * self.zoom)
        )

    def inverse_convert(self, x, y=None):
        """Converts screen coordinates to simulation coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(-self.offset[0] + (x - self.width / 2) / self.zoom),
            int(-self.offset[1] + (y - self.height / 2) / self.zoom)
        )

    def background(self, r, g, b):
        """Fills screen with one color."""
        self.screen.fill((r, g, b))

    def line(self, start_pos, end_pos, color):
        """Draws a line."""
        gfxdraw.line(
            self.screen,
            *start_pos,
            *end_pos,
            color
        )

    def rect(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.rectangle(self.screen, (*pos, *size), color)

    def box(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.box(self.screen, (*pos, *size), color)

    def circle(self, pos, radius, color, filled=True):
        gfxdraw.aacircle(self.screen, *pos, radius, color)
        if filled:
            gfxdraw.filled_circle(self.screen, *pos, radius, color)

    def polygon(self, vertices, color, filled=True):
        gfxdraw.aapolygon(self.screen, vertices, color)
        if filled:
            gfxdraw.filled_polygon(self.screen, vertices, color)

    def rotated_box(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255), filled=True):
        """Draws a rectangle center at *pos* with size *size* rotated anti-clockwise by *angle*."""
        x, y = pos
        l, h = size

        if angle:
            cos, sin = np.cos(angle), np.sin(angle)

        vertex = lambda e1, e2: (
            x + (e1 * l * cos + e2 * h * sin) / 2,
            y + (e1 * l * sin - e2 * h * cos) / 2
        )

        if centered:
            vertices = self.convert(
                [vertex(*e) for e in [(-1, -1), (-1, 1), (1, 1), (1, -1)]]
            )
        else:
            vertices = self.convert(
                [vertex(*e) for e in [(0, -1), (0, 1), (2, 1), (2, -1)]]
            )

        self.polygon(vertices, color, filled=filled)

    def rotated_rect(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255)):
        self.rotated_box(pos, size, angle=angle, cos=cos, sin=sin, centered=centered, color=color, filled=False)

    def arrow(self, pos, size, angle=None, cos=None, sin=None, color=(150, 150, 190)):
        if angle:
            cos, sin = np.cos(angle), np.sin(angle)

        self.rotated_box(
            pos,
            size,
            cos=(cos - sin) / np.sqrt(2),
            sin=(cos + sin) / np.sqrt(2),
            color=color,
            centered=False
        )

        self.rotated_box(
            pos,
            size,
            cos=(cos + sin) / np.sqrt(2),
            sin=(sin - cos) / np.sqrt(2),
            color=color,
            centered=False
        )

    def draw_axes(self, color=(100, 100, 100)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)
        self.line(
            self.convert((0, y_start)),
            self.convert((0, y_end)),
            color
        )
        self.line(
            self.convert((x_start, 0)),
            self.convert((x_end, 0)),
            color
        )

    def draw_grid(self, unit=50, color=(150, 150, 150)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)

        n_x = int(x_start / unit)
        n_y = int(y_start / unit)
        m_x = int(x_end / unit) + 1
        m_y = int(y_end / unit) + 1

        for i in range(n_x, m_x):
            self.line(
                self.convert((unit * i, y_start)),
                self.convert((unit * i, y_end)),
                color
            )
        for i in range(n_y, m_y):
            self.line(
                self.convert((x_start, unit * i)),
                self.convert((x_end, unit * i)),
                color
            )

    def draw_roads(self):
        for road in self.sim.roads:
            # Draw road background
            self.rotated_box(
                road.start,
                (road.length, 3.7),
                cos=road.angle_cos,
                sin=road.angle_sin,
                color=(180, 180, 220),
                centered=False
            )
            # Draw road lines
            # self.rotated_box(
            #     road.start,
            #     (road.length, 0.25),
            #     cos=road.angle_cos,
            #     sin=road.angle_sin,
            #     color=(0, 0, 0),
            #     centered=False
            # )

            # Draw road arrow
            if road.length > 5:
                for i in np.arange(-0.5 * road.length, 0.5 * road.length, 10):
                    pos = (
                        road.start[0] + (road.length / 2 + i + 3) * road.angle_cos,
                        road.start[1] + (road.length / 2 + i + 3) * road.angle_sin
                    )

                    self.arrow(
                        pos,
                        (-1.25, 0.2),
                        cos=road.angle_cos,
                        sin=road.angle_sin
                    )

                    # TODO: Draw road arrow

    def draw_vehicle(self, vehicle, road):
        l, h = vehicle.l, 2
        sin, cos = road.angle_sin, road.angle_cos

        x = road.start[0] + cos * vehicle.x
        y = road.start[1] + sin * vehicle.x

        self.rotated_box((x, y), (l, h), cos=cos, sin=sin, centered=True)

    def draw_vehicle_new(self, vehicle):
        l, h = vehicle.l, 2
        road = self.sim.roads[vehicle.road_id]
        sin, cos = road.angle_sin, road.angle_cos

        x = road.start[0] + cos * vehicle.x
        y = road.start[1] + sin * vehicle.x

        self.rotated_box((x, y), (l, h), cos=cos, sin=sin, centered=True)

    def draw_vehicles(self):
        if len(self.sim.paths) > 0:
            for vehicle in self.sim.vehicle_pool.vehicle_pool_list:
                self.draw_vehicle_new(vehicle)
        else:
            for road in self.sim.roads:
                # Draw vehicles
                for vehicle in road.vehicles:
                    self.draw_vehicle(vehicle, road)

    def draw_signals(self):
        for signal in self.sim.traffic_signals:
            for i in range(len(signal.roads)):
                color = (0, 255, 0) if signal.current_cycle[i] else (255, 0, 0)
                for road in signal.roads[i]:
                    a = 0
                    position = (
                        (1 - a) * road.end[0] + a * road.start[0],
                        (1 - a) * road.end[1] + a * road.start[1]
                    )
                    self.rotated_box(
                        position,
                        (1, 3),
                        cos=road.angle_cos, sin=road.angle_sin,
                        color=color)

    def draw_status(self):
        text_fps = self.text_font.render(f't={self.sim.t:.5}', False, (0, 0, 0))
        text_frc = self.text_font.render(f'n={self.sim.frame_count}', False, (0, 0, 0))

        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_frc, (100, 0))

    def draw_traffic_flow_button(self):
        if len(self.sim.generators) == 0:
            return
        # to draw buttons
        if self.traffic_flow_button.draw(self.screen, self.sim.generators[0], self.text_font):
            print('flow')

    def draw_vehicle_velocity_button(self):
        if len(self.sim.generators) == 0:
            return
        # to draw buttons
        if self.vehicle_velocity_button.draw(self.screen, self.sim.generators[0], self.text_font):
            print('velocity')

    def draw_light_2lane_button(self):
        # to draw buttons
        if self.light_2lane_button.draw(self.screen, self.sim, self.text_font):
            print('light2lane')
            self.sim = Simulation()

            # Play with these
            n = 15
            a = 2
            b = 12
            l = 300

            # Nodes
            WEST_RIGHT_START = (-b - l, a)
            WEST_LEFT_START = (-b - l, -a)

            SOUTH_RIGHT_START = (a, b + l)
            SOUTH_LEFT_START = (-a, b + l)

            EAST_RIGHT_START = (b + l, -a)
            EAST_LEFT_START = (b + l, a)

            NORTH_RIGHT_START = (-a, -b - l)
            NORTH_LEFT_START = (a, -b - l)

            WEST_RIGHT = (-b, a)
            WEST_LEFT = (-b, -a)

            SOUTH_RIGHT = (a, b)
            SOUTH_LEFT = (-a, b)

            EAST_RIGHT = (b, -a)
            EAST_LEFT = (b, a)

            NORTH_RIGHT = (-a, -b)
            NORTH_LEFT = (a, -b)

            # Roads
            WEST_INBOUND = (WEST_RIGHT_START, WEST_RIGHT)
            SOUTH_INBOUND = (SOUTH_RIGHT_START, SOUTH_RIGHT)
            EAST_INBOUND = (EAST_RIGHT_START, EAST_RIGHT)
            NORTH_INBOUND = (NORTH_RIGHT_START, NORTH_RIGHT)

            WEST_OUTBOUND = (WEST_LEFT, WEST_LEFT_START)
            SOUTH_OUTBOUND = (SOUTH_LEFT, SOUTH_LEFT_START)
            EAST_OUTBOUND = (EAST_LEFT, EAST_LEFT_START)
            NORTH_OUTBOUND = (NORTH_LEFT, NORTH_LEFT_START)

            WEST_STRAIGHT = (WEST_RIGHT, EAST_LEFT)
            SOUTH_STRAIGHT = (SOUTH_RIGHT, NORTH_LEFT)
            EAST_STRAIGHT = (EAST_RIGHT, WEST_LEFT)
            NORTH_STRAIGHT = (NORTH_RIGHT, SOUTH_LEFT)

            WEST_RIGHT_TURN = turn_road(WEST_RIGHT, SOUTH_LEFT, TURN_RIGHT, n)
            WEST_LEFT_TURN = turn_road(WEST_RIGHT, NORTH_LEFT, TURN_LEFT, n)

            SOUTH_RIGHT_TURN = turn_road(SOUTH_RIGHT, EAST_LEFT, TURN_RIGHT, n)
            SOUTH_LEFT_TURN = turn_road(SOUTH_RIGHT, WEST_LEFT, TURN_LEFT, n)

            EAST_RIGHT_TURN = turn_road(EAST_RIGHT, NORTH_LEFT, TURN_RIGHT, n)
            EAST_LEFT_TURN = turn_road(EAST_RIGHT, SOUTH_LEFT, TURN_LEFT, n)

            NORTH_RIGHT_TURN = turn_road(NORTH_RIGHT, WEST_LEFT, TURN_RIGHT, n)
            NORTH_LEFT_TURN = turn_road(NORTH_RIGHT, EAST_LEFT, TURN_LEFT, n)

            self.sim.create_roads([
                WEST_INBOUND,
                SOUTH_INBOUND,
                EAST_INBOUND,
                NORTH_INBOUND,

                WEST_OUTBOUND,
                SOUTH_OUTBOUND,
                EAST_OUTBOUND,
                NORTH_OUTBOUND,

                WEST_STRAIGHT,
                SOUTH_STRAIGHT,
                EAST_STRAIGHT,
                NORTH_STRAIGHT,

                *WEST_RIGHT_TURN,
                *WEST_LEFT_TURN,

                *SOUTH_RIGHT_TURN,
                *SOUTH_LEFT_TURN,

                *EAST_RIGHT_TURN,
                *EAST_LEFT_TURN,

                *NORTH_RIGHT_TURN,
                *NORTH_LEFT_TURN
            ])

            def road(a): return range(a, a + n)

            self.sim.create_gen({
                'vehicle_rate': 30,
                'vehicles': [
                    [3, {'path': [0, 8, 6]}],
                    [1, {'path': [0, *road(12), 5]}],
                    [1, {'path': [0, *road(12 + n), 7]}],

                    [3, {'path': [1, 9, 7]}],
                    [1, {'path': [1, *road(12 + 2 * n), 6]}],
                    [1, {'path': [1, *road(12 + 3 * n), 4]}],

                    [3, {'path': [2, 10, 4]}],
                    [1, {'path': [2, *road(12 + 4 * n), 7]}],
                    [1, {'path': [2, *road(12 + 5 * n), 5]}],

                    [3, {'path': [3, 11, 5]}],
                    [1, {'path': [3, *road(12 + 6 * n), 4]}],
                    [1, {'path': [3, *road(12 + 7 * n), 6]}]
                ]})

            self.sim.create_signal([[0, 2], [1, 3]])

    def draw_smart_2lane_button(self):
        if self.smart_2lane_button.draw(self.screen, self.sim, self.text_font):
            print('smart2lane')
            self.sim = Simulation()

            # Play with these
            n = 15
            a = 2
            b = 12
            l = 300

            # Nodes
            WEST_RIGHT_START = (-b - l, a)
            WEST_LEFT_START = (-b - l, -a)

            SOUTH_RIGHT_START = (a, b + l)
            SOUTH_LEFT_START = (-a, b + l)

            EAST_RIGHT_START = (b + l, -a)
            EAST_LEFT_START = (b + l, a)

            NORTH_RIGHT_START = (-a, -b - l)
            NORTH_LEFT_START = (a, -b - l)

            WEST_RIGHT = (-b, a)
            WEST_LEFT = (-b, -a)

            SOUTH_RIGHT = (a, b)
            SOUTH_LEFT = (-a, b)

            EAST_RIGHT = (b, -a)
            EAST_LEFT = (b, a)

            NORTH_RIGHT = (-a, -b)
            NORTH_LEFT = (a, -b)

            # Roads
            WEST_INBOUND = (WEST_RIGHT_START, WEST_RIGHT)
            SOUTH_INBOUND = (SOUTH_RIGHT_START, SOUTH_RIGHT)
            EAST_INBOUND = (EAST_RIGHT_START, EAST_RIGHT)
            NORTH_INBOUND = (NORTH_RIGHT_START, NORTH_RIGHT)

            WEST_OUTBOUND = (WEST_LEFT, WEST_LEFT_START)
            SOUTH_OUTBOUND = (SOUTH_LEFT, SOUTH_LEFT_START)
            EAST_OUTBOUND = (EAST_LEFT, EAST_LEFT_START)
            NORTH_OUTBOUND = (NORTH_LEFT, NORTH_LEFT_START)

            WEST_STRAIGHT = (WEST_RIGHT, EAST_LEFT)
            SOUTH_STRAIGHT = (SOUTH_RIGHT, NORTH_LEFT)
            EAST_STRAIGHT = (EAST_RIGHT, WEST_LEFT)
            NORTH_STRAIGHT = (NORTH_RIGHT, SOUTH_LEFT)

            WEST_RIGHT_TURN = turn_road(WEST_RIGHT, SOUTH_LEFT, TURN_RIGHT, n)
            WEST_LEFT_TURN = turn_road(WEST_RIGHT, NORTH_LEFT, TURN_LEFT, n)

            SOUTH_RIGHT_TURN = turn_road(SOUTH_RIGHT, EAST_LEFT, TURN_RIGHT, n)
            SOUTH_LEFT_TURN = turn_road(SOUTH_RIGHT, WEST_LEFT, TURN_LEFT, n)

            EAST_RIGHT_TURN = turn_road(EAST_RIGHT, NORTH_LEFT, TURN_RIGHT, n)
            EAST_LEFT_TURN = turn_road(EAST_RIGHT, SOUTH_LEFT, TURN_LEFT, n)

            NORTH_RIGHT_TURN = turn_road(NORTH_RIGHT, WEST_LEFT, TURN_RIGHT, n)
            NORTH_LEFT_TURN = turn_road(NORTH_RIGHT, EAST_LEFT, TURN_LEFT, n)

            self.sim.create_roads([
                WEST_INBOUND,
                SOUTH_INBOUND,
                EAST_INBOUND,
                NORTH_INBOUND,

                WEST_OUTBOUND,
                SOUTH_OUTBOUND,
                EAST_OUTBOUND,
                NORTH_OUTBOUND,

                WEST_STRAIGHT,
                SOUTH_STRAIGHT,
                EAST_STRAIGHT,
                NORTH_STRAIGHT,

                *WEST_RIGHT_TURN,
                *WEST_LEFT_TURN,

                *SOUTH_RIGHT_TURN,
                *SOUTH_LEFT_TURN,

                *EAST_RIGHT_TURN,
                *EAST_LEFT_TURN,

                *NORTH_RIGHT_TURN,
                *NORTH_LEFT_TURN
            ])

            def road(a): return range(a, a + n)

            self.sim.create_gen({
                'vehicle_rate': 30,
                'vehicles': [
                    [3, {'path': [0, 8, 6]}],
                    [1, {'path': [0, *road(12), 5]}],
                    [1, {'path': [0, *road(12 + n), 7]}],

                    [3, {'path': [1, 9, 7]}],
                    [1, {'path': [1, *road(12 + 2 * n), 6]}],
                    [1, {'path': [1, *road(12 + 3 * n), 4]}],

                    [3, {'path': [2, 10, 4]}],
                    [1, {'path': [2, *road(12 + 4 * n), 7]}],
                    [1, {'path': [2, *road(12 + 5 * n), 5]}],

                    [3, {'path': [3, 11, 5]}],
                    [1, {'path': [3, *road(12 + 6 * n), 4]}],
                    [1, {'path': [3, *road(12 + 7 * n), 6]}]
                ]})

    def draw_smart_4lane_button(self):
        if self.smart_4lane_button.draw(self.screen, self.sim, self.text_font):
            print('smart4lane')
            self.sim = Simulation()

            # Play with these
            n = 15
            a = 2
            b = 12
            l = 300

            # Nodes
            WEST_RIGHT_START = (-b - l, a)
            WEST_LEFT_START = (-b - l, -a)

            SOUTH_RIGHT_START = (a, b + l)
            SOUTH_LEFT_START = (-a, b + l)

            EAST_RIGHT_START = (b + l, -a)
            EAST_LEFT_START = (b + l, a)

            NORTH_RIGHT_START = (-a, -b - l)
            NORTH_LEFT_START = (a, -b - l)

            WEST_RIGHT = (-b, a)
            WEST_LEFT = (-b, -a)

            SOUTH_RIGHT = (a, b)
            SOUTH_LEFT = (-a, b)

            EAST_RIGHT = (b, -a)
            EAST_LEFT = (b, a)

            NORTH_RIGHT = (-a, -b)
            NORTH_LEFT = (a, -b)

            WEST_RIGHT_START_1 = (-b - l, 3 * a)
            WEST_LEFT_START_1 = (-b - l, -3 * a)
            SOUTH_RIGHT_START_1 = (3 * a, b + l)
            SOUTH_LEFT_START_1 = (-3 * a, b + l)
            EAST_RIGHT_START_1 = (b + l, -3 * a)
            EAST_LEFT_START_1 = (b + l, 3 * a)
            NORTH_RIGHT_START_1 = (-3 * a, -b - l)
            NORTH_LEFT_START_1 = (3 * a, -b - l)

            WEST_RIGHT_1 = (-b, 3 * a)
            WEST_LEFT_1 = (-b, -3 * a)
            SOUTH_RIGHT_1 = (3 * a, b)
            SOUTH_LEFT_1 = (-3 * a, b)
            EAST_RIGHT_1 = (b, -3 * a)
            EAST_LEFT_1 = (b, 3 * a)
            NORTH_RIGHT_1 = (-3 * a, -b)
            NORTH_LEFT_1 = (3 * a, -b)

            # Roads
            WEST_INBOUND = (WEST_RIGHT_START, WEST_RIGHT)
            SOUTH_INBOUND = (SOUTH_RIGHT_START, SOUTH_RIGHT)
            EAST_INBOUND = (EAST_RIGHT_START, EAST_RIGHT)
            NORTH_INBOUND = (NORTH_RIGHT_START, NORTH_RIGHT)

            WEST_OUTBOUND = (WEST_LEFT, WEST_LEFT_START)
            SOUTH_OUTBOUND = (SOUTH_LEFT, SOUTH_LEFT_START)
            EAST_OUTBOUND = (EAST_LEFT, EAST_LEFT_START)
            NORTH_OUTBOUND = (NORTH_LEFT, NORTH_LEFT_START)

            WEST_STRAIGHT = (WEST_RIGHT, EAST_LEFT)
            SOUTH_STRAIGHT = (SOUTH_RIGHT, NORTH_LEFT)
            EAST_STRAIGHT = (EAST_RIGHT, WEST_LEFT)
            NORTH_STRAIGHT = (NORTH_RIGHT, SOUTH_LEFT)

            WEST_STRAIGHT_1 = (WEST_RIGHT_1, EAST_LEFT_1)
            SOUTH_STRAIGHT_1 = (SOUTH_RIGHT_1, NORTH_LEFT_1)
            EAST_STRAIGHT_1 = (EAST_RIGHT_1, WEST_LEFT_1)
            NORTH_STRAIGHT_1 = (NORTH_RIGHT_1, SOUTH_LEFT_1)

            WEST_RIGHT_TURN = turn_road(WEST_RIGHT_1, SOUTH_LEFT_1, TURN_RIGHT, n)
            WEST_LEFT_TURN = turn_road(WEST_RIGHT, NORTH_LEFT, TURN_LEFT, n)

            SOUTH_RIGHT_TURN = turn_road(SOUTH_RIGHT_1, EAST_LEFT_1, TURN_RIGHT, n)
            SOUTH_LEFT_TURN = turn_road(SOUTH_RIGHT, WEST_LEFT, TURN_LEFT, n)

            EAST_RIGHT_TURN = turn_road(EAST_RIGHT_1, NORTH_LEFT_1, TURN_RIGHT, n)
            EAST_LEFT_TURN = turn_road(EAST_RIGHT, SOUTH_LEFT, TURN_LEFT, n)

            NORTH_RIGHT_TURN = turn_road(NORTH_RIGHT_1, WEST_LEFT_1, TURN_RIGHT, n)
            NORTH_LEFT_TURN = turn_road(NORTH_RIGHT, EAST_LEFT, TURN_LEFT, n)

            WEST_INBOUND_1 = (WEST_RIGHT_START_1, WEST_RIGHT_1)
            SOUTH_INBOUND_1 = (SOUTH_RIGHT_START_1, SOUTH_RIGHT_1)
            EAST_INBOUND_1 = (EAST_RIGHT_START_1, EAST_RIGHT_1)
            NORTH_INBOUND_1 = (NORTH_RIGHT_START_1, NORTH_RIGHT_1)

            WEST_OUTBOUND_1 = (WEST_LEFT_1, WEST_LEFT_START_1)
            SOUTH_OUTBOUND_1 = (SOUTH_LEFT_1, SOUTH_LEFT_START_1)
            EAST_OUTBOUND_1 = (EAST_LEFT_1, EAST_LEFT_START_1)
            NORTH_OUTBOUND_1 = (NORTH_LEFT_1, NORTH_LEFT_START_1)

            self.sim.create_roads([
                WEST_INBOUND,  # 0
                SOUTH_INBOUND,  # 1
                EAST_INBOUND,  # 2
                NORTH_INBOUND,  # 3

                WEST_OUTBOUND,  # 4
                SOUTH_OUTBOUND,  # 5
                EAST_OUTBOUND,  # 6
                NORTH_OUTBOUND,  # 7

                WEST_STRAIGHT,  # 8
                SOUTH_STRAIGHT,  # 9
                EAST_STRAIGHT,  # 10
                NORTH_STRAIGHT,  # 11

                WEST_INBOUND_1,  # 12
                SOUTH_INBOUND_1,  # 13
                EAST_INBOUND_1,  # 14
                NORTH_INBOUND_1,  # 15

                WEST_OUTBOUND_1,  # 16
                SOUTH_OUTBOUND_1,  # 17
                EAST_OUTBOUND_1,  # 18
                NORTH_OUTBOUND_1,  # 19

                *WEST_RIGHT_TURN,  # 20
                *WEST_LEFT_TURN,  # 20+1n

                *SOUTH_RIGHT_TURN,  # 20+2n
                *SOUTH_LEFT_TURN,  # 20+3n

                *EAST_RIGHT_TURN,  # 20+4n
                *EAST_LEFT_TURN,  # 20+5n

                *NORTH_RIGHT_TURN,  # 20+6n
                *NORTH_LEFT_TURN,  # 20+7n

                WEST_STRAIGHT_1,
                SOUTH_STRAIGHT_1,
                EAST_STRAIGHT_1,
                NORTH_STRAIGHT_1
            ])

            def road(a):
                return range(a, a + n)

            self.sim.create_gen({
                'vehicle_rate': 10,
                'vehicles': [
                    # straight
                    [3, {'path': [0, 8, 6]}],
                    [3, {'path': [1, 9, 7]}],
                    [3, {'path': [2, 10, 4]}],
                    [3, {'path': [3, 11, 5]}],

                    [1, {'path': [12, *road(20), 17]}],
                    [1, {'path': [0, *road(20 + n), 7]}],

                    [1, {'path': [13, *road(20 + 2 * n), 18]}],
                    [1, {'path': [1, *road(20 + 3 * n), 4]}],

                    [1, {'path': [14, *road(20 + 4 * n), 19]}],
                    [1, {'path': [2, *road(20 + 5 * n), 5]}],

                    [1, {'path': [15, *road(20 + 6 * n), 16]}],
                    [1, {'path': [3, *road(20 + 7 * n), 6]}],

                ]})

    def draw_light_4lane_button(self):
        if self.light_4lane_button.draw(self.screen, self.sim, self.text_font):
            print('light4lane')
            self.sim = Simulation()

            # Play with these
            n = 15
            a = 2
            b = 12
            l = 300

            # Nodes
            WEST_RIGHT_START = (-b - l, a)
            WEST_LEFT_START = (-b - l, -a)

            SOUTH_RIGHT_START = (a, b + l)
            SOUTH_LEFT_START = (-a, b + l)

            EAST_RIGHT_START = (b + l, -a)
            EAST_LEFT_START = (b + l, a)

            NORTH_RIGHT_START = (-a, -b - l)
            NORTH_LEFT_START = (a, -b - l)

            WEST_RIGHT = (-b, a)
            WEST_LEFT = (-b, -a)

            SOUTH_RIGHT = (a, b)
            SOUTH_LEFT = (-a, b)

            EAST_RIGHT = (b, -a)
            EAST_LEFT = (b, a)

            NORTH_RIGHT = (-a, -b)
            NORTH_LEFT = (a, -b)

            WEST_RIGHT_START_1 = (-b - l, 3 * a)
            WEST_LEFT_START_1 = (-b - l, -3 * a)
            SOUTH_RIGHT_START_1 = (3 * a, b + l)
            SOUTH_LEFT_START_1 = (-3 * a, b + l)
            EAST_RIGHT_START_1 = (b + l, -3 * a)
            EAST_LEFT_START_1 = (b + l, 3 * a)
            NORTH_RIGHT_START_1 = (-3 * a, -b - l)
            NORTH_LEFT_START_1 = (3 * a, -b - l)

            WEST_RIGHT_1 = (-b, 3 * a)
            WEST_LEFT_1 = (-b, -3 * a)
            SOUTH_RIGHT_1 = (3 * a, b)
            SOUTH_LEFT_1 = (-3 * a, b)
            EAST_RIGHT_1 = (b, -3 * a)
            EAST_LEFT_1 = (b, 3 * a)
            NORTH_RIGHT_1 = (-3 * a, -b)
            NORTH_LEFT_1 = (3 * a, -b)

            # Roads
            WEST_INBOUND = (WEST_RIGHT_START, WEST_RIGHT)
            SOUTH_INBOUND = (SOUTH_RIGHT_START, SOUTH_RIGHT)
            EAST_INBOUND = (EAST_RIGHT_START, EAST_RIGHT)
            NORTH_INBOUND = (NORTH_RIGHT_START, NORTH_RIGHT)

            WEST_OUTBOUND = (WEST_LEFT, WEST_LEFT_START)
            SOUTH_OUTBOUND = (SOUTH_LEFT, SOUTH_LEFT_START)
            EAST_OUTBOUND = (EAST_LEFT, EAST_LEFT_START)
            NORTH_OUTBOUND = (NORTH_LEFT, NORTH_LEFT_START)

            WEST_STRAIGHT = (WEST_RIGHT, EAST_LEFT)
            SOUTH_STRAIGHT = (SOUTH_RIGHT, NORTH_LEFT)
            EAST_STRAIGHT = (EAST_RIGHT, WEST_LEFT)
            NORTH_STRAIGHT = (NORTH_RIGHT, SOUTH_LEFT)

            WEST_STRAIGHT_1 = (WEST_RIGHT_1, EAST_LEFT_1)
            SOUTH_STRAIGHT_1 = (SOUTH_RIGHT_1, NORTH_LEFT_1)
            EAST_STRAIGHT_1 = (EAST_RIGHT_1, WEST_LEFT_1)
            NORTH_STRAIGHT_1 = (NORTH_RIGHT_1, SOUTH_LEFT_1)
            # WEST_RIGHT_TURN = turn_road(WEST_RIGHT, SOUTH_LEFT, TURN_RIGHT, n)
            # WEST_LEFT_TURN = turn_road(WEST_RIGHT, NORTH_LEFT, TURN_LEFT, n)
            #
            # SOUTH_RIGHT_TURN = turn_road(SOUTH_RIGHT, EAST_LEFT, TURN_RIGHT, n)
            # SOUTH_LEFT_TURN = turn_road(SOUTH_RIGHT, WEST_LEFT, TURN_LEFT, n)
            #
            # EAST_RIGHT_TURN = turn_road(EAST_RIGHT, NORTH_LEFT, TURN_RIGHT, n)
            # EAST_LEFT_TURN = turn_road(EAST_RIGHT, SOUTH_LEFT, TURN_LEFT, n)
            #
            # NORTH_RIGHT_TURN = turn_road(NORTH_RIGHT, WEST_LEFT, TURN_RIGHT, n)
            # NORTH_LEFT_TURN = turn_road(NORTH_RIGHT, EAST_LEFT, TURN_LEFT, n)

            WEST_RIGHT_TURN = turn_road(WEST_RIGHT_1, SOUTH_LEFT_1, TURN_RIGHT, n)
            WEST_LEFT_TURN = turn_road(WEST_RIGHT, NORTH_LEFT, TURN_LEFT, n)

            SOUTH_RIGHT_TURN = turn_road(SOUTH_RIGHT_1, EAST_LEFT_1, TURN_RIGHT, n)
            SOUTH_LEFT_TURN = turn_road(SOUTH_RIGHT, WEST_LEFT, TURN_LEFT, n)

            EAST_RIGHT_TURN = turn_road(EAST_RIGHT_1, NORTH_LEFT_1, TURN_RIGHT, n)
            EAST_LEFT_TURN = turn_road(EAST_RIGHT, SOUTH_LEFT, TURN_LEFT, n)

            NORTH_RIGHT_TURN = turn_road(NORTH_RIGHT_1, WEST_LEFT_1, TURN_RIGHT, n)
            NORTH_LEFT_TURN = turn_road(NORTH_RIGHT, EAST_LEFT, TURN_LEFT, n)

            WEST_INBOUND_1 = (WEST_RIGHT_START_1, WEST_RIGHT_1)
            SOUTH_INBOUND_1 = (SOUTH_RIGHT_START_1, SOUTH_RIGHT_1)
            EAST_INBOUND_1 = (EAST_RIGHT_START_1, EAST_RIGHT_1)
            NORTH_INBOUND_1 = (NORTH_RIGHT_START_1, NORTH_RIGHT_1)

            WEST_OUTBOUND_1 = (WEST_LEFT_1, WEST_LEFT_START_1)
            SOUTH_OUTBOUND_1 = (SOUTH_LEFT_1, SOUTH_LEFT_START_1)
            EAST_OUTBOUND_1 = (EAST_LEFT_1, EAST_LEFT_START_1)
            NORTH_OUTBOUND_1 = (NORTH_LEFT_1, NORTH_LEFT_START_1)

            self.sim.create_roads([
                WEST_INBOUND,  # 0
                SOUTH_INBOUND,  # 1
                EAST_INBOUND,  # 2
                NORTH_INBOUND,  # 3

                WEST_OUTBOUND,  # 4
                SOUTH_OUTBOUND,  # 5
                EAST_OUTBOUND,  # 6
                NORTH_OUTBOUND,  # 7

                WEST_STRAIGHT,  # 8
                SOUTH_STRAIGHT,  # 9
                EAST_STRAIGHT,  # 10
                NORTH_STRAIGHT,  # 11

                WEST_INBOUND_1,  # 12
                SOUTH_INBOUND_1,  # 13
                EAST_INBOUND_1,  # 14
                NORTH_INBOUND_1,  # 15

                WEST_OUTBOUND_1,  # 16
                SOUTH_OUTBOUND_1,  # 17
                EAST_OUTBOUND_1,  # 18
                NORTH_OUTBOUND_1,  # 19

                *WEST_RIGHT_TURN,  # 20
                *WEST_LEFT_TURN,  # 20+1n

                *SOUTH_RIGHT_TURN,  # 20+2n
                *SOUTH_LEFT_TURN,  # 20+3n

                *EAST_RIGHT_TURN,  # 20+4n
                *EAST_LEFT_TURN,  # 20+5n

                *NORTH_RIGHT_TURN,  # 20+6n
                *NORTH_LEFT_TURN,  # 20+7n

                WEST_STRAIGHT_1,
                SOUTH_STRAIGHT_1,
                EAST_STRAIGHT_1,
                NORTH_STRAIGHT_1
            ])

            def road(a):
                return range(a, a + n)

            self.sim.create_gen({
                'vehicle_rate': 10,
                'vehicles': [
                    # straight
                    [3, {'path': [0, 8, 6]}],
                    [3, {'path': [1, 9, 7]}],
                    [3, {'path': [2, 10, 4]}],
                    [3, {'path': [3, 11, 5]}],

                    [1, {'path': [12, *road(20), 17]}],
                    [1, {'path': [0, *road(20 + n), 7]}],

                    [1, {'path': [13, *road(20 + 2 * n), 18]}],
                    [1, {'path': [1, *road(20 + 3 * n), 4]}],

                    [1, {'path': [14, *road(20 + 4 * n), 19]}],
                    [1, {'path': [2, *road(20 + 5 * n), 5]}],

                    [1, {'path': [15, *road(20 + 6 * n), 16]}],
                    [1, {'path': [3, *road(20 + 7 * n), 6]}],

                ]})
            self.sim.create_signal([[0, 2], [1, 3]])
            self.sim.create_signal([[12, 14], [13, 15]])

    def draw_round_button(self):
        if self.round_button.draw(self.screen, self.sim, self.text_font):
            print('round_lane')
            self.sim = Simulation()

            # Play with these
            n = 15
            a = 2
            b = 20
            c = 5
            r = 10
            l = 300

            # Nodes
            WEST_RIGHT_START = (-b - l, a - c)
            WEST_LEFT_START = (-b - l, -a - c)

            SOUTH_RIGHT_START = (a - c, b + l)
            SOUTH_LEFT_START = (-a - c, b + l)

            EAST_RIGHT_START = (b + l, -a + c)
            EAST_LEFT_START = (b + l, a + c)

            NORTH_RIGHT_START = (-a + c, -b - l)
            NORTH_LEFT_START = (a + c, -b - l)

            WEST_RIGHT = (-b, a - c)
            WEST_LEFT = (-b, -a - c)

            SOUTH_RIGHT = (a - c, b)
            SOUTH_LEFT = (-a - c, b)

            EAST_RIGHT = (b, -a + c)
            EAST_LEFT = (b, a + c)

            NORTH_RIGHT = (-a + c, -b)
            NORTH_LEFT = (a + c, -b)

            WEST = (-r, c)
            SOUTH = (c, r)
            EAST = (r, -c)
            NORTH = (-c, -r)

            # Roads
            WEST_INBOUND = (WEST_RIGHT_START, WEST_RIGHT)
            SOUTH_INBOUND = (SOUTH_RIGHT_START, SOUTH_RIGHT)
            EAST_INBOUND = (EAST_RIGHT_START, EAST_RIGHT)
            NORTH_INBOUND = (NORTH_RIGHT_START, NORTH_RIGHT)

            WEST_OUTBOUND = (WEST_LEFT, WEST_LEFT_START)
            SOUTH_OUTBOUND = (SOUTH_LEFT, SOUTH_LEFT_START)
            EAST_OUTBOUND = (EAST_LEFT, EAST_LEFT_START)
            NORTH_OUTBOUND = (NORTH_LEFT, NORTH_LEFT_START)

            WEST_LEFT_TURN = (NORTH, WEST_LEFT)
            SOUTH_LEFT_TURN = (WEST, SOUTH_LEFT)
            EAST_LEFT_TURN = (SOUTH, EAST_LEFT)
            NORTH_LEFT_TURN = (EAST, NORTH_LEFT)

            WEST_RIGHT_TURN = curve_road(WEST_RIGHT, WEST, (WEST[0], WEST_RIGHT[1]), resolution=n)
            SOUTH_RIGHT_TURN = curve_road(SOUTH_RIGHT, SOUTH, (SOUTH_RIGHT[0], SOUTH[1]), resolution=n)
            EAST_RIGHT_TURN = curve_road(EAST_RIGHT, EAST, (EAST[0], EAST_RIGHT[1]), resolution=n)
            NORTH_RIGHT_TURN = curve_road(NORTH_RIGHT, NORTH, (NORTH_RIGHT[0], NORTH[1]), resolution=n)

            WEST_SOUTH = curve_road(WEST, SOUTH, (WEST[0], SOUTH[1]), resolution=n)
            SOUTH_EAST = curve_road(SOUTH, EAST, (EAST[0], SOUTH[1]), resolution=n)
            EAST_NORTH = curve_road(EAST, NORTH, (EAST[0], NORTH[1]), resolution=n)
            NORTH_WEST = curve_road(NORTH, WEST, (WEST[0], NORTH[1]), resolution=n)

            self.sim.create_roads([
                WEST_INBOUND,
                SOUTH_INBOUND,
                EAST_INBOUND,
                NORTH_INBOUND,

                WEST_OUTBOUND,
                SOUTH_OUTBOUND,
                EAST_OUTBOUND,
                NORTH_OUTBOUND,

                WEST_LEFT_TURN,
                SOUTH_LEFT_TURN,
                EAST_LEFT_TURN,
                NORTH_LEFT_TURN,

                *WEST_RIGHT_TURN,
                *SOUTH_RIGHT_TURN,
                *EAST_RIGHT_TURN,
                *NORTH_RIGHT_TURN,

                *WEST_SOUTH,
                *SOUTH_EAST,
                *EAST_NORTH,
                *NORTH_WEST
            ])

            def road(a): return range(a, a + n)

            self.sim.create_gen({
                'vehicle_rate': 30,
                'vehicles': [
                    [2, {'path': [0, *road(12), *road(12 + 4 * n), 10, 6]}],
                    [1, {'path': [0, *road(12), 9, 5]}],
                    [1, {'path': [0, *road(12), *road(12 + 4 * n), *road(12 + 5 * n), 11, 7]}],

                    [2, {'path': [1, *road(12 + n), *road(12 + 5 * n), 11, 7]}],
                    [1, {'path': [1, *road(12 + n), 10, 6]}],
                    [1, {'path': [1, *road(12 + n), *road(12 + 5 * n), *road(12 + 6 * n), 8, 4]}],

                    [2, {'path': [2, *road(12 + 2 * n), *road(12 + 6 * n), 8, 4]}],
                    [1, {'path': [2, *road(12 + 2 * n), 11, 7]}],
                    [1, {'path': [2, *road(12 + 2 * n), *road(12 + 6 * n), *road(12 + 7 * n), 9, 5]}],

                    [2, {'path': [3, *road(12 + 3 * n), *road(12 + 7 * n), 9, 5]}],
                    [1, {'path': [3, *road(12 + 3 * n), 8, 4]}],
                    [1, {'path': [3, *road(12 + 3 * n), *road(12 + 7 * n), *road(12 + 4 * n), 10, 6]}],

                ]
            })

    def draw(self):
        # Fill background
        self.background(*self.bg_color)

        # Major and minor grid and axes
        # self.draw_grid(10, (220,220,220))
        # self.draw_grid(100, (200,200,200))
        # self.draw_axes()

        self.draw_roads()
        self.draw_vehicles()
        self.draw_signals()

        # Draw status info
        self.draw_status()

        # to draw buttons
        self.draw_traffic_flow_button()
        self.draw_vehicle_velocity_button()
        self.draw_light_2lane_button()
        self.draw_light_4lane_button()
        self.draw_smart_2lane_button()
        self.draw_smart_4lane_button()
        self.draw_round_button()