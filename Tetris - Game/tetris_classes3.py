#----------------------------------------------#
# Tetris Classes 3 (Final)                     #
# By: Ethan Zohar                              #
# May 26, 2017                                 #
# Holds all of the classes for the tetris game #
#----------------------------------------------#

#---------------------------------------------------------------------------------------#
import pygame                                                                           #
                                                                                        #
GRIDSIZE = 600//24                                                                      #
                                                                                        #
GREY = (192,192,192)                                                                    #
BLACK     = (  0,  0,  0)                                                               #
RED       = (255,  0,  0)                                                               #
GREEN     = (  0,255,  0)                                                               # Initializes all the needed variables for the classes
BLUE      = (  0,  0,255)                                                               #
ORANGE    = (255,127,  0)                                                               #
CYAN      = (  0,183,235)                                                               #
MAGENTA   = (255,  0,255)                                                               #
YELLOW    = (255,255,  0)                                                               #
WHITE     = (255,255,255)                                                               #
COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]   #
CLR_names = ['black','red','green','blue','orange','cyan','magenta','yellow','white']   #
FIGURES   = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]   #
#---------------------------------------------------------------------------------------#

class Block(object):                    
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row
        self.clr = clr

    def __str__(self):                  
        return '('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def draw(self, surface, gridsize):
        """ (str, int) -> (none)
        draws the blocks on the screen
        """
        x = self.col * gridsize                                         #
        y = self.row * gridsize                                         #
        CLR = COLOURS[self.clr]                                         # Draws the blocks on the screen
        pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 0)        #
        pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 1) #
        
    def imageDraw(self, surface, gridsize, image): 
        """ (str, int, img) -> (none)
        draws the images on the screen
        """                    
        x = self.col * gridsize         #
        y = self.row * gridsize         # Draws the images
        CLR = image[self.clr-1]         # of the blocks on the screen
        surface.blit(CLR, (x,y))        #

    def shadowDraw(self, surface, gridsize=20):
        """ (str, int) -> (none)
        draws the shadow on the screen
        """                     
        x = self.col * gridsize                                         #
        y = self.row * gridsize                                         #
        CLR = COLOURS[self.clr-1]                                       # Draws the shadow
        pygame.draw.rect(surface, GREY,(x,y,gridsize+1,gridsize+1), 0)  #
        pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 1) #

    def move_down(self):
        """ (none) -> (none)
        moves the block down
        """                
        self.row = self.row + 1

#---------------------------------------#
class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0                          
        self.blocks = [Block()]*blocksNo      
        self._colOffsets = [0]*blocksNo  
        self._rowOffsets = [0]*blocksNo
        
    def _update(self):
        """ (none) -> (none)
        resets the cluster
        """
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i] 
            blockROW = self.row+self._rowOffsets[i] 
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize):
        """ (str, int) -> (none)
        calls draw from block
        """
        for block in self.blocks:
            block.draw(surface, gridsize)               # Draws all of the blocks
            
    def imageDraw(self, surface, gridsize, image):
        """ (str, int, img) -> (none)
        calls imageDraw from block
        """                     
        for block in self.blocks:
            block.imageDraw(surface, gridsize, image)   # Draws all of the images

    def collides(self, other):
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block.col == obstacle.col and block.row == obstacle.row:
                    return True
        return False
    
    def append(self, other): 
        """ Append all blocks from another cluster to this one.
        """
        for i in other.blocks:
            self.blocks.append(i)

