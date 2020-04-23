import token_display
import random
import csv, os, time

def small_sample_token_list(tokens: list, probabilities: dict, keyPress:str, divergence: str): #If the probability dist change, this needs to change
    """Returns the tokenList that you should be getting in the learning phase, not dependent on random() because small sample doesn't show probability well"""
    tokenList = [] #Draw from this to determine the token 
    for i, probability in enumerate(probabilities[divergence][keyPress]): 
        multiples = int(probability*10) #How many times the circle should be repeated
        tokenList.extend([tokens[i] for _ in range(multiples)]) #Add to the tokenList the number of multiples
    return tokenList 
    
def determine_learning_token(tokenList: list):
    """Updates the tokenList with one already removed and returns the chosen token color"""
    chosen = random.choice(tokenList)
    tokenList.remove(chosen)
    return chosen.fillColor

def determine_token(tokens: list, probabilities: dict, keyPress: str, divergence: str):
    """Returns the color of the token that was chosen"""
    weights = probabilities[divergence][keyPress]
    return random.choices(tokens, weights)[0].fillColor
  
def randomize_tokens(tokens:list, colors:list):
    """Randomizes the color order of the tokens"""
    random.shuffle(colors) 
    order = tokens
    for i, color in enumerate(colors): 
        order[i].fillColor = color 
    return order 
    
def randomize_values(values:list):
    """Randomizes the order of value distributions for tokens"""
    order = values.copy()  
    random.shuffle(order)
    print("Order: ", order) 
    return order 
    
def randomize_divergence():
    """Randomizes the order of divergence"""
    order = ["HD", "LD"]
    random.shuffle(order)
    return order
    
def randomize_rooms(rooms):
    """Randomizes the order of rooms"""
    order = rooms
    random.shuffle(order)
    return order
    
def room_divergence_mapping(roomOrder:list, divergenceOrder: list) -> dict:
    """Returns a dictionary mapping the room and divergence, {"square": "HD"}, "triangle":"LD"}"""
    map = dict()
    for i, room in enumerate(roomOrder): 
        map[room] = divergenceOrder[i]
    return map
    
def token_value_mapping(tokenColorOrder: list, values: list) -> dict: 
    """Returns a dictionary mapping the token colors to the values"""
    map = dict()
    for i, token in enumerate(tokenColorOrder):
        map[token.fillColor] = values[i]
    return map
    
def get_token_color_order(tokens:list):
    """Takes a list of token objects and returns a list of the fillColors in order"""
    colors = []
    for token in tokens: 
        colors.append(token.fillColor) 
    return colors 
   
def randomize_16_questions(tokenColorOrder:list, rooms:list):
    """Returns a shuffled list of 16 tuples that is the room, direction and token of the question"""
    groups = []
    for room in rooms: 
        for direction in ["left", "right"]:
            for token in tokenColorOrder: 
                groups.append((room, direction, token))
    random.shuffle(groups)
    return groups

def color_prob_mapping(tokenColorOrder:list):
    """Returns a dict mapping the color of the token and the index of the probability it is associated with."""
    cpMapping = dict()
    for i, color in enumerate(tokenColorOrder):
        cpMapping[color] = i 
    return cpMapping
    
def openDataFile(subject=0):
    """Open a csv data file for output with a filename that nicely uses the current date and time"""
    directory= "data"
    if not os.path.isdir(directory):
        os.mkdir(directory)
    try:
        filename="{}/subject{}_{}.csv".format(directory, subject,time.strftime('%m%d%Y'))
        # , time.strftime('%Y-%m-%dT%H:%M:%S') if want to append date and time of file, to avoid overwriting data
        datafile = open(filename, 'w',newline='')
    except Exception as e:
        filename="{}/subject{}_{}.csv".format(directory, subject, subject,time.strftime('%m%d%Y')) #for MS Windows
        datafile = open(filename, 'w',newline='')
    return datafile




