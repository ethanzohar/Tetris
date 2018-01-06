#-----------------------------------------#
# Tetris Template 3 (Final)               #
# By: Ethan Zohar                         #
# May 26, 2017                            #
# Holds the main code for the tetris game #
#-----------------------------------------#

#-----------------------------------#
from tetris_classes3 import *       #
from random import randint          #
import time                         # Imports all the modules needed
import pygame                       #
pygame.init()                       #
#-----------------------------------#

#-----------------------------------------------#
HEIGHT = 600                                    #
WIDTH  = 800                                    #
GRIDSIZE = HEIGHT//24                           #
screen=pygame.display.set_mode((WIDTH,HEIGHT))  # Sets up the display and colours
GREY = (50,50,50)                               #
CYAN      = (  0,183,235)                       #
BLACK = (0,0,0)                                 #
#-----------------------------------------------#

font = pygame.font.SysFont("Ariel Black",50)        #initializes the
fontBig = pygame.font.SysFont("Ariel Black",100)    #fonts

#-------------------------------------------------------------------#
img = []                                                            #
for i in range(7):                                                  #
    img.append(pygame.image.load('IMG_' + str(i) + '.JPG'))         # Initializes all the images for the tetris peices
    img[i] = img[i].convert_alpha()                                 #
    img[i] = pygame.transform.scale(img[i], (GRIDSIZE, GRIDSIZE))   #
#-------------------------------------------------------------------#

#-------------------------------------------------------------------#
background = pygame.image.load('stock2.jpg')                        #
background.convert_alpha()                                          #
background = pygame.transform.scale(background, (WIDTH, HEIGHT))    #
                                                                    #
start = pygame.image.load('start.jpg')                              #
start.convert_alpha()                                               # Initializes and resizes all the images
start = pygame.transform.scale(start, (WIDTH, HEIGHT))              #
                                                                    #
end = pygame.image.load('end.jpg')                                  #
end.convert_alpha()                                                 #
end = pygame.transform.scale(end, (WIDTH, HEIGHT))                  #
                                                                    #
pauseImg = pygame.image.load('pause.png')                           #
pauseImg.convert_alpha()                                            #
pauseImg = pygame.transform.scale(pauseImg, (400,400))              #      
#-------------------------------------------------------------------#

#---------------------------------------#
pygame.mixer.music.load('song.wav')     #
pygame.mixer.music.set_volume(0.1)      #
pygame.mixer.music.play(loops = -1)     #
oof = pygame.mixer.Sound('oof2.wav')    # Initializes all of the sounds
oof.set_volume(1000)                    #
ouch = pygame.mixer.Sound('ouch.wav')   #   
ouch.set_volume(1000)                   #
tick = pygame.mixer.Sound('tick.wav')   #   
tick.set_volume(1000)                   #
#---------------------------------------#
    
