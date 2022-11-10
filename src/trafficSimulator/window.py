import numpy as np
import pygame
from src.trafficSimulator.button import traffic_flow_button, vehicle_velocity_button, scene_light_2lane_button, scence_round_button, scence_light_4lane_button, scence_smart_4lane_button,scence_smart_2lane_button
from src.trafficSimulator import Simulation, TURN_LEFT, TURN_RIGHT, turn_road, curve_road
# from vehicle_pool import VehiclePool
from pygame import gfxdraw
import os
from src.examples.roundabout import round_about
from src.examples.smart_2lane import smart_2lane
from src.examples.smart_4lane import smart_4lane
from src.examples.trafficlight_2lane import traffic_light_2lane
from src.examples.trafficlight_4lane import traffic_light_4lane


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
            if loop:
                loop(self.sim)

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

    def rotated_rect(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 250)):
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

        self.rotated_box((x, y), (l, h), cos=cos, sin=sin, centered=True, color=vehicle.color)

    def draw_vehicles(self):
        if len(self.sim.paths) > 0:
            for vehicle in self.sim.vehicle_pool.vehicle_pool_list:
                self.draw_vehicle_new(vehicle)
        else:
            for road in self.sim.roads:
                # Draw vehicles
                for vehicle in road.vehicles:
                    self.draw_vehicle(vehicle, road)

    def draw_summary(self):
        text_wait = self.text_font.render(f'Average Waiting Time={(self.sim.waittime-self.sim.besttime*self.sim.passingcars)}', False, (0, 0, 0))
        text_crash = self.text_font.render(f'Crash={self.sim.crashtime}', False, (0, 0, 0))
        text_throughput = self.text_font.render(f'Throughput={self.sim.throughput}', False, (0, 0, 0))
        text_besttime = self.text_font.render(f'Best Passing Time={self.sim.besttime}', False, (0, 0, 0))
        text_lasttime = self.text_font.render(f'Last Passing Time={self.sim.currentusage}', False, (0, 0, 0))
        text_passingeff=self.text_font.render(f'Passing Rate={(round(self.sim.throughput / (self.sim.t+0.001) * 60))}Per Minute', False, (0, 0, 0))
        self.screen.blit(text_wait, (1000,0 ))
        self.screen.blit(text_crash, (1000, 20))
        self.screen.blit(text_throughput, (1000, 40))
        self.screen.blit(text_besttime, (1000, 60))
        self.screen.blit(text_lasttime, (1000, 80))
        self.screen.blit(text_passingeff, (1000, 100))

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
        # to draw buttons
        if self.traffic_flow_button.draw(self.screen, self.sim.vehicle_pool, self.text_font):
            print('flow')

    def draw_vehicle_velocity_button(self):
        # to draw buttons
        if self.vehicle_velocity_button.draw(self.screen, self.sim.vehicle_pool, self.text_font):
            print('velocity')

    def draw_light_2lane_button(self):
        if self.light_2lane_button.draw(self.screen, self.sim, self.text_font):
            self.sim = traffic_light_2lane()

    def draw_smart_2lane_button(self):
        if self.smart_2lane_button.draw(self.screen, self.sim, self.text_font):
            self.sim = smart_2lane()

    def draw_smart_4lane_button(self):
        if self.smart_4lane_button.draw(self.screen, self.sim, self.text_font):
            self.sim = smart_4lane()

    def draw_light_4lane_button(self):
        if self.light_4lane_button.draw(self.screen, self.sim, self.text_font):
            self.sim = traffic_light_4lane()

    def draw_round_button(self):
        if self.round_button.draw(self.screen, self.sim, self.text_font):
            self.sim = round_about()

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
        self.draw_summary()