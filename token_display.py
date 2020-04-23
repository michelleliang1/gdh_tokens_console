from psychopy import visual, event, core
from psychopy.hardware import keyboard
import math
import random

#Rooms
room1_img = "Picture2.jpg"
room2_img = "Picture3.jpg"

#Arrows 
leftArrow_img = "leftarrow.png"
rightArrow_img = "rightarrow.png"
grayRightArrow_img = "grayedrightarrow.png" 
grayLeftArrow_img = "grayedleftarrow.png"

#Chart for translating the rating scale to the actual rating data
prob_table=[None]*12
prob_table[0]=-999
prob_table[1]=0.0
prob_table[2]=0.1
prob_table[3]=0.2
prob_table[4]=0.3
prob_table[5]=0.4
prob_table[6]=0.5
prob_table[7]=0.6
prob_table[8]=0.7
prob_table[9]=0.8
prob_table[10]=0.9
prob_table[11]=1.0


def show_instr(win, instruction_slide):
    '''Displays the image of instruction slide'''
    image = visual.ImageStim(win, image=instruction_slide)
    image.draw()
    win.flip()
    event.waitKeys(keyList = ['space'])
   
def show_prompt(win, instruction_slide, waitTime):
    '''Displays the image of prompt slide'''
    image = visual.ImageStim(win, image=instruction_slide)
    image.draw()
    win.flip()
    core.wait(waitTime) 
    
def getString(win, question: str) -> str:
    '''Gets the participant number and condition at the beginning of the task'''
    string = ""
    while True:
        message = visual.TextStim(win, text = question + " " + string, color = "black", units="pix", height=35, wrapWidth=1000)
        message.draw()
        win.flip()
        keyPress = event.waitKeys(keyList = ['0','1','2','3','4','5','6','7','8','9','p','return'])
        if keyPress[0] == 'return':
            return string
        else:
            string = string + keyPress[0]
             
def draw_fixation_cross(win, waitTime:float):
    """Displays the fixation cross for the waiting room"""
    horizontal = visual.Line(win, start=(-20,0), units="pix", end=(20,0), lineColor="black", lineWidth=8)
    vertical = visual.Line(win, start=(0,20), units="pix", end=(0,-20), lineColor="black", lineWidth=8)
    horizontal.draw()
    vertical.draw()
    win.flip()
    core.wait(waitTime) 

def criterion_passed(win, actual: float, colorToken: str, direction: str, room: str, waitTime, assess=False) -> tuple: 
    """Subject must guess the probability of getting a specific token correct within 0.1 of the real probability to move on. 
    Returns a tuple of rated probability, actual probability and correctness.""" 
    labell = ['0.0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']
    label = ['1','2','3','4','5','6','7','8','9','10','11']
    scale = visual.RatingScale(
        win, low=1, high=11, markerStart=6,pos=(0,100),scale=None, tickMarks=label,labels=labell,markerColor="Black",lineColor='Grey',textSize=0.5,textColor='Black',noMouse=True,
        leftKeys='left', rightKeys = 'right', acceptKeys='space',showAccept=False)
    scale.marker.size=(.4,.4)
    scale.reset()
    roomNumber = 0
    if room == "square":
        roomNumber = 1
    elif room == "triangle":
        roomNumber = 2
    while scale.noResponse:
        token = visual.Circle(win, radius = 50, fillColor=colorToken, units='pix', pos=(0,200)) 
        stringBuilder = "What is the probability of receiving the " + colorToken + " token when pressing the " + direction + " arrow in room " + str(roomNumber) + "?"
        instructions = "Use LEFT and RIGHT arrows to scroll, then hit SPACEBAR to select"
        instruction = visual.TextStim(win, text=instructions, color = "black", units="pix", height=25, wrapWidth=1000, pos=(0,-100))
        if room == "square":
            shape = visual.ImageStim(win, image=room1_img, units="pix")
            question = visual.TextStim(win, text=stringBuilder, color = "black", units="pix", height=25, wrapWidth=1500) 
        else:
            shape = visual.ImageStim(win, image=room2_img, units="pix") #size=(850, 775), pos=(0,10))
            question = visual.TextStim(win, text=stringBuilder, color = "black", units="pix", height=25, wrapWidth=1500) #wrapWidth=400, pos=(0,-50))  
        shape.draw() 
        question.draw()
        instruction.draw()
        token.draw()
        scale.draw()
        win.flip() 
        
    if prob_table[scale.getRating()] <= round(actual+0.1, 1) and prob_table[scale.getRating()] >= round(actual-0.1, 1):
        correct = True
        result = visual.TextStim(win, text = "CORRECT", color = "green", units="pix", height=50, wrapWidth=1000, pos=(0,-200)) 
    else:
        correct = False
        result = visual.TextStim(win, text = "INCORRECT", color = "red", units="pix", height=50, wrapWidth=1000, pos=(0,-200))
    shape.draw()
    question.draw()
    instruction.draw()
    if assess == False: 
        result.draw()
    token.draw()
    scale.draw()
    win.flip()
    core.wait(waitTime) 
    draw_fixation_cross(win, waitTime) 
    return (prob_table[scale.getRating()], actual, correct)
    