#---------------------------------------#
COLUMNS = 14                            #
ROWS = 22                               # 
LEFT = 9                                # 
RIGHT = LEFT + COLUMNS                  # 
MIDDLE = LEFT + COLUMNS//2              #
TOP = 1                                 # Initializes all of the varaibles on the grid
FLOOR = TOP + ROWS                      #
NEXTX = 27                              #
NEXTY = 6                               #
HOLDX = 3                               #
HOLDY = 6                               #
#---------------------------------------#

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redraw_screen(pause):
    if gameScreen == 0:                                         # If the game hasn't started yet
        screen.blit(start,(0,0))
    elif gameScreen == 1:                                       # If the game is being played
        realTime = time.clock()                                 # Initialize the timer
        timeText = 'Time: ' + str(int(realTime - addedTime))    #
        scoreText = 'Score: ' + str(score)                      #
        holdText = 'HOLD'                                       # Initialize the onscreen text
        nextText = 'NEXT'                                       #
        levelText = 'Level: ' + str(level)                      #
        
        screen.blit(background,(0,0))                           # Draw the background image
        
        for x in range(LEFT*GRIDSIZE + GRIDSIZE,RIGHT*GRIDSIZE, GRIDSIZE):          #
            pygame.draw.line(screen, GREY, (x,TOP*GRIDSIZE),(x, FLOOR*GRIDSIZE))    # Draws the grid
        for y in range(TOP*GRIDSIZE, (ROWS+1)*GRIDSIZE, GRIDSIZE):                  # Inside the playfield
            pygame.draw.line(screen, GREY, (LEFT*GRIDSIZE, y),(RIGHT*GRIDSIZE, y))  #
            
        shadow.draw(screen, GRIDSIZE)                   # 
        shape.imageDraw(screen, GRIDSIZE, img)          #
        nextShape.imageDraw(screen, GRIDSIZE, img)      #
        floor.draw(screen, GRIDSIZE)                    #
        leftWall.draw(screen, GRIDSIZE)                 # 
        rightWall.draw(screen, GRIDSIZE)                # Draws all of the objects on the screen
        square(RIGHT+2, TOP+2, 6, GRIDSIZE)             #
        square(1, TOP+2, 6, GRIDSIZE)                   #
        obstacle.imageDraw(screen, GRIDSIZE, img)       #
        if holdShapeNo > 0:                             #
            holdShape.imageDraw(screen, GRIDSIZE, img)  #

        timeDisplay = font.render(timeText, 1, WHITE)   #
        scoreDisplay = font.render(scoreText, 1, WHITE) #
        holdDisplay = font.render(holdText, 1, WHITE)   # Initializes all of the text
        nextDisplay = font.render(nextText, 1, WHITE)   #
        levelDisplay = font.render(levelText, 1, WHITE) #
        
        screen.blit(timeDisplay, (10, 480))             #
        screen.blit(scoreDisplay,(10,560))              #
        screen.blit(holdDisplay,(50,230))               # Displays all of the text
        screen.blit(nextDisplay,(655,230))              #
        screen.blit(levelDisplay,(10,520))              #

        if pause:                                           # If the game is paused
            screen.blit(pauseImg, (200,100))                # Draw the pause button on the screen

    else:                                                   # If the game has ended
        screen.blit(end,(0,0))                              #Draws the end screen image
        scoreText = str(score)                              #
        scoreDisplay = fontBig.render(scoreText, 1, WHITE)  # Displays the final score text
        screen.blit(scoreDisplay,(370,520))                 #
    pygame.display.update()                                 # Updates the screen


def square(x, y, size, gridsize):
    """ (int, int, int, int) -> (none)
    draws a square on the screen when given the position and dimenstions of the square
    """
    x *= gridsize   # Puts the given values
    y *= gridsize   # onto the grid
    for i in range(size):                                                                               # Runs a for loop for the vertical lines of the square
        pygame.draw.rect(screen, BLACK,(x,y+(i*gridsize),gridsize+1,gridsize+1), 0)                     #
        pygame.draw.rect(screen, BLACK,(x+((size-1)*gridsize),y+(i*gridsize),gridsize+1,gridsize+1), 0) # Draws the black and white
        pygame.draw.rect(screen, WHITE,(x,y+(i*gridsize),gridsize+1,gridsize+1), 1)                     # cubes for the square
        pygame.draw.rect(screen, WHITE,(x+((size-1)*gridsize),y+(i*gridsize),gridsize+1,gridsize+1), 1) #
    for i in range(1,size-1):                                                                           # Runs a for loop for the horizontal lines of the square
        pygame.draw.rect(screen, BLACK,(x+(i*gridsize),y,gridsize+1,gridsize+1), 0)                     #
        pygame.draw.rect(screen, BLACK,(x+(i*gridsize),y+((size-1)*gridsize),gridsize+1,gridsize+1), 0) # Draws the black and white
        pygame.draw.rect(screen, WHITE,(x+(i*gridsize),y,gridsize+1,gridsize+1), 1)                     # cubes for the square
        pygame.draw.rect(screen, WHITE,(x+(i*gridsize),y+((size-1)*gridsize),gridsize+1,gridsize+1), 1) #

#-----------------------------------------------#
shapeNo = randint(1,7)                          # 
shape = Shape(MIDDLE, TOP+1 ,shapeNo)           #
                                                #
nextShapeNo = randint(1,7)                      # 
if nextShapeNo == 7:# If the nextshape is a cube#
    NEXTX = 28 # Move it over one to center it  #
else:                                           #
    NEXTX = 27                                  #
nextShape = Shape(NEXTX, NEXTY, nextShapeNo)    # Initializes all of the objects
                                                #
holdShapeNo = 0                                 #
shadow = Shadow(MIDDLE, TOP, shapeNo)           #
floor = Floor(LEFT,FLOOR,COLUMNS)               #
leftWall = Wall(LEFT-1, TOP, ROWS+1)            #
rightWall = Wall(RIGHT, TOP, ROWS+1)            #
obstacle = Obstacles(LEFT, FLOOR)               #
#-----------------------------------------------#

