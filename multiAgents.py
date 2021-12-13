# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        foodList = childGameState.getFood().asList()
        minFood = float('inf')
        for food in foodList:
            dist = manhattanDistance(newPos, food)
            if dist < minFood:
                minFood = dist

        ghostDist = 0
        for ghost in currentGameState.getGhostPositions():
            ghostDist = manhattanDistance(newPos, ghost)
            if (ghostDist < 2):
                return -float('inf')

        return childGameState.getScore() + 1/minFood

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        "*** YOUR CODE HERE ***"

        def minimax(self, gameState, agentIndex, checkDepth):
            #print("1")

            #When finish a round -> reset
            if agentIndex == gameState.getNumAgents():
                agentIndex = 0
                checkDepth += 1

            #Max Depth
            if checkDepth == self.depth:
                return self.evaluationFunction(gameState)

            #Win or Lose
            if gameState.isWin() or gameState.isLose():
                #print("Win or Lose")
                return self.evaluationFunction(gameState)

            if agentIndex == self.index:
                #For Pacman we call max_Function
                return maxF(self,gameState, agentIndex, checkDepth)
            else:
                #For Ghosts we call min_Function
                return minF(self,gameState, agentIndex, checkDepth)

            #error
            pass

        def maxF(self, gameState, agentIndex, checkDepth):
            #print("2")

            value = float('-inf') # # representation of negative infinity in python
            finalAction = "NONE" # set finalAction as "none" in case there is no possible Action

            for action in gameState.getLegalActions(agentIndex):

                if action == Directions.STOP:
                    continue

                successor = gameState.getNextState(agentIndex, action)
                evaluation = minimax(self,successor, agentIndex + 1, checkDepth)

                if value < evaluation:
                    value = max(value, evaluation)
                    finalAction = action

            if checkDepth == 0:
                return finalAction
            else:
                return value

        def minF(self, gameState, agentIndex, checkDepth):
            #print("3")

            value = float('inf') # representation of positive infinity in python

            for action in gameState.getLegalActions(agentIndex):

                if action == Directions.STOP:
                    continue

                successor = gameState.getNextState(agentIndex, action)
                evaluation = minimax(self,successor, agentIndex + 1, checkDepth)

                if value > evaluation:
                    value = min(value, evaluation)

            return value

        #call 'minimax' function with self, gamestate and
        # agentIndex=0 which means we talk about pacman and depth = 0
        return minimax(self,gameState, 0, 0)

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def alpha_beta(self, gameState, agentIndex, checkDepth, alpha, beta):
            #print("1")

            #When finish a round -> reset
            if agentIndex == gameState.getNumAgents():
                agentIndex = 0
                checkDepth += 1

            #Max Depth
            if checkDepth == self.depth:
                return self.evaluationFunction(gameState)

            #Win or Lose
            if gameState.isWin() or gameState.isLose():
                #print("Win or Lose")
                return self.evaluationFunction(gameState)

            if agentIndex == self.index:
                #For Pacman we call max_Function
                return maxF(self,gameState, agentIndex, checkDepth, alpha, beta)
            else:
                return minF(self,gameState, agentIndex, checkDepth, alpha, beta)

            #error
            pass

        def maxF(self, gameState, agentIndex, checkDepth, alpha, beta):
            #print("2")

            value = float('-inf') # negative inf
            finalAction = "NONE" # set finalAction as "none" in case there is no possible Action

            for action in gameState.getLegalActions(agentIndex):

                if action == Directions.STOP:
                    continue

                successor = gameState.getNextState(agentIndex, action)
                evaluation = alpha_beta(self,successor, agentIndex + 1, checkDepth, alpha, beta)

                if value < evaluation:
                    value = max(value, evaluation)
                    finalAction = action

                #pruning
                alpha = max(alpha,evaluation)
                if beta < alpha:
                    break

            if checkDepth == 0:
                return finalAction
            else:
                return value

        def minF(self, gameState, agentIndex, checkDepth, alpha, beta):
            #print("3")

            value = float('inf')

            for action in gameState.getLegalActions(agentIndex):

                if action == Directions.STOP:
                    continue

                successor = gameState.getNextState(agentIndex, action)
                evaluation = alpha_beta(self,successor, agentIndex + 1, checkDepth, alpha, beta)

                if value > evaluation:
                    value = min(value, evaluation)

                #pruning
                beta = min(beta,evaluation)
                if beta < alpha:
                    break

            return value

        return alpha_beta(self,gameState,0,0,float('-inf'),float('inf'))

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectimax(self, gameState, agentIndex, checkDepth):

            #When finish a round -> reset
            if agentIndex == gameState.getNumAgents():
                agentIndex = 0
                checkDepth += 1

            #Max Depth
            if checkDepth == self.depth:
                return self.evaluationFunction(gameState)

            #Win or Lose
            if gameState.isWin() or gameState.isLose():
                #print("Win or Lose")
                return self.evaluationFunction(gameState)

            if agentIndex == self.index:
                #For Pacman we call max_Function
                return maxF(self,gameState, agentIndex, checkDepth)
            else:
                return expectF(self,gameState, agentIndex, checkDepth)

            #error
            pass

        def maxF(self, gameState, agentIndex, checkDepth):

            value = -999999 # negative inf
            finalAction = "NONE" # set finalAction as "none" in case there is no possible Action

            for action in gameState.getLegalActions(agentIndex):

                if action == Directions.STOP:
                    continue

                successor = gameState.getNextState(agentIndex, action)
                evaluation = expectimax(self,successor, agentIndex + 1, checkDepth)

                if value < evaluation:
                    value = max(value, evaluation)
                    finalAction = action

            if checkDepth == 0:
                return finalAction
            else:
                return value

        def expectF(self,gameState,agentIndex,checkDepth):

            value = 0
            
            for action in gameState.getLegalActions(agentIndex):
                
                if action == Directions.STOP:
                    continue

                successor = gameState.getNextState(agentIndex, action)
                evaluation = expectimax(self, successor, agentIndex + 1, checkDepth)
                
                value += evaluation / len(gameState.getLegalActions(agentIndex)) #probability

            print(value)
            return value
            
            
        return expectimax(self,gameState,0,0)
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    foodLeft = currentGameState.getNumFood()
    capsulesLeft = len(currentGameState.getCapsules())
    
    ghostDist = 0
    for ghost in currentGameState.getGhostPositions():
        ghostDist = manhattanDistance(newPos, ghost)
        #ghost too close
        if (ghostDist < 2):
            return -float('inf')

    #same as q1
    minFood = float('inf')
    for food in foodList:
        dist = manhattanDistance(newPos, food)
        if dist < minFood:
            minFood = dist

    win_or_lose = 0
    if currentGameState.isLose():
        win_or_lose = -1000
    elif currentGameState.isWin():
        win_or_lose = 1000

    foodLeftWeight = 9000#950050
    capsLeftWeight = 1000#10000
    foodDistWeight = 80#950

    finalFoodLeft = (1/(foodLeft+1)) * foodLeftWeight
    finalMinFood = (1/(minFood+1)) * foodDistWeight
    finalCapsulesLeft = (1/(capsulesLeft+1)) * capsLeftWeight

    return finalFoodLeft + finalMinFood + finalCapsulesLeft + win_or_lose + ghostDist


    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
