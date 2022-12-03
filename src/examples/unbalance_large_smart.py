from src.trafficSimulator import *


def smart_2lane_unbalance_large():
    # Play with these
    n = 15
    a = 2
    b = 10
    c = 40
    l = 90

    sim = Simulation(a,b,c)

    # Nodes
    WEST_RIGHT_START = (-b - l - c, a)
    WEST_LEFT_START = (-b - l - c, -a)

    SOUTH_RIGHT_START = (a, b + l + c)
    SOUTH_LEFT_START = (-a, b + l + c)

    EAST_RIGHT_START = (b + l + c, -a)
    EAST_LEFT_START = (b + l + c, a)

    NORTH_RIGHT_START = (-a, -b - l - c)
    NORTH_LEFT_START = (a, -b - l - c)

    WEST_RIGHT = (-b, a)
    WEST_LEFT = (-b, -a)

    SOUTH_RIGHT = (a, b)
    SOUTH_LEFT = (-a, b)

    EAST_RIGHT = (b, -a)
    EAST_LEFT = (b, a)

    NORTH_RIGHT = (-a, -b)
    NORTH_LEFT = (a, -b)

    WEST_BUFFER_START = (-b - c, a)
    SOUTH_BUFFER_START = (a, b + c)
    EAST_BUFFER_START = (b + c, -a)
    NORTH_BUFFER_START = (-a, -b - c)

    # Roads

    WEST_INBOUND = (WEST_RIGHT_START, WEST_BUFFER_START)
    SOUTH_INBOUND = (SOUTH_RIGHT_START, SOUTH_BUFFER_START)
    EAST_INBOUND = (EAST_RIGHT_START, EAST_BUFFER_START)
    NORTH_INBOUND = (NORTH_RIGHT_START, NORTH_BUFFER_START)

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

    WEST_BUFFER = (WEST_BUFFER_START, WEST_RIGHT)
    SOUTH_BUFFER = (SOUTH_BUFFER_START, SOUTH_RIGHT)
    EAST_BUFFER = (EAST_BUFFER_START, EAST_RIGHT)
    NORTH_BUFFER = (NORTH_BUFFER_START, NORTH_RIGHT)

    sim.create_roads([
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

        WEST_BUFFER,
        SOUTH_BUFFER,
        EAST_BUFFER,
        NORTH_BUFFER,

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

    sim.paths = [
        {
            'id': 1,
            'weight': 10,
            'roads': [0, 12, 8, 6],
            'collision_path' : [4,10,12,5,6,9],
            # 'length' : [l,c,2*b,b+c+l]
        },
        {
            'id': 2,
            'weight': 10,
            'roads': [0, 12,*road(16), 5],
            'buffer_index': 1,
            'road_without_collision': [0, 1],
            'collision_path': [10 ,9],
            # 'length': [l, c, 0.8, b + c + l]
        },
        {
            'id': 3,
            'weight': 10,
            'roads': [0, 12,*road(16 + n), 7],
            'collision_path': [4, 8, 6, 7]
        },
        {
            'id': 4,
            'weight': 3,
            'roads': [1, 13, 9, 7],
            'buffer_index': 1,
            'road_without_collision': [1, 13, 7],
            'collision_path': [1,7,3,9,8,12],
            'length': [l, c, 2 * b, b + c + l]
        },
        {
            'id': 5,
            'weight': 1,
            'roads': [1, 13, *road(16 + 2 * n), 6],
            'buffer': [13],
            'road_without_collision': [1, 13, 6],
            'collision_path': [1,12]
        },
        {
            'id': 6,
            'weight': 1,
            'roads': [1, 13, *road(16 + 3 * n), 4],
            'buffer': [13],
            'road_without_collision': [1, 13, 4],
            'collision_path': [7,9,10,11]
        },
        {
            'id': 7,
            'weight': 10,
            'roads': [2, 14, 10, 4],
            'buffer': [14],
            'road_without_collision': [2, 14, 4],
            'collision_path': [4,10,6,11,12,3],
            'length': [l, c, 2 * b, b + c + l]

        },
        {
            'id': 8,
            'weight': 10,
            'roads': [2, 14, *road(16 + 4 * n), 7],
            'buffer': [14],
            'road_without_collision': [2, 14, 7],
            'collision_path': [4,3]
        },
        {
            'id': 9,
            'weight': 10,
            'roads': [2, 14,*road(16 + 5 * n), 5],
            'buffer': [14],
            'road_without_collision': [2, 14, 5],
            'collision_path': [4,10,1,6]
        },
        {
            'id': 10,
            'weight': 3,
            'roads': [3, 15, 11, 5],
            'buffer': [15],
            'road_without_collision': [3, 15, 5],
            'collision_path': [7,1,9,2,3,6]
        },
        {
            'id': 11,
            'weight': 1,
            'roads': [3, 15, *road(16 + 6 * n), 4],
            'buffer': [15],
            'road_without_collision': [3, 15, 4],
            'collision_path': [7,6],
            'length': [l, c, 2 * b, b + c + l]
        },
        {
            'id': 12,
            'weight': 1,
            'roads': [3, 15, *road(16 + 7 * n), 6],
            'buffer': [15],
            'road_without_collision': [3, 15, 6],
            'collision_path': [7,1,4,9]
        }
    ]

    #sim.create_signal([[0, 2], [1, 3]])
    return sim


if __name__ == '__main__':
    # Start simulation
    win = Window(smart_2lane_unbalance_large())
    win.zoom = 10
    win.run(steps_per_update=10)
