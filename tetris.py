import random
import time

# Define the game board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Define the shapes of the Tetris pieces
SHAPES = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # Square
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # I-shape
    [(0, 0), (0, 1), (1, 1), (2, 1)],  # L-shape
    [(2, 0), (0, 1), (1, 1), (2, 1)],  # Reverse L-shape
    [(1, 0), (2, 0), (0, 1), (1, 1)],  # S-shape
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z-shape
    [(1, 0), (0, 1), (1, 1), (2, 1)],  # T-shape
]

# Define the colors of the Tetris pieces
COLORS = [
    '\033[91m',  # Red
    '\033[93m',  # Yellow
    '\033[92m',  # Green
    '\033[94m',  # Blue
    '\033[96m',  # Cyan
    '\033[95m',  # Magenta
    '\033[90m',  # Gray
]

# Define the game state
board = [[0 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]
score = 0
level = 1
lines_cleared = 0
game_over = False
current_piece = None
next_piece = None

# Define functions to manipulate the game board
def add_piece_to_board(piece, position):
    for x, y in piece:
        board[position[1] + y][position[0] + x] = piece.index((x, y)) + 1

def remove_piece_from_board(piece, position):
    for x, y in piece:
        board[position[1] + y][position[0] + x] = 0

def is_valid_position(piece, position):
    for x, y in piece:
        if position[0] + x < 0 or position[0] + x >= BOARD_WIDTH or \
           position[1] + y < 0 or position[1] + y >= BOARD_HEIGHT or \
           board[position[1] + y][position[0] + x] != 0:
            return False
    return True

def clear_lines():
    global board, score, level, lines_cleared
    lines_to_clear = []
    for y in range(BOARD_HEIGHT):
        if all(board[y][x] != 0 for x in range(BOARD_WIDTH)):
            lines_to_clear.append(y)
    lines_cleared += len(lines_to_clear)
    score += len(lines_to_clear) ** 2 * level
    level = 1 + lines_cleared // 10
    for y in reversed(lines_to_clear):
        board.pop(y)
        board.insert(0, [0 for x in range(BOARD_WIDTH)])

def get_random_piece():
    return random.choice(SHAPES)
def print_board():
    # Clear the screen
    print('\033[2J\033[H', end='')

    # Print the board
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x] == 0:
                print('.', end='')
            else:
                print(COLORS[board[y][x] - 1] + '#', end='')
        print()

    # Print the score and level
    print('Score: ', score)
    print('Level: ', level)
    print('Lines cleared: ', lines_cleared)

    # Print the next piece
    print('Next piece:')
    for y in range(4):
        for x in range(4):
            if (x, y) in next_piece:
                print(COLORS[SHAPES.index(next_piece)] + '#', end='')
            else:
                print(' ', end='')
        print()
        
# Initialize the game state
current_piece = get_random_piece()
next_piece = get_random_piece()

# Start the game loop
while not game_over:
    # Handle user input
    command = None
    while command not in ['a', 'd', 's', 'q']:
        print_board()
        command = input('Press A to move left, D to move right, S to move down, Q to quit: ').lower()
    if command == 'a':
        new_position = (current_piece_position[0] - 1, current_piece_position[1])
        if is_valid_position(current_piece, new_position):
            remove_piece_from_board(current_piece, current_piece_position)
            current_piece_position = new_position
            add_piece_to_board(current_piece, current_piece_position)
    elif command == 'd':
        new_position = (current_piece_position[0] + 1, current_piece_position[1])
        if is_valid_position(current_piece, new_position):
            remove_piece_from_board(current_piece, current_piece_position)
            current_piece_position = new_position
            add_piece_to_board(current_piece, current_piece_position)
    elif command == 's':
        new_position = (current_piece_position[0], current_piece_position[1] + 1)
        if is_valid_position(current_piece, new_position):
            remove_piece_from_board(current_piece, current_piece_position)
            current_piece_position = new_position
            add_piece_to_board(current_piece, current_piece_position)
        else:
            # The current piece has landed, so add it to the board and clear any lines that it completes
            add_piece_to_board(current_piece, current_piece_position)
            clear_lines()
            current_piece = next_piece
            next_piece = get_random_piece()
            current_piece_position = (BOARD_WIDTH // 2 - 1, 0)
            if not is_valid_position(current_piece, current_piece_position):
                game_over = True
    elif command == 'q':
        game_over = True

    # Move the current piece down one row
    if not game_over:
        new_position = (current_piece_position[0], current_piece_position[1] + 1)
        if is_valid_position(current_piece, new_position):
            remove_piece_from_board(current_piece, current_piece_position)
            current_piece_position = new_position
            add_piece_to_board(current_piece, current_piece_position)
        else:
            # The current piece has landed, so add it to the board and clear any lines that it completes
            add_piece_to_board(current_piece, current_piece_position)
            clear_lines()
            current_piece = next_piece
            next_piece = get_random_piece()
            current_piece_position = (BOARD_WIDTH // 2 - 1, 0)
            if not is_valid_position(current_piece, current_piece_position):
                game_over = True

    # Wait for a short time to control the speed of the game
    time.sleep(0.1)

# Print the final game over message
print_board()
print('Game over! Your final score is:', score)
