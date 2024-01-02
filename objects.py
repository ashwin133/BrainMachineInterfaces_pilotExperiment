"""
create classes for game
"""
import pygame
import numpy as np

class GameStats():
    """
    Holds all game performance related information
    """
    def __init__(self):
        pass


class Wall():
    import pygame

import pygame

class Maze():

    def __init__(self,mazeDims,gameEngine):
        self.wallList = []
        # def each wall and add it to list
        for wall in range(len(mazeDims[:,0])):
            wall_ = Wall(gameEngine,(mazeDims[wall,0],mazeDims[wall,1]),(mazeDims[wall,2],mazeDims[wall,3]),wall)
            self.wallList.append(wall_)

        

import pygame
import math
import random

class Wall:
    def __init__(self, gameEngine, top_left, bottom_right, id, color=None):
        """
        Initialize a Wall object with oscillation properties.

        Inputs:
        @param: top_left (tuple): The (x, y) coordinates for the top left corner.
        @param: bottom_right (tuple): The (x, y) coordinates for the bottom right corner.
        @param: color (tuple): Wall color.
        @param: oscillation_axis (str): Axis of oscillation ('vertical' or 'horizontal').
        @param: oscillation_range (int): Maximum distance the wall moves from the initial position.
        @param: oscillation_speed (float): Speed of oscillation.
        """
        self.move = False
        oscillationTypes = ['vertical','horizontal']
        self.id = id
        self.initial_top_left = top_left
        self.initial_bottom_right = bottom_right
        self.oscillation_axis = random.choice(oscillationTypes)
        self.oscillation_range = random.uniform(40,50)
        self.oscillation_speed = random.uniform(0.23,0.3)
        self.time = 0  # Internal timer for oscillation

        # Calculate width and height based on the top left and bottom right points
        self.width = bottom_right[0] - top_left[0]
        self.height = bottom_right[1] - top_left[1]

        # Create the pygame.Rect object
        self.rect = pygame.Rect(top_left, (self.width, self.height))
        # Set default color
        self.color = color if color else gameEngine.colours['BLACK']

    def update(self):
        """
        Update the wall position to make it oscillate.
        """
        if self.id > 3 and self.move == True:
            # Calculate the oscillation offset
            if self.oscillation_axis == 'vertical':
                offset = self.oscillation_range * math.sin(self.time * self.oscillation_speed)
                self.rect.y = self.initial_top_left[1] + offset
            elif self.oscillation_axis == 'horizontal':
                offset = self.oscillation_range * math.sin(self.time * self.oscillation_speed)
                self.rect.x = self.initial_top_left[0] + offset

            # Increment the internal timer
            self.time += 1

    def draw(self, gameEngine):
        """
        Draw the wall onto a screen.

        Inputs:
        @param: screen (pygame.Surface): The Pygame surface to draw the wall on.
        """
        pygame.draw.rect(gameEngine.screen, self.color, self.rect)




