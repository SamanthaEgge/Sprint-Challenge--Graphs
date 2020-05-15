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

## Opposites Table
# Used for swapping directionals around for connections
opposites = {
  'n': 's',
  'e': 'w',
  's': 'n',
  'w': 'e'
}



## Cannot use stack??
# stack:{000, E}, {104, S}
# Dictionary? Stack?
# order to dictionary 
## This only provides n e s w, NOT room numbers

def discover_map():
  ## Need to discover every spot and direction on the map, so will be doing breadth first search
  # Back tracking method? I think this will only work with DFS
  discover_string = []
  counter = 0

  # Create queue for later
  queue = set()

  #Holding variables for us in function
  prev_room = None
  direction_traveled = None
  untouched_nodes = False
  
  while len(map_dict) < 499 or len(discover_string) > 0:
    ## Gets current set of exits
    exits = player.current_room.get_exits()
    ## check the current room agains the dictionary
    if player.current_room.id not in map_dict:
      new_data = {}
      # Develops new entry in map dict for new nodes discovered
      map_dict[player.current_room.id] = {}
      # This only triggers on first room
      if prev_room is None:
        for exit in exits:
          # new_tuple = (player.current_room.id, exit)
          new_data[exit] = '?'
        ## Just need to know which room to attend. Check at end if there's still question marks before moving.
        # queue.add(player.current_room.id)
        map_dict[player.current_room.id] = new_data

      # This should trigger for each new node discovered
      else:
        for exit in exits:
          ## This sets the dictionary to point at the past room
          # Then it also connects current room
          if opposites[direction_traveled] == exit:
            map_dict[prev_room][direction_traveled] = player.current_room.id
            map_dict[player.current_room.id][opposites[direction_traveled]] = prev_room
          else:
            # Build exits, flip boolean so I know I have new nodes to explore
            untouched_nodes = True
            map_dict[player.current_room.id][exit] = '?'
    #This Node exists, so we need to examine the current dictionary and see if we need to update anything
    else:
      for exit in exits:
        ## Adds connecting paths
        # if this was previous direction traveled, updated prev node and current node to path (might already be done)
        if opposites[direction_traveled] == exit:
          map_dict[prev_room][direction_traveled] = player.current_room.id
          map_dict[player.current_room.id][opposites[direction_traveled]] = prev_room
        ## Creates new zones to the queue, and adds untouched paths to dictionary
        elif exit not in map_dict[player.current_room.id]:
          untouched_nodes = True
          map_dict[player.current_room.id][exit] = '?'
        
    ## Now that we've dealt with the dictionary and queue we need to move to the next room
    possible_directions = []

    ## We're going D E E P
    # This is finding all possible exits, then adding those to our possibilities
    # print('map_dict', map_dict)
    for exit in exits:
      if map_dict[player.current_room.id][exit] is '?':
        possible_directions.append(exit)
    
    ## If there's possible directions, we're going to roll those directions and then move into it
    if len(possible_directions) > 0:
      queue.discard(player.current_room.id)
      if len(possible_directions) > 1:
        queue.add(player.current_room.id)
      # print('we have possible directions', possible_directions)
      direction_roll = possible_directions[random.randint(0, len(possible_directions)-1)]
      discover_string.append(direction_roll)
      prev_room = player.current_room.id
      direction_traveled = direction_roll
      player.travel(direction_roll)

    ## If we don't have possible directions we need to move backwards through our string trail until we do
    else:
      while len(possible_directions) == 0:
        # print(len(discover_string))
        # print(queue)
        if len(discover_string) == 0:
          return
        queue.discard(player.current_room.id)
        last_discover = discover_string[len(discover_string)-1]
        player.travel(opposites[last_discover])
        discover_string.pop(len(discover_string)-1)
        move_exits = player.current_room.get_exits()
        for exit in move_exits:
          if map_dict[player.current_room.id][exit] is '?':
            possible_directions.append(exit)
        # print('random move')
        # random_dir = move_exits[random.randint(0, len(move_exits)-1)]
        # player.travel(random_dir)
      direction_roll = possible_directions[random.randint(0, len(possible_directions)-1)]
      discover_string.append(direction_roll)
      prev_room = player.current_room.id
      direction_traveled = direction_roll
      player.travel(direction_roll)
  print('we found all 500 rooms')





