"""
8 Puzzle Solver Using DFS, IDS, and A* Algorithms

Author :            Brigham Thornock
Class :             CS 4365.002
Last Modification : 2/9/2023

Summary :   This script will take a file input of line of numbers representing an 8 puzzle.
            For example:
            Input: 7 1 * 6 8 2 5 4 3

            Puzzle Representation:  7 6 1
                                    * 8 2
                                    5 4 3

            The puzzle can be solved by swapping * with nearby numbers until the goal state
            is reached

            Goal State: 7 8 1
                        6 * 2
                        5 4 3

            This script solves the puzzle using Depth First Search (DFS),
            Iterative Depth Limited Search (IDS), and A* using two different heuristic
            functions

Usage:      python assignment_1.py <algorithm> <input_file>

            Where <algorithm> is dfs, ids, astar1, or astar2 and <input_file> is the file
            used for puzzle start state in one line

"""

import sys

MAX_DEPTH = 10                      # set maximum tree depth

GOAL_STATE = ['7', '8', '1',        # set goal of the puzzle
              '6', '*', '2',
              '5', '4', '3']

enqueued = 0                        # number of states enqueued
path = []                           # path from root to goal state


class Node:
    """
    A class to represent nodes in search path

    Attributes
    ----------
    state : list
        a list of characters corresponding to the 8 puzzle
    parent : node
        parent of the given node

    Methods
    ----------
    is_root()
        returns true if root of tree, false otherwise
    expand()
        gets a list of children from given node
    path()
        gets a list of the states from node to root
    depth()
        gets integer depth of node
    """

    def __init__(self, state, parent):
        """
        Initialize node
        :param state: state of puzzle stored in node
        :param parent: parent of the node
        """
        self.state = state
        self.parent = parent

    def is_root(self):
        """
        Checks if node is root
        :return: false if not root, true otherwise
        """
        if self.parent:         # if the node has a parent return false
            return False
        else:
            return True

    def expand(self):
        """
        Expands given node to get all children
        :return: list of children nodes
        """
        star_index = self.state.index('*')                                  # index of star
        state = self.state                                                  # current node state
        children = []                                                       # list of children

        if star_index - 3 >= 0:                                             # up
            child_state = swap(state, star_index, star_index - 3)           # get new state
            if child_state not in self.path():                              # make sure node hasn't been made
                child = Node(child_state, self)                             # create new node
                children.append(child)                                      # add node to list

        if star_index != 2 and star_index != 5 and star_index != 8:         # right
            child_state = swap(state, star_index, star_index + 1)
            if child_state not in self.path():
                child = Node(child_state, self)
                children.append(child)

        if star_index + 3 <= 8:                                             # down
            child_state = swap(state, star_index, star_index + 3)
            if child_state not in self.path():
                child = Node(child_state, self)
                children.append(child)

        if star_index != 0 and star_index != 3 and star_index != 6:         # left
            child_state = swap(state, star_index, star_index - 1)
            if child_state not in self.path():
                child = Node(child_state, self)
                children.append(child)

        return children

    def path(self):
        """
        Finds the path from the given node to the root
        :return: list of states from node to root
        """
        node_path = [self]                              # add start node to path
        state_path = [self.state]                       # add start state to state path
        while not node_path[-1].is_root():              # while current node has a parent
            parent = node_path[-1].parent               # parent is last node in stack
            node_path.append(parent)                    # add parent to path
            state_path.append(parent.state)
        return state_path[::-1]                         # return stack in reverse

    def depth(self):
        """
        Get depth of node in tree by getting size of path
        :return: depth of node
        """
        return len(self.path())


def print_state(state):
    """
    Print the state as the puzzle matrix
    :param state: state to be printed
    """
    index = 0
    for i in range(3):                      # print row by row
        for j in range(3):                  # column by column
            print(state[index], end=' ')
            index += 1
        print(end='\n')


def swap(state, index_1, index_2):
    """
    Swap two values in state
    :param state: state being manipulated
    :param index_1: index of value being swapped
    :param index_2: index of value being swapped
    :return: state with swapped values
    """
    new_state = state.copy()
    new_state[index_1], new_state[index_2] = new_state[index_2], new_state[index_1]
    return new_state