def learnRewards(win, writer, responseClock, valueDist: list, tokenColors:list, valueMapping: dict, waitTime:float, allTokenValues:list, colorMap:dict):
    RL_results = []
    uniqueValues = list(set(valueDist)) #Gets all the unique values from the value distribution
    #t1 = visual.TextStim(win, text='$'+valueDist[0], color = "black", units="pix", height=25, wrapWidth=550, pos=(-250, 150))
    t2 = visual.TextStim(win, text='$0', color = "black", units="pix", height=25, wrapWidth=550, pos=(-125, 150))
    t3 = visual.TextStim(win, text='$1', color = "black", units="pix", height=25, wrapWidth=550, pos=(0, 150))
    t4 = visual.TextStim(win, text='$3', color = "black", units="pix", height=25, wrapWidth=550, pos=(125, 150))
    #t5 = visual.TextStim(win, text='$'+valueDist[4], color = "black", units="pix", height=25, wrapWidth=550, pos=(250, 150))
    instructions1 = "What is the current value of the token shown below?"
    instructions2 = "Use LEFT and RIGHT arrows to scroll, hit SPACEBAR to select"
    instruction1 = visual.TextStim(win, text=instructions1, color = "black", units="pix", height=25, wrapWidth=1000, pos=(0,250))
    instruction2 = visual.TextStim(win, text=instructions2, color = "black", units="pix", height=25, wrapWidth=1000, pos=(0,20))
    selectionBox = visual.Rect(win, width = 80, height = 80, pos=(-125, 150), lineColor="black", lineWidth=6)
    firstSelections = [False, False, False, False, False]
    while all(firstSelections) == False:
        firstSelections = [False, False, False, False, False] #Reset
        for i, color in enumerate(tokenColors):
            firstSelection = True #This is their first guess at the value of the token
            token = visual.Circle(win, radius = 50, fillColor=color, units='pix', pos=(0,-100))
            circlePositionChange = 0
            correct = False
            while correct == False:
                selectionBox.pos = (selectionBox.pos[0]+circlePositionChange, selectionBox.pos[1])
                #t1.draw()
                t2.draw()
                t3.draw()
                t4.draw()
                #t5.draw()
                instruction1.draw()
                instruction2.draw()
                selectionBox.draw()
                token.draw()
                win.flip()
                circlePositionChange=0
                keyPress = event.waitKeys(keyList = ['left', 'right', 'space'])
                if keyPress[0] == 'right' and selectionBox.pos[0] != 125:
                    circlePositionChange += 125
                elif keyPress[0] == 'left' and selectionBox.pos[0] != -125:
                    circlePositionChange -= 125
                elif keyPress[0] == 'space': #Selected an answer
                    for value in [t2, t3, t4]: #Check if it's the correct answer
                        if selectionBox.pos[0] == value.pos[0]:
                            if '$' + valueMapping[color] == value.text:
                                result = visual.TextStim(win, text = "CORRECT", color = "green", units="pix", height=50, wrapWidth=1000, pos=(0,-250))
                                result.draw()
                                correct = True
                                if firstSelection == True:
                                    firstSelections[i] = True
                                else:
                                    firstSelections[i] = False
                            else:
                                firstSelection = False
                                result = visual.TextStim(win, text = "INCORRECT", color = "red", units="pix", height=50, wrapWidth=1000, pos=(0,-250))
                                result.draw()
                            #t1.draw()
                            t2.draw()
                            t3.draw()
                            t4.draw()
                            #t5.draw()
                            instruction1.draw()
                            instruction2.draw()
                            selectionBox.draw()
                            token.draw()
                            win.flip()
                            writer.writerow([1, value.text[1:], responseClock.getTime(), 0, 0, allTokenValues.index(valueDist)+1, valueMapping[color], colorMap[color], "NaN" , "", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN"])

                            #Save trial to .mat
                            RL_results.append([1, float(value.text[1:]), responseClock.getTime(), 0, 0, allTokenValues.index(valueDist)+1, float(valueMapping[color]), colorMap[color]])

                            core.wait(waitTime) #Wait for 1 second
                            draw_fixation_cross(win, waitTime)
    return RL_results

                                              
def selected_value(win,value:str):
    """Returns the text object of the selected value."""
    return visual.TextStim(win, text=value, color="white", pos=(0,0), height=40, bold=True)
    
def selected_token(win,tokenColor:str):
    """Returns the circle object of the selected token."""
    return visual.Circle(win, radius = 50, fillColor=tokenColor, units='pix', pos=(0,0)) 
    
def draw_learning_room(win, room_img, tokens: list, speed, spinningTime, spinning=False, arrowSelected=None): 
    """Draws the learning room with no values shown and one arrow grayed out."""
    if room_img == "Picture2.jpg":
        message = "Room 1"
    else:
        message = "Room 2"
    roomTitle = visual.TextStim(win, text=message, color="black", units="pix", height=35, wrapWidth=1000, pos=(0,300))
    room = visual.ImageStim(win, image=room_img, units="pix")
    if arrowSelected == "right": #Subject can only select the right arrow first
        right = visual.ImageStim(win, image=rightArrow_img, units="pix", size=(100,100), pos=(200,-250))
        left = visual.ImageStim(win, image=grayLeftArrow_img, units="pix", size=(100,100), pos=(-200,-250))
    elif arrowSelected == "left": #Subject can only select the left arror first 
        right = visual.ImageStim(win, image=grayRightArrow_img, units="pix", size=(100,100), pos=(200,-250))
        left = visual.ImageStim(win, image=leftArrow_img, units="pix", size=(100,100), pos=(-200,-250))
    circle1 = tokens[0]
    circle2 = tokens[1]
    circle3 = tokens[2]
    circle4 = tokens[3]
    circle5 = tokens[4]
    room.draw()
    roomTitle.draw()
    
    if spinning == False:
        right.draw()
        left.draw()
        circle1.draw()
        circle2.draw()
        circle3.draw()
        circle4.draw()
        circle5.draw()
        win.flip()
        if arrowSelected == "right": 
            keyPressed = event.waitKeys(keyList = ['right'])  
        elif arrowSelected == "left":
            keyPressed = event.waitKeys(keyList = ['left']) 
        return keyPressed[0] 
    else:
        spinTime = core.CountdownTimer(spinningTime)
        while spinTime.getTime() > 0:
            for i in range(0, 360, 5):
                spinSpeed = core.CountdownTimer(speed) #Controls the speed at which the circles spin
                while spinSpeed.getTime() > 0:
                    angle1 = i * math.pi / 180
                    circle1.pos = ((50 * math.sin(angle1))*2, (50 * math.cos(angle1))*2)

                    angle2 = (i + 72) * math.pi / 180
                    circle2.pos = ((50 * math.sin(angle2))*2, (50 * math.cos(angle2))*2)

                    angle3 = (i + 144) * math.pi / 180
                    circle3.pos = ((50 * math.sin(angle3))*2, (50 * math.cos(angle3))*2)

                    angle4 = (i + 216) * math.pi / 180
                    circle4.pos = ((50 * math.sin(angle4))*2, (50 * math.cos(angle4))*2)

                    angle5 = (i + 288) * math.pi/ 180
                    circle5.pos = ((50 * math.sin(angle5))*2, (50 * math.cos(angle5))*2)

                    room.draw()
                    roomTitle.draw()

                    if arrowSelected == "right": #Highlights the arrow selected
                        rightBox = visual.Rect(win, width = 130, height = 130, pos=(200,-250), lineColor="black", lineWidth=6)
                        rightBox.draw()
                    else:
                        leftBox = visual.Rect(win, width = 130, height = 130, pos=(-200,-250), lineColor="black", lineWidth=6)
                        leftBox.draw()

                    right.draw()
                    left.draw()
                    circle1.draw()
                    circle2.draw()
                    circle3.draw()
                    circle4.draw()
                    circle5.draw()
                    win.flip()
 
def draw_room(win, room_img, tokens: list, values: list, speed, spinningTime, responseTime, loss, spinning=False, arrowPressed=None) -> str:
    """Draws the square when tokens are not spinning and when its spinning."""
    lossAmt = loss
    if room_img == "Picture2.jpg":
        message = "Room 1"
    else:
        message = "Room 2"
    roomTitle = visual.TextStim(win, text=message, color="black", units="pix", height=35, wrapWidth=1000, pos=(0,300))
    room = visual.ImageStim(win, image=room_img, units="pix")
    right = visual.ImageStim(win, image=rightArrow_img, units="pix", size=(100,100), pos=(200,-250))
    left = visual.ImageStim(win, image=leftArrow_img, units="pix", size=(100,100), pos=(-200,-250))
    #lossBox = visual.Rect(win, width = 130, height = 130, pos=(400,300), lineColor="black", lineWidth=6)
    lossValue = visual.TextStim(win, text="$"+str(round(lossAmt, 2)), color="black", units="pix", height=35, wrapWidth=1000, pos=(400,300))

    value1 = values[0]
    value2 = values[1]
    value3 = values[2]
    value4 = values[3]
    value5 = values[4]
    circle1 = tokens[0]
    circle2 = tokens[1]
    circle3 = tokens[2]
    circle4 = tokens[3]
    circle5 = tokens[4]

    kb = keyboard.Keyboard()

    if spinning == False:
        kb.clearEvents()
        timer = core.StaticPeriod()
        while True:
            lossValue = visual.TextStim(win, text="$" + str(round(lossAmt, 2)), color="black", units="pix", height=35,
                                        wrapWidth=1000, pos=(400, 300))
            room.draw()
            roomTitle.draw()
            #lossBox.draw()
            lossValue.draw()
            right.draw()
            left.draw()
            circle1.draw()
            circle2.draw()
            circle3.draw()
            circle4.draw()
            circle5.draw()
            win.flip()
            keyPressed = kb.getKeys(keyList=['left', 'right'], clear=True)

            #keyPressed = event.getKeys(keyList=['left', 'right'])
            timer.start(0.5)
            if len(keyPressed) == 1:
                print(type(keyPressed[0].name))
                break
            else:
                lossAmt -= 0.01
                timer.complete()

        return [keyPressed[0].name, lossAmt] #key that was pressed, cents that was lost
    else:
        spinTime = core.CountdownTimer(spinningTime)
        while spinTime.getTime() > 0:
            for i in range(0, 360, 5):
                spinSpeed = core.CountdownTimer(speed) #Controls the speed at which the circles spin
                while spinSpeed.getTime() > 0:
                    angle1 = i * math.pi / 180
                    circle1.pos = ((50 * math.sin(angle1))*2, (50 * math.cos(angle1))*2)
                    value1.pos = ((50 * math.sin(angle1))*2, (50 * math.cos(angle1))*2)

                    angle2 = (i + 72) * math.pi / 180
                    circle2.pos = ((50 * math.sin(angle2))*2, (50 * math.cos(angle2))*2)
                    value2.pos = ((50 * math.sin(angle2))*2, (50 * math.cos(angle2))*2)

                    angle3 = (i + 144) * math.pi / 180
                    circle3.pos = ((50 * math.sin(angle3))*2, (50 * math.cos(angle3))*2)
                    value3.pos = ((50 * math.sin(angle3))*2, (50 * math.cos(angle3))*2)

                    angle4 = (i + 216) * math.pi / 180
                    circle4.pos = ((50 * math.sin(angle4))*2, (50 * math.cos(angle4))*2)
                    value4.pos = ((50 * math.sin(angle4))*2, (50 * math.cos(angle4))*2)

                    angle5 = (i + 288) * math.pi / 180
                    circle5.pos = ((50 * math.sin(angle5))*2, (50 * math.cos(angle5))*2)
                    value5.pos = ((50 * math.sin(angle5))*2, (50 * math.cos(angle5))*2)

                    room.draw()
                    roomTitle.draw()
                    #lossBox.draw()
                    lossValue.draw()

                    if arrowPressed == "right":
                        rightBox = visual.Rect(win, width = 130, height = 130, pos=(200,-250), lineColor="black", lineWidth=6)
                        rightBox.draw()
                    else:
                        leftBox = visual.Rect(win, width = 130, height = 130, pos=(-200,-250), lineColor="black", lineWidth=6)
                        leftBox.draw()

                    right.draw()
                    left.draw()
                    circle1.draw()
                    circle2.draw()
                    circle3.draw()
                    circle4.draw()
                    circle5.draw()
                    win.flip()

def draw_token(win, room_img, arrowPressed, selectedTokenColor, selectedValue, waitTime, learning=False):
    """Draws the selected token in the middle of the window with the selected value"""
    if room_img == "Picture2.jpg":
        message = "Room 1"
    else:
        message = "Room 2"
    roomTitle = visual.TextStim(win, text=message, color="black", units="pix", height=35, wrapWidth=1000, pos=(0,300))
    room = visual.ImageStim(win, image=room_img, units="pix")
    room.draw()
    roomTitle.draw()
    if arrowPressed == "right":
        rightBox = visual.Rect(win, width = 130, height = 130, pos=(200,-250), lineColor="black", lineWidth=6)
        right = visual.ImageStim(win, image=rightArrow_img, units="pix", size=(100,100), pos=(200,-250))
        rightBox.draw()
        right.draw()
    else:
        leftBox = visual.Rect(win, width = 130, height = 130, pos=(-200,-250), lineColor="black", lineWidth=6)
        left = visual.ImageStim(win, image=leftArrow_img, units="pix", size=(100,100), pos=(-200,-250))
        leftBox.draw()
        left.draw()
    if learning == True and arrowPressed == "right":
        grayLeft = visual.ImageStim(win, image=grayLeftArrow_img, units="pix", size=(100,100), pos=(-200,-250))
        grayLeft.draw()
    elif learning == True and arrowPressed == "left":
        grayRight = visual.ImageStim(win, image=grayRightArrow_img, units="pix", size=(100,100), pos=(200,-250))
        grayRight.draw()
    elif learning == False and arrowPressed == "right":
        left = visual.ImageStim(win, image=leftArrow_img, units="pix", size=(100,100), pos=(-200,-250))
        left.draw()
    elif learning == False and arrowPressed == "left":
        right = visual.ImageStim(win, image=rightArrow_img, units="pix", size=(100,100), pos=(200,-250))
        right.draw()
            
    selected_token(win, selectedTokenColor).draw()
        
    win.flip()
    core.wait(waitTime)


def draw_room_description(win, room, arrow, instrWaitTime):
    if room == "square" and arrow == "left":
        message = "Left Arrow in Room 1"
    elif room == "square" and arrow == "right":
        message = "Right Arrow in Room 1"
    elif room == "triangle" and arrow == "left":
        message = "Left Arrow in Room 2"
    elif room == "triangle" and arrow == "right":
        message = "Right Arrow in Room 2"

    roomPrompt = visual.TextStim(win, text=message, color="black", units="pix", height=35, wrapWidth=1000, pos=(0,0))

    roomPrompt.draw()
    win.flip()
    core.wait(instrWaitTime)



