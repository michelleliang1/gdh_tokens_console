from psychopy import visual,event,core
import csv, os
import random
import token_data
import token_display
import scipy.io as sio 
from datetime import datetime 
import math

allRooms = ["square", "triangle"]
#pattern1 is named square 
#pattern2 is named triangle

#Rooms
room1_img = "Picture2.jpg" #horizontal lines 
room2_img = "Picture3.jpg" #squiggly lines 

probabilities = {"HD": {"left": (0.7, 0.1, 0.2, 0, 0), "right": (0.1, 0.7, 0, 0.2, 0)}, #probabilities are 1 to 1 with the order of the token
                "LD" : {"left": (0, 0.1, 0.2, 0, 0.7), "right": (0, 0.1, 0, 0.2, 0.7)}}

#Value Distributions
tv1 = ["3", "0", "1", "1", "3"]
tv2 = ["0", "3", "1", "1", "3"]
tv3 = ["1", "1", "0", "3", "0"]
allTokenValues = [tv1, tv2, tv3]
   
waitTime = .50 #for fixation cross, outcome screens
responseTime = 1
spinningTime = .75 #time the tokens are spinning
speed = 0.000005 #spin speed
responseClock = core.Clock()
instrWaitTime = .75

win = visual.Window([1000,800], fullscr = True, color="white", units='pix') #Change back to True
event.globalKeys.add(key='escape', func=core.quit, name='shutdown')
win.mouseVisible = False
squareKeyPresses = []
triangleKeyPresses = []

#Instruction Slides 
i1 = "i1.jpg"
i2 = "i2.jpg"
i3 = "i3.jpg"
i4 = "i4.jpg"
i5 = "i5.jpg"
i6 = "i6.jpg"

#Tokens
tokenColors = ["red", "blue", "orange", "green", "purple"]
t1 = visual.Circle(win, radius = 50, fillColor=tokenColors[0], units='pix', pos=(-8.71557427, 99.61946981)) #Extracted from the draw_token function, print out the positions
t2 = visual.Circle(win, radius = 50, fillColor=tokenColors[1], units='pix', pos=(92.05048535, 39.07311285))
t3 = visual.Circle(win, radius = 50, fillColor=tokenColors[2], units='pix', pos=(65.6059029, -75.47095802))
t4 = visual.Circle(win, radius = 50, fillColor=tokenColors[3], units='pix', pos=(-51.50380749, -85.71673007))
t5 = visual.Circle(win, radius = 50, fillColor=tokenColors[4], units='pix', pos=(-97.43700648, 22.49510543))
allTokens = [t1, t2, t3, t4, t5] #location of allTokens is fixed

#Values 
randomDists = token_data.randomize_values(allTokenValues) #Returns a randomized order of value distributions,
values = randomDists[0]  #Take the first value dist and do a learning probability training phase
print("Values: ", values) 
value1 = visual.TextStim(win, text=values[0], pos=(-8.71557427, 99.61946981), color="white", height=30, bold=True)
value2 = visual.TextStim(win, text=values[1], pos=(92.05048535, 39.07311285), color="white", height=30, bold=True)
value3 = visual.TextStim(win, text=values[2], pos=(65.6059029, -75.47095802), color="white", height=30, bold=True)
value4 = visual.TextStim(win, text=values[3], pos=(-51.50380749, -85.71673007), color="white", height=30, bold=True)
value5 = visual.TextStim(win, text=values[4], pos=(-97.43700648, 22.49510543), color="white", height=30, bold=True) 
allValues = [value1, value2, value3, value4, value5]

#Subject Specific 
tokenOrder = token_data.randomize_tokens(allTokens, tokenColors) #If you want the token color positions to be randomized, need to change locations of it, these are token objects.
tokenColorsList= token_data.get_token_color_order(tokenOrder) 
print("Token Colors List: ", tokenColorsList) 

roomOrder = token_data.randomize_rooms(allRooms) #square first then triangle or vice versa
valueMapping = token_data.token_value_mapping(allTokens, values) #{color:value}
print("Value Mapping: ", valueMapping)
roomMapping = token_data.room_divergence_mapping(roomOrder, token_data.randomize_divergence()) #square is HD and triangle is LD or vice versas
print("Room Mapping: ", roomMapping) 
participantNumber = token_display.getString(win, "Please enter a participant number:")

