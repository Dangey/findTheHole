from graphics import *
from holeObject import Hole #import Hole class from holeObject.py
import random #for random number selection
import datetime #for current date

'''
Created by Anthony Soto

Last updated on 4/30/2019

Title: Find the Hole

Dependent files and their methods:
- game.py (this)
    - startScreen()
    - gameScreen()
    - saveScores(totalSteps, difficulty)
    - pickDifficulty()
    - endScreen()
    - main()
- holeObject.py
    -Class Hole(object)
        - __init__
        - makeHole(self,win)
        - undrawHole(self)
        - getPoint(self)
        - checkPoints(self, point1)
        - checkCircles(self, hole)
- graphics.py (many graphic methods)

This concept was inspired by the Find the Hole option on the Project syllabus.

Game Flow:

The game begins on the startScreen, which contains two option buttons --> Start, Exit
    Start will progress the code to the gameScreen
    Exit will close the window and kill the program
    
Once on the gameScreen, three difficulty options appear as buttons --> Easy, Medium, Hard
    When pressed, variables that determine hole size and hole number are set to values
    that are distinctive to that difficulty type.
    
From here, holes are generated. While being generated, they are checked to see if they overlap.
If they do, that hole is not used, and another is generated and checked.

Once all holes meet requirements, the user HUD is made. User is prompted to click to begin.
Upon clicking, the user can now click across the screen. Each click leaves a brown dot, and is counted
and shown at the bottom of the screen as "Steps: #". Similarly, attempts left is shown on the bottom
right, as "Attempts Left: (max_attempts - clicks)" (currently 25 - user_clicks). This decrements
with each user click. On the bottom right, "Holes 0/#" indicates how many holes have been found
out of how many holes there are in total.

A user click that falls within the radius of a hole will reveal that hole, and be added as a hole found.
Once all holes are found before all attempts are used, the user wins. If all attempts are used, and all
holes are NOT found, the user loses.

A win will send the code to record the user's run as "(Difficulty) (Steps)" in the "scores ( current date).txt" file.
If the file does not exist, it will be created. If it does, it will be appended too.

Win or Lose, the user is prompted to click to continue at this point.
If the user has lost, they will be directed to the start screen the game flow is repeated.
If the user has won, they wil be taken to the end screen.

The end screen displays all three difficulties and the lowest number of steps it took to win in each one.
If there is no score, it will display 'N/A'. This reads only from scores recorded on the current day.

The user is prompted to click. This click will take them to the startScreen, where the game flow is repeated.

User can only exit by clicking the "Exit" button on the startScreen. Or clicking the X on the window. 

'''

#window dimensions
width = 800
height = 400

#screen-transition flags
start = True
game = False
end = False

#difficulty flags
easy = False
medium = False
hard = False

#game title
title = 'FIND THE HOLE'

#window
win = GraphWin(title,width,height)
win.yUp()

#list and dictionary of lists for holding score data
raw_data = []
score_data = {
    "Easy" : [],
    "Medium" : [],
    "Hard" : []
    }

#############startScreen method##############################################################
def startScreen():
    win.setBackground('light green')
#*************Button Variables***************************************
    startB_topleft_x = width/2.2
    startB_topleft_y = height/1.85
    startB_botright_x = width/1.81
    startB_botright_y = height/2.2

    exitB_topleft_x = width/2.2
    exitB_topleft_y = height/2.6
    exitB_botright_x = width/1.81
    exitB_botright_y = height/3.5
#*************Button Variables end***********************************
#*************Drawing Buttons****************************************
    buttonColor = 'green'

    startButton = Rectangle(Point(startB_topleft_x, startB_topleft_y),
                            Point(startB_botright_x, startB_botright_y))
    startButton.setOutline(buttonColor)
    startButton.draw(win)

    exitButton = Rectangle(Point(exitB_topleft_x, exitB_topleft_y),
                           Point(exitB_botright_x, exitB_botright_y))
    exitButton.setOutline(buttonColor)
    exitButton.draw(win)