def h1(node):
    """
    Heuristic function of A* search
    Calculates difference between values in given node and goal state
    Each value will be its integer value, * will be 9
    :param node: state being checked
    :return: difference between node values and goal state values
    """
    state = node.state
    result = 0
    for i in range(9):                                              # for each value in state
        if state[i] != '*' and GOAL_STATE[i] == '*':                # some value and *
            result += 9 - int(state[i])
        elif state[i] == '*' and GOAL_STATE[i] != '*':              # * and some value
            result += 9 - int(GOAL_STATE[i])
        elif state[i] != '*' and GOAL_STATE[i] != '*':              # two values
            result += abs(int(state[i]) - int(GOAL_STATE[i]))
    return result


def h2(node):
    """
    Heuristic function of A* search
    Calculates distance between current position and goal position
    :param node: state being checked
    :return: total distance between current state and goal state
    """
    state = node.state
    result = 0
    for i in range(9):                                              # check each index
        goal_index = GOAL_STATE.index(state[i])
        x1 = i % 3                                                  # get position of index
        if i - 6 >= 0:
            y1 = 2
        elif i - 3 >= 0:
            y1 = 1
        else:
            y1 = 0

        x2 = goal_index % 3                                         # get position of goal index
        if goal_index - 6 >= 0:
            y2 = 2
        elif goal_index - 3 >= 0:
            y2 = 1
        else:
            y2 = 0

        result += ((x2-x1)**2 + (y2-y1)**2)**0.5                    # compute distance between indices

    return result                                                   # return total distance


def dfs(node, depth):
    """
    Depth first search of puzzle
    :param node: start node
    :param depth: maximum depth for search
    :return: Null
    """
    global enqueued                 # number of enqueued states
    global path                     # path of search
    enqueued += 1

    if path:                        # if the path has been found finish process
        return

    if node.depth() > depth:        # if the max depth has been reached end
        return

    if node.state == GOAL_STATE:    # if the goal has been reached end
        path = node.path()          # set path to node's path
        return

    for child in node.expand():     # for each of the node's children
        dfs(child, depth)           # search for that child

    return


def ids(node):
    """
    Iterative dfs for 8 puzzle search
    :param node: root node for search
    :return: null
    """
    for depth in range(MAX_DEPTH):  # iterate through depths
        dfs(node, depth)            # call dfs with current depth
        if path:                    # exit if solution found
            return


def astar(node, h):
    """
    A* algorithm for 8 puzzle search
    :param node: root node
    :param h: heuristic function h(x)
    :return: null
    """
    global path                                             # path list
    global enqueued                                         # number of states enqueued

    states_enqueued = []                                    # list of states enqueued
    visited = []                                            # list of states visited
    curr = node                                             # current node for loop
    states_enqueued.append(curr)                            # add current node to states enqueued

    while h(curr) != 0:                                     # loop until solution found
        visited.append(curr)                                # add current node to visited path
        children = curr.expand()                            # get children of current node
        min_child = 10000                                   # minimum child for current node

        for child in children:
            if child not in states_enqueued:
                states_enqueued.append(child)

            fx = h(child) + child.depth()                   # calculate f(x) = h(x) + g(x)

            if fx < min_child and child not in visited:     # find minimum cost child and set to current
                min_child = fx
                curr = child

    if h(curr) == 0:                                        # check if current node is goal
        path = curr.path()
        enqueued = len(states_enqueued)


alg = sys.argv[1]                                   # algorithm for search
fp = sys.argv[2]                                    # filepath for input

f = open(fp, 'r')                                   # open and read file
text = f.readline()
f.close()

start_state = text.split()                          # split input into array

root = Node(start_state, None)

if alg == 'dfs':                                    # Depth First Search
    dfs(root, MAX_DEPTH)
elif alg == 'ids':                                  # Iterative Depth First Search
    ids(root)
elif alg == 'astar1':                               # A* with heuristic 1
    astar(root, h1)
elif alg == 'astar2':                               # A* with heuristic 2
    astar(root, h2)
else:
    print("Algorithm options are: dfs, ids, astar1, astar2")
    exit()

if path:                        # if the puzzle is solved print the results
    for s in path:
        print_state(s)
        print()
    print("Number of moves: {}\nNumber of states enqueued: {}".format(len(path) - 1, enqueued))
else:
    print("Solution could not be found in depth {}".format(MAX_DEPTH))