#---------------------------------------#
class Obstacles(Cluster):
    """ Collection of tetrominoe blocks on the playing field, left from previous shapes.
        
    """        
    def __init__(self, col = 0, row = 0, blocksNo = 0):
        Cluster.__init__(self, col, row, blocksNo)      # initially the playing field is empty(no shapes are left inside the field)

    def findFullRows(self, top, bottom, columns):
        """ (int, int, int) -> (list)
        returns a list of the full rows when given the dimensions of the playing field
        """
        fullRows = []
        rows = []
        for block in self.blocks:                       
            rows.append(block.row)                      # make a list with only the row numbers of all blocks
            
        for row in range(top, bottom):                  # starting from the top (row 0), and down to the bottom
            if rows.count(row) == columns:              # if the number of blocks with certain row number
                fullRows.append(row)                    # equals to the number of columns -> the row is full
        return fullRows                                 # return a list with the full rows' numbers

    def removeFullRows(self, fullRows, score, mult, sound):
        """ (list, int, bool, bool) -> (int, bool, bool)
        returns the score, multiplier, and sound trigger when given the full rows
        """
        amount = 0
        for row in fullRows:                            # for each full row, STARTING FROM THE TOP (fullRows are in order)
            amount += 1
            for i in reversed(range(len(self.blocks))): # check all obstacle blocks in REVERSE ORDER,
                                                        # so when popping them the index doesn't go out of range !!!
                if self.blocks[i].row == row:
                    self.blocks.pop(i)                  # remove each block that is on this row
                    sound = True
                elif self.blocks[i].row < row:
                    self.blocks[i].move_down()          # move down each block that is above this row
        if amount < 4:                          # If you took out less than 4 rows at once       
            for i in range(amount):             # Run a for loop through the amount of rows taken out
                mult = False                    # Multiply is false
                score += 100                    # Add 100 to score
        elif amount == 4 and mult == True:      # If you took out 4 rows at once and your last take out was also 4 rows
            score += 1200                       # Add 1200 points to score
            mult = True                         # Multiply is true
        elif amount == 4 and mult == False:     # If you took out 4 rows at once and your last take out was not 4 rows
            score += 800                        # Add 800 points to score
            mult = True                         # Multiply is true
        return score,mult,sound

    def findTop(self):
        """ (none) -> (bool)
        returns a boolean saying if the obstacle has hit the top of the screen
        """
        kill = False                    # Kill originally equals false
        for block in self.blocks:       # Runs a for loop through all of the blocks in the obstacle
            if block.row < 2:           # Checks to see if any of the blocks are above the top 2 rows
                kill = True             # Set kill to true
        return kill
#---------------------------------------#
class Shape(Cluster):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        Cluster.__init__(self, col, row, 4)
        self.clr = clr
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1] 
        self._rowOffsets = [-1,-1, 0, 0] 
        self._rotate()
        
    def __str__(self):                  
        return FIGURES[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def _rotate(self):
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]] #       
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]] #
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]] #
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]] #
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]] #            
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o                 
            _colOffsets = [[-1, 0, 0, 0], [1, 1, 0,-1], [1, 0, 0,0], [-1, -1, 0,1]]
            _rowOffsets = [[-1,-1, 0, 1], [-1,0, 0, 0], [1, 1, 0, -1], [1, 0, 0, 0]]
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]] #
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]] #           
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]] #
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]] #
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]] #
        self._colOffsets = _colOffsets[self._rot] 
        self._rowOffsets = _rowOffsets[self._rot] 
        self._update()

    def move_left(self):
        """ (none) -> (none)
        moves the shape left
        """
        self.col = self.col - 1                   
        self._update()
        
    def move_right(self):  
        """ (none) -> (none)
        moves the shape right
        """             
        self.col = self.col + 1                   
        self._update()
        
    def move_down(self):
        """ (none) -> (none)
        moves the shape down
        """                
        self.row = self.row + 1                   
        self._update()
        
    def move_up(self): 
        """ (none) -> (none)
        moves the shape up
        """                 
        self.row = self.row - 1                   
        self._update()

    def rotateClkwise(self):
        """ (none) -> (none)
        rotates the shape clockwise
        """
        self._rot = (self._rot + 1)%4  
        self._rotate()

    def rotateCntclkwise(self):
        """ (none) -> (none)
        rotates the shape counterclockwise
        """
        self._rot = (self._rot - 1)%4  
        self._rotate()

class Shadow(Shape):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        Is a child class of shape and calls functions from the shape class
    """
    def draw(self, surface, gridsize = 20):
        """ (str, int) -> (none)
        calls shadowDraw from block
        """                     
        for block in self.blocks:
            block.shadowDraw(surface, gridsize)         # Calls shadowDraw from the block class instead of the normal draw
            
    def moveToBottom(self, floor, obstacle):
        """ (int, int) -> (none)
        moves the shadow to the bottom of the screen when given the floor and the obstacles
        """
        while self.collides(floor) == False and self.collides(obstacle) == False:   # While the shadow has not hit the bottom
            self.move_down()    # Move down
        self.move_up()          # Move up one peice so that it is not in the ground
        self._update()          # Updates the shadow

    def update(self, other):
        """ (object) -> (none)
        updates the shadow's position and shape when given the other object to update too
        """
        self.col = other.col                #
        self.row = other.row                #
        self.clr = other.clr                # Sets all of the shadows variables to the shapes variables
        self._rot = other._rot              #
        self._rotate()                      #
#---------------------------------------#
class Floor(Cluster):
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i 
        self._update() # private       
            
#---------------------------------------#
class Wall(Cluster):
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i 
        self._update()

    