#*************Drawing Buttons end************************************
#*************Setting Text on Buttons********************************
    #title
    titleColor = 'green'
    titleStyle = 'bold'
    #buttons
    textColor = 'green'
    textStyle = 'italic'

    titleMessage = Text(Point(width/2, height*3/4), title)
    titleMessage.setSize(36)
    titleMessage.setStyle(titleStyle)
    titleMessage.setFill(titleColor)
    titleMessage.draw(win)

    startOption = Text(Point(width/2, height/2), 'Start')
    startOption.setSize(22)
    startOption.setStyle(textStyle)
    startOption.setFill(textColor)
    startOption.draw(win)

    exitOption = Text(Point(width/2, height/3), 'Exit')
    exitOption.setSize(22)
    exitOption.setStyle(textStyle)
    exitOption.setFill(textColor)
    exitOption.draw(win)
#*************Setting Text on StartScreen end*************************
#*************Clicking on Options*************************************
    #grabs mouse coordinates on-click, separates click (x,y) into separate x, y variables
    user_click = win.getMouse()
    uc_x = user_click.getX()
    uc_y = user_click.getY()

    #START OPTION
    #if mouse clicks inside Start button, check gamescreen flag, uncheck startscreen flag
    if (uc_x >= startB_topleft_x and uc_x <= startB_botright_x
        and uc_y <= startB_topleft_y and uc_y >= startB_botright_y):
        global start
        start = False
        global game
        game = True

        #undraws all things drawn
        startButton.undraw()
        exitButton.undraw()
        titleMessage.undraw()
        startOption.undraw()
        exitOption.undraw()

    #EXIT OPTION
    #if mouse clicks inside Exit button, close window, kill program
    if (uc_x >= exitB_topleft_x and uc_x <= exitB_botright_x
        and uc_y <= exitB_topleft_y and uc_y >= exitB_botright_y):
        win.close()
        exit()
#*************Clicking on Options end*********************************
#############startScreen method end##########################################################

##############gameScreen method##############################################################
def gameScreen():
    win.setBackground('green')
    hudBar = Rectangle(Point(0,height/8), Point(width,0))
    hudBar.setFill('black')
    hudBar.draw(win)
    
    pickDifficulty()

    global easy, medium, hard
    #max/min radiuses for hole size, holes for total # of holes, then diff for difficulty type
    if easy:
        max_radius = 80
        min_radius = 70
        holes = 3
        diff = 'Easy'
    elif medium:
        max_radius = 60
        min_radius = 50
        holes = 5
        diff = 'Medium'
    elif hard:
        max_radius = 40
        min_radius = 30
        holes = 8
        diff = 'Hard'

    holes_list = []

#****************************Hole Generator****************************
    for x in range(holes): #for-loop for # of holes
        while True: #reiterates until hole does not overlap with another hole
            #generates random x and y coordinates, and radius. Creates Hole instance variable.
            temp_r = random.randint(min_radius,max_radius)
            #for x and y, shrunk in the possible values to make room for HUD and so circles don't
            #clip the edges.
            temp_x = random.randint((10 + temp_r), ((width-10) - temp_r))
            temp_y = random.randint((height/8 + temp_r), ((height-10) - temp_r))
            temp = Hole(temp_x, temp_y, temp_r)

            #flag for if Hole overlaps with another hole. Defaults to True.
            canAdd = True

            #instance of first hole being added. Cannot overlap since its the first.
            #Breaks out of while loop. No need to compare to empty list.
            if (x == 0):
                holes_list.append(temp)
                break
            
            #checks if randomly generated holes overlap at all. Compares new hole to list of holes.
            for j in holes_list:
                if temp.checkCircles(j): #calls Hole method, checkCircles. Returns True if overlap.
                    canAdd = False #ticks flag to false if overlap
                    break #break out of for-loop. No need to check the rest of the list.

            #if hole does not overlap, add to list and break out of while loop.
            #if hole DOES overlap, do nothing. While loop reiterates.
            if canAdd:
                holes_list.append(temp)
                break
