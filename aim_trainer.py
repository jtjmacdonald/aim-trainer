import pygame, random, math, time, sqlite3, numpy
from pygame.locals import *

pygame.init()                                               # called to use pygame module

clock = pygame.time.Clock()                                 
width = 800
height = 600
windowSurface = pygame.display.set_mode((width, height))    # windowSurface is the window
pygame.display.set_caption("Aim Trainer")                   # setting the window name for the game


# game start variables
cx = random.randint(20, width - 20)         # max width of a circle is 20; no matter what the res, there will not be targets outside the
cy = random.randint(20, height - 20)        # window the player can see
width_of_circle = random.randint(14, 20)    # where the width of circles is set (from 14 to 20)
hits = 0
#scoreData = [random.randint(100, 999)/100.00, random.randint(100, 999)/100.00, random.randint(100, 999)/100.00, random.randint(100, 999)/100.00, random.randint(100, 999)/100.00, random.randint(100, 999)/100.00, random.randint(100, 999)/100.00, random.randint(100, 999)/100.00, random.randint(100, 999)/100.00, ] # this is sample data for the bubble sort, as a placeholder for actual data to be taken in from a database
# the comment for the above is off screen ---------->
sortedScoreData = []
# this variable is checked when data is placed into the database, to ensure repeat entries do not occur
inserted = False

#defining shape dimensions
rect1 = (266, 266, 266, 120)
rect2 = (266, 100, 266, 120)
rect3 = (266, 432, 266, 120)

# defining colours

