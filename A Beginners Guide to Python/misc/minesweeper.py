import random
from functools import partial
import sys

EMPTY_SQUARE_CHARACTER = "-"
BOMB_CHARACTER = "B"
FLAG_CHARACTER = "F"

def build_board(num_rows, num_cols, bomb_count=0, empty_character=EMPTY_SQUARE_CHARACTER):
    assert num_rows >= 1 and num_cols >= 1, "DIMS ERROR"

    board_temp = [BOMB_CHARACTER] * bomb_count + [empty_character] * ( (num_rows * num_cols) - bomb_count)

    if bomb_count:
        random.shuffle(board_temp)

    board = []
    for i in range(0, num_rows * num_cols, num_rows):
        board.append(board_temp[i:i+num_rows])
    return board

def set_square(x, y, new_val, board):
    """
    This function indexes into the given board at position (x, y).
    We then change that value to new_val. Returns nothing.
    """
    board[x][y] = new_val

def get_square(x, y, board):
    """
    This function takes a board and returns the value at that square(x,y).
    """
    return board[x][y]

def display_board(board):
    print(*board, sep="\n")

def neighbour_squares(x, y, num_rows, num_cols):
    """
    (x, y) 0-based index co-ordinate pair.
    num_rows, num_cols: specifiy the max size of the board
    
    returns all valid (x, y) coordinates from starting position.
    """
    offsets = [(-1,-1), (-1,0), (-1,1),
               ( 0,-1),         ( 0,1),
               ( 1,-1), ( 1,0), ( 1,1)]
    
    result = []
    for x2, y2 in offsets:
        
        px = x + x2
        py = y + y2
        
        #row_check = 0 <= px < num_rows
        #col_check = 0 <= py < num_cols
        
        row_check = 0 <= px < num_cols
        col_check = 0 <= py < num_rows

        if row_check and col_check:
            point = (px, py)
            result.append(point)
            
    return result
    
def count_occurence_of_character_in_neighbour_squares(x, y, board, character):
    """
    returns the number of neighbours of (x,y) that are bombs. Max is 8, min is 0.
    """
    num_rows = len(board[0])
    num_cols = len(board)
        
    squares = neighbour_squares(x, y, num_rows, num_cols)

    character_found = 0
    for px, py in squares:
        
        square_value = get_square(px, py, board)
        
        if square_value == character:
            character_found += 1
          
    return character_found

def flag_square(row, col, player_board):
    p_square = get_square(row, col, player_board)
    
    if p_square in "012345678":
        # do nothing
        return
    
    ## set flag
    if p_square == EMPTY_SQUARE_CHARACTER:
        set_square(row, col, FLAG_CHARACTER, player_board)
    
    ## Deflag if flag is already set
    if p_square == FLAG_CHARACTER:
        set_square(row, col, EMPTY_SQUARE_CHARACTER, player_board)
        return
     
def reveal_square(row, col, player_board, game_board):
    p_square = get_square(row, col, player_board)
    
    if p_square in "012345678" or p_square == FLAG_CHARACTER:
        ## do nothing
        return
    
    g_square = get_square(row, col, game_board)
    
    if g_square == BOMB_CHARACTER:
        return
        #return game_over()
    
    else:
        bomb_count = count_occurence_of_character_in_neighbour_squares(row, col, game_board, BOMB_CHARACTER)
        set_square(row, col, str(bomb_count), player_board)

class PlayGame():

    def __init__(self):
        self.player_board = [[]]
        self.game_board = [[]]

        self.is_playing = True

        ## Command -> (function, help text)
        self.COMMANDS = {
                        "flag": (self.flag, "Flags/deflags square(x,y). Example useage: flag x y"),
                        "pick": (self.pick,  "Selects square(x, y) to reveal, its game over if you reveal a bomb. Example useage: pick x y"),
                        "hint": (self.hint,  "The computer checks if square(x, y) is a bomb or not. Example useage: hint x y"), 
                        "new" : (self.new_game, "Starts a new game with a board size of (x,y) with z bombs. Example useage: new x y z"), 
                        "cheat": (self.cheat, "Shows the location of all bombs. Example useage: cheat"),
                        "help": (self.help, "Returns information about a instruction. Example useage: help cheat"),
                        "commands": (self.get_command_keys, "Returns a list of valid commands."),
                        "exit": (self.exit, "Exit the application. Example useage: exit")
        }

    def exit(self):
        self.is_playing = False
        

    def new_game(self, rows, cols, bomb_count):
        self.game_board = build_board(rows, cols, bomb_count = bomb_count)
        self.player_board = build_board(rows, cols, bomb_count=0)

    def pick(self, row, col):
        reveal_square(row, col, self.player_board, self.game_board)

        g_square = get_square(row, col, self.game_board)
        if g_square == BOMB_CHARACTER:
            return self.game_over()

    def flag(self, row, col):
        flag_square(row, col, self.player_board)

    def cheat(self):
        display_board(self.game_board)
        print("\n")

    def hint(self, row, col):
        g_square = get_square(row, col, self.game_board)

        is_bomb = g_square == BOMB_CHARACTER
        print(f"Is square({row},{col}) a bomb?: {str(is_bomb)}")


    def game_over(self):
        print("============")
        print("GAME OVER")
        print("=============")
        display_board(self.game_board)
        self.game_board = [[]]
        self.player_board = [[]]

    
    def get_command_keys(self):
        print(self.COMMANDS.keys())

    def help(self, topic=None):
        if topic is None:
            print(self.COMMANDS["help"][1])
    
        elif topic in self.COMMANDS:
            print(self.COMMANDS[topic][1])

        else:
            print(f"help {topic} was not understood")

    def parse_command(self, command):
        instruction, *arguments = command.split(" ")

        for i, arg in enumerate(arguments):
            if arg.isdigit():
                arguments[i] = int(arg)

        if instruction in self.COMMANDS:
            self.COMMANDS[instruction][0](*arguments)
        else:
            print(f"FAILED TO PARSE COMMAND: {command}")

def main():
    DEBUG = False #True

    if DEBUG:
        random.seed(243)

    print("+--------------------------------+")
    print("|   WELCOME TO MINSWEEPER 1.0!   |")
    print("+--------------------------------+")
    print("How to play: type 'commands' for a list of valid inputs. Then type 'help x' for information about how to use command 'x'")
    print("")

    game = PlayGame()

    while game.is_playing:
        s = input("Command: ")
        game.parse_command(s)
        display_board(game.player_board)
        print("\n")

if __name__ == "__main__":
    main()