#****************************Hole Generator end************************
#*********************Gameplay*****************************************       
    #counter variables for # of click, and holes found
    clicks = 0
    holes_found = 0
    #variable for max_attempts, lose condition
    max_attempts = 25
    #flags for win/loss condition
    won = False
    loss = False

    #HUD text for Steps: 0 and Holes: 0/0, initializer
    stepsMessage = Text(Point(width/2,height/16),("Steps: " + str(clicks)))
    stepsMessage.setSize(22)
    stepsMessage.setFill('yellow')
    stepsMessage.draw(win)
    foundMessage = Text(Point(width*6/7,height/16),
                        ("Holes: " + str(holes_found) + "/" + str(holes)))
    foundMessage.setSize(22)
    foundMessage.setFill('yellow')
    foundMessage.draw(win)
    attemptsLeftMessage = Text(Point(width/7,height/16),
                        ("Attempts Left: " + str(max_attempts - clicks)))
    attemptsLeftMessage.setSize(22)
    attemptsLeftMessage.setFill('yellow')
    attemptsLeftMessage.draw(win)

    #prompt for click to begin game
    win.promptMouse(width/2,height/2,"Click Anywhere to Start")

    #initialize lists for gathering steps and found holes.
    #Will help later with undrawing.
    stepList = []
    foundList = []

    #Game Loop************************************************************
    while True:
        #undraws previous message text, updates clicks and holes_found, then redraws
        stepsMessage.undraw()
        foundMessage.undraw()
        attemptsLeftMessage.undraw()
        stepsMessage.setText("Steps: " + str(clicks))
        foundMessage.setText("Holes: " + str(holes_found) + "/" + str(holes))
        attemptsLeftMessage.setText("Attempts Left: " + str(max_attempts - clicks))
        stepsMessage.draw(win)
        foundMessage.draw(win)
        attemptsLeftMessage.draw(win)
        
        #if list of found holes is equal to the total # of holes, break while loop
        if (len(foundList) == holes):
            won = True
            break

        if ((max_attempts - clicks) <= 0):
            loss = True
            break

        #wait for user input of click, draw point on screen, add to stepList, increment clicks
        step = win.getMouse()
        step.setFill('brown')
        step.draw(win)
        stepList.append(step)
        clicks += 1

        #Validator
        #goes through holes_list, calls Hole method --> checkPoints
        #if returns True, draw Hole on screen, add Hole to foundList
        #remove from holes_list since there is no need to check this particular hole anymore
        #increment holes_found
        for hole in holes_list:
            if hole.checkPoints(step):
                hole.makeHole(win)
                foundList.append(hole)
                holes_list.remove(hole)
                holes_found += 1
    #Game Loop end********************************************************
    #*********************Gameplay end************************************

    #Loss/Win Condition message
    condMessage = Text(Point(width/2,height/2),"")
    condMessage.setStyle('bold')
    condMessage.setSize(30)
    condMessage.setFill('yellow')
    #Set message to Win or Lose based on condition flags
    if loss:
        condMessage.setText('YOU LOSE')
    elif won:
        condMessage.setText('YOU WIN')
        saveScores(clicks, diff) #method for saving score
        
    #draw message to window, prompt for click to continue
    condMessage.draw(win)
    win.promptMouse(width/2, height/3, "Click anywhere to Continue")
    
    #Undraw ALL
    for i in stepList: #undraw all points
        i.undraw()
    for k in foundList:#undraw all holes, using Hole method, undrawHole.
        k.undrawHole()
    stepsMessage.undraw()
    foundMessage.undraw()
    attemptsLeftMessage.undraw()
    condMessage.undraw()
    hudBar.undraw()

    #tick game flag to False, end flag to True. This sends screen to end, showing scores. Only on Win.
    global start, game, end
    if won:
        game = False
        end = True
    else: #tick game flag to False, start flag to True. This sends screen back to startScreen
        start = True
        game = False
        
