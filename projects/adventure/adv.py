from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


# Logic for sprint 

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def peek(self):
        return self.stack[-1]
    def size(self):
        return len(self.stack)

def traverse_maze(player):
    # What we will return
    traversal_path = []  # List of tuples
    
    opposite_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

    # rooms we have visited and rooms ahead
    visited_rooms = set() 
    s = Stack()

    cur_room = player.current_room

    # added two initially because I instantly pop one. Probably not good practice.
    # s.push(cur_room) # current, room and direction traveled

    while len(visited_rooms) != 500:
        # Cur room id

        if cur_room.id not in visited_rooms:
            visited_rooms.add(cur_room.id)

        prev_room = cur_room

        # choose a direction
        for direction in cur_room.get_exits():
            if cur_room.get_room_in_direction(direction).id not in visited_rooms: 
                # updates
                s.push(opposite_direction[direction])
                player.travel(direction)
                traversal_path.append(direction)
                visited_rooms.add(player.current_room.id)

                cur_room = player.current_room
                break # so we don't actually loop over the other exits. Just the first unexplored
        
        # This is what makes us traverse. Means it wasn't updated in loop above.
        if cur_room == prev_room:
            direction = s.pop()
            player.travel(direction)
            traversal_path.append(direction)

            cur_room = player.current_room


        # Choose a random direction to travse
            # keep track of forks in the road, so when we get to a dead end we can traverse to an unexplored fork

    return list(traversal_path)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = traverse_maze(player)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
