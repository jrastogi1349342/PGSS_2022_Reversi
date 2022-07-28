import copy
import random
import sys


print("Reversi - Written by Diya Hundiwala, Bea Ricafort, Jai Rastogi, and Alena Hemminger. Led by Dr. Neil Simonetti.")


# Defines starting points for both players -- both White and Black have 2 pieces at the start
w_score = 2
b_score = 2


# Defines an empty list, which will eventually be filled with legal moves
legals = [] 


# Clears board by putting a space into every position on the board
def clear_board(board):
	for r in range(0, 8): 
		board[r] = [" "," "," "," "," "," "," "," "]

    
# Method used for swapping (turns every W to B and every B to W)
def flip_board(board): 
	for r in range(0, 8):
		for c in range(0, 8):
			if board[r][c] == "B":
				board[r][c] = "W"
			elif board[r][c] == "W":
				board[r][c] = "B"


def print_board(board): # Prints the board to the user
	print ("\n\n\n\n\n\n\n   1   2   3   4   5   6   7   8")
	for r in range(0, 8):
		if r > 0:
			print("  ---+---+---+---+---+---+---+---") 
		for c in range(0, 8):
			if c > 0:
				print(" | ", end = "")
			else:
				print(chr(65+r), end = "  ")
			print(board[r][c], end = "")
		print()
	print()

  
# Checks all directions of a specific disk position: returns zero if nothing should be flipped or returns the number of items to be flipped in this direction
def check_dir(board, r, c, color, dx, dy):
  count = 1
  r = r + dy
  c = c + dx
  opp = "B" if color == "W" else "W"
  if (c > -1 and c < 8 and r > -1 and r < 8 and board[r][c] == opp):
      r = r + dy
      c = c + dx
      while (c > -1 and c < 8 and r > -1 and r < 8 and board[r][c] == opp):
          r = r+dy
          c = c+dx
          count = count+1
      if (c > -1 and c < 8 and r > -1 and r < 8 and board[r][c] == color):
          return count
  return 0


def make_move(board, color, position): # Places the color on the board at a certain position
    board[position[0]][position[1]] = color
    for i in range(0, 3):
      for j in range (0, 3):
          if (i != 1 or j != 1):
              n = check_dir(board, position[0], position[1], color, i-1, j-1)
              row = position[0]
              col = position[1]
              for k in range(0, n):
                  col = col + i - 1
                  row = row + j - 1
                  board[row][col] = color


def legal_moves(board, color): # Returns a list of legal moves
	legals = []
	for r in range(0, 8):
		for c in range(0, 8):
			if (board[r][c] == " " and (check_dir(board, r, c, color, -1, -1) 
                                  or check_dir(board, r, c, color, -1, 0) 
                                  or check_dir(board, r, c, color, -1, 1) 
                                  or check_dir(board, r, c, color, 0, -1) 
                                  or check_dir(board, r ,c, color, 0, 1) 
                                  or check_dir(board, r, c, color, 1, -1) 
                                  or check_dir(board, r, c, color, 1, 0) 
                                  or check_dir(board, r, c, color, 1, 1))):
				legals.append([r,c])
	return legals

  
# Determines score by summing W and B disks on the board
# Set scores to 0 each time so points lost are not added upon / to new score
def get_score(board):
  global w_score
  global b_score
  w_score = 0
  b_score = 0
  for r in range(0, 8):
    for c in range(0, 8):
      if board[r][c] == "W":
        w_score += 1
      if board[r][c] == "B":
        b_score += 1
  print(f"White Score: {w_score}")
  print(f"Black Score: {b_score}")

  
# Checks whether it is the end of the game by evaluating whether there are no legal moves left for either player
def check_end_of_game(board):
  return (len(legal_moves(board,"B")) == 0) or (len(legal_moves(board, "W")) == 0)


def check_win(board): # Evaluates who is the winner of the game 
  global w_score
  global b_score
  if check_end_of_game(board) is False: 
    return None
  if w_score > b_score: 
    return "White"
  elif b_score > w_score:
    return "Black"
  else: 
    return "Draw"


def player_turn(board, color): # Takes player input and determines whether it is a legal move
  while True:
    print("Player's Turn - Type desired location (letter and number with no space and press enter): ")
    inp = input()
    if len(inp) == 0:
       print("Not a legal move, try again.")
       continue
    
    r = ord(inp[0]) % 32 - 1
    c = int(inp[1]) - 1
    is_legal = True
    
    for move in legal_moves(board, color):
      if [r,c] == move:
        is_legal = True
        break
      else:
        is_legal = False 
        
    if is_legal == False: 
      print("Not a legal move, try again.")
      continue
    elif is_legal:
      return [r,c]


def random_turn(board, color): # Returns a random legal move that can be made by color
  return random.choice(legal_moves(board, color))

  
# calc_board Function / Board Evaluation Routine: Returns a numeric value for positions on the board
def calc_board(board, color):
	corner = 50
	corner_risk = -10
	edge = 15
	danger = -5
	other = 1
  
	weights = [[corner, corner_risk, edge, edge, edge, edge, corner_risk, corner],
             [corner_risk, corner_risk, danger, danger, danger, danger, corner_risk, corner_risk],
						 [edge, danger, other, other, other, other, danger, edge],
             [edge, danger, other, other, other, other, danger, edge],
						 [edge, danger, other, other, other, other, danger, edge],
             [edge, danger, other, other, other, other, danger, edge],
						 [corner_risk, corner_risk, danger, danger, danger, danger, corner_risk, corner_risk],
             [corner, corner_risk, edge, edge, edge, edge, corner_risk, corner]]
  
	board_eval = 0
  
	for r in range(0, 8):
		for c in range(0, 8):
			if board[r][c] == color:
				board_eval += weights[r][c]
			elif board[r][c] != " ":
				board_eval -= weights[r][c]
        
	return board_eval


