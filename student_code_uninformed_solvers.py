from solver import *
from queue import Queue


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.expand()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        current = self.currentState
        self.visited[current] = True
        if current.state == self.victoryCondition:
            return True
        while current.nextChildToVisit < len(current.children):
            temp = current.children[current.nextChildToVisit]
            current.FIRST_CHILD_INDEX += 1
            if temp in self.visited:
                pass
            else:
                self.visited[temp] = False
                self.gm.makeMove(temp.requiredMovable)
                self.currentState = temp
                self.expand()
                return False
        if current.requiredMovable == False:
            return False
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
        
    def expand(self):
        movables = self.gm.getMovables()
        for temp in movables:
            self.gm.makeMove(temp)
            child = GameState(self.gm.getGameState(), self.currentState.depth + 1, temp)
            if child not in self.visited:
                pass
            else:
                self.gm.reverseMove(temp)
                continue
            self.currentState.children.append(child)
            child.parent = self.currentState
            self.gm.reverseMove(temp)


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.my_init()
        
    def my_init(self):
        self.init = False
        self.queue = Queue()
        self.queue.put(self.currentState)

    def generate(self, target_state):
        paths = []
        current = target_state
        while current.parent:
            temp = current.requiredMovable
            paths.insert(0, temp)
            current = current.parent
        return paths

    def back(self,):
        current = self.currentState
        while current.parent is not None:
            temp = current.requiredMovable
            self.gm.reverseMove(temp)
            current = current.parent
            
    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.init:
            pass
        else:
            self.init = True
            self.solveOneStep()
        if self.queue == False:
            pass
        else:
            target = self.queue.get()
            self.back()
            required = self.generate(target)
            for move in required:
                self.gm.makeMove(move)
            self.currentState = target
            self.visited[target] = True
            if target.state == self.victoryCondition:
                return True
            movables = self.gm.getMovables()
            for move in movables:
                self.gm.makeMove(move)
                temp = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                self.currentState.children.append(temp)
                temp.parent = self.currentState
                if temp not in self.visited:
                    pass
                else:
                    self.gm.reverseMove(move)
                    continue
                self.visited[temp] = False
                self.queue.put(temp)
                self.gm.reverseMove(move)

