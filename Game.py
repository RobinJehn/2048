import numpy as np
import random

class Game():
    
    def __init__(self, visual):
        self.board = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.previousState = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.addRandomTwo()
        self.visual = visual
    
    
    def addRandomTwo(self):
        indices = [i for i, x in enumerate(self.board) if x == 0]
        index = random.choice(indices)
        self.board[index] = 2
        
    def checkIfMax(self, reward):
        for i in range(16):
            if self.board[i] > self.board[15]:
                return 0 if reward > 0 else reward
        return reward
        
    def getPreviousState(self):
        return self.previousState
      
    def play(self, render, action):
        stopped = False
        self.previousState = self.board
        
        # Down
        if action == 0:
            d_arr, reward = self.down()
            if (np.array_equal(self.board, d_arr)): # If action not possible
                if np.array_equal(self.board, self.left()[0]) and np.array_equal(self.board, self.up()[0]) and np.array_equal(self.board, self.right()[0]):
                    if render == True:
                        self.visual.drawLoosingMessage()
                    stopped = True
            
                reward = -4
            else:
                self.board = d_arr
                self.addRandomTwo()
                if render == True:
                    self.visual.displayBoard(self.board)
            
        # Left
        elif action == 1:
            l_arr, reward = self.left()
            if (np.array_equal(self.board, l_arr)): # If action not possible
                if np.array_equal(self.board, self.down()[0]) and np.array_equal(self.board, self.up()[0]) and np.array_equal(self.board, self.right()[0]):
                    if render == True:
                        self.visual.drawLoosingMessage()
                    stopped = True
            
                reward = -4
            else:
                self.board = l_arr
                self.addRandomTwo()
                if render == True:
                    self.visual.displayBoard(self.board)
        
        # Up
        elif action == 2:
            u_arr, reward = self.up()
            if (np.array_equal(self.board, u_arr)): # If action not possible
                if np.array_equal(self.board, self.down()[0]) and np.array_equal(self.board, self.left()[0]) and np.array_equal(self.board, self.right()[0]):
                    if render == True:
                        self.visual.drawLoosingMessage()
                    stopped = True
            
                reward = -4
            else:
                self.board = u_arr
                self.addRandomTwo()
                if render == True:
                    self.visual.displayBoard(self.board)
            
        
        # Right
        elif action == 3:
            r_arr, reward = self.right()
            if (np.array_equal(self.board, r_arr)): # If action not possible
                if np.array_equal(self.board, self.left()[0]) and np.array_equal(self.board, self.up()[0]) and np.array_equal(self.board, self.down()[0]):
                    if render == True:
                        self.visual.drawLoosingMessage()
                    stopped = True
            
                reward = -4
            else:
                self.board = r_arr
                self.addRandomTwo()
                if render == True:
                    self.visual.displayBoard(self.board)

        if render == True:
            self.visual.update()

        #Check if max is in bottom right corner
        reward = self.checkIfMax(reward)

        return reward, stopped
        
    def down(self):
        reward = 0
        arr = self.board.copy()
        for i in range(4):
            for j in range(3):
                for k in range(3-j):
                    if arr[(3-j)*4+i] == arr[(2-j-k)*4+i] and arr[(3-j)*4+i] != 0:
                        arr[(3-j)*4+i] = 2*arr[(3-j)*4+i]
                        arr[(2-j-k)*4+i] = 0
                        reward += arr[(3-j)*4+i]
                        break
                    if arr[(2-j-k)*4+i] != 0:
                        break

        for i in range(4):
            for j in range(3):
                    if arr[(3-j)*4+i] == 0:
                        for k in range(3-j):
                            if arr[(3-j)*4+i] == 0:
                                arr[(3-j)*4+i] = arr[(2-k-j)*4+i] 
                                arr[(2-k-j)*4+i] = 0

        return arr, reward

    def left(self):
        reward = 0
        arr = self.board.copy()
        for i in range(4):
            for j in range(3):
                for k in range(3-j):
                    if arr[i*4+j] == arr[i*4+j+1+k] and arr[i*4+j] != 0:
                        arr[i*4+j] = 2*arr[i*4+j]
                        arr[i*4+j+1+k] = 0
                        reward += arr[i*4+j]
                        break
                    if arr[i*4+j+1+k] != 0:
                        break

        for i in range(4):
            for j in range(3):
                    if arr[i*4+j] == 0:
                        for k in range(3-j):
                            if arr[i*4+j] == 0:
                                arr[i*4+j] = arr[i*4+j+1+k] 
                                arr[i*4+j+1+k] = 0
                                
        return arr, reward

    def right(self):
        reward = 0
        arr = self.board.copy()
        for i in range(4):
            for j in range(3):
                for k in range(3-j):
                    if arr[4*(4-i)-j-1] == arr[4*(4-i)-j-2-k] and arr[4*(4-i)-j-1] != 0:
                        arr[4*(4-i)-j-1] = 2*arr[4*(4-i)-j-1]
                        arr[4*(4-i)-j-2-k] = 0
                        reward += arr[4*(4-i)-j-1]
                        break
                    if arr[4*(4-i)-j-2-k] != 0:
                        break

        for i in range(4):
            for j in range(3):
                    if arr[4*(4-i)-j-1] == 0:
                        for k in range(3-j):
                            if arr[4*(4-i)-j-1] == 0:
                                arr[4*(4-i)-j-1] = arr[4*(4-i)-j-2-k] 
                                arr[4*(4-i)-j-2-k] = 0
                                
        return arr, reward

    def up(self):
        reward = 0
        arr = self.board.copy()
        for i in range(4):
            for j in range(3):
                for k in range(3-j):
                    if arr[j*4+3-i] == arr[(j+1+k)*4+3-i] and arr[j*4+3-i] != 0:
                        arr[j*4+3-i] = 2*arr[j*4+3-i]
                        arr[(j+1+k)*4+3-i] = 0
                        reward = arr[j*4+3-i]
                        break
                    if arr[(j+1+k)*4+3-i] != 0:
                        break

        for i in range(4):
            for j in range(3):
                    if arr[j*4+3-i] == 0:
                        for k in range(3-j):
                            if arr[j*4+3-i] == 0:
                                arr[j*4+3-i] = arr[(j+1+k)*4+3-i] 
                                arr[(j+1+k)*4+3-i] = 0
                                
        return arr, reward
