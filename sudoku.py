#!/usr/bin/env python
#coding:utf-8
import sys
import time
import itertools
import queue
import heapq
"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"

class CSP(object):
    
    def __init__(self, board):
        self.X = list(board.keys())
        self.D = {}
        self.C = {}
        self.P = {}
        
        for var, value in board.items():
            if value == 0:
                self.D[var] = set(range(1,10))
            else:
                self.D[var] = {value}
            self.C[var] = adj_list(var)
            self.P[var] = set()
        
    def getVariables(self):
        return self.X

    def getDomains(self):
        return self.D
    
    def getConstraints(self,var):
        return self.C[var]

    def getVarDomain(self,var):
        return self.D[var]

    def reduceDomain(self, var, num):
        self.D[var].remove(num)

    def copy(self):
        return self



def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this

    sudoku = CSP(board)
    sudoku = ac3(sudoku) #preprocessing AC-3 to prune domains
    solved = backtrack({var:value for var,value in board.items() if value != 0}, sudoku)
    
    return solved


def backtrack(assignment, csp):
    '''Helper function'''
    if isComplete(assignment): return assignment
    var = MRV(csp, assignment)

    for value in csp.getVarDomain(var).copy():
        if isConsistent(csp, assignment, var, value):
            assignment[var] = value
            if FC(csp,assignment,var,value):
                result = backtrack(assignment, csp)
                if result: return result
                del assignment[var]
                for value in csp.P[var]:
                    csp.D[var].add(value)
                csp.P[var] = set()
    
    return False


def FC(csp, assignment, var, val):

    q = queue.deque([neighbor for neighbor in csp.getConstraints(var) if not neighbor in assignment])

    while q:
        neighbor = q.popleft()
        if revise(csp, neighbor, var):
            if csp.D[neighbor] == set():
                return False

    return True




def ac3(csp):
    '''AC-3 PREPROCESSING'''
    q = queue.deque()
    for var in csp.X:        
        for adjacency in csp.getConstraints(var):
            q.append((var, adjacency))
    
    while q:
        
        (x,y) = q.popleft()
        
        if revise(csp, x, y):

            if not csp.getVarDomain(x):
                return False

            for adjacency in csp.getConstraints(x) - {y}:
                q.append((adjacency,x))
                
    return csp


def revise(csp, x, y) -> bool:
    '''helper method to reduce a variable's domain. 
    csp: a CSP object with X:variables, D: domains, C: constraints
    x: varied whose domain is to be reduced
    y: the compared-to variable 
    return: whether it has been reduced
    '''
    revised = False
    ydomain = csp.getVarDomain(y)
    if y in csp.getConstraints(x) and len(ydomain) == 1:
        xdomain = csp.getVarDomain(x)
        csp.D[x] = xdomain - ydomain
        if csp.D[x] != xdomain:
            csp.P[x].add(ydomain.copy().pop())
            revised = True

    return revised



def isComplete(assignment):
    return len(assignment) == 81



def MRV(csp, assignment):
    '''helper function to determine the most constrained unassigned variable left'''

    #generate a dictionary containing unassigned variables and the respective sizes of their domains.
    length = {var:len(domain) for var,domain in csp.getDomains().items() if not assignment.get(var)}

    return min(length, key=length.get)



def LCV(csp, var):
    '''helper function to determine the least constraining value in a variable's domain'''
    freqs = {val: 0 for val in csp.getVarDomain(var)}
    for node in csp.getConstraints(var):
        for value in freqs.keys():
            if value in csp.getVarDomain(node):
                freqs[value] += 1

    return sorted(freqs, key=freqs.get)



def isConsistent(csp, assignment, var, val):
    for neighbor in csp.getConstraints(var):
        if assignment.get(neighbor) == val : 
            return False

    return True



def adj_list(var):
    '''helper function to return the adjacency list of a variable'''

    adjacencies = set()
    nums = set(str(x) for x in range(1,10))
    letters = set(char for char in ROW)
    row = set(''.join(x) for x in itertools.product(var[0], nums))
    col = set(''.join(x) for x in itertools.product(letters, var[1]))
    
    adjacencies = row.union(col, box(var))

    return adjacencies - {var}



def box(var) -> list:
    '''Helper method that returns the variables that are inside the input variable's box'''
    #extract number and letter code from var
    num = int(var[1])
    charint = ord(var[0]) - 64
    
    #generate adjacenct columns, rows
    cols = list(range(num - (num-1)%3, num + 3 - (num-1)%3 ))
    rows = [chr(x + 64) for x in list(range(charint - (charint-1)%3, charint + 3 - (charint-1)%3 ))]
    
    return {letter + str(number) for letter, number in [x for x in itertools.product(rows,cols)]}



if __name__ == '__main__':

    if len(sys.argv) > 1:

        #  Read individual board from command line arg.
        sudoku = sys.argv[1]

        if len(sudoku) != 81:
            print("Error reading the sudoku string %s" % sys.argv[1])
        else:
            board = { ROW[r] + COL[c]: int(sudoku[9*r+c])
                      for r in range(9) for c in range(9)}
            
            print_board(board)

            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()
            print_board(solved_board)
            print(end_time - start_time)
            out_filename = 'output.txt'
            outfile = open(out_filename, "w")
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

    else:

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            
            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                    for r in range(9) for c in range(9)}

            # Print starting board.
            print_board(board)

            # Solve with backtracking
            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()
            
            # Print solved board. 
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")