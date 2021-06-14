import sys, copy
from sys import maxsize #like INT_MAX in c++
from copy import deepcopy #method to allow for children to be saved apart from it's parent

#globals to keep track of all seen states and the number of nodes expanded
live_states = []
num_nodes_expanded = 0  #pretty much a static

#------- Problem Class ---------
class Problem:
  goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] #hold the goal/end state internally in the problem class

  def __init__(self, puzzle_board, row_num): #board contructor
    self.puzzle_board = puzzle_board
    self.row_num = row_num
    self.blank_y_pos, self.blank_x_pos = self.find_blank_tile() #order here is y->x, or row->col

  def find_blank_tile(self):
    for row in range(len(self.puzzle_board)): #rows
      for col in range(len(self.puzzle_board)): #cols
        if self.puzzle_board[row][col] == 0: #blank found
          return row, col #return

  def swap_tiles(self, new_y, new_x):
    temp_blank = self.puzzle_board[self.blank_y_pos][self.blank_x_pos] #hold blank slot
    self.puzzle_board[self.blank_y_pos][self.blank_x_pos] = self.puzzle_board[new_y][new_x] #old blank spot gets tile
    self.puzzle_board[new_y][new_x] = temp_blank #new board spot gets the blank

  #define operators for the problem class (return true or false depending on success or failure)
  def move_up(self): #move up (operates directly on the current problem)
    if 0 not in self.puzzle_board[0]: #make sure the blank space is not in the top row (i.e moving up is a legal move)
      self.swap_tiles(self.blank_y_pos - 1, self.blank_x_pos) #swap the current blank and the next higher tile
      self.blank_y_pos = self.blank_y_pos - 1  #move the blank pos one higher
      return True

    else: #else fail
      return False

  def move_down(self): #move down (operates directly on the current problem)
    if 0 not in self.puzzle_board[2]: #make sure the blank space is not in the bottom row
      self.swap_tiles(self.blank_y_pos + 1, self.blank_x_pos) #swap the current blank and the next lower tile
      self.blank_y_pos = self.blank_y_pos + 1  #move the blank pos one lower
      return True

    else: #else fail
      return False

  def move_left(self): #move left (operates directly on the current problem)
    in_left_col = False #current blank tile shouldn't be in the left column
    for row in range(self.row_num):
      if self.puzzle_board[row][0] == 0: #if this is true, can't move to the left
        in_left_col = True
        break

    if in_left_col == False:
      self.swap_tiles(self.blank_y_pos, self.blank_x_pos - 1) #swap the current blank and the next left tile
      self.blank_x_pos = self.blank_x_pos - 1  #move the blank pos one to the left
      return True

    else: #else fail
      return False

  def move_right(self): #move right (operates directly on the current problem)
    in_right_col = False #current blank tile shouldn't be in the right column
    for row in range(self.row_num):
      if self.puzzle_board[row][2] == 0: #if this is true, can't move to the right
        in_right_col = True
        break

    if in_right_col == False:
      self.swap_tiles(self.blank_y_pos, self.blank_x_pos + 1) #swap the current blank and the next roght tile
      self.blank_x_pos = self.blank_x_pos + 1  #move the blank pos one to the right
      return True

    else: #else fail
      return False

  def print_board(self):
    to_print = []
    for row in range(len(self.puzzle_board)): #rows
      for col in range(len(self.puzzle_board)): #cols
        to_print.append(self.puzzle_board[row][col]) #save current row
      print(to_print) #print row
      to_print = [] #clear row to print

#--------- Node Class ---------
class Node:
  def __init__(self, problem, path, heuristic): #node initialization
    self.problem = problem
    self.path = path
    self.heuristic = heuristic

#--------- Graph Search Functions ---------
def save_child(node, children):
  child = deepcopy(node) #creates a child based on the last move
  child.path += 1  #increment path cost by one for each move (here each edge just costs 1)
  children.append(child)