##### discover_string = instead of using directions, use ids
## try to find the nearest id which has an open pathway



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)


# if len(visited_rooms) == len(room_graph):
#     print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

    #   print(map_dict)
    #   prev_room = player.current_room.id
    # else:
    #   ## This means the id is in the dictionary
    #   ## For every single one other than first one
    #   # Need to figure out which directions are here
    #   exits = player.current_room.get_exits()
    #   for direction in map_dict[player.current_room.id]:
    #     if 
      # map_dict[player.current_room.id] = {}


    ## Now pick a direction and go
    # new_direction = exits[random.randint(0, len(exits)-1)]



  # print('we found all 500 rooms')
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
def find_deadends(full_map):
  ## This method uses the map_dict to determine traversal path
  ## It finds all dead ends
  ## It back tracks for each dead end to it's pivot location (next room with 3 exits)
  prev_direction = None
  dead_ends = {}

  opposites = {
    'n': 's',
    'e': 'w',
    's': 'n',
    'w': 'e'
  }

  # direction = None
  direction_room = None
  prev_direction = None
  prev_room = None


  # def get_keyvalue(dicset):
  #   for key, value in dicset.items():
  #     direction = key
  #     direction_room = value
  #     return direction, direction_room


  # This grabs every dead end room id
  ## This should be recursion if I had 1 sliver of a brain
  for room in map_dict:
    num_exits = map_dict[room]
    if len(num_exits) == 1:
      prev_room = room
      print('heres starter room', room)
      for key in map_dict[room]:
        prev_direction = key
        print('heres our prev direction', prev_direction)
      direction_room = map_dict[room][prev_direction]
      print('heres our new direction room', direction_room)
      # print(map_dict[room])
      # print('WHATS EVEN PRINT',direction_room)
      # print(prev_direction)
      # print(map_dict)
      # print(map_dict[83])
      # print(map_dict[99])
      # print('direction',direction)
      while len(map_dict[direction_room]) is 2:
        print('SUSPECT MAP DICT TWO', map_dict[direction_room])
        for path in map_dict[direction_room]:
          print('checking SUSPECT MAP DICT', map_dict[direction_room])
          print('path options', path)
          ## Makes sure you aren't moving backwards. Opposite choice, should move you back down the path you came from
          if path not in map_dict[direction_room]:
            print('fuck you')
          elif map_dict[direction_room][path] != prev_room:
            print('prev_room, map_dict[dir_room][path]', prev_room, map_dict[direction_room][path])
            print('HERE BE A PATH',path)
            print(map_dict[direction_room])
            prev_room = direction_room ## 80
            prev_direction = path ## n
            direction_room = map_dict[prev_room][prev_direction] #11 'e', 's'
            print('')

      if direction_room in dead_ends:
        dead_ends[direction_room].append(opposites[prev_direction])
      else:
        dead_ends[direction_room] = [opposites[prev_direction]]
      print('YARR BE OUR DEAD ENDS',dead_ends)
      #   # There are two nodes here with two different directions, we need the direction that is not prev_direction to point at our next node in line.
      #   # make that new direction the prev_direction
      #   # After while loop take inverse of prev_direction and direction_room and assign it to dead_ends
      #   print('thIISS?', prev_direction, direction)
      #   print(direction_room)
      #   direction, direction_room = get_keyvalue(map_dict[direction_room])
      #   dead_ends[direction_room] = opposites[direction]
        # if direction is not prev_direction:

      # Pairs dead_end to next room

  print('dead-ends', dead_ends)
  

  # for death in dead_ends:
  #   path_number = None
  #   # map_dict[death][]
  #   ## Access room, get_exit, save dir as prev_direction, get exit id number
  #   # access that id.get_exits
  #   # if len(num_exits) == 2:
  #   # 


  ## Save to dictionary:
      # pivot: direction of deadend

  
  # pass

def pivot_path(direction):
  pass

# while len(visited_rooms) < 500:
#   ## Get all deadends

#   pass




#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
discover_map()
find_deadends(map_dict)
while True:
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