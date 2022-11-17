import requests
from bs4 import BeautifulSoup
import sys

#################### SUDOKU SOLVER CLASS ####################
class Solver:
    # Init with puzzle as argument
    def __init__(self, p):
        self.puzzle = p

    def get_row(self, i):
        return self.puzzle[i]

    def get_col(self, i):
        ret = []
        for r in self.puzzle:
            ret.append(r[i])
        return ret

    # Gets a 3x3 square from the puzzle
    def get_sq(self, r, c):
        ret = []
        start_row = r - r % 3
        start_col = c - c % 3
        for a in range(3):
            for b in range(3):
                ret.append(self.puzzle[start_row + a][start_col + b])
        return ret

    # Check if a number already exists in a row, column, or square
    def is_valid(self, num, r, c):
        row = self.get_row(r)
        col = self.get_col(c)
        sq = self.get_sq(r, c)
        if num in row or num in col or num in sq:
            return False
        else:
            return True

    # Solve puzzle with a backtracking algorithm
    def solve_puzzle(self, r, c):
        # Base case: end of puzzle reached
        if r == 8 and c == 9:
            return True
        # Check that col val does not overflow (max = 8)
        if c == 9:
            r = r + 1
            c = 0
        # Check if number is already assigned to box
        if self.puzzle[r][c] > 0:
            return self.solve_puzzle(r, c + 1)

        # Go through numbers 1 - 9 and put valid ones in box until full puzzle is complete
        for num in range(1, 10, 1):
            # Set valid number and test the rest of the puzzle
            if self.is_valid(num, r, c):
                self.puzzle[r][c] = num
                if self.solve_puzzle(r, c + 1):
                    return True
            # Clear guess and try again if not valid
            self.puzzle[r][c] = 0
        # End reached - no solution found
        return False
#################### END OF CLASS ####################


# Help message for usage
def print_help_msg():
    sys.exit("ARGS\n\t-h: display this help message\n\t1: easy difficulty\n\t2: medium difficulty\n\t3: hard difficulty\n\t4: hardest difficulty\n")

# Basic utility function for printing puzzle
def print_puzzle(p):
    for row in p:
        print(row)

# Use bs4 and requests to parse HTML puzzle data from websudoku.com
def scrape_puzzle(level):
    r = requests.get('https://nine.websudoku.com/?level=' + level)
    soup = BeautifulSoup(r.text, 'html.parser')
    new_puzzle = []
    # Get individual cells from id tags
    for a in range(9):
        new_row = []
        for b in range(9):
            var = soup.find(id="f" + str(a) + str(b))
            if 'value' in var.attrs:
                new_row.append(int(var.attrs['value']))
            else:
                new_row.append(0)
        new_puzzle.append(new_row)
    return new_puzzle


# Gets a new puzzle and solves it, prints before and after solving
def main():
    if len(sys.argv) != 2:
        print_help_msg()
    elif sys.argv[1] != '1' and sys.argv[1] != '2' and sys.argv[1] != '3' and sys.argv[1] != '4':
        print_help_msg()
    else:
        p = scrape_puzzle(sys.argv[1])
        print('ORIGINAL PUZZLE')
        print_puzzle(p)

        s = Solver(p)
        s.solve_puzzle(0, 0)
        print("\n\nSOLVED PUZZLE")
        print_puzzle(s.puzzle)

if __name__ == "__main__":
    main()