def explore_node(node):
  global num_nodes_expanded #reference global

  children = []

  if node.problem.move_up(): #check if move is possible and if yes, do it
    live_states.append(node.problem.puzzle_board) #append this possible move
    save_child(node, children) #deepcopy child to children
    node.problem.move_down() #reset to before move

  if node.problem.move_down(): #check if move is possible and if yes, do it
    live_states.append(node.problem.puzzle_board) #append this possible move
    save_child(node, children) #deepcopy child to children
    node.problem.move_up() #reset

  if node.problem.move_left(): #check if move is possible and if yes, do it
    live_states.append(node.problem.puzzle_board) #append this possible move
    save_child(node, children) #deepcopy child to children
    node.problem.move_right() #reset

  if node.problem.move_right(): #check if move is possible and if yes, do it
    live_states.append(node.problem.puzzle_board) #append this possible move
    save_child(node, children) #deepcopy child to children
    node.problem.move_left() #reset

  # print(live_states) #debug

  num_nodes_expanded += len(children)
  return children

def remove_node(frontier): #removes the cheapest node
  lowest_cost_seen = maxsize
  positition = maxsize #position of the node to remove

  for n in range(len(frontier)):
    if frontier[n].path + frontier[n].heuristic < lowest_cost_seen: #f formula
      lowest_cost_seen = frontier[n].path + frontier[n].heuristic
      positition = n

  node = frontier.pop(positition)
  return node

def misplaced_tiles(node):
  total_misplaced_tiles = 0 #keep track of the total number of misplaced tiles

  for row in range(len(node.problem.puzzle_board)):
    for col in range(len(node.problem.puzzle_board)):
      if node.problem.puzzle_board[row][col] != node.problem.goal_state[row][col]: #found a misplaced tile
        if node.problem.puzzle_board[row][col] != 0: #ignore the blank tile itself
          total_misplaced_tiles += 1

  return total_misplaced_tiles

def find_in_goal_state(node, row, col):
  tile = node.problem.puzzle_board[row][col] #find current tile

  #output where this tile belongs
  if tile == 1:
    row = 0
    col = 0

  elif tile == 2:
    row = 0
    col = 1

  elif tile == 3:
    row = 0
    col = 2

  elif tile == 4:
    row = 1
    col = 0

  elif tile == 5:
    row = 1
    col = 1

  elif tile == 6:
    row = 1
    col = 2

  elif tile == 7:
    row = 2
    col = 0

  elif tile == 8:
    row = 2
    col = 1

  return row, col

def euclidean_distance(node):
  heurisitic = 0 #start as 0

  for row in range(len(node.problem.puzzle_board)):
    for col in range(len(node.problem.puzzle_board)):
      if node.problem.puzzle_board[row][col] != node.problem.goal_state[row][col]: #misplaced tile
        if node.problem.puzzle_board[row][col] != 0: #ignore blank tile
          row_diff, col_diff = find_in_goal_state(node, row, col) #these are where the tile should be
          distance = pow(pow((row - row_diff), 2) + pow(col - col_diff, 2), 0.5) #distance formula
          heurisitic += distance #add the distance

  return heurisitic

def expand(set_list, node, choice):
  print("The best state to expand with a g(n) = " + str(node.path) + " and h(n) = " + str(node.heuristic) + " is...")
  node.problem.print_board()
  print("Expanding this node...") #print expand message
  print(" ")

  children = explore_node(node) #get possible children

  if choice == 1: #blind uniform search
    for child in children: #no need to update the hueristic
      if child.problem.puzzle_board not in live_states: #if not already a live state
        set_list.append(child) #insert to set
        live_states.append(child.problem.puzzle_board) #upadate live states

  elif choice == 2: #misplaced tile hueristic
    for child in children: #update the heuristic for the childen
      child.heuristic = misplaced_tiles(child)
      if child.problem.puzzle_board not in live_states: #if not already a live state
        set_list.append(child) #insert to set
        live_states.append(child.problem.puzzle_board) #upadate live states

  elif choice == 3: #euclidean distance hueristic
    for child in children: #update the heuristic for the childen
      child.heuristic = euclidean_distance(child)
      if child.problem.puzzle_board not in live_states: #if not already a live state
        set_list.append(child) #insert to set
        live_states.append(child.problem.puzzle_board) #upadate live states

  return set_list