##############gameScreen method end##########################################################

##############saveScores method##############################################################
def saveScores(totalSteps, difficulty):
    date = datetime.datetime.now()

    #File written as: "scores 4-30-2019.txt"
    filename = ("scores " + str(date.month) + "-" + str(date.day) + "-" + str(date.year) + ".txt")
    #Try to append to file. If cannot, create file in except portion.
    try:
        scores = open(filename, "a")
    except:
        scores = open(filename, "w")
        scored.write('High Scores')

    #write difficulty and score on separate lines
    scores.write("\n" + difficulty)
    scores.write(" " + str(totalSteps))
    scores.close()

    #read into score_data list
    read_into = open(filename, "r")
    global raw_data
    raw_data = read_into.readlines() #reads file lines into list
    raw_data.pop(0) #removes 'High Scores' line from raw_data list
    read_into.close()
    
##############saveScores method end##########################################################

##############pickDifficulty method##########################################################
def pickDifficulty():
#*************Button Variables***************************************
    easyB_topleft_x = width/2.2
    easyB_topleft_y = height/1.19
    easyB_botright_x = width/1.82
    easyB_botright_y = height/1.32

    mediumB_topleft_x = width/2.33
    mediumB_topleft_y = height/1.55
    mediumB_botright_x = width/1.75
    mediumB_botright_y = height/1.8

    hardB_topleft_x = width/2.2
    hardB_topleft_y = height/2.28
    hardB_botright_x = width/1.82
    hardB_botright_y = height/2.75
#*************Button Variables end***********************************
#*************Drawing Buttons****************************************
    buttonColor = 'light green'

    easyButton = Rectangle(Point(easyB_topleft_x, easyB_topleft_y),
                            Point(easyB_botright_x, easyB_botright_y))
    easyButton.setOutline(buttonColor)
    easyButton.draw(win)

    mediumButton = Rectangle(Point(mediumB_topleft_x, mediumB_topleft_y),
                           Point(mediumB_botright_x, mediumB_botright_y))
    mediumButton.setOutline(buttonColor)
    mediumButton.draw(win)

    hardButton = Rectangle(Point(hardB_topleft_x, hardB_topleft_y),
                           Point(hardB_botright_x, hardB_botright_y))
    hardButton.setOutline(buttonColor)
    hardButton.draw(win)
#*************Drawing Buttons end************************************
#*************Setting Text on Buttons********************************
    textColor = 'light green'
    textStyle = 'bold'

    easyOption = Text(Point(width/2, height*4/5), 'Easy')
    easyOption.setSize(22)
    easyOption.setStyle(textStyle)
    easyOption.setFill(textColor)
    easyOption.draw(win)

    mediumOption = Text(Point(width/2, height*3/5), 'Medium')
    mediumOption.setSize(22)
    mediumOption.setStyle(textStyle)
    mediumOption.setFill(textColor)
    mediumOption.draw(win)

    hardOption = Text(Point(width/2, height*2/5), 'Hard')
    hardOption.setSize(22)
    hardOption.setStyle(textStyle)
    hardOption.setFill(textColor)
    hardOption.draw(win)
#*************Setting Text on StartScreen end*************************
#*************Clicking on Options*************************************
    #reset difficulty flags
    global easy, medium, hard
    easy = False
    medium = False
    hard = False

    while True:
        #grabs mouse coordinates on-click, separates click (x,y) into separate x, y variables
        user_click = win.getMouse()
        uc_x = user_click.getX()
        uc_y = user_click.getY()

