from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


def traverse(room, visited=set()):
    traversed_path = []

    # add starting room to visited set
    visited.add(room.id)

    # for each direction provided in room exits method
    for direction in room.get_exits():
        # move to that room and store in next_room
        next_room = room.get_room_in_direction(direction)

        # need reverse directions because they are opposite based on what appears on map visual
        reversed_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

        # if that room has not already been visited...
        if next_room.id not in visited:
            # recurse on that room
            next_room_path = traverse(next_room, visited)

            # after recursing, if valid direction path, store path
            if next_room_path:
                path = [direction] + next_room_path + \
                    [reversed_directions[direction]]
            # not valid path so reverse direction and store that path
            else:
                path = [direction, reversed_directions[direction]]
            # add path taken to traversed array
            traversed_path = traversed_path + path

    # return complete path to traversing the maze
    return traversed_path


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = traverse(player.current_room)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