def graph_search(problem, choice):
  path = 0
  heuristic = 0

  node = Node(problem, path, heuristic)  #first node (initial state)

  if choice == 2: #update heuristic for misplaced tiles
    node.heuristic = misplaced_tiles(node)
  elif choice == 3: #update heuristic for euclidean distance
    node.heuristic = euclidean_distance(node)

  frontier = [node] #initialize with first state
  max_queue_size = 0

  while True: #loop until return
    max_queue_size = max(len(frontier), max_queue_size) #max size seen so far is the max queue size ever seen

    if not frontier: #if this happens, failure!
      print("No solution can be found")
      return

    (node) = remove_node(frontier) #remove next node

    if node.problem.puzzle_board == problem.goal_state: #check if goal only after we remove - thanks Rutuja :)
      print("Solution found!") #if this happens, success
      print(" ")
      print("Number of nodes expanded: " + str(num_nodes_expanded))
      print("Max queue size: " + str(max_queue_size))
      return

    frontier = expand(frontier, node, choice)

#--------- Main Function ---------
def main():
  intro  = "Welcome to Alejandro Sherman's 8-puzzle solver.\n"
  intro  += "Type '1' to use a default puzzle, or '2' to enter your own puzzle.\n"
  print(intro)

  first_choice = int(input())
  puzzle = []

  if first_choice == 1:
    intro2 = "Enter the difficulty you wish to start with.(6 is the demo puzzle)\n"
    intro2 += "Your choices are '0', '1', '2', '3', '4', '5' and '6'.\n"
    print(intro2)

    second_choice = int(input())
    if second_choice == 0:
      puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    elif second_choice == 1:
      puzzle = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    elif second_choice == 2:
      puzzle = [[1, 2, 0], [4, 5, 3], [7, 8, 6]]
    elif second_choice == 3:
      puzzle = [[0, 1, 2], [4, 5, 3], [7, 8, 6]]
    elif second_choice == 4:
      puzzle = [[8, 7, 1], [6, 0, 2], [5, 4, 3]]
    elif second_choice == 5:
      puzzle = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]
    elif second_choice == 6:
      puzzle = [[1, 0, 3], [4, 2, 6], [7, 5, 8]]
    else:
      print ("Please try again and select an a valid option")
      sys.exit(0)

  elif first_choice == 2:
    print("Enter your puzzle, use a zero to represent the blank and press enter when done with each step.")
    first_row = input("Enter the first row, using a space between numbers: ")
    first_row = [int(d) for d in first_row.split() if d.isdigit()]
    second_row = input("Enter the second row, using a space between numbers: ")
    second_row = [int(d) for d in second_row.split() if d.isdigit()]
    third_row = input("Enter the third row, using a space between numbers: ")
    third_row = [int(d) for d in third_row.split() if d.isdigit()]

    puzzle = [first_row, second_row, third_row]

  else:
    print ("Please try again and select an a valid option")
    sys.exit(0)

  problem = Problem(puzzle, 3)

  intro2  = "Choice of algorithms to use:\n"
  intro2  += "1. Uniform Cost Search\n"
  intro2  += "2. A* with Misplaced Tile Heuristic\n"
  intro2  += "3: A* with Euclidean Distance Heuristic\n"
  print(intro2)

  third_choice = int(input())

  if third_choice == 1:
    #print("Initiate algorithm with Uniform cost search")
    print("Initiating Uniform Cost Search on")
    problem.print_board()
    print(" ")
    graph_search(problem, third_choice)

  elif third_choice == 2:
    #print("Initiate algorithm with A* with misplaced tile heuristic")
    print("Initiating A* with Misplaced Tile Heuristic on")
    problem.print_board()
    print(" ")
    graph_search(problem, third_choice)

  elif third_choice == 3:
    #print("Initiate algorithm with A* with Euclidean distance")
    print("Initiating A* with Euclidean Distance Heuristic on")
    problem.print_board()
    print(" ")
    graph_search(problem, third_choice)

  else:
    print("Please try again and select an a valid option")
    sys.exit(0)

main()
