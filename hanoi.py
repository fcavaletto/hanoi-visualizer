# --- Tower of Hanoi Animation Script ---
# Solves the Tower of Hanoi problem with visual animation and move counter.
# Written to be educational, modular, and easy to follow.

from time import time, sleep
import sys, os
from typing import List
from dataclasses import dataclass

# --- Constants ---
PEGS = [0, 1, 2]  # Labels for the three pegs: 0 = source, 1 = auxiliary, 2 = destination

# --- Data Structure for Game State ---
@dataclass
class GameState:
    num_of_discs: int    # Total number of discs in the starting stack
    delay: float         # Delay between visual frames (seconds)
    moves_count: int = 0 # Number of moves made (initialized to zero)

# --- Function to Print the Board ---
def print_board(board: List[List[int]], state: GameState) -> None:
    """
    Visually prints the current board state in the terminal.
    Uses ANSI escape codes to update the screen smoothly.
    """
    n = state.num_of_discs
    levels = [i for i in range(n, 0, -1)]  # Levels from top to bottom

    board_height = len(levels) + 2  # (levels + base + empty line)

    # --- Smooth screen update ---
    print(f"\033[{board_height}A", end='')  # Move cursor up
    print("\033[J", end='')                  # Clear from cursor down

    # --- Print each level of pegs ---
    for level in levels:
        line = f"{level:2d}   "
        for stack in board:
            if len(stack) < level:
                # Empty space with peg
                line += ' ' * n + '|' + ' ' * n
            else:
                # Draw the disk
                disk_size = stack[level-1]
                line += ' ' * (n - disk_size + 1) + '=' * (disk_size * 2 - 1) + ' ' * (n - disk_size + 1)
        print(line)

    # --- Print the base ---
    print('     ' +  '-' * (n * 6 + 3))
    print()
    
    sleep(state.delay)  # Small pause for animation effect

# --- Function to Move the Stack ---
def move_stack(board: List[List[int]], stack_height: int, origin: int, destination: int, state: GameState, print_flag: bool = True) -> None:
    """
    Recursively moves a stack of disks from origin to destination.
    """
    assert not board[destination] or board[destination][-1] > board[origin][-stack_height], "Invalid move detected."

    if stack_height == 1:
        # Base case: move one disk directly
        board[destination].append(board[origin].pop())
        state.moves_count += 1
        if print_flag:
            print_board(board, state)
    else:
        # Recursive case: move stack of height - 1 to auxiliary peg
        the_other_peg = 3 - origin - destination  # The peg not involved
        move_stack(board, stack_height-1, origin, the_other_peg, state, print_flag)
        move_stack(board, 1, origin, destination, state, print_flag)
        move_stack(board, stack_height-1, the_other_peg, destination, state, print_flag)

# --- Main Execution ---
def main() -> None:
    """
    Parses arguments, sets up initial game state, and runs the solution.
    """
    # --- Argument parsing ---
    if len(sys.argv) < 3:
        print("Usage: python hanoi.py <num_of_discs> <num_of_discs_to_move> [--noprint] [delay=X]")
        sys.exit(1)

    num_of_discs = int(sys.argv[1])
    num_of_discs_to_move = int(sys.argv[2])

    # --- Handle optional delay ---
    delay = 0.01  # Default
    if any('delay' in arg for arg in sys.argv):
        _, delay_str = [arg for arg in sys.argv if 'delay' in arg][0].split('=')
        delay = float(delay_str)

    # --- Create the game state object ---
    state = GameState(num_of_discs=num_of_discs, delay=delay)

    print_flag = '--noprint' not in sys.argv

    # --- Set up initial board ---
    board = [[num_of_discs - i for i in range(num_of_discs)], [], []]

    # --- Initial board print ---
    if print_flag:
        print('\n\n' + '\n' * num_of_discs)  # Reserve space for animation
        print_board(board, state)

    # --- Start solving ---
    start_time = time()
    move_stack(board, num_of_discs_to_move, 0, 2, state, print_flag)
    end_time = time()

    # --- Results ---
    print(f"Moves taken: {state.moves_count}")
    print(f"Time elapsed: {end_time - start_time:.6f} seconds\n")

# --- Entry Point ---
if __name__ == '__main__':
    main()
