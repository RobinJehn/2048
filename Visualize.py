from pygame.locals import *
import pygame, sys, time, random
import pygame.gfxdraw
import AI

class Visualize():
    
    def __init__(self, width, height):
        self.showTrainOption = False
        self.showPlayTrainedModel = False
        self.width = width
        self.height = height
        self.center_x = int(width / 2)
        self.center_y = int(height / 2)
        self.board_top_left_x = self.center_x - 335
        self.board_top_left_y = self.center_y - 335
        self.initializeScreen()
        self.initializeFonts()
        self.ai = AI.AI(self)
        print('Visualization initialized')
     
    def update(self):
        pygame.display.update()
     
    def initializeScreen(self):
        self.mainClock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption('2048')
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        
    def initializeFonts(self):
        self.smallText = pygame.font.Font("freesansbold.ttf",20)
        self.mediumText = pygame.font.Font("freesansbold.ttf",60)
        self.largeText = pygame.font.Font("freesansbold.ttf",100)
        
    def drawText(self, text, font, color, x, y):
        textobj, textrect = self.textObjects(text, font)
        textrect.center = (x, y)
        self.screen.blit(textobj, textrect)

    def textObjects(self, text, font):
        textobj = font.render(text, 1, (0,0,0))
        textrect = textobj.get_rect()
        return textobj, textrect
     
    def drawRoundedRect(self, rect, color, corner_radius):
        if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
            raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

        # need to use anti aliasing circle drawing routines to smooth the corners
        pygame.gfxdraw.aacircle(self.screen, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.aacircle(self.screen, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.aacircle(self.screen, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
        pygame.gfxdraw.aacircle(self.screen, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

        pygame.gfxdraw.filled_circle(self.screen, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.filled_circle(self.screen, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.filled_circle(self.screen, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
        pygame.gfxdraw.filled_circle(self.screen, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

        rect_tmp = pygame.Rect(rect)

        rect_tmp.width -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(self.screen, color, rect_tmp)

        rect_tmp.width = rect.width
        rect_tmp.height -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(self.screen, color, rect_tmp)
        

    def displayBoard(self, board):
        self.screen.fill((255,255,255))
        self.drawRoundedRect(pygame.Rect(self.board_top_left_x, self.board_top_left_y, 670, 670), (187, 174, 161), 10)
        for i in range (16): 
            if board[i] == 0:
                colour = (255, 255, 255)
            if board[i] == 2:
                colour = (238, 228, 217)
            if board[i] == 4:
                colour = (236, 224, 200)
            if board[i] == 8:
                colour = (241, 176, 120)
            if board[i] == 16:
                colour = (235, 140, 81)
            if board[i] == 32:
                colour = (244, 124, 96)
            if board[i] == 64:
                colour = (234, 87, 54)
            if board[i] == 128:
                colour = (242, 220, 106)
            if board[i] == 256:
                colour = (235, 206, 76)
            if board[i] == 512:
                colour = (228, 193, 43)
            if board[i] == 1024:
                colour = (221, 180, 10)
            if board[i] == 2048:
                colour = (236, 196, 0)
                
            x = self.board_top_left_x + 20 + 160*(i%4) 
            y = self.board_top_left_y + 20 + int(i/4) * 160
            text = str(board[i]) if board[i] > 0 else ''
            self.drawRoundedRect(pygame.Rect(x, y, 150, 150), colour, 10)
            self.drawText(text, self.mediumText, (0,0,0), x + 75, y + 75)

        for i in range(16):
            if board[i] == 2048:
                self.drawWinningMessage()

        pygame.display.update()
    
    def drawLoosingMessage(self):
        self.drawRoundedRect(pygame.Rect(880,620,800,200), (50, 50, 50), 10)
        self.drawText("You have lost!", self.largeText, (0, 0, 0), 1280, 720)
        pygame.display.update()
        
    def drawWinningMessage():
        self.drawRoundedRect(pygame.Rect(880,620,800,200), (50, 50, 50), 10)
        self.drawText("You have won!", self.largeText, (237, 204, 97), 1280, 720)
        pygame.display.update()
        main_menu()
        
    def mouseInRect(self, mouse_x, mouse_y, rect_x, rect_y, rect_w, rect_h):
        rect_x_upper_bound = int(rect_x + rect_w/2)
        rect_x_lower_bound = int(rect_x - rect_w/2)
        rect_y_upper_bound = int(rect_y + rect_h/2)
        rect_y_lower_bound = int(rect_y - rect_h/2)
        return  rect_x_upper_bound > mouse_x > rect_x_lower_bound and rect_y_upper_bound > mouse_y > rect_y_lower_bound
          
    def simulationButton(self, text, font, center_x, center_y, w, h, colour, hover_colour, render, games):
        top_left_x = int(center_x - w/2)
        top_left_y = int(center_y - h/2)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.mouseInRect(mouse_x, mouse_y, center_x, center_y, w, h):
            pygame.draw.rect(self.screen, hover_colour, (top_left_x, top_left_y, w, h)) # Hover animation
            if click[0] == 1:
                print('Simulation started. Render ' + str(render))
                self.ai.getTrainingData(games, render)
                self.showTrainOption = True
        else:
            pygame.draw.rect(self.screen, colour, (top_left_x, top_left_y, w, h))

        self.drawText(text, font, (0, 0, 0), center_x, center_y) # Button text
        
    def trainButton(self, text, font, center_x, center_y, w, h, colour, hover_colour):
        top_left_x = int(center_x - w/2)
        top_left_y = int(center_y - h/2)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if self.mouseInRect(mouse_x, mouse_y, center_x, center_y, w, h):
            pygame.draw.rect(self.screen, hover_colour, (top_left_x, top_left_y, w, h))
            if click[0] == 1:
                print('Training started')
                self.ai.trainOnData()
                self.showPlayTrainedModel = True
        else:
            pygame.draw.rect(self.screen, colour, (top_left_x, top_left_y, w, h))

        self.drawText(text, font, (0,0,0), center_x, center_y)
        
        
    def playModelButton(self, text, font, center_x, center_y, w, h, colour, hover_colour):
        top_left_x = int(center_x - w/2)
        top_left_y = int(center_y - h/2)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.mouseInRect(mouse_x, mouse_y, center_x, center_y, w, h):
            pygame.draw.rect(self.screen, hover_colour, (top_left_x, top_left_y, w, h))
            if click[0] == 1:
                print('Play model')
                self.ai.playModel()
                # Play Model
        else:
            pygame.draw.rect(self.screen, colour, (top_left_x, top_left_y, w, h))

        self.drawText(text, font, (0,0,0), center_x, center_y)

    def mainMenu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill((255,255,255)) # White background
            self.drawText('Main Menu', self.largeText, (0, 0, 0), int(self.width/2), 100) # Main Menu text  
            
            self.simulationButton("Start Game and Render", self.smallText, self.center_x, self.center_y, 280, 50, (100,100,100), (200,200,200), True, 10)
            self.simulationButton("Start Game without Render", self.smallText, self.center_x, self.center_y + 100, 280, 50, (100,100,100), (200,200,200), False, 1000)
            if self.showTrainOption:
                self.trainButton("Train on Data", self.smallText, self.center_x, self.center_y + 200, 280, 50, (100,100,100), (200,200,200))

            if self.showPlayTrainedModel:
                self.playModelButton("Play with Model", self.smallText, self.center_x, self.center_y + 300, 280, 50, (100,100,100), (200,200,200))

            pygame.display.update()
            self.mainClock.tick(60)


visuals = Visualize(1920, 1080)
visuals.mainMenu()