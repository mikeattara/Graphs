from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


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
# traversal_path = ['n', 'n']
traversal_path = []


def dft(room, visited, random_direction):
    # dft
    stack = []
    stack.append(player.current_room.id)
    is_dead_end = False

    while len(stack) > 0:
        v = stack.pop()
        if v not in visited:
            if player.current_room.id not in visited:

                # log directions with '?'
                visited[v] = {}
                for i in range(0, len(player.current_room.get_exits())):
                    visited[v][player.current_room.get_exits()[i]] = '?'

                if random_direction in player.current_room.get_exits():
                    prev = player.current_room.id
                    # travels
                    player.travel(random_direction)

                    # logs the direction
                    visited[v][random_direction] = player.current_room.id
                    traversal_path.append(random_direction)
                else:
                    is_dead_end = True

                if random_direction == 'n':
                    visited[v]['s'] = prev
                if random_direction == 's':
                    visited[v]['n'] = prev
                if random_direction == 'e':
                    visited[v]['w'] = prev
                if random_direction == 'w':
                    visited[v]['e'] = prev

            for neighbor in room[v][1]:
                next = room[v][1][neighbor]
                stack.append(next)
    print(is_dead_end)
    # return is_dead_end


def traverse_path(room):
    """
    picks a random unexplored direction from the player's current room
    """
    # previous node
    prev = player.current_room.id
    # create traverseal graph
    visited = {}
    visited[0] = {}
    for i in range(0, len(player.current_room.get_exits())):
        visited[0][player.current_room.get_exits()[i]] = '?'

    random_direction = None
    # pick random unexplosed direction - picks next one on the list
    for direction in visited[player.current_room.id]:
        if visited[0][direction] == '?':
            random_direction = direction
            break

    """
    travels and logs that direction
    """

    # travels
    player.travel(random_direction)

    # logs the direction
    visited[0][random_direction] = player.current_room.id
    traversal_path.append(random_direction)

    """
    loops
    """

    # while len(visited) != len(room):

    # dft(room, visited, random_direction)

    # bfs
    visited = set()
    queue = Queue()
    queue.enqueue([player.current_room.id])
    while queue.size() > 0:
        path = queue.dequeue()
        v = path[-1]
        if v not in visited:
            visited.add(v)

            for exit in g[v]:
                if g[v][exit] == '?':
                    return path
            for neighbor in room[v][1]:
                new_path = [*path, neighbor]
                queue.enqueue(new_path)


g = {}

while len(g) < len(room_graph):
    current = player.current_room.id
    print(current)
    if current not in g:
        g[current] = current

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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
