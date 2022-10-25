from src.trafficSimulator import *

# Create simulation
sim = Simulation()

n = 15
a = 4  # road width
l = 150  # road length which is half screen length

buffer_1 = ((0, 0), (a, 0))
buffer_1_turn_left = ((a/2, a/2), (a/2, -a/2))
buffer_2 = ((a, 0), (2*a, 0))
buffer_3 = ((0, a), (a, a))
buffer_3_turn_left = ((a/2, 3*a/2), (a/2, a/2))
buffer_4 = ((a, a), (2*a, a))

WEST_RIGHT_TURN = turn_road((0, a), (a/2, 3*a/2), 1, n)
# Add multiple roads
sim.create_roads([
    # buffer_1_turn_left,
    buffer_2,
    WEST_RIGHT_TURN,
])

# Start simulation
win = Window(sim)
win.offset = (-20, -20)
win.run(steps_per_update=5)
