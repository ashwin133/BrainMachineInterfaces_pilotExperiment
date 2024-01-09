"""
create classes for game
"""
import pygame
import numpy as np
import queue
import math
from multiprocessing import shared_memory
import time
from config_streaming import rigidBodyParts

class GameStats():
    """
    Holds all game performance related information
    """
    def __init__(self):
        pass

class Config():
    """
    Holds information about configuration of game chosen
    """
    def __init__(self,useSimulatedData, userInputMethod,saveGameData,saveGameDataPath,inputBodyPart,calibrated):
        self.useSimulatedData = useSimulatedData
        self.userInputMethod = userInputMethod
        self.saveGameData = saveGameData
        self.saveGameDataPath = saveGameDataPath
        self.inputBodyPart = inputBodyPart
        self.calibrated = calibrated



class BlinkingSkull:
    def __init__(self, x, y,width,height, gameEngine):
        self.image = gameEngine.piranhaImage
        self.image = pygame.transform.scale(self.image, (width,height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = True
        self.blink = False
        self.period = 500
        self.reverseBlinkTime = 0 

    def update(self):
        if self.blink:
            if self.reverseBlinkTime < pygame.time.get_ticks():
                self.visible = not self.visible  # Toggle visibility
                self.reverseBlinkTime = pygame.time.get_ticks() + self.period
        else:
            self.visible = False

    def draw(self, gameEngine):
        if self.visible:
            gameEngine.screen.blit(self.image, self.rect)


class DangerBar:
    def __init__(self, x, y, width, height, color, max_time,gameEngine):
        """
        Initialize a danger bar.

        Args:
            x, y (int): The coordinates of the top-left corner of the bar.
            width, height (int): The dimensions of the bar.
            color (tuple): The color of the bar in RGB.
            max_time (float): The time it takes for the bar to completely fill.
        """
        self.outer_rect = pygame.Rect(x, y, width, height)  # The static outer rectangle
        self.inner_rect = pygame.Rect(x, y, 0, height)  # The growing inner rectangle
        self.color = color
        self.max_time = max_time
        self.start_time = pygame.time.get_ticks()   # Start time
        self.progress = 0


    def update(self):
        """
        Update the inner rectangle's width based on the elapsed time.
        """
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Time in seconds
        self.progress = min(elapsed_time / self.max_time, 1)  # Progress ratio (0 to 1)
        self.inner_rect.width = int(self.outer_rect.width * self.progress)  # Update width
        
            

    def draw(self, gameEngine):
        """
        Draw the danger bar onto the screen.

        Args:
            screen (pygame.Surface): The surface to draw the danger bar on.
        """
        pygame.draw.rect(gameEngine.screen, (200, 200, 200), self.outer_rect)  # Draw outer rect (border)
        pygame.draw.rect(gameEngine.screen, self.color, self.inner_rect)  # Draw inner rect (progress)



class Minion:
    def __init__(self, x, y, width, height, speed,color = (255,255,0),piranhaImage = None, useImg = True,stopTime = 20000):
        """
        Initialize a minion.

        Args:
            x (int): The x-coordinate of the minion's starting position.
            y (int): The y-coordinate of the minion's starting position.
            width (int): The width of the minion.
            height (int): The height of the minion.
            color (tuple): The color of the minion in RGB.
            speed (float): The speed at which the minion moves.
        """
        self.useImg = True
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed
        self.image = pygame.transform.scale(piranhaImage, (width, height))
        self.currentImage = self.image
        self.stopTime = pygame.time.get_ticks() + stopTime
        
    def update(self, gameEngine):
        """
        Update the minion's position to move towards the target.

        Args:
            target_rect (pygame.Rect): The rect of the target to move towards.
        """
        # Calculate the direction vector to the target
        dir_x = gameEngine.cursor.rect.x - self.rect.x
        dir_y = gameEngine.cursor.rect.y - self.rect.y

        # Normalize the direction
        distance = math.hypot(dir_x, dir_y)
        if distance == 0:  # Prevent division by zero
            dir_x, dir_y = 0, 0
        else:
            dir_x, dir_y = dir_x / distance, dir_y / distance

        # Move towards the target
        self.rect.x += dir_x * self.speed
        self.rect.y += dir_y * self.speed

        angle = np.rad2deg(math.atan2(dir_y,dir_x))
        #print(angle)
        flip_horizontally = False
        flip_vertically = True
        if -angle > 90 or -angle < -90:
            flipped_image = pygame.transform.flip(self.image, flip_horizontally, flip_vertically)
        else:
            flipped_image = self.image

        self.currentImage =  pygame.transform.rotate(flipped_image, -angle)

    def draw(self, gameEngine):
        """
        Draw the minion on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the minion on.
        """
        if self.useImg:
            gameEngine.screen.blit(self.currentImage, self.rect)

        else:
            pygame.draw.rect(gameEngine.screen, self.color, self.rect)
        
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
    def __init__(self, gameEngine, top_left, bottom_right, id, color=None,visibility = True):
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
        self.visibility = visibility
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
        self.surface = pygame.Surface((self.rect.width, self.rect.height))  
        self.surface.fill(self.color) 

        brick_color = (153, 31, 35)  # Dark red/brown for bricks
        mortar_color = (115, 23, 25)  # Darker color for mortar lines

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(brick_color)

        brick_height = 12
        brick_width = 40

        # Draw horizontal mortar lines
        for y in range(0, self.height, brick_height):
            pygame.draw.line(self.surface, mortar_color, (0, y), (self.width, y))

        # Draw vertical mortar lines
        for y in range(0, self.height, brick_height):
            for x in range(0, self.width, brick_width):
                if y % (2 * brick_height) == 0:  # Offset every other row
                    offset_x = brick_width // 2
                else:
                    offset_x = 0
                pygame.draw.line(self.surface, mortar_color, (x + offset_x, y), (x + offset_x, y + brick_height))



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
        if self.visibility:
            #pygame.draw.rect(gameEngine.screen, self.color, self.rect)
            gameEngine.screen.blit(self.surface, self.rect)




class Cursor:
    def __init__(self, x, y, width, height, color,imagePaths,frozenColour = (255,0,0),useImg = True,delaySamples = 0,unstableMode = False,controlMethod = 'Mouse',gameEngine = None):
        """
        Initialize a velocity-controlled cursor with inertia.

        Args:
            x (int): The x-coordinate of the cursor's starting position.
            y (int): The y-coordinate of the cursor's starting position.
            width (int): The width of the cursor.
            height (int): The height of the cursor.
            color (tuple): The color of the cursor in RGB.

        """
        self.controlMethod = controlMethod
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
        self.cooldown = 1000 # cooldown time when frozen from hitting wall in ms 
        self.last_hit_time = None # store time of hit
        self.resetLatch = 0
        # Scale the image
        if self.useImg:
            self.images = {direction: pygame.image.load(path) for direction, path in imagePaths.items()}
            for key in self.images.keys():
                self.images[key] = pygame.transform.scale(self.images[key], (width, height))
            #self.rect = self.image.get_rect(topleft=(x, y))
        self.currentImage = self.images['right']
        self.delayLength = delaySamples
        self.unstableMode = unstableMode
        if self.unstableMode:
            if delaySamples != 0:
                self.velocity_queue = queue.Queue(maxsize=delaySamples)
                for _ in range(delaySamples):
                    self.velocity_queue.put([0,0])
                #print(self.velocity_queue)

        self.xRange = gameEngine.xRange
        self.yRange = gameEngine.yRange
        self.debugger = gameEngine.debugger
        self.usePCA = gameEngine.performCalibrationUsingPrincipleComponent
        if self.usePCA:
            self.leftRightPCA = gameEngine.pcaleftRight
            self.upDownPCA = gameEngine.pcaUpDown
            self.xInvert = gameEngine.xInvert
            self.yInvert = gameEngine.yInvert
                

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
            if self.rect.top < 50:
                self.rect.top = 50
                self.velocity[1] = 0
            if self.rect.bottom > pygame.display.get_surface().get_height():
                self.rect.bottom = pygame.display.get_surface().get_height()
                self.velocity[1] = 0
        self.selectImageBasedOnDirection()
            
    def selectImageBasedOnDirection(self):
        # change image based on velocity
        initialImage =  self.images['right']
        angle = np.rad2deg(math.atan2(self.velocity[1],self.velocity[0]))
        #print(angle)
        flip_horizontally = False
        flip_vertically = True
        if -angle > 90 or -angle < -90:
            flipped_image = pygame.transform.flip(initialImage, flip_horizontally, flip_vertically)
        else:
            flipped_image = initialImage
        if angle != 0:
            self.currentImage =  pygame.transform.rotate(flipped_image, -angle)
        if False:
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
            
            #print(velAngle)

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
        if self.controlMethod == 'Keypad':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.velocity[0] -= self.acceleration  # Accelerate left
            if keys[pygame.K_RIGHT]:
                self.velocity[0] += self.acceleration  # Accelerate right

            if keys[pygame.K_UP]:
                self.velocity[1] -= self.acceleration  # Accelerate up
            if keys[pygame.K_DOWN]:
                self.velocity[1] += self.acceleration  # Accelerate down

        elif self.controlMethod == 'Mouse':
            # Get current mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            # Calculate distance from the cursor to the mouse position
            distanceX = mouseX - self.rect.centerx
            distanceY = mouseY - self.rect.centery

            if self.unstableMode:
                if self.delayLength > 0:
                    distanceX_, distanceY_ = self.velocity_queue.get()
                    self.velocity_queue.put([distanceX, distanceY])

                    # Update the cursor's position to the oldest value in the queue
                        
                # Adjust the velocity based on the distance to the mouse position accounting for a scale factor
                self.velocity[0] += distanceX_ * 0.02
                self.velocity[1] += distanceY_ * 0.02
                # positiveFeedbackFactor = 0.0  # Adjust as needed
                # self.velocity[0] += self.velocity[0] * positiveFeedbackFactor
                # self.velocity[1] += self.velocity[1] * positiveFeedbackFactor
            else:
                self.velocity[0] += distanceX * 0.02
                self.velocity[1] += distanceY * 0.02

        elif self.controlMethod == "bodyTracking":
                bodyController = "VelocityBased"

                if bodyController == "PositionBased":

                    if self.usePCA:
                        
                        normalised_x_val = 1 -  (self.leftRightPCA.transform(self.controlPos.reshape(1,-1)) - self.userMinXValue) / self.xRange
                        normalised_y_Val =  (self.upDownPCA.transform(self.controlPos.reshape(1,-1)) - self.userMinYValue) / self.yRange
                    else:
                        normalised_x_val = 1 -  (self.controlPos[1] - self.userMinXValue) / self.xRange
                        normalised_y_Val = 1 - (self.controlPos[2] - self.userMinYValue) / self.yRange
                    #print(normalised_x_val)
                    #print(normalised_y_Val)
                    self.rect.x = normalised_x_val * pygame.display.get_surface().get_width()
                    self.rect.y = normalised_y_Val * pygame.display.get_surface().get_height()
                
                elif bodyController == "VelocityBased":
                    if self.usePCA:
                        if self.xInvert:
                            normalised_x_val = 1 -  (  self.leftRightPCA.transform(self.controlPos.reshape(1,-1)) - self.userMinXValue) / self.xRange
                        else:
                            normalised_x_val =   (self.leftRightPCA.transform(self.controlPos.reshape(1,-1)) - self.userMinXValue) / self.xRange
                        if self.yInvert:
                            normalised_y_Val = ( self.upDownPCA.transform(self.controlPos.reshape(1,-1)) - self.userMinYValue) / self.yRange
                        else:  
                            normalised_y_Val = 1 - (self.upDownPCA.transform(self.controlPos.reshape(1,-1)) - self.userMinYValue) / self.yRange
                    else:
                        normalised_x_val = 1 -  (self.controlPos[1] - self.userMinXValue) / self.xRange
                        normalised_y_Val = 1 - (self.controlPos[2] - self.userMinYValue) / self.yRange
                    
                    x_target = normalised_x_val * pygame.display.get_surface().get_width() 
                    y_target = normalised_y_Val * pygame.display.get_surface().get_height()
                    self.debugger.disp(2,x_target,y_target)
                    distanceX = x_target - self.rect.centerx
                    distanceY = y_target - self.rect.centery
                    self.velocity[0] = distanceX * 0.06
                    self.velocity[1] = distanceY * 0.06

                

    
    def checkIfCursorHitWall(self,gameEngine):
        gameEngine.debugger.dispMsg(5,'Entered  cursor hit wall check',frequency = 100)
        for wall in gameEngine.maze.wallList:
            gameEngine.debugger.dispMsg(5,'Specific wall did not hit cursor',frequency = 100)
            gameEngine.debugger.disp(5,'cursor rect',self.rect,'wall rect',wall.rect,frequency = 100)

            if self.useImg:
                cursor_mask = pygame.mask.from_surface(self.currentImage)
                target_mask = pygame.mask.from_surface(wall.surface) # change to target image 

                offset = (wall.rect.x - self.rect.x, wall.rect.y - self.rect.y)
                if cursor_mask.overlap(target_mask, offset):
                    # collision detected
                    gameEngine.debugger.dispMsg(5,'Collision Detected')
                    self.is_frozen = True
                    self.last_hit_time = pygame.time.get_ticks()
                    self.color = self.frozenCursorColour
                    gameEngine.gameStatistics.score -= 50
                    break

            elif pygame.Rect.colliderect(self.rect,wall.rect):
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
    def __init__(self, width, height, color,gameEngine,useImg = False, image = None):
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
        self.useImg = useImg
        if self.useImg:
            self.currentImage = pygame.transform.scale(image,(width,height))

        #self.rect = self.image.get_rect(topleft=(x, y))



    def draw(self, gameEngine):
        """
        Draw the target onto the screen.

        Args:
            screen (pygame.Surface): The surface to draw the target on.
        """
        if self.useImg:
            gameEngine.screen.blit(self.currentImage, self.rect)
        else:
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

class Dangerzone():

    def __init__(self,x,y,width,height,gameEngine):
        self.rect = pygame.Rect(x, y, width, height)
        self.activeImage = gameEngine.skullImage
        self.activeImage = pygame.transform.scale(self.activeImage, (width, height))
        self.active = False
    
    def draw(self,gameEngine):
        """
        Draw the target onto the screen.

        Args:
            screen (pygame.Surface): The surface to draw the target on.
        """
        if self.active:
            gameEngine.screen.blit(self.activeImage, self.rect)
        else:
            pass
            #pygame.draw.rect(gameEngine.screen, self.color, self.rect)


class EnergyZone():

    def __init__(self,x,y,width,height,gameEngine):
        self.rect = pygame.Rect(x, y, width, height)
        self.activeColor = (0,128,0)
        self.chargingColor = (255,165,0)
        self.disabledColor = (255,0,0)
        self.active = False
        self.color = self.activeColor
        self.charge = 100
        self.minionSpawn = False
        self.width = width
        self.height = height
    
    def update(self,gameEngine):
            if self.minionSpawn == False:
                if self.rect.colliderect(gameEngine.cursor.rect):
                    if self.charge != 0:
                        self.charge -= 1
                        self.color = self.chargingColor
                        return 1
                    elif self.charge == 0:
                        self.color = self.disabledColor
                else:
                    if self.charge == 0:
                        self.color = self.disabledColor
                    else:
                        self.color = self.activeColor
            else:
                if self.minionSpawn:
                    # when minions have spawned we want to charge energy zones
                     # if coliision and energy zone uncharged then charge it
                    if self.rect.colliderect(gameEngine.cursor.rect):
                        if self.charge != 100:
                            self.charge += 1
                            self.color = self.chargingColor
                        elif self.charge == 100:
                            self.color = self.activeColor
                    else:
                        if self.charge == 100:
                            self.color = self.activeColor
                        else:
                            self.color = self.disabledColor



    def draw(self,gameEngine):
        """
        Draw the target onto the screen.

        Args:
            screen (pygame.Surface): The surface to draw the target on.
        """

        pygame.draw.rect(gameEngine.screen, self.color, self.rect)


class GameEngine():
    """
    Holds all information regarding game mechanics and objects
    """

    def __init__(self):
        self.gameStatistics = GameStats()
        self.lastTargetPlacedTime = 0
        self.targets = []
        self.lastMinionPlacedTime = 0
        self.minions = []
        self.placeMinionTime = None
        self.energyZones = []
        

    # functions to handle optitrack inputs
        
    def initSharedMemory(self,sharedMemoryName,noDataTypes,noBodyParts):
        """
        Function initialises parameters of the shared memory for use later. This function should only 
        be called when shared memory is needed.

        @param: sharedMemoryName: Name of the shared memory which should match the shared memory dumping data
        @param: noDataTypes: Number of dimensions for each body part (DOF), typically 6
        @param: noBodyParts: Number of body parts, typically 51
        """
        # shared memory either needs to be simulated or actually used
        if self.config.userInputMethod  == "bodyTracking":
            if self.config.useSimulatedData is not True:
                self.debugger.disp(3,'Shared memory is initialised for live motion capture', '')
                self.sharedMemName = sharedMemoryName
                self.sharedMemShape = (noBodyParts,noDataTypes)
                self.sharedMemSize =  noDataTypes * noBodyParts
            elif self.config.useSimulatedData is True:

                self.debugger.disp(3,'Shared memory is being simulated for motion capture', '')
                # initialise key parameters
                self.sharedMemName = sharedMemoryName
                self.sharedMemShape = (noBodyParts,noDataTypes)
                self.sharedMemSize =  noDataTypes * noBodyParts

                # create the shared memory simulating the action of the data retrieval script 
                shared_block = shared_memory.SharedMemory(size= self.sharedMemSize * 8, name=self.sharedMemName, create=True)
                shared_array = np.ndarray(shape=self.sharedMemShape, dtype=np.float64, buffer=shared_block.buf)
        else:
            # nothing happens as shared memory is not needed as input is not body tracking
            self.debugger.disp(3,'Shared memory not being used as control method is not bodyTracking', '')


    def enterCalibrationStage(self):
        """
        Enter calibration stage for rigid body tracking only
        """

        # TODO: change print statements to debugger.disp 
        self.calibrationTimeEnd = self.timeBeforeCalibration + self.calibrationTime
        # warn user for calibration

        print('Before we start, the calibration stage must be undertaken')
        print('Face upright and standing towards the computer and keep your chosen body point straight and pointed forwards')
        print('Calibration will start in 5')
        time.sleep(1)
        print('4')
        time.sleep(1)
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        print('Calibrating - point your chosen body part forwards and keep it straight')

        self.controlBodyPartIdx = rigidBodyParts.index(self.config.inputBodyPart)
        self.debugger.disp(3,"Control is set using".format(self.controlBodyPartIdx))
        
        # Either calibrate using real time data or simulate it if using recorded data

        if self.config.useSimulatedData is not True:
            # Real time data recording

            # retrieve latest information from shared memory
            shared_block = shared_memory.SharedMemory(size= self.sharedMemSize * 8, name=self.sharedMemName, create=False)
            shared_array = np.ndarray(shape=self.sharedMemShape, dtype=np.float64, buffer=shared_block.buf)
            controlRigidBodyInitialData = np.array(shared_array[self.controlBodyPartIdx,:]) # idx of rigid body controlling

            
            # SAVE DATA IF REQUESTED
            if self.config.saveGameData == True:
                # Write the information of the control rigid body to the relevant datastore
                self.controlRigidBodyDatastore[self.controlRigidBodyDatastoreIteration,:] = controlRigidBodyInitialData[:6]
                self.controlRigidBodyDatastoreIteration += 1

                # Write all rigid body part information to the relavent datastore
                self.allBodyPartsDatastore[self.allBodyPartsDataStoreIteration,:,:] =  np.array(shared_array[:,0:6])
                self.allBodyPartsDataStoreIteration += 1


        elif self.config.useSimulatedData: # USING SIMULATED DATA

            # read data from datastore and increment index
            controlRigidBodyInitialData = self.controlBodyPartreadDataStore[self.controlBodyPartreadDataStoreIteration] 
            self.controlBodyPartreadDataStoreIteration += 1

            # TODO: add workflow to save read data if needed at a later stage

        
        # Now calibrate using rigid body control data
    
        calibrationFromVector = controlRigidBodyInitialData[3:6]
        calibrationToVector = np.array([1,0,0]) # TODO: needs to be changed for other rigid body parts?
        self.calcCalibrationConstants(calibrationToVector,calibrationFromVector)
        self.calibratedXValue, self.calibratedYValue =  np.matmul(self.calibrationMatrix,np.array(controlRigidBodyInitialData[0:3]))[1:3]

        print('Correct plane has been calibrated')
        print('The program will now calibrate the x and y range')
        print('Please move your right arm wherever possible')
        print('The program will form this new range based on your motion in the next 7 seconds')

        # initialise the control range to no range and update later based on the users range of movements
        self.userMaxXValue = -10000
        self.userMinXValue = 10000
        self.userMaxYValue = -10000
        self.userMinYValue = 10000

    def performCalibrationStage(self):
        self.performCalibrationUsingPrincipleComponent = True

        if self.performCalibrationUsingPrincipleComponent is not True:
            # DEFAULT
            while pygame.time.get_ticks() < self.calibrationTimeEnd:
                self.fetchSharedMemoryData()
                # TODO: may need to adjust these for different rigid bodies
                # as game x is typically the body y plane (right) and game y is the body z plane (up) 
                self.userMaxXValue = max(self.controlPos[1],self.userMaxXValue)
                self.userMaxYValue = max(self.controlPos[2],self.userMaxYValue)
                self.userMinXValue = min(self.controlPos[1],self.userMinXValue)
                self.userMinYValue = min(self.controlPos[2],self.userMinYValue)
                print('executed')
                time.sleep(1/120)
        elif self.performCalibrationUsingPrincipleComponent is True:
            self.calibrateControlUsingPCA()
            
 
        # End calibration stage
        self.debugger.disp(2,'Calibration stage is now over')
        # TODO: add code to make calibration even with respect to far distance to middle?

        # set range of control input based on user's movement range
        self.xRange = self.userMaxXValue - self.userMinXValue

        
        self.yRange = self.userMaxYValue - self.userMinYValue

        self.config.calibrated = True
     
    
    def calibrateControlUsingPCA(self):
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
        # first calibrate right and left
        self.calibrationPos_rl = []
        self.calibrationDir_rl = []

        # Warn user
        print('First we will calibrate the right-left plane')
        print('Move your controller right and left only for three seconds')
        print('The principle component in this direction will be used as the control mapping')
        print('Calibration will start in 2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        print('Calibrating the left right axis')
        currTime = pygame.time.get_ticks()

        # collect data for left and right for 3.5 s
        while pygame.time.get_ticks() <currTime + 3500:
            self.fetchSharedMemoryData()
            # TODO: may need to adjust these for different rigid bodies
            # as game x is typically the body y plane (right) and game y is the body z plane (up) 
            self.userMaxXValue = max(self.controlPos[1],self.userMaxXValue)
            self.userMinXValue = min(self.controlPos[1],self.userMinXValue)
            self.calibrationPos_rl.append(self.controlPos)
            self.calibrationDir_rl.append(self.controlDir)
            print(self.userMinXValue,self.userMaxXValue)
            time.sleep(1/120)
        
        # apply pca
        
        self.calibrationPos_rl = np.asarray(self.calibrationPos_rl)
        #X_std = StandardScaler().fit_transform(self.calibrationPos_rl)
        pca = PCA(n_components=1)
        x_pca = pca.fit_transform(self.calibrationPos_rl)
        self.userMinXValue = min(x_pca)
        self.userMaxXValue = max(x_pca)
        print(pca.explained_variance_ratio_)
        self.xRange = self.userMaxXValue - self.userMinXValue
        self.pcaleftRight = pca

        print("To assess the direction, please place your controller to the left")
        print('Calibration will start in 2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        print('Calibrating...')
        self.fetchSharedMemoryData()
        normalised_x_Val_min =  (self.pcaleftRight.transform(self.controlPos.reshape(1,-1)) - self.userMinXValue) / self.xRange
        print('Now move your controller right')
        print('Calibration will start in 2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        print('Calibrating...')
        self.fetchSharedMemoryData()
        normalised_x_Val_max =  (self.pcaleftRight.transform(self.controlPos.reshape(1,-1)) - self.userMinXValue) / self.xRange
        if normalised_x_Val_min > normalised_x_Val_max:
            self.xInvert = True
        else:
            self.xInvert = False

        # --- NEXT CALIBRATE UP AND DOWN ---
        self.calibrationPos_rl = []
        self.calibrationDir_rl = []

        # Warn user
        print('First we will calibrate the up-down plane')
        print('Move your controller up and down only for three seconds')
        print('The principle component in this direction will be used as the control mapping')
        print('Calibration will start in 2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        print('Calibrating the up down axis')
        currTime = pygame.time.get_ticks()
        self.calibrationPos_rl = []
        self.calibrationDir_rl = []

        # collect data for up and down for 3.5 s
        while pygame.time.get_ticks() <currTime + 3500:
            self.fetchSharedMemoryData()
            # TODO: may need to adjust these for different rigid bodies
            # as game x is typically the body y plane (right) and game y is the body z plane (up) 
            
            self.calibrationPos_rl.append(self.controlPos)
            self.calibrationDir_rl.append(self.controlDir)
            print(self.userMinXValue,self.userMaxXValue)
            time.sleep(1/120)
        
        # apply pca
        
        self.calibrationPos_rl = np.asarray(self.calibrationPos_rl)
        #X_std = StandardScaler().fit_transform(self.calibrationPos_rl)
        pca = PCA(n_components=1)
        y_pca = pca.fit_transform(self.calibrationPos_rl)
        self.userMinYValue = min(y_pca)
        self.userMaxYValue = max(y_pca)
        self.yRange = self.userMaxYValue - self.userMinYValue
        self.pcaUpDown = pca

        
        print("To assess the direction, please place your hand down")
        print('Calibration will start in 2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        print('Calibrating...')
        self.fetchSharedMemoryData()
        normalised_y_Val_min =  (self.pcaUpDown.transform(self.controlPos.reshape(1,-1)) - self.userMinYValue) / self.yRange
        print('Now move your hand up')
        print('Calibration will start in 2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        print('Calibrating...')
        self.fetchSharedMemoryData()
        normalised_y_Val_max =  (self.pcaUpDown.transform(self.controlPos.reshape(1,-1)) - self.userMinYValue) / self.yRange
        if normalised_y_Val_min > normalised_y_Val_max:
            self.yInvert = True
        else:
            self.yInvert = False


        print("PCA based calibration has finished" )


    def calcCalibrationConstants(self,calibrationToVector, calibrationFromVector):
        """
        attempts to calibrate for person standing off x axis by finding the transformation
        matrix to transform off axis motion to the standard axes
        returns a transformation matrix that can convert directions and positions 
        """
        # calculate thetha from dot product
        thetha_rad = np.arccos(np.dot(calibrationToVector,calibrationFromVector)/(np.linalg.norm(calibrationToVector) * np.linalg.norm(calibrationFromVector)))

        # calculate Q
        Q = np.zeros((3,3))
        Q[0,0] = np.cos(thetha_rad)
        Q[1,1] = Q[0,0]
        Q[0,1] = np.sin(thetha_rad)
        Q[1,0] = - Q[0,1]
        Q[2,2] = 1

        self.calibrationMatrix = Q.transpose()

    def fetchSharedMemoryData(self):

        """
        Fetches latest data either in real time from shared memory or from simulated datastores
        """

        # Data does not need to be saved

        if self.config.useSimulatedData is not True: 
            shared_block = shared_memory.SharedMemory(size= self.sharedMemSize * 8, name=self.sharedMemName, create=False)
            shared_array = np.ndarray(shape=self.sharedMemShape, dtype=np.float64, buffer=shared_block.buf)
            controlBodyData = np.array(shared_array[self.controlBodyPartIdx])

            # Record data if requested
            if self.config.saveGameData is True: 
                # Record control body
                self.controlBodyPartDataStore[self.controlBodyPartDataStoreIteration,:] = controlBodyData[:6]
                self.controlBodyPartDataStoreIteration += 1

                # Record all rigid bodies
                self.allBodyPartsDatastore[self.allBodyPartsDataStoreIteration,:,:] =  np.array(shared_array[:,0:6])
                self.allBodyPartsDataStoreIteration += 1

        # Read control rigid body data from datastore if using simulated data
        elif self.config.useSimulatedData is True:
            controlBodyData = self.controlBodyPartreadDataStore[self.controlBodyPartreadDataStoreIteration] 
            self.controlBodyPartreadDataStoreIteration += 1
            
        
        # Process the data 

        # both workflows have this adjustment
        self.controlPos = np.matmul(self.calibrationMatrix,controlBodyData[0:3])
        self.controlDir = np.matmul(self.calibrationMatrix,controlBodyData[3:6])
        
        # pass this to the cursor after calibration stage
        if self.config.calibrated is True:
            self.cursor.controlPos = self.controlPos
            self.cursor.controlDir = self.controlDir
            self.cursor.userMinYValue = self.userMinYValue
            self.cursor.userMaxYValue = self.userMaxYValue
            self.cursor.userMinXValue = self.userMinXValue
            self.cursor.userMaxXValue = self.userMaxXValue

            
            
        



    def spawnEnergyZones(self):
        # spawn an energy zone in 
        # Bottom Right Energy Zone
        self.energyZones.append(EnergyZone(1245-100,715-100,100,100,self))
        
        
        # Top Right Energy Zone
        self.energyZones.append(EnergyZone(1245-100,75,100,100,self))

        # Top Left Enery Zone
        self.energyZones.append(EnergyZone(25,75,100,100,self))

    def updateEnergyZones(self):
        for energyZone in self.energyZones:
            energy = energyZone.update(self)
            if energy == 1:
                print('flag')
                #self.dangerBar.progress -= 0.02
                self.dangerBar.start_time += 67
                if self.dangerBar.progress < 0:
                    self.dangerBar.progress == 0
    
    def drawEnergyZones(self):
        for energyZone in self.energyZones:
            energyZone.draw(self)

    def spawnDangerBar(self,time):
        # Create a danger bar at the top of the screen
        self.dangerBar = DangerBar(50, 10, 700, 20, (255, 0, 0), time,self)  # 30 seconds to fill
    
    def updateDangerBar(self):
        self.dangerBar.update()
        if self.dangerBar.progress > 0.99 and self.placeMinionTime is None:
            self.placeMinionTime = pygame.time.get_ticks() + 3000
            self.dangerzone.active = True
            self.piranhaOnSign.activate()
            self.activateEnergyZones()
        
        if self.dangerzone.active == True:
            # Check if all energy zones are charged if danger zone is active

            fullyCharged = True
            for energyZone in self.energyZones:
                if energyZone.charge != 100:
                    fullyCharged = False

            if fullyCharged:  # minion off
                self.placeMinionTime = None
                self.dangerzone.active = False

                self.dangerBar.start_time = pygame.time.get_ticks()
                for energyZone in self.energyZones:
                    energyZone.charge = 100
                    energyZone.minionSpawn = False
                
                self.piranhaOffSign.activate()
                # add code


    def activateEnergyZones(self):
        """
        triggers when minions start to spawn
        """
        for energyZone in self.energyZones:
            energyZone.minionSpawn = True
            energyZone.charge = 0

    def draw_sea(self):
        colors = [(30, 135, 168), (15, 120, 158),(0, 105, 148) ]
        section_height = self.screen_height // len(colors)
        for i, color in enumerate(colors):
            pygame.draw.rect(self.screen, color, (0, i * section_height, self.screen_width, section_height + 1))
    def draw_waves(self):
        time = pygame.time.get_ticks()
        wave_color = (255, 255, 255, 100)
        for i in range(0, self.screen_width, 20):
            wave_y = self.screen_height * 0.8 + 10 * np.sin(i * 0.05 + time * 0.002)  # Sinusoidal wave pattern
            pygame.draw.arc(self.screen, wave_color, (i, wave_y, 80, 50), np.pi, 2 * np.pi, 3)

    def drawDangerBar(self):
        self.dangerBar.draw(self)
    
    def spawnDangerZone(self,x,y,width,height):
        self.dangerzone = Dangerzone(x,y,width,height,self)
    
    def drawDangerZone(self):
        self.dangerzone.draw(self)

    def checkSpawnMinion(self,placeFromZone = True):
        # when self.placeMinionTime is not None
        if placeFromZone:
            if self.placeMinionTime is not None and  pygame.time.get_ticks()  > self.placeMinionTime:
                # place target every self.targetPlaceFrequency seconds
                self.minions.append(Minion(25,665,self.minionWidth,self.minionHeight,self.minionSpeed,piranhaImage=self.piranhaImage))
                self.lastMinionPlacedTime = pygame.time.get_ticks()
                self.placeMinionTime = pygame.time.get_ticks() + self.minionPlaceFrequency
        else:
            if pygame.time.get_ticks() -  self.lastMinionPlacedTime > self.minionPlaceFrequency:
                # place target every self.targetPlaceFrequency seconds
                self.minions.append(Minion(300,300,self.minionWidth,self.minionHeight,self.minionSpeed,piranhaImage=self.piranhaImage))
                self.lastMinionPlacedTime = pygame.time.get_ticks()

    def updateAndDrawBlinkingSkull(self):
        self.blinkingSkull.blink = self.dangerzone.active
        self.blinkingSkull.update()
        self.blinkingSkull.draw(self)

    def updateAndDrawMinion(self):
        for idx,minion in enumerate(self.minions):
            minion.update(self)
            minion.draw(self)
            if pygame.time.get_ticks() > minion.stopTime:
                del self.minions[idx]


    def checkIfMinionHitCursor(self):
        for idx in range(len(self.minions)-1,-1,-1):

            if self.cursor.useImg:
                cursor_mask = pygame.mask.from_surface(self.cursor.currentImage)
                minion_mask = pygame.mask.from_surface(self.minions[idx].currentImage)

                offset = (self.minions[idx].rect.x - self.cursor.rect.x, self.minions[idx].rect.y - self.cursor.rect.y)
                if cursor_mask.overlap(minion_mask, offset):
                    # collision detected
                    self.gameStatistics.score -= 50
                    del self.minions[idx]

            elif self.minions[idx].rect.colliderect(self.cursor.rect):
                #self.targets[idx].color = self.colours['GREEN']
                self.gameStatistics.score -= 50
                del self.minions[idx]


    def checkPlaceTarget(self):
        if pygame.time.get_ticks() -  self.lastTargetPlacedTime > self.targetPlaceFrequency and len(self.targets) < self.maxTargets:
            # place target every self.targetPlaceFrequency seconds
            self.targets.append(Target(self.targetWidth,self.targetHeight,self.colours['RED'],self,useImg=True,image=self.targetImage))
            self.lastTargetPlacedTime = pygame.time.get_ticks()
    
    def drawTargets(self):
        for target in self.targets:
            target.draw(self)
    
    def checkIfCursorHitTarget(self):
        for idx,target in enumerate(self.targets):
            if self.cursor.useImg:
                cursor_mask = pygame.mask.from_surface(self.cursor.currentImage)
                target_mask = pygame.mask.from_surface(target.currentImage) # change to target image 

                offset = (target.rect.x - self.cursor.rect.x, target.rect.y - self.cursor.rect.y)
                if cursor_mask.overlap(target_mask, offset):
                    # collision detected
                    self.gameStatistics.score += 25
                    del self.targets[idx]
            elif target.rect.colliderect(self.cursor.rect):
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
        self.maze.wallList.append(Wall(self,(0,0),(1270,50),id = -1,visibility = False))
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





class PiranhaNestDestroyedSign:
    def __init__(self, gameEngine, font, message="Piranha Nest Destroyed"):
        self.screen = gameEngine.screen
        self.font = font
        self.message = message
        self.visible = False
        self.display_time = 2000  # 2000 milliseconds or 2 seconds
        self.start_time = None

    def activate(self):
        self.visible = True
        self.start_time = pygame.time.get_ticks()

    def update_and_draw(self):
        if self.visible:
            # Check if 2 seconds have passed
            if pygame.time.get_ticks() - self.start_time > self.display_time:
                self.visible = False

            if self.visible:
                text_surface = self.font.render(self.message, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
                self.screen.blit(text_surface, text_rect)


class PiranhaNestSpawnedSign:
    def __init__(self, gameEngine, font, message="Piranha Nest Spawned"):
        self.screen = gameEngine.screen
        self.font = font
        self.message = message
        self.visible = False
        self.display_time = 2000  # 2000 milliseconds or 2 seconds
        self.start_time = None

    def activate(self):
        self.visible = True
        self.start_time = pygame.time.get_ticks()

    def update_and_draw(self):
        if self.visible:
            # Check if 2 seconds have passed
            if pygame.time.get_ticks() - self.start_time > self.display_time:
                self.visible = False

            if self.visible:
                text_surface = self.font.render(self.message, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
                self.screen.blit(text_surface, text_rect)