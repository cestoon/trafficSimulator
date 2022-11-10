from src.trafficSimulator import *


def traffic_light_4lane():
    sim = Simulation()

    # Play with these
    n = 15
    a = 2
    b = 12
    l = 50

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

    sim.create_roads([
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


    def road(a): return range(a, a + n)


    sim.paths = [
        {
            'id': 1,
            'weight': 3,
            'roads': [0, 8, 6]
        },
        {
            'id': 2,
            'weight': 3,
            'roads': [1, 9, 7]
        },
        {
            'id': 3,
            'weight': 3,
            'roads': [2, 10, 4]
        },
        {
            'id': 4,
            'weight': 3,
            'roads': [3, 11, 5]
        },
        {
            'id': 5,
            'weight': 1,
            'roads': [12, *road(20), 17]
        },
        {
            'id': 6,
            'weight': 1,
            'roads': [0, *road(20 + n), 7]
        },
        {
            'id': 7,
            'weight': 1,
            'roads': [13, *road(20 + 2 * n), 18]
        },
        {
            'id': 8,
            'weight': 1,
            'roads': [1, *road(20 + 3 * n), 4]
        },
        {
            'id': 9,
            'weight': 1,
            'roads': [14, *road(20 + 4 * n), 19]
        },
        {
            'id': 10,
            'weight': 1,
            'roads': [2, *road(20 + 5 * n), 5]
        },
        {
            'id': 11,
            'weight': 1,
            'roads': [15, *road(20 + 6 * n), 16]
        },
        {
            'id': 12,
            'weight': 1,
            'roads': [3, *road(20 + 7 * n), 6]
        }
    ]

    sim.create_signal([[0, 2], [1, 3]])
    sim.create_signal([[12, 14], [13, 15]])

    return sim


if __name__ == '__main__':
    # Start simulation
    win = Window(traffic_light_4lane())
    win.zoom = 10
    win.run(steps_per_update=10)
