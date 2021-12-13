# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util




class Node:

    def __init__(self,state,parent,action,path_cost):
        self.state = state
        self.parent = parent 
        self.action = action
        self.path_cost = path_cost

def comperator(item1,item2):
    return item1.path_cost < item2.path_cost


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    
    from util import Stack

    actions = []                                                                        #list of actions to get to the goal

    flag = 0
    visited = []                                                                        #visited is the set of the nodes that have been visitied
    nodes = Stack()                                                                     #a stack with the nodes to be visited     
    nodes.push(Node(problem.getStartState(),None,None,0))                               #the current node     
    visited.append(problem.getStartState())

    while not nodes.isEmpty():
        current = nodes.pop()                                                           #the current state
        visited.append(current.state)
        if problem.isGoalState(current.state):
            flag = 1
            break 
        successors = problem.getSuccessors(current.state)                               #getting the successors of the current state
        for succ in successors:
            if succ[0] not in visited:
                nodes.push(Node(succ[0],current,succ[1],succ[2]))
                


    if flag == 0:                                                             #In case there's no path available to our goal
        print("No path can be found for the solution")
        return None
    else:                                                                           #There's a path
        while current != None :                                                     #Backtracking
            actions.append(current.action)
            current = current.parent

        actions.pop(len(actions)-1)                                                 #The root contains an action of "None" so we remove it from our list of actions
        actions.reverse()                                                           #We reverse the list since we've done the backtracking from the end 
        return actions                                                              #"Job's Done!"


    '''print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    '''


   


def breadthFirstSearch(problem):

    from util import Queue

    flag = 0
    visited = []                                                                    #List of visited nodes
    actions = []                                                                    #List of actions to be returned
    nodes = Queue()                                                                 #A queue for bfs

    

    nodes.push(Node(problem.getStartState(),None,None,0))
    visited.append(problem.getStartState())

    while not nodes.isEmpty():
        current = nodes.pop()
        if problem.isGoalState(current.state):
            flag = 1
            break
        successors = problem.getSuccessors(current.state)
        for succ in successors:
            if succ[0] not in visited:
                nodes.push(Node(succ[0],current,succ[1],succ[2]))
                visited.append(succ[0])
    
    if flag == 0:                                                             #In case there's no path available to our goal
        print("No path can be found for the solution")
        return None
    else:                                                                           #There's a path
        while current != None :                                                     #Backtracking
            actions.append(current.action)
            current = current.parent

        actions.pop(len(actions)-1)                                                 #The root contains an action of "None" so we remove it from our list of actions
        actions.reverse()                                                           #We reverse the list since we've done the backtracking from the end 
        return actions                                                              #"Job's Done!
    



    
def uniformCostSearch(problem):
    
    from util import PriorityQueue

    flag = 0
    nodes = PriorityQueue()
    actions = []                                                                    #List of actions pacman needs to do to get to the goal
    visited = []                                                                    #Set of the nodes pacman has visited 
    current = Node(problem.getStartState(),None,None,0)                             #Initializing the current node with the starting position of Pacman
    nodes.push(current,current.path_cost)                                           #Adding current as the first node to our Priority Queue                                                   


    while not nodes.isEmpty():

        current = nodes.pop()
        if current.state not in visited:
            visited.append(current.state)
            if problem.isGoalState(current.state):
                flag = 1
                break
            succesors = problem.getSuccessors(current.state)
            for succ in succesors:
                nodes.push(Node(succ[0],current,succ[1],succ[2]+current.path_cost),succ[2] + current.path_cost) 
    
    if flag == 0:                                                             #In case there's no path available to our goal
        print("No path can be found for the solution")
        return None
    else:                                                                           #There's a path
        while current != None :                                                     #Backtracking
            actions.append(current.action)
            current = current.parent

        actions.pop(len(actions)-1)                                                 #The root contains an action of "None" so we remove it from our list of actions
        actions.reverse()                                                           #We reverse the list since we've done the backtracking from the end 
        return actions                                                              #"Job's Done!





def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):


    from util import PriorityQueue

    nodes = PriorityQueue()
    actions = []                                                                    #List of actions pacman needs to do to get to the goal
    visited = []                                                                    #Set of the nodes pacman has visited 
    current = Node(problem.getStartState(),None,None,0)                             #Initializing the current node with the starting position of Pacman
    nodes.push(current,current.path_cost)                                           #Adding current as the first node to our Priority Queue                                                 
    flag = 0


    while not nodes.isEmpty():

        current = nodes.pop()
        if current.state not in visited:
            visited.append(current.state)
            if problem.isGoalState(current.state):
                flag = 1
                break
            succesors = problem.getSuccessors(current.state)
            for succ in succesors:
                if succ[0] not in visited:
                    nodes.push(Node(succ[0],current,succ[1],succ[2]+current.path_cost),succ[2] + current.path_cost + heuristic(succ[0],problem)) 
                
    
    if flag == 0:                                                                   #In case there's no path available to our goal
        print("No path can be found for the solution")
        return None
    else:                                                                           #There's a path
        while current != None :                                                     #Backtracking
            actions.append(current.action)
            current = current.parent

        actions.pop(len(actions)-1)                                                 #The root contains an action of "None" so we remove it from our list of actions
        actions.reverse()                                                           #We reverse the list since we've done the backtracking from the end 
        return actions                                                              #"Job's Done!

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
