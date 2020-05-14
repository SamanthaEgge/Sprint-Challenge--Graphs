from room import Room
from player import Player
from world import World
from util import Queue, Stack

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
# print(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


## Map Dictionary
# this is a map of every room in the graph and the directions it has in order to use it to help with traversal while walking the maze
map_dict = {}

## Labyrinth String
# Add each step made through the maze, until no new directions available (and not pivot paths). Start at end of lab string and step back until stack direction is available
lab_string = []


## Cannot use stack??
# stack:{000, E}, {104, S}
# Dictionary? Stack?
# order to dictionary 
## This only provides n e s w, NOT room numbers




# TRAVERSAL TEST - DO NOT MODIFY
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

opposites = {
  'n': 's',
  'e': 'w',
  's': 'n',
  'w': 'e'
}

def discover_map():
  ## Need to discover every spot and direction on the map, so will be doing breadth first search
  # Back tracking method? I think this will only work with DFS
  discover_string = []
  # Create Queue, starting with first vertex
  queue = set()
  visited = set()


  prev_room = None
  direction_traveled = None
  
  while len(map_dict) < 500:
    ## Gets current set of exits
    exits = player.current_room.get_exits()
    ## check the current room agains the dictionary
    if player.current_room.id not in map_dict:
      new_data = {}
      new_tupe = ()
      # Develops new entry in map dict
      map_dict[player.current_room.id] = {}
      if prev_room is None:
        for exit in exits:
          new_tupe = (player.current_room.id, exit)
          queue.append(new_tupe)
          new_data[exit] = '?'
        map_dict[player.current_room.id] = new_data
      else:
        for exit in exits:
          ## This sets the dictionary to point at the past room
          # Then it also connects current room
          if opposites[direction_traveled] == exit:
            old_direction = (prev_room, direction_traveled)
            visited.add(old_direction)
            map_dict[prev_room][exit] = player.current_room.id
            map_dict[player.current_room.id][opposites[direction_traveled]] = prev_room
          else:
            new_tupe = (player.current_room.id, exit)
            queue.add(new_tupe)
            new_data[exit] = '?'
            map_dict[player.current_room.id][exit] = '?'
    else:
      for exit in exits:
        if exit is not in map_dict[player.current_room.id]:
          map_dict[player.current_room.id][exit] = '?'
          new_tupe(player.current_room, exit)
          queue.add(new_tupe)
        




    #   print(map_dict)
    #   prev_room = player.current_room.id
    # else:
    #   ## This means the id is in the dictionary
    #   ## For every single one other than first one
    #   # Need to figure out which directions are here
    #   exits = player.current_room.get_exits()
    #   for direction in map_dict[player.current_room.id]:
    #     if 
      map_dict[player.current_room.id] = {}


    ## Now pick a direction and go
    new_direction = exits[random.randint(0, len(exits)-1)]



  print('we found all 500 rooms')
  ## Now it's time to locate empty locations





  ## Run until all 500 spots are found
  ## Record room directions to dictionary
  ## Once map is full, find all empty slots
  ## Go through and navigate to empty slots

  ## profit

  # Traversal??
  # 000: 
  # 001: 



# LET'S DO THE REAL THING
def find_deadends(map_dict):
  ## This method uses the map_dict to determine traversal path
  ## It finds all dead ends
  ## It back tracks for each dead end to it's pivot location (next room with 3 exits)

  ## Save to dictionary:
      # pivot: direction of deadend
  pass

def pivot_path(direction):
  pass

# while len(visited_rooms) < 500:
#   ## Get all deadends

#   pass




#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
  discover_map()
  cmds = input("-> ").lower().split(" ")
  if cmds[0] in ["n", "s", "e", "w"]:
    player.travel(cmds[0], True)
  elif cmds[0] == "q":
    break
  else:
    print("I did not understand that command.")



### Create Dictionary that is used as a "success" measure of the application (len of dictionary)
## Success metric
# visited = {
#   000: {n, s, e, w}
#   }
## Create counter for # of steps
## Open Map file
## Parse map file for all dead-ends & add these to an array
# For each room in the array, find their turning point (Backtrack until 3 direction are found). 434 (dead-end) 281: n = 350
## Save direction + pivot node in dictionary
## pivot_dict = {
#     000: s, n
#   }
## Need to come up with case if multiple dead end routes.
#
## Perform DFT, except always prioritize deadend nodes, if not, proceed to next stack node
## Success?
## Randomize order of direction when 3/4 way option?
## when 2 ways, always go new direction
## When 3 ways, check for pivot node, if not roll for initial direction (not previous)

## ?? I'm not revisiting?
# Stack??
# ALWAYS priotize pivots, do anything on this route after that until route is dead
# Go back to my last turn and find my path forward

# ??? 

## Do some sort of searching? to figure out a random direction
## Everytime a Dead-end pivot node is reached, proceed to end of path, then turn back.