# CS-4365-Assignment-1
## 8 Puzzle Solver Using DFS, IDS, and A* Algorithms
Author :            Brigham Thornock

Class :             CS 4365.002

Last Modification : 2/9/2023

Summary :   

            This script will take a file input of line of numbers representing an 8 puzzle.

            For example:
            Input: 7 1 * 6 8 2 5 4 3
            Puzzle Representation:  7 6 1
                                    * 8 2
                                    5 4 3
            
            The puzzle can be solved by swapping * with nearby numbers until the goal state is reached
            Goal State: 7 8 1
                        6 * 2
                        5 4 3
            
            This script solves the puzzle using Depth First Search (DFS), Iterative Depth Limited Search (IDS), and A* using two different heuristic functions.
            
Usage:      python assignment_1.py <algorithm> <input_file>
            
            Where <algorithm> is dfs, ids, astar1, or astar2 and <input_file> is the file used for puzzle start state in one line