def look_ahead(board, level, color): # Returns the best value for any possible move
	if (level == 0):
		return calc_board(board, color)
	else: 
		legal_move_list = legal_moves(board, "W" if color == "B" else "B")
		best_val = -999
    
		for my_move in legal_move_list:
			temp_board = copy.deepcopy(board)
			flip_board(temp_board)
      
			make_move(temp_board, color, my_move)
      
			if check_end_of_game(temp_board):
				return -1000
				
			val = look_ahead(temp_board, level - 1, color)
			if val > best_val:
				best_val = val
        
		return -best_val 


def smart_turn(board, level, color): # Returns the best legal move
	if color == "W":
		legal_move_list = legal_moves(board, "W")
	elif color == "B":
		legal_move_list = legal_moves(board, "B")
    
	random.shuffle(legal_move_list)
	best_val = -1001
	best_move = []
  
	for my_move in legal_move_list:
		temp_board = copy.deepcopy(board)
		make_move(temp_board, color, my_move)
    
		if check_win(temp_board):
			return my_move
      
		val = look_ahead(temp_board,level,color)
		if val > best_val:
			best_val = val
			best_move = copy.copy(my_move)
      
	return best_move


def start(): # Creates start menu of the game
	while True: 
		global player_dictionary
		print("Pick your game mode - Type 1, 2, 3, 4, 5, or 6:\n1. Player vs. Computer (Easy)\n2. Player vs. Computer (Hard)\n3. Player vs. Player\n4. Computer vs. Computer\n5. Computer vs. Smart Computer\n6. Smart Computer Lvl. 0 vs. Smart Computer Lvl. 1\n7. Smart Computer Lvl. 1 vs. Smart Computer Lvl. 2\n8. Smart Computer Lvl. 2 vs. Smart Computer Lvl. 3")
		inp = input()
		is_legal = True
		
		if inp == "1":
			player_dictionary = {"W" : "player","B" : "random"}
			is_legal = True
			break
		elif inp == "2":
			player_dictionary = {"W" : "player","B" : "smart3"}
			is_legal = True
			break
		elif inp == "3":
			player_dictionary = {"W" : "player","B" : "player"}
			is_legal = True
			break
		elif inp == "4":
			player_dictionary = {"W" : "random","B" : "random"}
			is_legal = True
			break
		elif inp == "5":
			player_dictionary = {"W" : "random","B" : "smart3"}
			is_legal = True
			break
		elif inp == "6":
			player_dictionary = {"W" : "smart0","B" : "smart1"}
			is_legal = True
			break
		elif inp == "7":
			player_dictionary = {"W" : "smart1","B" : "smart2"}
			is_legal = True
			break
		elif inp == "8":
			player_dictionary = {"W" : "smart2","B" : "smart3"}
			is_legal = True
			break
		else: 
			is_legal = False
			print("Not a valid mode, try again.")
			continue
		if is_legal: 
			return


def end(): # Either terminates the game or allows for replay 
	while True: 
		global game_over
		print("Would you like to play again? Type Y/N.")
		inp = input()
		is_legal = True 
    
		if inp == "Y" or inp == "y": 
			game_over = False 
			is_legal = True
			clear_board(the_board)
      
			the_board[4][4] = the_board[3][3] = "W"
			the_board[3][4] = the_board[4][3] = "B"
      
			print_board(the_board)
			start()
			play()
			break
		elif inp == "N" or inp == "n":
			sys.exit()
		else: 
			is_legal = False
			print("Not a valid option, try again.")
			continue
		if is_legal: 
			return


def play(): # Begins gameplay 
	global game_over
	global color
	global position 

	while not game_over:
		if player_dictionary[color] == "player":
			position = player_turn(the_board,color)
		elif player_dictionary[color] == "random":
			position = random_turn(the_board, color)
		# The second parameter of smart_turn determines the level of look_ahead
		elif player_dictionary[color] == "smart0":
			position = smart_turn(the_board, 0, color)
		elif player_dictionary[color] == "smart1":
			position = smart_turn(the_board, 1, color)
		elif player_dictionary[color] == "smart2":
			position = smart_turn(the_board, 2, color)
		elif player_dictionary[color] == "smart3":
			position = smart_turn(the_board, 3, color)
		else:
			print("I'm confused.")
			break
		
		make_move(the_board, color, position)
		print_board(the_board)
		get_score(the_board)
		pause = True	
	
		if check_end_of_game(the_board):
			if check_win(the_board) != "Draw":
				game_over = True
				pause = False
				if w_score > b_score:
					color = "W"
				if b_score > w_score:
					color = "B"
				print("Congratulations," + color + ", you are the winner!")
			else:
				game_over = True
				pause = False
				print("The game is a draw.")
	
		if color == "W":
			color = "B"
		else:
			color = "W"
				
		if pause:
			input("Press Enter to continue.")

# The code below allows for gameplay     
the_board = [[], [], [], [], [], [], [], []]
clear_board(the_board)
the_board[4][4] = the_board[3][3] = "W"
the_board[3][4] = the_board[4][3] = "B"
 
game_over = False
color = "B"
position = []
player_dictionary = {"W" : "player", "B" : "player"}
print_board(the_board)

while not game_over: 
	start()
	play() 

while game_over:
	end()