#-----------------------#
inPlay = True           #
shadowUpdate = True     #
gameScreen = 0          #
addedTime = 0           #
score = 0               #
level = 1               #
mult = False            # Initilizes all of the variables used in the game
frameCount = 0          #
shiftTrigger = False    #
pause = False           #
pauseTrigger = False    #
levelMove = 20          #
sound = False           #
#-----------------------#

shadow.update(shape)                                                # Updates the shadow
shadow.moveToBottom(floor, obstacle)                                # Moves it to the bottom of the screen

#---------------------------------------#
#   main program                        #
#---------------------------------------#

while inPlay:                                                       # While loop that runs the game
    if gameScreen == 0:                                             #If the game hasn't started
        for event in pygame.event.get():                            #
            if event.type == pygame.QUIT:                           # If you press the X then quit the game
                inPlay = False                                      #
                
            if event.type == pygame.KEYDOWN:                        # 
                if event.key == pygame.K_SPACE and pause == False:  # If the spacebar is pressed
                    if gameScreen == 0:                             # then start the game
                        gameScreen = 1                              #
    elif gameScreen == 1:                                           # If the game has started
        frameCount+=1                                               # Add 1 to frameCount

        if pause and frameCount % 30 == 0:                          # If the game is paused
            addedTime += 1                                          # Add 1 to the addedTime so that the time doesn't add up
            
        if frameCount % levelMove == 0 and pause == False:          # If the game is playing and the peice should move down
            shape.move_down()                                       # Move the peice down
            if shape.collides(floor) or shape.collides(obstacle):   # If the shape collides with the floor
                shape.move_up()                                     #
                obstacle.append(shape)                              #
                shape = Shape(MIDDLE, TOP+1, nextShapeNo)           # Move the shape up and generate new objects
                shapeNo = nextShapeNo                               #
                nextShapeNo = randint(1,7)                          #
                if nextShapeNo == 7:                                # If the nextshape is a cube
                    NEXTX = 28                                      # Move it over one to center it  
                else:                                           
                    NEXTX = 27  
                nextShape = Shape(NEXTX, NEXTY, nextShapeNo)        #
                shadow.update(shape)                                # Generate a new nextShape, update the shadow
                shadow.moveToBottom(floor, obstacle)                # and move the shadow to the bottom
                shiftTrigger = False                                #
                tick.play()                                         # Play a sound
            
        fullRows = obstacle.findFullRows(TOP, FLOOR, COLUMNS)                           # Finds the full rows and removes their blocks from the obstacles
        (score, mult, sound) = obstacle.removeFullRows(fullRows, score, mult, sound)    # Removes the full rows and gives the variables needed for the score

        if sound:                           # If the sound is triggered
            ouch.play()                     # Play the sound
            sound = False

        keys = pygame.key.get_pressed()     # Initializes the keys varaible

        for event in pygame.event.get():
            if event.type == pygame.QUIT:         
                inPlay = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and pause == False:     # If you press up and the game is not paused            
                    shape.rotateClkwise()                   # Rotate the shape
                    if shape.collides(leftWall) or shape.collides(rightWall) or shape.collides(floor) or shape.collides(obstacle): # If the shape collides
                        shape.rotateCntclkwise()            # Rotate it back
                    shadow.update(shape)                    # Update the
                    shadow.moveToBottom(floor, obstacle)    # shadow
                if event.key == pygame.K_LEFT and pause == False:   #If you press left and the game is not paused
                    shape.move_left()                       # Move left
                    if shape.collides(leftWall) or shape.collides(obstacle): # If the shape collides
                        shape.move_right()                  # Move right
                    shadow.update(shape)                    # Update the
                    shadow.moveToBottom(floor, obstacle)    # shadow
                if event.key == pygame.K_RIGHT and pause == False: # If you press right and the game is not paused
                    shape.move_right()                      # Move right
                    if shape.collides(rightWall) or shape.collides(obstacle): # If the shape collides
                        shape.move_left()                   # Move left
                    shadow.update(shape)                    # Update the
                    shadow.moveToBottom(floor, obstacle)    # shadow
                if event.key == pygame.K_SPACE and pause == False: # If you press space and the game is not paused
                    while shape.collides(floor) == False and shape.collides(obstacle) == False: #While the shape is not colliding with the floor
                        shape.move_down()                       # Move down
                    shape.move_up()                             #
                    obstacle.append(shape)                      #
                    shape = Shape(MIDDLE, TOP+1, nextShapeNo)   # Move the shape up and generate new objects
                    shapeNo = nextShapeNo                       #
                    nextShapeNo = randint(1,7)                  #
                    if nextShapeNo == 7:                        # If the nextshape is a cube
                        NEXTX = 28                              # Move it over one to center it  
                    else:                                           
                        NEXTX = 27  
                    nextShape = Shape(NEXTX, NEXTY, nextShapeNo)    #
                    shadow.update(shape)                            # Generate a new nextShape, update the shadow
                    shadow.moveToBottom(floor, obstacle)            # and move the shadow to the bottom
                    shiftTrigger = False                            #
                    tick.play()                                     # Play a sound
                if event.key == pygame.K_LSHIFT and holdShapeNo != shapeNo and shiftTrigger == False and pause == False: # If you press shift and the hold is available
                    if holdShapeNo > 0:                         # If there is already a holdshape
                        shape = Shape(MIDDLE, TOP, holdShapeNo)
                        if shapeNo == 7:                        # If the holdShape is a cube
                            HOLDX = 4                           # Move it over one to center it
                        else:
                            HOLDX = 3
                        holdShape = Shape (HOLDX, HOLDY, shapeNo)   # Make the holdshape a new object
                        extraShapeNo = shapeNo                      #
                        shapeNo = holdShapeNo                       # Changes around the shape numbers
                        holdShapeNo = extraShapeNo                  # 
                    else:                                           # If there is no holdshape
                        holdShapeNo = shapeNo                       # Make holdShapeNo = to shapeNo
                        if holdShapeNo == 7:                        # If the holdShape is a cube
                            HOLDX = 4                               # Move it over one to center it
                        else:
                            HOLDX = 3
                        holdShape = Shape(HOLDX, HOLDY, holdShapeNo)    # Make the holdshape a new object with the same number as shape
                        shape = Shape(MIDDLE, TOP, nextShapeNo)         # Make shape a new object with the same number as holdshape
                        nextShapeNo = randint(1,7)                      # make a new nextShapeNo
                        if nextShapeNo == 7:                            # If the nextShape is a cube
                            NEXTX = 28                                  # Move the nextShape over one to center it
                        else:
                            NEXTX = 27
                        nextShape = Shape(NEXTX, NEXTY, nextShapeNo)    # Make nextShape a new object
                    shadow.update(shape)                                #
                    shadow.moveToBottom(floor, obstacle)                # Update the shadow and reset the shiftTrigger
                    shiftTrigger = True                                 #
                if event.key == pygame.K_ESCAPE:                        # If escape is pressed
                    if pauseTrigger == False:                           # If the game is not paused
                        pause = True                                    # Pause the game
                        pauseTrigger = True                             # Pause the game
                    elif pauseTrigger == True:                          # If the game is not paused
                        pause = False                                   # Unpause
                        pauseTrigger = False                            # Unpause
        if keys[pygame.K_DOWN] and frameCount % 3 == 0 and pause == False:  # If you press and hold down and the game is playing
            shape.move_down()                               # Move down
            if shape.collides(floor) or shape.collides(obstacle):           # If the shape collides with the floor
                shape.move_up()                             #
                obstacle.append(shape)                      #
                shape = Shape(MIDDLE, TOP+1, nextShapeNo)   # Move the shape up and generate new objects
                shapeNo = nextShapeNo                       #
                nextShapeNo = randint(1,7)                  #
                if nextShapeNo == 7:                        # If the nextshape is a cube
                    NEXTX = 28                              # Move it over one to center it  
                else:                                           
                    NEXTX = 27  
                nextShape = Shape(NEXTX, NEXTY, nextShapeNo)# Re-Initialize the nextShape object
                tick.play()                                 # Play a sound
            shadow.update(shape)                            # Generate a new nextShape, update the shadow
            shadow.moveToBottom(floor, obstacle)            # and move the shadow to the bottom
            shiftTrigger = False   
                    
        kill = obstacle.findTop()   # Kill is equal to if the obstacle has hit the top of the screen
        if kill:                    # If kill is true
            oof.play()              # Play the death sound
            gameScreen = 2          # Put the game into the gameover screen

        if 500 <= score < 1000:     # If your score is between 500 and 1000
            level = 2               # Set level to 2
            levelMove = 10          # Change the speed that the blocks fall
        elif score >= 1000:         # If your score is above 1000
            level = 3               # Set level to 3
            levelMove = 5           # Change the speed that the blocks fall
    else:                           # If the gameScreen is 2
        inPlay = False              # Break the while loop
    redraw_screen(pause)            # Redraw the screen
    pygame.time.delay(30)           # Delay 30 miliseconds

if gameScreen == 2:                 # If the game has been quit because they lost
    pygame.time.delay(4000)         # Delay 4 seconds
pygame.quit()                       # Quit
    
    
