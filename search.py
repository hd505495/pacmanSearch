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
    """Search the deepest nodes in the search tree first."""
    fringe = util.Stack()
    explored = []

    node = (problem.getStartState(), [])  # tuple containing state and list for actions
    fringe.push(node)

    while not fringe.isEmpty():
        currState, actions = fringe.pop()  # take from top of stack

        if currState not in explored:  # prevent cycles in graph
            explored.append(currState)
            if problem.isGoalState(currState):
                return actions
            else:
                for childState, childAction, childCost in problem.getSuccessors(currState):
                    updatedActionsList = actions + [childAction]  # can only append list to list
                    nextNode = (childState, updatedActionsList)
                    fringe.push(nextNode)
    return actions
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    fringe = util.Queue()
    explored = []

    node = (problem.getStartState(), [])  # tuple containing state and list for actions
    fringe.push(node)

    while not fringe.isEmpty():
        currState, actions = fringe.pop()  # takes from front of queue

        if currState not in explored:  # prevent cycles in graph
            explored.append(currState)
            if problem.isGoalState(currState):
                return actions
            else:
                for childState, childAction, childCost in problem.getSuccessors(currState):
                    updatedActionsList = actions + [childAction]  # can only append list to list
                    nextNode = (childState, updatedActionsList)
                    fringe.push(nextNode)
    return actions

    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # this data structure does a lot of work for the ucs algorithm,
    # so the rest of this function will look quite similar to bfs, dfs traversal
    frontier = util.PriorityQueue()  # priority queue ordered by past cost g
    explored = {}  # dictionary with state as key, cost as value

    node = (problem.getStartState(), [], 0)  # tuple of state, action list, cost
    # push not update here bc frontier is previously empty
    frontier.push(node, 0)  # this push takes item and priority

    while not frontier.isEmpty():
        # pops lowest cost node due to PriorityQueue structure
        currState, actions, currCost = frontier.pop()

        # always keep least cost path for any node
        if (currState not in explored) or (currCost < explored[currState]):
            explored[currState] = currCost

            if problem.isGoalState(currState):
                return actions
            else:
                for childState, childAction, childCost in problem.getSuccessors(currState):
                    updatedActionsList = actions + [childAction]  # can only append list to list
                    updatedCost = currCost + childCost
                    nextNode = (childState, updatedActionsList, updatedCost)

                    # If item already in priority queue with higher priority, update its priority and rebuild the heap.
                    # If item already in priority queue with equal or lower priority, do nothing.
                    # If item not in priority queue, do the same thing as self.push.
                    frontier.update(nextNode, updatedCost)
    return actions
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    explored = []

    node = (problem.getStartState(), [], 0)
    frontier.push(node, 0)

    while not frontier.isEmpty():
        # priority has sorted, taking lowest cost node
        currState, actions, currCost = frontier.pop()
        if currState not in explored:
            explored.append((currState, currCost))

        if problem.isGoalState(currState):
            return actions
        else:
            for childState, childAction, childCost in problem.getSuccessors(currState):
                updatedActionsList = actions + [childAction]  # can only append list to list
                #updatedCost = currCost + childCost
                updatedCost = problem.getCostOfActions(updatedActionsList)
                nextNode = (childState, updatedActionsList, updatedCost)

                isExplored = False  # want to know if expanded child node has been visited
                for exploredNode in explored:  # don't worry about states already explored
                    exploredState, exploredCost = exploredNode
                    if childState == exploredState:
                        # only disregard when expanded child's cost is more
                        if updatedCost >= exploredCost:
                            isExplored = True
                if not isExplored:
                    # frontier.push(nextNode, updatedCost + heuristic(childState, problem))
                    frontier.push(nextNode, updatedCost)
                    # explored.append((childState, childCost))
    return actions

    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