BLACK = (0, 0, 0)
RED = (255, 0 ,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


# This class will be used to define the difficulty parameters.
# Current plan: Read in difficulty parameters from a file.

class Difficulty():
    def __init__(self, timeAdded, targetsOnScreen, upperLimit):
        self.timeAdded = timeAdded
        self.targetsOnScreen = targetsOnScreen
        self.upperLimit = upperLimit


    def ReadDifficulty(self, difficulty):
        
        if difficulty == "easy":
            difficultyFile = open("easy.txt", "r")
        if difficulty == "medium":
            difficultyFile = open("medium.txt", "r")
        if difficulty == "hard":
            difficultyFile = open("hard.txt", "r")
        
        var = 1
        for line in difficultyFile:
            splitLine = line.split(":")
            splitLine[1] = splitLine[1].strip("\n")
            print(splitLine[0], splitLine[1])
            if var == 1:
                self.timeAdded = splitLine[1]
            elif var == 2:
                self.targetsOnScreen = splitLine[1]
            elif var == 3:
                self.upperLimit = splitLine[1]
            var = var + 1
        
            
            


def LoadMainMenu():

    windowSurface.fill(BLACK)
    menuButtons = []
    menuButtons.append(pygame.Rect(266, 100, 266, 120))
    menuButtons.append(pygame.Rect(266, 266, 266, 120))
    menuButtons.append(pygame.Rect(266, 432, 266, 120))
        
    for rect in menuButtons:                            # this prints the rectangles which the user controls the game via
        pygame.draw.rect(windowSurface, RED, rect)

    if event.type == MOUSEBUTTONDOWN:
        # Start Game
        if menuButtons[0].collidepoint(pygame.mouse.get_pos()):  
            startGame(cx, cy, width_of_circle, gameDiff.upperLimit, hits, inserted)
        # Select Difficulty
        if menuButtons[1].collidepoint(pygame.mouse.get_pos()):
            # loadDifficultyMenu(menuButtons)
            pass
        # Leaderboard
        if menuButtons[2].collidepoint(pygame.mouse.get_pos()):
            loadLeaderboard()
    
    windowSurface.blit(titlefont.render('AIM TRAINER', True, WHITE, None), (170,15))
    windowSurface.blit(buttonfont.render('Start Game', True, BLACK, None), (310,140))
    windowSurface.blit(buttonfont.render('Select Difficulty', True, BLACK, None), (290,306))
    windowSurface.blit(buttonfont.render('Leaderboard', True, BLACK, None), (310,472))

        
    pygame.display.update()
    clock.tick(60)
    
def loadDifficultyMenu(menuButtons):
    while True:
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:           
                pygame.quit()                       
                quit()
        
        windowSurface.fill(BLACK)
        time.sleep(0.5) # attempting to delay the program so that infinite recursion doesn't occur with buttons that refer to themselves
                
        diffButtons = []
        diffButtons.append(pygame.Rect(266, 100, 266, 120))
        diffButtons.append(pygame.Rect(266, 266, 266, 120))
        diffButtons.append(pygame.Rect(266, 432, 266, 120))     
        diffButtons.append(pygame.Rect(80, 432, 266, 120)) # back button   
        
        windowSurface.blit(titlefont.render('DIFFICULTY SELECT', True, YELLOW, None), (170,15))
        windowSurface.blit(buttonfont.render('Easy', True, BLACK, None), (310,140))
        windowSurface.blit(buttonfont.render('Medium', True, BLACK, None), (290,306))
        windowSurface.blit(buttonfont.render('Hard', True, BLACK, None), (310,472))
        windowSurface.blit(buttonfont.render('Back', True, WHITE, None), (110,472))
        
        if diffButtons[0].collidepoint(pygame.mouse.get_pos()):
            gameDiff = Difficulty.ReadDifficulty(Difficulty, "easy")
        if diffButtons[1].collidepoint(pygame.mouse.get_pos()):
            gameDiff = Difficulty.ReadDifficulty(Difficulty, "medium")
        if diffButtons[2].collidepoint(pygame.mouse.get_pos()):
            gameDiff = Difficulty.ReadDifficulty(Difficulty, "hard")
        if diffButtons[3].collidepoint(pygame.mouse.get_pos()):
            LoadMainMenu()
        pygame.display.update()
        clock.tick(60)

def loadLeaderboard():
    while True:
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:           
                pygame.quit()                       
                quit()
        scoreData = []
        scoreData = scoresTableToArray()
        sortedScoreData = bubbleSortArray(scoreData)


        windowSurface.fill(BLACK)
                
        LBButtons = []
        LBButtons.append(pygame.Rect(30, 432, 266, 120)) # back button   
        
        
        for rect in LBButtons:
            pygame.draw.rect(windowSurface, RED, rect)
            
        printHeight = 100
        
        for i in range(len(sortedScoreData)):
            windowSurface.blit(scoreFont.render(str(i + 1) + ". " + str(sortedScoreData[i]), True, WHITE, None), (335, printHeight))
            printHeight = printHeight + 35
            
            
        windowSurface.blit(titlefont.render('Leaderboard', True, YELLOW, None), (210,15))
        windowSurface.blit(buttonfont.render('Back', True, WHITE, None), (125,472))
        
        if LBButtons[0].collidepoint(pygame.mouse.get_pos()):
            LoadMainMenu()
            
        pygame.display.update()
        clock.tick(60)
    
    

def startGame(cx, cy, width_of_circle, gameDiff, hits, inserted):
    startTime = time.time()

    inserted = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        windowSurface.fill(BLACK)
        windowSurface.blit(buttonfont.render('Hits: ' + str(hits), True, WHITE, None), (110,472))

        x = pygame.mouse.get_pos()[0] # pulls the x value from the get_pos
        y = pygame.mouse.get_pos()[1] 
        click = pygame.mouse.get_pressed() # returns booleans for each mousebutton, if true when called then button is being clicked

        sqx = (x - cx)**2
        sqy = (y - cy)**2

        if math.sqrt(sqx + sqy) < width_of_circle and click[0] == 1: # if the circle created outside the loop is clicked, then it creates a new circle, and covers the previous circle
            windowSurface.fill(BLACK)
            cx = random.randint(20, width - 20)
            cy = random.randint(20, height - 20)
            width_of_circle = random.randint(14, 20)
            hits = hits + 1

    
        pygame.draw.circle(windowSurface, WHITE, (cx, cy), width_of_circle)

        if hits == 15:
            endTime = time.time()
            gameTime = round((endTime - startTime), 3)
            print(gameTime)
            endGame(gameTime, inserted)
        pygame.display.update()
        clock.tick(60)
        
def endGame(gameTime, inserted):                                    # function called when game ends; displays score (time), saves to database
    while True:
        
        windowSurface.fill(BLACK)
        time.sleep(0.5)

        windowSurface.blit(buttonfont.render("Game Complete", True, WHITE, None), (310,50))
        windowSurface.blit(buttonfont.render("Time Completed: " + str(gameTime), True, WHITE, None), (310,140))
        windowSurface.blit(buttonfont.render("Difficulty: ", True, WHITE, None), (310,230))

        if inserted == False:                       # checks if the data is already in the database
            initDatabaseConnection(gameTime)
            inserted = True                         # ensures that future checks will fail

        pygame.display.update()
        clock.tick(60)
    
def bubbleSortArray(scoreData):
    sortedScoreData = scoreData
    swapped = True
    while (swapped == True):
        swapped = False
        for i in range(len(sortedScoreData) - 1):
            if sortedScoreData[i] > sortedScoreData[i + 1]:
                sortedScoreData[i], sortedScoreData[i+1] = sortedScoreData[i+1], sortedScoreData[i]
                swapped = True
    return sortedScoreData

def initDatabaseConnection(gameTime):
    import sqlite3

    con = sqlite3.connect('scores.sqlite')      # connecting to the sqlite3 database

    cur = con.cursor()

    # Create the score table, if it doesn't already exist
    cur.execute('''CREATE TABLE IF NOT EXISTS scores (game_time real NOT NULL) ''')

    # Save the newly created score to the database
    # scoreID will automatically increment, taking the place of the hidden primary key
    cur.execute(" INSERT INTO scores values (?)", (gameTime,))

    print("database insertion complete!")

    # Commit the new entry (save to disk)
    con.commit()

    # Close the connection
    con.close()

def scoresTableToArray():
    con = sqlite3.connect('scores.sqlite')
    cur = con.cursor()

    # Create the score table, if it doesn't already exist
    cur.execute('''CREATE TABLE IF NOT EXISTS scores (game_time real NOT NULL) ''')

    scoreData = []
    cur.execute('select * from scores')
    allScores = cur.fetchall() # retrieves a tuple of scores from the database
    scoreArray = numpy.asarray(allScores) # converts the tuple to a 2d array
    scoreData = scoreArray.flatten() # converts the 2d array to a 1d array

    con.close()
    return scoreData

    

    










            
    
    

# defining global variables/function variables/default variables

titlefont = pygame.font.SysFont('Arial', 70)    # note that sysfont changes based on operating system
scoreFont = pygame.font.SysFont('Arial', 40)
buttonfont = pygame.font.SysFont('Arial', 32)
gameDiff = Difficulty(2, 1, 20)
gameDiff.ReadDifficulty("easy")


print(gameDiff.timeAdded, gameDiff.targetsOnScreen, gameDiff.upperLimit)

# Main Game Loop


while True:                                     
    for event in pygame.event.get():            #
        if event.type == pygame.QUIT:           #   Ensures that when the user wishes to close the program, python unloads itself properly.
            pygame.quit()                       #
            quit()                              #
    LoadMainMenu()



