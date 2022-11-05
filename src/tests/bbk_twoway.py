from src.trafficSimulator import *

# Create simulation
sim = Simulation()

n = 15
a = 4  # road width， const
l = 150  # road length which is half screen length

EAST_INBOUND = ((a + l, 0), (2 * a, 0))
WEST_OUTBOUND = ((0, 0), (-l, 0))

WEST_INBOUND = ((-l, a), (0, a))
EAST_OUTBOUND = ((2 * a, a), (a + l, a))

SOUTH_INBOUND = ((3 * a / 2, l), (3 * a / 2, 3 * a / 2))
NORTH_OUTBOUND = ((3 * a / 2, -a / 2), (3 * a / 2, -l))

SOUTH_OUTBOUND = ((a / 2, 3 * a / 2), (a / 2, l))
NORTH_INBOUND = ((a / 2, -l), (a / 2, -a / 2))

buffer_1 = ((0, 0), (a, 0))
buffer_1_left = ((a, 0), (0, 0))
buffer_1_down = ((a / 2, -a / 2), (a / 2, a / 2))

buffer_2 = ((a, 0), (2 * a, 0))
buffer_2_left = ((2 * a, 0), (a, 0),)
buffer_2_up = ((3 * a / 2, a / 2), (3 * a / 2, -a / 2))

buffer_3 = ((0, a), (a, a))
buffer_3_down = ((a / 2, a / 2), (a / 2, 3 * a / 2))

buffer_4 = ((a, a), (2 * a, a))
buffer_4_up = ((3 * a / 2, 3 * a / 2), (3 * a / 2, a / 2))

# Add multiple roads
sim.create_roads([
    WEST_INBOUND,
    buffer_3,
    buffer_4,
    EAST_OUTBOUND,

    SOUTH_INBOUND,
    buffer_4_up,
    buffer_2_up,
    NORTH_OUTBOUND,

    EAST_INBOUND,
    buffer_2_left,
    buffer_1_left,
    WEST_OUTBOUND,

    NORTH_INBOUND,
    buffer_1_down,
    buffer_3_down,
    SOUTH_OUTBOUND,
])

# add cars
sim.create_gen({
    'vehicle_rate': 40,
    'vehicles': [
        [1, {"path": [0, 1, 2, 3]}],
        [1, {"path": [4, 5, 6, 7]}],
        [1, {"path": [8, 9, 10, 11]}],
        [1, {"path": [12, 13, 14, 15]}]
    ]
})

sim.create_signal([[0, 8], [4, 12]], {'stop_distance': 18, 'slow_distance': 30, 'hide_signal': True})

# Start simulation
win = Window(sim)
win.zoom = 10
win.run(steps_per_update=5)