class Cursor:
    def __init__(self, x, y, width, height, color,imagePaths,frozenColour = (255,0,0),useImg = True):
        """
        Initialize a velocity-controlled cursor with inertia.

        Args:
            x (int): The x-coordinate of the cursor's starting position.
            y (int): The y-coordinate of the cursor's starting position.
            width (int): The width of the cursor.
            height (int): The height of the cursor.
            color (tuple): The color of the cursor in RGB.

        """
        self.useImg = useImg
        self.rect = pygame.Rect(x, y, width, height)
        self.startingRect = self.rect
        self.healthyCursorColour = color
        self.color = self.healthyCursorColour
        self.frozenCursorColour = frozenColour  # set at red
        self.velocity = [0, 0]  # Velocity in pixels per frame (x, y)
        self.acceleration = 2    # Acceleration rate
        self.friction = 0.92      # Friction coefficient
        self.is_frozen = False
        self.cooldown = 2000 # cooldown time when frozen from hitting wall in ms 
        self.last_hit_time = None # store time of hit
        self.resetLatch = 0
        # Scale the image
        if self.useImg:
            self.images = {direction: pygame.image.load(path) for direction, path in imagePaths.items()}
            for key in self.images.keys():
                self.images[key] = pygame.transform.scale(self.images[key], (width, height))
            #self.rect = self.image.get_rect(topleft=(x, y))
        self.currentImage = self.images['right']
    def update(self):
        """
        Update the cursor's position based on its velocity, applying friction.
        """
        if self.is_frozen:
            self.velocity[0] = 0
            self.velocity[1] = 0
        else:

            # Apply friction to the velocity to create inertia
            self.velocity[0] *= self.friction
            self.velocity[1] *= self.friction

            # Update the cursor's position
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

            # Keep the cursor within the window bounds
            if self.rect.left < 0:
                self.rect.left = 0
                self.velocity[0] = 0
            if self.rect.right > pygame.display.get_surface().get_width():
                self.rect.right = pygame.display.get_surface().get_width()
                self.velocity[0] = 0
            if self.rect.top < 0:
                self.rect.top = 0
                self.velocity[1] = 0
            if self.rect.bottom > pygame.display.get_surface().get_height():
                self.rect.bottom = pygame.display.get_surface().get_height()
                self.velocity[1] = 0
        self.selectImageBasedOnDirection()
            
    def selectImageBasedOnDirection(self):
        # change image based on velocity
        try:
            velAngle = np.rad2deg(np.arctan(np.abs(self.velocity[1]/self.velocity[0])))
        except ZeroDivisionError:
            if self.velocity[1] > 0: 
                velAngle = 270
            elif self.velocity[1] < 0:
                velAngle = 90
            else:
                velAngle = 0
        

        if self.velocity[0] > 0 and self.velocity[1] < 0:
            velAngle = velAngle
        elif self.velocity[0] < 0 and self.velocity[1] < 0:
            velAngle = 180 - velAngle
        elif self.velocity[0] < 0 and self.velocity[1] > 0:
            velAngle = 180 + velAngle
        elif self.velocity[0] > 0 and self.velocity[1] > 0:
            velAngle = 360 - velAngle
        
        print(velAngle)

        if  45 < velAngle < 135:
            self.currentImage = self.images['up']
        elif 135 < velAngle < 225:
            self.currentImage = self.images['left']
        elif 225 < velAngle < 315:
            self.currentImage = self.images['down']
        elif velAngle < 45 or velAngle > 315:
            self.currentImage = self.images['right']


    def draw(self, screen):
        """
        Draw the cursor onto the screen.

        Args:
            screen (pygame.Surface): The surface to draw the cursor on.
        """
        if self.useImg:
            screen.blit(self.currentImage, self.rect)

        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def handle_keys(self):
        """
        Adjust the cursor's velocity based on key presses.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity[0] -= self.acceleration  # Accelerate left
        if keys[pygame.K_RIGHT]:
            self.velocity[0] += self.acceleration  # Accelerate right

        if keys[pygame.K_UP]:
            self.velocity[1] -= self.acceleration  # Accelerate up
        if keys[pygame.K_DOWN]:
            self.velocity[1] += self.acceleration  # Accelerate down
    
    def checkIfCursorHitWall(self,gameEngine):
        gameEngine.debugger.dispMsg(5,'Entered  cursor hit wall check',frequency = 100)
        for wall in gameEngine.maze.wallList:
            gameEngine.debugger.dispMsg(5,'Specific wall did not hit cursor',frequency = 100)
            gameEngine.debugger.disp(5,'cursor rect',self.rect,'wall rect',wall.rect,frequency = 100)
            if pygame.Rect.colliderect(self.rect,wall.rect):
                    gameEngine.debugger.dispMsg(5,'Collision Detected')
                    self.is_frozen = True
                    self.last_hit_time = pygame.time.get_ticks()
                    self.color = self.frozenCursorColour
                    gameEngine.gameStatistics.score -= 50
                    break
            
    def reset(self,gameEngine):
        self.is_frozen = False
        self.resetLatch = pygame.time.get_ticks() + 1000 # time to move away from wall
        self.color = self.healthyCursorColour




class Target:
    def __init__(self, width, height, color,gameEngine):
        """
        Initialize a target with width, height, and color.

        Args:
            width (int): The width of the target.
            height (int): The height of the target.
            color (tuple): The color of the target in RGB.
        """
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(0, 0, width, height)  # initialise it
        self.place_randomly(gameEngine)

    def draw(self, gameEngine):
        """
        Draw the target onto the screen.

        Args:
            screen (pygame.Surface): The surface to draw the target on.
        """
        pygame.draw.rect(gameEngine.screen, self.color, self.rect)

    def place_randomly(self,gameEngine):
        """
        Place the target at a random location on the screen, avoiding walls.

        Args:
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
            walls (list): A list of pygame.Rect objects representing the walls.
        """
        placed = False
        while not placed:
            # Generate a random location
            x = random.randint(0, gameEngine.screen_width - self.width)
            y = random.randint(0, gameEngine.screen_height - self.height)
            self.rect.topleft = (x, y)

            # Check if the target is in a wall
            if not any(wall.rect.colliderect(self.rect) for wall in gameEngine.maze.wallList):
                placed = True


class GameEngine():
    """
    Holds all information regarding game mechanics and objects
    """

    def __init__(self):
        self.gameStatistics = GameStats()
        self.lastTargetPlacedTime = 0
        self.targets = []

    def checkPlaceTarget(self):
        if pygame.time.get_ticks() -  self.lastTargetPlacedTime > self.targetPlaceFrequency:
            # place target every self.targetPlaceFrequency seconds
            self.targets.append(Target(self.targetWidth,self.targetHeight,self.colours['RED'],self))
            self.lastTargetPlacedTime = pygame.time.get_ticks()
    
    def drawTargets(self):
        for target in self.targets:
            target.draw(self)
    
    def checkIfCursorHitTarget(self):
        for idx,target in enumerate(self.targets):
            if target.rect.colliderect(self.cursor.rect):
                #self.targets[idx].color = self.colours['GREEN']
                self.gameStatistics.score += 25
                del self.targets[idx]
                break


    def checkIfCursorHitWall(self):
        self.debugger.dispMsg(3,'Entered game engine cursor hit wall check',frequency = 100)
        if self.cursor.is_frozen == False and pygame.time.get_ticks() > self.cursor.resetLatch:
            self.cursor.checkIfCursorHitWall(self)

        if self.cursor.is_frozen and self.cursor.last_hit_time + self.cursor.cooldown < pygame.time.get_ticks():
            # reset with a cooldown of 1 s
            self.cursor.reset(self)

    def createMaze(self):
        self.maze = Maze(self.mazeDims,self)
    def drawMaze(self):
        for wall in self.maze.wallList:
            wall.update()
            wall.draw(self)
    def checkRunningStatus(self):
        if self.testMode == True:
            if pygame.time.get_ticks() > self.testTime:
                self.quitProgram()
    def gatherKeyPresses(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quitProgram()
                
            
            # or get movement from key presses
            if event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.KEYUP:
                if event.key == ord('q'):
                    self.quitProgram()
    
    def quitProgram(self):
        self.running = False





class Debugger():
    """
    Used to debug program
    Debug Levels 0 should not not execute every timestamp
    Debug Levels 1 should have a frequency level set at least at 100 hz
    Debug Levels:
    0 - Only Crucial outputs that are deemed necessary to run the game
    1 - Outputs to understand how the high level dynamics of the game work
    2 - Outputs to understand how lower level dynamics of the game work
    3 > - Outputs mainly used to debug individual lines of code
    """

    def __init__(self,debugLevel):
        self.debugLevel= debugLevel
        self.test = False
        self.dispMsg(0,' --- Debugger is starting up at level {} ---'.format(self.debugLevel))

    def dispMsg(self,debugLevel,msg,frequency = None):
        if self.debugLevel >= debugLevel:
            if frequency == None or pygame.time.get_ticks() % frequency == 0:
                print('Time:', pygame.time.get_ticks())
                print(msg)

    def disp(self,debugLevel,*var,frequency = None):
        length = len(var)
        if self.debugLevel >= debugLevel:
            if frequency == None or pygame.time.get_ticks() % frequency == 0:
                print('Time:', pygame.time.get_ticks())
                for i in range(length//2):
                    print(var[2*i] , ": ",var[2*i+1])

    def returnDebuggingOutput(self,dataStore,targetBoxLocs, targetBoxHitTimes ,targetBoxAppearTimes,allBodyPartsData,boxSizeVarName,metadata,pointerLocs,gameEngine):
        if self.test:
            return {'Hand Motion':dataStore, 'Target Box Locations': targetBoxLocs,'Target Box Hit times': targetBoxHitTimes ,
                    'Target Box Appear Times' : targetBoxAppearTimes, 'Rigid Body Vectors Datastore': allBodyPartsData,
                    'Box Size': boxSizeVarName, 'Metadata': metadata,' Pointer Location' : pointerLocs, 'GameEngine Metadata': gameEngine}