#       print(uc_x, uc_y)
#       print(easyB_topleft_x, easyB_botright_x)
#       print(easyB_topleft_y, easyB_botright_y)

        #EASY OPTION
        #if mouse clicks inside Easy button, tick easy flag to True
        if (uc_x >= easyB_topleft_x and uc_x <= easyB_botright_x
            and uc_y <= easyB_topleft_y and uc_y >= easyB_botright_y):
            easy = True
            break #exits while loop w/o condition
        
        #MEDIUM OPTION
        #if mouse clicks inside Medium button, tick medium flag to True
        elif (uc_x >= mediumB_topleft_x and uc_x <= mediumB_botright_x
              and uc_y <= mediumB_topleft_y and uc_y >= mediumB_botright_y):
            medium = True
            break
            
        #HARD OPTION
        #if mouse clicks inside Hard button, tick hard flag to True
        elif (uc_x >= hardB_topleft_x and uc_x <= hardB_botright_x
              and uc_y <= hardB_topleft_y and uc_y >= hardB_botright_y):
            hard = True
            break

    #undraws all things drawn
    easyButton.undraw()
    mediumButton.undraw()
    hardButton.undraw()
    easyOption.undraw()
    mediumOption.undraw()
    hardOption.undraw()
#*************Clicking on Options end*********************************
##############pickDifficulty method end######################################################

##############endScreen method###############################################################

def endScreen():
    win.setBackground('light blue')

    #raw_data holds elements broken up by line from the "scores month-day-year.txt" file
    #for each element in raw_data (each line), split line by ' ' space.
    #append to list inside of dictionary using 1st half of split "Easy","Medium","Hard
    #as key for score_data dictionary. We are appending the int value of the second half
    #of the line --> "Easy 6"
    for data in raw_data:
        temp = []
        temp = data.split() #splits line: "Easy 6" into ['Easy', '6']
        score_data[temp[0]].append(int(temp[1]))

    #calculates the lowest number of steps taken for each level of difficulty
    #if there are no scores, difficulty has not been played. Set to 'N/A'.
    try:
        max_e = min(score_data['Easy'])
    except:
        max_e = 'N/A'
        
    try:
        max_m = min(score_data['Medium'])
    except:
        max_m = 'N/A'
        
    try:
        max_h = min(score_data['Hard'])
    except:
        max_h = 'N/A'

    #text for displaying scores
    header = Text(Point(width/2, height*4/5), "High Scores")
    header.setSize(30)
    header.setFill('black')
    easyMax = Text(Point(width/2, height*3/5), 'Easy: ' + str(max_e) + ' steps')
    easyMax.setSize(25)
    easyMax.setFill('black')
    medMax = Text(Point(width/2, height*2/5), 'Medium: ' + str(max_m) + ' steps')
    medMax.setSize(25)
    medMax.setFill('black')
    hardMax = Text(Point(width/2, height*1/5), 'Hard: ' + str(max_h) + ' steps')
    hardMax.setSize(25)
    hardMax.setFill('black')

    header.draw(win)
    easyMax.draw(win)
    medMax.draw(win)
    hardMax.draw(win)

    prompt = Text(Point(width/2, height/10), "Click anywhere to Continue")
    prompt.setSize(10)
    prompt.draw(win)
    win.getMouse()

    #undraw all elements on screen
    header.undraw()
    easyMax.undraw()
    medMax.undraw()
    hardMax.undraw()
    prompt.undraw()

    prompt = Text(Point(width/2, height/10), "Click to go to the Start Menu")
    prompt.setSize(10)
    prompt.draw(win)
    win.getMouse()
    prompt.undraw()
    
    #tick screen transition flags, end to False, start to True. Brings us to startScreen
    global start, end
    end = False
    start = True
##############endScreen method end###########################################################

#Main loop of progression.
def main():
    win.setBackground('black')

    #while loop for screen transitions. Checks global screen transition flags.
    while True:
        if start:
            startScreen()
        elif game:
            gameScreen()
        elif end:
            endScreen()

main()