#Data file SetUp
file = token_data.openDataFile(participantNumber) #creates a new file with the participant number
writer = csv.writer(file, delimiter=",") #connects to a writer
RL_resultArray = []
PL_resultArray = []

colorMap = {"purple": 1, "blue": 2, "red":3, "orange": 4, "green":5}

token_display.show_instr(win, i1)
token_display.show_instr(win, i2)
writer.writerow(["Phase", "Choice(arrow or amount)", "Response Time", "Divergence", "Room", "rewardDist", "tokenValue", "tokenColor", "loss", "", "room", "tokenColor", "arrow", "ratedProbability", "trueProbability", "responseTime"])


#Phase 1 - Learning Probabilities Phase 

learningRoomOrder = token_data.randomize_rooms(allRooms) 


for room in learningRoomOrder:
    arrowOrder = ["left", "right"]
    for direction in arrowOrder:
        if room == "square":
            tokenList = token_data.small_sample_token_list(tokenOrder, probabilities, direction, roomMapping["square"])
            token_display.draw_room_description(win, room, direction, instrWaitTime)
            for i in range(10): #CHANGE BACK TO 10
                token_display.draw_learning_room(win, room1_img, tokenOrder, speed, spinningTime, False, direction)
                selectedTokenColor = token_data.determine_learning_token(tokenList)
                token_display.draw_learning_room(win, room1_img, tokenOrder, speed, spinningTime, True, direction)
                token_display.draw_token(win, room1_img, direction, selectedTokenColor, None, waitTime, True)
                token_display.draw_fixation_cross(win, waitTime)
                writer.writerow([0, 1 if direction == 'left' else 2, responseClock.getTime(), 1 if roomMapping[room] == "HD" else 2, 1 if room == "square" else 2, 0, 0, colorMap[selectedTokenColor], "NaN", "", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN"])

                #Save.mat data for the trial
                RL_resultArray.append([0, 1 if direction == 'left' else 2, responseClock.getTime(), 1 if roomMapping[room] == "HD" else 2, 1 if room == "square" else 2, 0, 0, colorMap[selectedTokenColor]])


        else:
            tokenList = token_data.small_sample_token_list(tokenOrder, probabilities, direction, roomMapping["triangle"])
            token_display.draw_room_description(win, room, direction, instrWaitTime)
            for i in range(10): #CHANGE BACK TO 10
                token_display.draw_learning_room(win, room2_img,tokenOrder, speed, spinningTime, False, direction)
                selectedTokenColor = token_data.determine_learning_token(tokenList)
                token_display.draw_learning_room(win, room2_img, tokenOrder, speed, spinningTime, True, direction)
                token_display.draw_token(win, room2_img, direction, selectedTokenColor, None, waitTime, True)
                token_display.draw_fixation_cross(win, waitTime)
                writer.writerow([0, 1 if direction == 'left' else 2, responseClock.getTime(), 1 if roomMapping[room] == "HD" else 2, 1 if room == "square" else 2, 0, 0, colorMap[selectedTokenColor], "NaN", "", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN"])

                #Save.mat data for the trial
                RL_resultArray.append([0, 1 if direction == 'left' else 2, responseClock.getTime(), 1 if roomMapping[room] == "HD" else 2, 1 if room == "square" else 2, 0, 0, colorMap[selectedTokenColor]])


#Phase 2 - Learning Rewards and Gambling Phase
token_display.show_instr(win, i3)

for distribution in randomDists:
    token_display.show_instr(win, i5)
    valueMappings = token_data.token_value_mapping(allTokens, distribution) 
    print("ValueMappings", valueMappings) 
    results = token_display.learnRewards(win, writer, responseClock, distribution, tokenColors, valueMappings, waitTime, allTokenValues, colorMap)
    RL_resultArray.extend(results) #Add the data from the learning reward phase


    roomOrdering = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2]
    random.shuffle(roomOrdering) 
    for room in roomOrdering:
        loss = 0
        if room == 1:
           response = token_display.draw_room(win, room1_img, tokenOrder, allValues, speed, spinningTime, responseTime, loss, False, None)
           squareKeyPresses.append(response[0])
           loss = response[1]

           selectedTokenColor = token_data.determine_token(tokenOrder, probabilities, response[0], roomMapping["square"])
           selectedValue = token_display.selected_value(win, valueMapping[selectedTokenColor])
           token_display.draw_room(win, room1_img, tokenOrder, allValues, speed, spinningTime, responseTime, loss, True, response[0])
           token_display.draw_token(win, room1_img, response[0], selectedTokenColor, selectedValue, waitTime)
           token_display.draw_fixation_cross(win, waitTime)
           if response[0] != None:
                writer.writerow([2, 1 if response[0] == 'left' else 2, responseClock.getTime(), 1 if roomMapping["square"] == "HD" else 2, room, allTokenValues.index(distribution)+1, selectedValue.text, colorMap[selectedTokenColor], loss, "", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN"])
                   
                #Save.mat data for the trial
                RL_resultArray.append([2, 1 if response[0] == 'left' else 2, responseClock.getTime(), 1 if roomMapping["square"] == "HD" else 2, room, allTokenValues.index(distribution)+1, float(selectedValue.text), colorMap[selectedTokenColor], loss])
        
        elif room == 2:
           response = token_display.draw_room(win, room2_img, tokenOrder, allValues, speed, spinningTime, responseTime, loss, False, None)
           triangleKeyPresses.append(response[0])
           loss = response[1]

           selectedTokenColor = token_data.determine_token(tokenOrder, probabilities, response[0], roomMapping["triangle"])
           selectedValue = token_display.selected_value(win, valueMapping[selectedTokenColor])
           token_display.draw_room(win, room2_img, tokenOrder, allValues, speed, spinningTime, responseTime, loss, True, response[0])
           token_display.draw_token(win, room2_img, response[0], selectedTokenColor, selectedValue, waitTime)
           token_display.draw_fixation_cross(win, waitTime) 
           if response[0] != None:
                writer.writerow([2, 1 if response[0] == 'left' else 2, responseClock.getTime(), 1 if roomMapping["triangle"] == "HD" else 2, room, allTokenValues.index(distribution)+1, selectedValue.text, colorMap[selectedTokenColor], loss, "", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN"])
                
                #Save.mat data for the trial
                RL_resultArray.append([2, 1 if response[0] == 'left' else 2, responseClock.getTime(), 1 if roomMapping["triangle"] == "HD" else 2, room, allTokenValues.index(distribution)+1, float(selectedValue.text), colorMap[selectedTokenColor], loss])

#Probability Learning Assessment

token_display.show_instr(win, i4)

questions = token_data.randomize_16_questions(tokenColorsList, learningRoomOrder) #20 questions 
index = token_data.color_prob_mapping(tokenColorsList)
for question in questions:
    room, direction, color = question
    result = token_display.criterion_passed(win, probabilities[roomMapping[room]][direction][index[color]], color, direction, room, waitTime, assess=True)
    writer.writerow(["NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN" , "", 1 if room == "square" else 2, colorMap[color], 1 if direction == 'left' else 2, result[0], result[1], responseClock.getTime()])
    
    #Save .mat data for the trial
    PL_resultArray.append([1 if room == "square" else 2, colorMap[color], 1 if direction == 'left' else 2, result[0], result[1], responseClock.getTime()])

# Get ending timestamp for experiment session
endTimestamp = datetime.now()
subjectTimestamp = endTimestamp.strftime('%m%d%Y-%H%M%S')

# Format subject data filename
subjectDataFilename = 'S' + str(participantNumber).zfill(3) + '_' + subjectTimestamp + '.mat'

# Format subject data and save it as a MATLAB MAT data file
sio.savemat(os.path.join('data', subjectDataFilename), {
    'RewardLearning'    : RL_resultArray,
    'ProbLearning'    : PL_resultArray} )


token_display.show_instr(win, i6)


#Data Look Up
#Phases
#0 = Probability Learning
#1 = Reward Learning
#2 = Gambling

#Room
#0 = on reward learning trials
#1 = Horizontal lines
#2 = Squiggly lines

#Divergence
#0 = on reward learning trials
#1 = HD
#2 = LD

#tokenColors
#1 = Purple
#2 = Blue
#3 = Red
#4 = Orange
#5 = Green

#Arrow
#1 = left
#2 = right
