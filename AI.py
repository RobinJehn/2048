import Game
import random
import time
import numpy as np
from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.python.keras import backend as K

config = tf.compat.v1.ConfigProto( device_count = {'GPU': 1 , 'CPU': 4} )
sess = tf.compat.v1.Session(config=config) 
K.set_session(sess)

class AI():
    
    def __init__(self, visual):
        self.training_data = [] # [Observation, Action]
        self.initializeModel()
        self.visual = visual
      
    def playModel(self):
        for i in range(1):
            game = Game.Game(self.visual)
            for i in range(1000):
                prediction = self.model.predict(np.array([game.board]))
                print(prediction)
                action = np.argmax(prediction, axis = 1)
                reward, stopped = game.play(True, action)
                if stopped == True:
                    time.sleep(5)
                    self.visual.mainMenu()
                else:
                    while reward == -4:
                        action = random.randint(0,3)
                        reward, stopped = game.play(True, action)

                print("Move: " + str(i) + "; Action: " + str(action))
                
      
    def getTrainingData(self, games, render):
        game_steps = 1000000
        for i in range(games):
            stopped = False
            game = Game.Game(self.visual)

            for j in range(game_steps):
                action = random.randint(0,3)
                reward, stopped = game.play(render, action)
                if render:
                    print("Game step: " + str(j) + "; Action: " + str(action) + "; Reward: " + str(reward))
                
                if reward > 0:
                    # convert to one-hot (this is the output layer for our neural network)
                    if action == 0:
                        output = [1,0,0,0]
                    elif action == 1:
                        output = [0,1,0,0]
                    elif action == 2:
                        output = [0,0,1,0]
                    elif action == 3:
                        output = [0,0,0,1]
                        
                    # saving our training data
                    self.training_data.append([game.getPreviousState(), output])
                if stopped:
                    break
        print(len(self.training_data))
            
    def trainOnData(self):
        self.trainModel()
        test_x = np.array([[0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0]])
        prediction = self.model.predict(test_x)
        print(prediction)
        print("\nIndices of Max element : ", np.argmax(prediction, axis = 1))       
     
    def initializeModel(self):
        self.model = Sequential()
        self.model.add(Dense(12, input_dim=16, activation='relu'))
        self.model.add(Dense(8, activation='relu'))
        self.model.add(Dense(8, activation='relu'))
        self.model.add(Dense(4, activation='relu'))
        self.model.add(Dense(4, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        
    def trainModel(self):
        input = np.array([data_point[0] for data_point in self.training_data])
        for i in range (10):
            print(input[i])

        output = np.array([data_point[1] for data_point in self.training_data])            

        history = self.model.fit(input, output, epochs=100, batch_size=64)
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['loss'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Accuracy', 'Loss'], loc='upper left')
        plt.show()