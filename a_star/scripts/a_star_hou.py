import hou
import math
import sys

sys.path.append("/Users/vineetvijaykumar/rebelway/rebelwayAppliedML/a_star/scripts/")

from a_star import AStarPathFinding


def get_maze_from_grid():
    grid = hou.pwd().parm('grid_path').eval()
    geo = hou.node(grid).geometry()

    prims = geo.prims()
    num_rows = num_columns = int(math.sqrt(len(prims)))

    grid_matrix = []

    for row in range(num_rows):
        new_row = []
        for col in range(num_columns):
            prim_index = row * num_columns + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")
            new_row.append(1 if color == (1.0, 1.0, 1.0) else 0)
        grid_matrix.append(new_row)

    return grid_matrix


def position_object(obj_path, row, col, cell_size=1):
    main_char = hou.node(obj_path)
    world_x = col * cell_size
    world_z = row * cell_size

    center = main_char.parmTuple("t").eval()
    main_char.parmTuple("t").set((world_x, 0, world_z))
    pos = (row, col)
    return pos

def get_npc_grid_position(npc_path, cell_size=1):
    npc_node = hou.node(npc_path)
    if not npc_node:
        raise ValueError("Invalid NPC path")

    world_x, world_y, world_z = npc_node.parmTuple("t").eval()
    col = int(round(world_x / cell_size))
    row = int(round(world_z / cell_size))

    return (row, col)

def solve_maze():
    node = hou.pwd()

    # Get character paths from HDA parms
    main_char_path = node.parm('main_char').eval()

    npc_paths = []
    i = 1
    while True:
        parm = node.parm(f'npc_{i}')
        if not parm:
            break  # Stop when there are no more npc_i parms
        npc_path = parm.eval()
        if npc_path:
            npc_paths.append(npc_path)
        i += 1
    print(f"Found {len(npc_paths)} NPCs.")
    #
    # npc_path = node.parm("npc_1").eval()

    for idx, npc_path in enumerate(npc_paths):
        # Define start and target positions in grid space
        npc_row, npc_col = get_npc_grid_position(npc_path)
        start_pos = position_object(npc_path, npc_row, npc_col, 1)  # row, col
        target_pos = position_object(main_char_path, 6, 1, 1)

        # Read maze from the grid
        maze = get_maze_from_grid()

        # Run A* algorithm
        pathFinder = AStarPathFinding(maze, start_pos, target_pos)
        path = pathFinder.find_path()

        if not path:
            print("Path not found.")
            return

        print("Path found:", path)

        # Animate NPC along the path
        npc_node = hou.node(npc_path)
        frame_start = hou.intFrame()
        frame_step = 4  # Frames between steps
        cell_size = 1

        print('npc path', npc_path)
        for i, (row, col) in enumerate(path):

            world_x = col * cell_size
            world_y = 0
            world_z = row * cell_size
            frame = frame_start + i * frame_step

            # Create and set stepped keyframes
            for axis, value in zip(("tx", "ty", "tz"), (world_x, world_y, world_z)):
                key = hou.Keyframe()
                key.setFrame(frame)
                key.setValue(value)
                key.setExpression('constant()')
                # stepped
                npc_node.parm(axis).setKeyframe(key)

            if (row, col) == target_pos:
                print(f"Reached target at step {i}. Stopping animation.")
                break
