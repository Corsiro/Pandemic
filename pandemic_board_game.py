#pandemic
#things to work on: use list, sets or dict?; setup classes, separate into different files, etc...
#player_hands and other variables not updating correctly?
#importing modules used
import math
import random

#setup - global variables and arrays
num_players = 0 #number of players, changeable
current_player = 0 #keeps track of player turns, resets to zero to keep track of which player's turn it is
num_epidemic = 0 #sets number of epidemics in the deck, currently only 4 and 6 is set up to work, i think...
epi_deck = range(0) #empty epidemic deck to be set up
ob_counter = 0 #outbreak counter - game loss at 8
player_deck = range(48) #player deck without special cards, just location cards
player_discard = range(0) #discard pile for the player deck
player_hands = range(0, num_players) #keeps tracks of all player hands, position corresponds to player
inf_rate_list = [2, 2, 2, 3, 3, 4, 4, 4] #infection rate list that determines how many infection cards to draw
inf_rate_count = 0 #inf rate counter to track position in rate list
inf_rate = int(inf_rate_list[inf_rate_count]) #current infection rate
inf_deck = range(48) #infection deck
inf_discard =  range(0) #infection deck discard
city_board = range(48) #board setup, location with neighbors, color, number of cubes of each color, rsearch station and if it has outbroken in a given turn
disease_state = [[25, False, False],[25, False, False],[25, False, False],[25, False, False]] #disease state - num cubes left, cured, eradicated
players = range(0) #player info array
player_roles = ["dispatcher", "medic", "scientist", "researcher", "operations manager", "role", "role", "role", "role", "role", "role", "role"] #player roles/roles still available
city_num = None
city_list = range(48)
city_color = None
win_condition_met = None
neighbors = range(0)

#all setup functions in a start up, runs all necessary start up functions
def setup():
    global current_player
    current_player = 0
    board_setup()
    city_list_setup()
    player_setup()
    epidemic_setup()
    player_deck_setup()
    inf_setup()
    player_turn(current_player)
    return 
    
#player setup, sets up each player with location, role, and number of actions. (role 11 reserved for generalist for now)
def player_setup():
    #global variables/arrays used
    global num_players
    global player_roles
    global players
    while num_players not in [2, 3, 4]:
        num_players = int(input('how many players (2 - 4): '))
    i = 0
    #this while loop sets an array of players up with location in array corresponding to player number
    #each player has the attributes, location (as a number), role, and number of actions
    #role is randomly assigned from the roles list, and the role is then taken out
    #if statement separates out generalist who gets 5 actions rather than 4
    while i < num_players: 
        rand_role = random.randrange(0, 5)
        if rand_role == 11:
            player = [0, player_roles[rand_role], 5, i, False] #location, role, actions
            player_roles.pop(rand_role)
            players.append(player)
            i += 1
        else:
            player = [0, player_roles[rand_role], 4, i, False] #location, role, actions
            player_roles.pop(rand_role)
            players.append(player)
            i += 1
    return player_roles, players, num_players

#city board setup, fills the board array with info array of each city              
def board_setup():
    #each one is an array
    #[name, colour, research station, already outbroke this turn
    #y_cubes, b_cubes, u_cubes, r_cubes, (connecting cities 1 away)]  
    city = range(0)
    global city_board
    #iterates through all 48 cities and fills them to a set location in the city_board, for example, city_board[0] will always be Atlanta
    i = 0
    while i < 48:
        city_board[i] = range(0)
        if i == 0:
            city = ["Atlanta", "blue", True, False, 0, 0, 0, 0, 4, 2, 14]
            city_board[i] = city
            i += 1
        elif i == 1:
            city = ["San Francisco", "blue", False, False, 0, 0, 0, 0, 44, 40, 2, 12]
            city_board[i] = city
            i += 1	
        elif i == 2:
            city = ["Chicago", "blue", False, False, 0, 0, 0, 0, 1, 12, 13, 0, 3]
            city_board[i] = city
            i += 1
        elif i == 3:
            city = ["Montreal", "blue", False, False, 0, 0, 0, 0, 2, 4, 5]
            city_board[i] = city
            i += 1
        elif i == 4:
            city = ["Washington", "blue", False, False, 0, 0, 0, 0, 14, 0, 3, 5]
            city_board[i] = city
            i += 1
        elif i == 5:
            city = ["New York", "blue", False, False, 0, 0, 0, 0, 3, 4, 7, 6]
            city_board[i] = city
            i += 1
        elif i == 6:
            city = ["London", "blue", False, False, 0, 0, 0, 0, 5, 7, 8, 9]
            city_board[i] = city
            i += 1
        elif i == 7:
            city = ["Madrid", "blue", False, False, 0, 0, 0, 0, 5, 19, 24, 8, 6]
            city_board[i] = city
            i += 1
        elif i == 8:
            city = ["Paris", "blue", False, False, 0, 0, 0, 0, 6, 7, 9, 10, 24]
            city_board[i] = city
            i += 1
        elif i == 9:
            city = ["Essen", "blue", False, False, 0, 0, 0, 0, 6, 8, 10, 11]
            city_board[i] = city
            i += 1
        elif i == 10:
            city = ["Milan", "blue", False, False, 0, 0, 0, 0, 25, 9, 8]
            city_board[i] = city
            i += 1
        elif i == 11:
            city = ["St. Petersburg", "blue", False, False, 0, 0, 0, 0, 27, 25, 9]
            city_board[i] = city
            i += 1
        elif i == 12:
            city = ["Los Angeles", "yellow", False, False, 0, 0, 0, 0, 39, 1, 2, 13]
            city_board[i] = city
            i += 1
        elif i == 13:
            city = ["Mexico City", "yellow", False, False, 0, 0, 0, 0, 12, 2, 14, 15, 16]
            city_board[i] = city
            i += 1
        elif i == 14:
            city = ["Miami", "yellow", False, False, 0, 0, 0, 0, 13, 0, 4, 15]
            city_board[i] = city
            i += 1
        elif i == 15:
            city = ["Bogota", "yellow", False, False, 0, 0, 0, 0, 13, 14, 16, 19, 18]
            city_board[i] = city
            i += 1
        elif i == 16:
            city = ["Lima", "yellow", False, False, 0, 0, 0, 0, 13, 15, 17]
            city_board[i] = city
            i += 1
        elif i == 17:
            city = ["Santiago", "yellow", False, False, 0, 0, 0, 0, 16]
            city_board[i] = city
            i += 1
        elif i == 18:
            city = ["Buenos Aires", "yellow", False, False, 0, 0, 0, 0, 15, 19]
            city_board[i] = city
            i += 1
        elif i == 19:
            city = ["Sao Paulo", "yellow", False, False, 0, 0, 0, 0, 15, 18, 7, 20]
            city_board[i] = city
            i += 1
        elif i == 20:
            city = ["Lagos", "yellow", False, False, 0, 0, 0, 0, 19, 22, 21]
            city_board[i] = city
            i += 1
        elif i == 21:
            city = ["Khartoum", "yellow", False, False, 0, 0, 0, 0, 26, 20, 22, 23]
            city_board[i] = city
            i += 1
        elif i == 22:
            city = ["Kinshasa", "yellow", False, False, 0, 0, 0, 0, 20, 21, 23]
            city_board[i] = city
            i += 1
        elif i == 23:
            city = ["Johannesburg", "yellow", False, False, 0, 0, 0, 0, 21, 22]
            city_board[i] = city
            i += 1
        elif i == 24:
            city = ["Algiers", "black", False, False, 0, 0, 0, 0, 7, 8, 25, 26]
            city_board[i] = city
            i += 1
        elif i == 25:
            city = ["Istanbul", "black", False, False, 0, 0, 0, 0, 24, 26, 10, 11, 27, 29]
            city_board[i] = city
            i += 1
        elif i == 26:
            city = ["Cairo", "black", False, False, 0, 0, 0, 0, 24, 25, 29, 21, 30]
            city_board[i] = city
            i += 1
        elif i == 27:
            city = ["Moscow", "black", False, False, 0, 0, 0, 0, 11, 25, 28]
            city_board[i] = city
            i += 1
        elif i == 28:
            city = ["Tehran", "black", False, False, 0, 0, 0, 0, 27, 29, 31, 32]
            city_board[i] = city
            i += 1
        elif i == 29:
            city = ["Baghdad", "black", False, False, 0, 0, 0, 0, 25, 26, 30, 31, 28]
            city_board[i] = city
            i += 1
        elif i == 30:
            city = ["Riyadh", "black", False, False, 0, 0, 0, 0, 26, 29, 31]
            city_board[i] = city
            i += 1
        elif i == 31:
            city = ["Karachi", "black", False, False, 0, 0, 0, 0, 28, 29, 30, 33, 32]
            city_board[i] = city
            i += 1
        elif i == 32:
            city = ["Delhi", "black", False, False, 0, 0, 0, 0, 28, 31, 33, 34, 35]
            city_board[i] = city
            i += 1
        elif i == 33:
            city = ["Mumbai", "black", False, False, 0, 0, 0, 0, 31, 32, 34]
            city_board[i] = city
            i += 1
        elif i == 34:
            city = ["Chennai", "black", False, False, 0, 0, 0, 0, 33, 32, 35, 36, 37]
            city_board[i] = city
            i += 1
        elif i == 35:
            city = ["Kolkata", "black", False, False, 0, 0, 0, 0, 32, 34, 36, 41]
            city_board[i] = city
            i += 1
        elif i == 36:
            city = ["Bangkok", "red", False, False, 0, 0, 0, 0, 41, 35, 34, 37, 38]
            city_board[i] = city
            i += 1
        elif i == 37:
            city = ["Jakarta", "red", False, False, 0, 0, 0, 0, 39, 38, 36, 34]
            city_board[i] = city
            i += 1
        elif i == 38:
            city = ["Ho Chi Minh City", "red", False, False, 0, 0, 0, 0, 40, 41, 36, 37]
            city_board[i] = city
            i += 1
        elif i == 39:
            city = ["Sydney", "red", False, False, 0, 0, 0, 0, 12, 40, 37]
            city_board[i] = city
            i += 1
        elif i == 40:
            city = ["Manila", "red", False, False, 0, 0, 0, 0, 39, 41, 1, 42, 38]
            city_board[i] = city
            i += 1
        elif i == 41:
            city = ["Hong Kong", "red", False, False, 0, 0, 0, 0, 47, 42, 40, 38, 36, 35]
            city_board[i] = city
            i += 1
        elif i == 42:
            city = ["Taipei", "red", False, False, 0, 0, 0, 0, 43, 47, 41, 40]
            city_board[i] = city
            i += 1
        elif i == 43:
            city = ["Osaka", "red", False, False, 0, 0, 0, 0, 44, 42]
            city_board[i] = city
            i += 1
        elif i == 44:
            city = ["Tokyo", "red", False, False, 0, 0, 0, 0, 1, 45, 47, 43]
            city_board[i] = city
            i += 1
        elif i == 45:
            city = ["Seoul", "red", False, False, 0, 0, 0, 0, 44, 47, 46]
            city_board[i] = city
            i += 1
        elif i == 46:
            city = ["Beijing", "red", False, False, 0, 0, 0, 0, 47, 45]
            city_board[i] = city
            i += 1
        elif i == 47:
            city = ["Shanghai", "red", False, False, 0, 0, 0, 0, 46, 45, 44, 41, 42]
            city_board[i] = city
            i += 1
        else:
            pass
    return city_board
    
#sets number of epidemics based on preset number
def epidemic_setup():
    global num_epidemic
    global epi_deck
    num_epidemic = None
    while num_epidemic not in [4,5,6]:
        num_epidemic = int(input('how many epidemics (4, 5, or 6): '))
    while num_epidemic > 0:
        epi_deck.append(100)
        num_epidemic += -1
    return epi_deck, num_epidemic
                 
#player deck and hand setup
def player_deck_setup():
    #global variables/arrays
    global player_deck
    global player_hands
    global num_players
    #special_deck_cards puts 2 cards per player into the player deck 
    special_deck_total = range(48,65)
    random.shuffle(special_deck_total)
    print special_deck_total
    special_prep = range(0)
    while len(special_prep) < (num_players * 2):
        special_prep.append(special_deck_total[0])
        special_deck_total.pop(0)
        return special_prep
    print special_prep
    print special_deck_total
    player_deck.extend(special_prep)
    #shuffles deck 7 times
    i = 7 
    while i > 0:
        random.shuffle(player_deck)
        i += -1
    #draws players hands according to number of players set, and appends them to the corresponding player slot
    i = num_players
    while i > 0:
        player_hands[i-1] = range(0)
        if num_players == 3:
            player_hands[i-1].append(player_deck[0])
            player_deck.pop(0)
            player_hand[i-1].append(player_deck[0])
            player_deck.pop(0)
            player_hand[i-1].append(player_deck[0])
            player_deck.pop(0)
        elif num_players == 4:
            player_hands[i-1].append(player_deck[0])
            player_deck.pop(0)
            player_hands[i-1].append(player_deck[0])
            player_deck.pop(0)
        else:
            player_hands[i-1].append(player_deck[0])
            player_deck.pop(0)
            player_hands[i-1].append(player_deck[0])
            player_deck.pop(0)            
            player_hands[i-1].append(player_deck[0])
            player_deck.pop(0)
            player_hands[i-1].append(player_deck[0])
            player_deck.pop(0)
        i += -1
    #initiates player deck shuffle that places epidemics in more regular spacing than a random shuffle
    player_deck_shuffle()
    return player_deck, player_hands

#implement dividing player deck into num_epidemic piles, 
#add epidemic, shuffle and recombine
def player_deck_shuffle():
    #global elements
    global epi_deck
    global player_deck
    #creates an array of x number of piles of cards from the player deck based on number of epidemics chosen
    #this so far only works with even numbers as far as i can tell, need to fix / think about more
    pile = range(0,len(epi_deck))
    #while there are still cards in the epidemic deck, add a epidemic deck, and put a pile of cards into the corresponding slot 
    while len(epi_deck) > 0:
        pile[len(epi_deck)-1] = range(0)
        pile[len(epi_deck)-1].append(epi_deck[0])
        #this determines pile size
        a = len(player_deck) / len(epi_deck)
        while a > 0:
            pile[len(epi_deck)-1].append(player_deck[0])
            player_deck.pop(0)
            a += -1
        #shuffle each pile separately
        i = 7
        while i > 0:
            random.shuffle(pile[len(epi_deck)-1])
            i += -1
        epi_deck.pop()    
    #put the piles into the deck, stacking them on top of each other
    while len(pile) > 0:
        player_deck.extend(pile[len(pile)-1])
        pile.pop()
    return player_deck


#infect +1 to a city, with the given color        
def inf_1(number, color):
    global city_board
    global disease_state    
    city_inc = range(0)
    city_inc = city_board[number]
    inf_color = None
    #find out color of infection
    if color == "yellow":
        inf_color = 0
    elif color == "black":
        inf_color = 1
    elif color == "blue":
        inf_color = 2
    elif color == "red":
        inf_color = 3
    else:
        print "invalid color choice"
        pass
    #find out info about current disease color
    current_disease_state = range(0)
    current_disease_state = disease_state[inf_color]
    #if it is not eradicated and there are still cubes left, add a cube, and subtract one from the cube stock; if there are three cubes already on run outbreak
    if current_disease_state[2] == False and current_disease_state[0] > 0:
        if city_inc[inf_color] == 3:
            outbreak(number)
        else:
            city_inc[inf_color+4] += 1
            current_disease_state[0] += -1
            city_board[number] = city_inc
            disease_state[inf_color] = current_disease_state
    #if there are 0 cubes in the stock, Game over
    elif current_disease_state[0] <= 0:
        print "Game Over - You ran out of " + color + "cubes! You lose."
    #if it has been eradicated, the card is still drawn, but nothing else happens, 
    else:
        pass
    return city_board, disease_state

#Outbreak             
def outbreak(number):
    global ob_counter
    global city_board
    city_check = range(0)
    ob_counter += 1
    if ob_counter == 8:
        print "GAME OVER! The earth is beyond help. Outbreak is at " + str(ob_counter) + "." 
    else:
        i = 0
        city_inf = range(0)
        city_inf = city_board[number]
        city_inf[3] = True
        city_board[number] = city_inf
        while i+8 < len(city_board[number]):
            inf_1(city_inf[i+8], city_inf[1])
            i += 1
    return ob_counter, city_board

#initial setup - inf deck
#top three cards, infect city with 3 cube, 
#then 2 cubes for the next 3 cards 
#and 1 cube for the 3 after
#keeps track of changes in infection deck and discard pile
def inf_setup():
    global inf_deck
    global inf_discard
    global city_board
    current_city = range(0)
    i = 7
    while i > 0:
        random.shuffle(inf_deck)
        i += -1
    i = 0
    while i < 3:
        current_city = city_board[inf_deck[0]]
        inf_1(inf_deck[0], current_city[1])
        inf_1(inf_deck[0], current_city[1])
        inf_1(inf_deck[0], current_city[1])
        inf_discard.append(inf_deck[0])
        inf_deck.pop(0)
        i += 1
    while i > 2 and i < 6:
        inf_1(inf_deck[0], current_city[1])
        inf_1(inf_deck[0], current_city[1])
        inf_discard.append(inf_deck[0])
        inf_deck.pop(0)
        i += 1
    while i > 5 and i < 9:
        inf_1(inf_deck[0], current_city[1])
        inf_discard.append(inf_deck[0])
        inf_deck.pop(0)
        i += 1
    return inf_deck, inf_discard
    
#epidemic
#takes bottom card - add 3 to city, card to discard
#shuffle discard pile, replace on top of inf deck
def epidemic():
    global inf_deck
    global inf_discard
    global inf_rate_count
    global inf_rate_list
    global city_board
    current_city = range(0)
    #reverses the deck to take the bottom card
    inf_deck.reverse()
    current_city = city_board[inf_deck[0]]
    inf_1(inf_deck[0], current_city[1])
    inf_1(inf_deck[0], current_city[1])
    inf_1(inf_deck[0], current_city[1])
    inf_discard.append(inf_deck[0])
    inf_deck.pop(0)
    #shuffle the discard pile
    i = 7
    while i > 0:
        random.shuffle(inf_discard)
        i += -1
    #add the discard pile to the bottom of the deck
    inf_deck.extend(inf_discard)
    #reverse the deck so that the cards added from the discard pile are on top
    inf_deck.reverse()
    #clear the discard pile
    i = len(inf_discard)
    while i > 0:
        inf_discard.pop()
        i = len(inf_discard)
    #increase the rate count/infection rate
    inf_rate_count += 1
    inf_rate = inf_rate_list[inf_rate_count]
    return inf_rate_count, inf_rate, inf_deck, inf_discard

#things that happen at the end of a player's turn
def end_of_turn():
    global current_player
    global player_hands
    global player_deck
    global player_discard
    global city_board
    global players
    global win_condition_met
    check_win_condition_met()
    if win_condition_met == False:
        check_player_loc()
        check_eradication()
        current_hand = range(0)
        print current_player
        print player_hands
        current_hand = player_hands[current_player]
        player = range(0)
        player = players[current_player]
        player[2] = 4
        i = 0
        while i < 2:
            if len(player_deck) > 0:
                current_hand.append(player_deck[0])
                player_discard.append(player_deck[0])
                player_deck.pop(0)           
                i += 1
            else:
                print "Game Over - Player deck is empty! You lose."
        while 100 in current_hand:
            current_hand.remove(100)
            epidemic()
        while len(current_hand) > 7:
            dicard()
        inf_phase()
        if current_player == num_players - 1:
            current_player = 0
        else:
            current_player += 1
        i = 0
        while i < 48:
            current_city = city_board[i]
            current_city[3] = False
            i += 1
    else:
        print "Congratulations! All diseases are cured!"
    player_turn(current_player)
    return current_player, city_board, players

def check_eradication():	
    global disease_state
    i = 0
    while i < 4:
        state = disease_state[i]
        if state[0] == 25:
            state[2] = True
        else:
            pass
        disease_state[i] = state
        i += 1
    return disease_state
    
def check_win_condition_met():
    global disease_state
    global win_condition_met
    i = 0
    while i < 4:
        state = disease_state[i]
        win_condition_met = True
        win_condition_met = win_condition_met and state[1]
        i += 1
    return win_condition_met

    
#how to discard a card, not finished, just placeholder code    
def discard():
    global player_hands
    global current_player
    global player_discard
    current_hand = range(0)
    current_hand = player_hands[current_player]
    city = None
    city_num = None
    while city_num not in current_hand:
        city = str(input('which card would you like to discard (enter name): '))
        city_num = city2num(city)
    player_discard.append(current_player[city_num])
    current_hand.remove(city_num)
    player_hands[current_player] = current_hand
    return player_hands, player_discard

#what happens during the infection phase at the end of turn
def inf_phase():
    global inf_rate
    global inf_deck
    global inf_discard
    i = inf_rate
    while i != 0:
        inf_1(inf_deck[0], city_board[inf_deck[0]])
        inf_discard.append(inf_deck[0])
        inf_deck.pop(0)
        i += -1
    return inf_deck, inf_discard
    
#player actions below
def check_player_loc():
    global players
    global city_board
    global disease_state
    global num_players
    j = 0
    while j < num_players:
        player = range(0)
        player = players[j]
        if player[1] == "medic":
            i = 0
            while i < 4:
                state = range(0)
                state = disease_state[i]
                if state[1] == True:
                    city = range(0)
                    city = city_board[player[0]]
                    cubes = city[i+4]
                    city[i+4] = 0
                    state[0] += cubes
                    disease_state[i] = state
                    city_board[player[0]] = city
                i += 1
        j += 1
    return city_board, players, disease_state

#neighbors of the city
def check_neighbors(city_num):
    global neighbors
    global city_board
    neighbors = range(0)
    city = range(0)
    city = city_board[city_num]
    #take out the first 8 elements
    i = 8
    while i < len(city):
        neighbors.append(city[i])
        i += 1
    print neighbors
    return neighbors, city_board

def ferry():
    global players
    global current_player
    global city_board
    global disease_state
    global city_list
    global neighbors
    dest_city = None
    while dest_city not in city_list:
        dest_city = str(input('Which city would you like to go to (enter name): '))
    #dest_city needs to be converted to a number
    dest_city_num = city2num(dest_city)
    #is the destination a neighbor of the current city?
    player = players[current_player]
    #if yes move there
    check_neighbors(dest_city_num)
    if player[0] in neighbors and dest_city_num != player[0]:
        #-1 action
        player[2] -= 1
        player[0] = dest_city_num
        players[current_player] = player
        check_player_loc()
    else:
        print "not a valid move"
    neighbors = range(0)
    return players, neighbors
    
def charter():
    global players
    global current_player
    global player_hands
    global city_board
    global player_discard
    global city_list
    dest_city = None
    while dest_city not in city_list:
        dest_city = str(input('Which city would you like to go to (enter name): '))
    #does the player have the card with the current city in hand? 
    player = players[current_player]
    player_hand = player_hands[current_player]
    #convert city to number
    dest_city_num = city2num(dest_city)
    current_city_num = player[0]
    if current_city_num in player_hand:
    #if yes, discard the card and go to destination
    #-1 action
        player[2] -= 1
        player[0] = dest_city_num
        player_discard.append(dest_city_num)
        player_hand.remove(dest_city_num)
        players[current_player] = player
        player_hands = player_hand
        check_player_loc()
    else:
        print "not a valid move"
    return players, player_hands, player_discard
    
def direct():
    #does the player have the card with the destination city in hand? 
    global players
    global current_player
    global player_hands
    global city_board
    global player_discard
    global city_list
    dest_city = None
    while dest_city not in city_list:
        dest_city = str(input('Which city would you like to go to (enter name): '))
    player = players[current_player]
    player_hand = player_hands[current_player]
    #convert city to number
    dest_city_num = city2num(dest_city)
    if dest_city_num in player_hand:
    #if yes, discard the card and go to destination
    #-1 action
        player[2] -= 1
        player[0] = dest_city_num
        player_discard.append(dest_city_num)
        player_hand.remove(dest_city_num)
        players[current_player] = player
        player_hands = player_hand
        check_player_loc()
    else:
        print "not a valid move"
    return players, player_hands, player_discard
    
def shuttle():
    global players
    global current_player
    global city_board
    global city_list
    player = players[current_player]
    while dest_city not in city_list:
        dest_city = str(input('Which city would you like to go to (enter name): '))
    #convert city to number
    dest_city_num = city2num(dest_city)
    current_city_num = player[0]
    destination = range(0)
    current_city = range(0)
    destination = city_board(dest_city_num)
    current_city = city_board(current_city_num)
    #does the current city have a research station?
    #does the city you are going to have a research station?
    if  destination[2] == True and current_city[2] == True:
    #if yes to both go to destination
    #-1 action
        player[2] -= 1
        player[0] = dest_city_num
        players[current_player] = player
        check_player_loc()
    else:
        print "not a valid move"
    return players
        
def build():
    global current_player
    global players
    global current_player
    global city_board
    global research_stations
    global player_hands
    global player_discard
    global city_list
    build_city = None
    while build_city not in city_list:
        build_city = str(input('Which city would you like to build a research station (enter name): '))
    #convert city to number
    build_city_num = city2num(build_city)
    build_city = city_board[build_city_num]
    player = range(0)
    player = players[current_player]
    player_hand = player_hands[current_player]
    current_city = city_board[player[0]]
    #is the current player in the city, are there available research stations?
    if player[0] == build_city_num and research_stations != 0: 
        #is there a research station in the current city?
        if build_city[2] == False:
            #is the player the operations manager
            if player[1] == "operations manager":
                #take 1 from station stock
                research_stations -= 1
                #subtract an action
                player[2] -= 1
                build_city[2] = True
                city_board[build_city_num] = build_city
                players[current_player] = player				
            elif build_city_num in player_hand:
                research_stations -= 1
                player[2] -= 1
                build_city[2] = True
                #remove the city from player hand
                player_discard.append(build_city_num)
                player_hand.remove(build_city_num)
                player_hands[current_player] = player_hand
                city_board[build_city_num] = build_city
                players[current_player] = player				
            else:
                print "not a valid move"
        else:
            print "research station already here"
    elif player[0] == build_city_num and research_stations == 0:
        if build_city[2] == False:
            if player[1] == "operations manager":
                #ask for city 
                remove_city = None
                while remove_city not in city_list:
                    remove_city = str(input('Which city would you like to remove a research station from (enter name): '))
                city_num_remove = city2num(remove_city)
                if city_to_remove[2] == True:
                    city_to_remove = range(0)
                    city_to_remove = city_board[city_num_remove]
                    player[2] -= 1
                    #remove research station from city_to_remove, and add to current city
                    city_to_remove[2] = False
                    build_city[2] = True
                    city_board[city_num_remove] = city_to_remove
                    city_board[build_city_num] = build_city
                    players[current_player] = player
                else:
                    print "this city has no research station to remove."
            elif current_city_num in player_hand:
                if city_to_remove[2] == True:	
                    #ask for city
                    remove_city = None
                    while remove_city not in city_list:
                        remove_city = str(input('Which city would you like to remove a research station from (enter name): '))
                    city_num_remove = city2num(remove_city)
                    city_to_remove = range(0)
                    city_to_remove = city_board[city_num_remove]
                    player[2] -= 1
                    city_to_remove[2] = False
                    build_city[2] = True
                    city_board[city_num_remove] = city_to_remove
                    city_board[build_city_num] = build_city
                    player_discard.append(build_city_num)
                    player_hand.remove(build_city_num)
                    player_hands[current_player] = player_hand
                    players[current_player] = player		
                else:
                    print "this city has no research station to remove."			
            else:
                print "not a valid move"
        else:
            print "research station already here"
    else:
        print "not a valid move"
    return player_hands, city_board, players, player_discard
        
def treat_1():
    global disease_state
    global city_board
    global players
    global current_player
    global city_list
    player = range(0)
    player = players[current_player]
    color_list = ["yellow", "black", "blue", "red"]
    treat_color = None
    city = None
    while city not in city_list or treat_color not in color_list:
        city = str(input('which city would you like to treat: '))
        treat_color = str(input('what color of cube are you treating(yellow, black, blue, red): '))
    trt_color = None
    #is the color cured? 
    if treat_color == "yellow":
        trt_color = 0
    elif treat_color == "black":
        trt_color = 1
    elif treat_color == "blue":
        trt_color = 2
    elif treat_color == "red":
        trt_color = 3
    else:
        print "invalid color choice"
    #convert city to number
    city_num = city2num(city)
    cubes = None
    disease_color_state = range(0)
    disease_color_state = disease_state[trt_color]
    current_city = range(0)
    current_city = city_board[city_num]
    if city_num == player[0]:
        #cured or medic? yes, remove all cubes of that color from the city
        if disease_color_state[0] == True or player[1] == "medic" and current_city[trt_color+4] != 0:
            cubes = current_city[trt_color+4]
            current_city[trt_color+4] = 0
            disease_color_state[0] += cubes
            city_board[city_num] = current_city
            #-1 action	
            player[2] -= 1
            players[current_player] = player
            disease_state[trt_color] = disease_color_state
        #if not, take a cube of the color from the city
        elif current_city[trt_color+4] != 0:
            current_city[trt_color+4] -= 1
            city_board[city_num] = current_city
            disease_color_state[0] += 1
            #-1 action	
            player[2] -= 1
            players[current_player] = player
            disease_state[trt_color] = disease_color_state
        else:
            print "no cubes of that color on this city"
    else:
        print "not in chosen location"
    return players, city_board, disease_state
    
def give_card():
    global players
    global city_board
    global player_hands
    global city_list
    global current_player
    city = None
    to_player = None
    while to_player < 0 or to_player > num_players or city not in city_list or from_player == current_player:
        city = str(input('Which card are you giving (name of city card): '))
        to_player = int(input('Who are you giving to (0-3): '))
    player = range(0)
    player2 = range(0)
    player = players[current_player]
    player2 = players[to_player]
    hand = player_hands[current_player]
    hand2 = player_hands[to_player]
    #are you in the same city as the other player?
    if player[0] == player2[0]:
        #are you the researcher?
        #if yes, give the chosen card to the given player if it is not a special card, and remove from hand
        if player[1] == "researcher":
            city_num = city2num(city)
            if city_num in hand:
                hand2.append(city_num)
                hand.remove(city_num)
                player_hands[current_player] = hand
                player_hands[to_player] = hand2
                #-1 action	
                player[2] -= 1
                players[current_player] = player
            else:
                print "card not in hand"
        else:
            city_num = city2num(city)
            #does the card you are giving correspond to the city you are both in?
            #if yes, give the card, and remove from hand
            if city_num == player[0]:
                if city_num in hand:
                    hand2.append(city_num)
                    hand.remove(city_num)
                    player_hands[current_player] = hand
                    player_hands[to_player] = hand2
                    #-1 action
                    player[2] -= 1
                    players[current_player] = player
                else:
                    print "card not in hand."
            else:
                print "you do not have the card of this location."
    else:
        print "you are not in the same spot as player chosen."
    return player_hands
        
def take_card():
    global players
    global city_board
    global player_hands
    global city_list
    global current_player
    city = None
    from_player = None
    while from_player < 0 or from_player > num_players or city not in city_list or from_player == current_player:
        city = str(input('Which card are you giving (name of city card): '))
        from_player = int(input('Who are you giving to (0-3): '))
    player = range(0)
    player2 = range(0)
    player = players[current_player]
    player2 = players[from_player]
    hand = player_hands[current_player]
    hand2 = player_hands[from_player]
    #are you in the same city as the other player?
    if player[0] == player2[0]:
        #is player2 the researcher?
        #if yes, give the chosen card to the given player if it is not a special card, and remove from hand
        if player2[1] == 2:	#researcher?
            city_num = city2num(city)
            if city_num in hand2:
                hand.append(city_num)
                hand2.remove(city_num)
                player_hands[current_player] = hand
                player_hands[from_player] = hand2
                #-1 action	
                player[2] -= 1
                players[current_player] = player
            else:
                print "card is not in the other player's hand"
        else:
            city_num = city2num(city)
            #does the card you are taking correspond to the city you are both in?
            #if yes, take the card, and remove from hand
            if city_num == player2[0]:
                if city_num in hand:
                    hand.append(city_num)
                    hand2.remove(city_num)
                    player_hands[current_player] = hand
                    player_hands[from_player] = hand2
                    #-1 action
                    player[2] -= 1
                    players[current_player] = player
                else:
                    print "card is not in the other player's hand."
            else:
                print "the other player does not have the card of this location."
    else:
        print "you are not in the same spot as player chosen."
    return player_hands
    
def find_cure():
    global current_player
    global players
    global city_board
    global player_hands
    global disease_state
    cure_color = None
    cure_color_num = None
    cured = None
    while cure_color not in color_list or cured == True:
        cure_color = str(input('Which color would you like to cure(yellow, black, blue, red): '))
        if cure_color == "yellow":
            cure_color_num = 0
        elif treat_color == "black":
            cure_color_num = 1
        elif treat_color == "blue":
            cure_color_num = 2
        elif treat_color == "red":
            cure_color_num = 3
        else:
            print "invalid color"
        color_check_cured = range(0)
        color_check_cured = disease_state[cure_color_num]
        cured = color_check_cured[1]
    player = range(0)
    player = players[current_player]
    city_str = player[0]
    city_num = city2num(city_str)
    city = range(0)
    city = city_board[city_num]
    if city[2] == True: #at research station?
        hand = player_hands[current_player]
        if player[1] == "scientist":
            card1 = None
            card2 = None
            card3 = None
            card4 = None
            while card1 not in hand or card2 not in hand or card3 not in hand or card4 not in hand:
                #ask player to choose 4 cards
                card1 = str(input('Select a card to discard (city name): '))
                card2 = str(input('Select a card to discard (city name): '))
                card3 = str(input('Select a card to discard (city name): '))
                card4 = str(input('Select a card to discard (city name): '))
            card1_num = city2num(card1)
            card2_num = city2num(card2)
            card3_num = city2num(card3)
            card4_num = city2num(card4)
            card1_color = city_num2color(card1_num)
            card2_color = city_num2color(card2_num)
            card3_color = city_num2color(card3_num)
            card4_color = city_num2color(card4_num)
            same_color = [card1_color, card2_color, card3_color, card4_color]
            i = 0
            while i < 4:
                same_color_check = same_color_check and same_color[i] == cure_color
                i += 1
            if same_color_check == True:
                state = range(0)
                state = disease_state[cure_color_num]
                state[1] = True
                player_discard.extend(card1_num, card2_num, card3_num, card4_num)
                hand.remove(card1_num)
                hand.remove(card2_num)
                hand.remove(card3_num)
                hand.remove(card4_num)
                player[2] -= 1
                players[current_player] = player
                disease_state[cure_color_num] = state
                player_hands[current_player] = hand
            elif same_color_check == False:
                print "cards not the same colors"
        else:
            while card1 not in hand or card2 not in hand or card3 not in hand or card4 not in hand or card5 not in hand:
                #ask player to choose 5 cards
                card1 = str(input('Select a card to discard (city name): '))
                card2 = str(input('Select a card to discard (city name): '))
                card3 = str(input('Select a card to discard (city name): '))
                card4 = str(input('Select a card to discard (city name): '))
                card5 = str(input('Select a card to discard (city name): '))
            card1_num = city2num(card1)
            card2_num = city2num(card2)
            card3_num = city2num(card3)
            card4_num = city2num(card4)
            card5_num = city2num(card5)
            card1_color = city_num2color(card1_num)
            card2_color = city_num2color(card2_num)
            card3_color = city_num2color(card3_num)
            card4_color = city_num2color(card4_num)
            card5_color = city_num2color(card5_num)
            same_color = [card1_color, card2_color, card3_color, card4_color, card5_color]
            i = 0
            while i < 5:
                same_color_check = same_color_check and same_color[i] == cure_color
                i += 1
            if same_color_check == True:
                state = range(0)
                state = disease_state[cure_color_num]
                state[1] = True
                player_discard.extend(card1_num, card2_num, card3_num, card4_num, card5_num)
                hand.remove(card1_num)
                hand.remove(card2_num)
                hand.remove(card3_num)
                hand.remove(card4_num)
                hand.remove(card5_num)
                player[2] -= 1
                players[current_player] = player			
                disease_state[cure_color_num] = state
                player_hands[current_player] = hand
            elif same_color_check == False:
                print "cards not the same colors"
            else:
                print "cards not in hand"
    else:
        print "invalid action: not currently at a research station."
    check_player_loc()
    return players, player_hands, disease_state, player_discard
        
def move():
    global players
    global city_board
    global current_player
    global num_players
    global city_list
    global player_hands
    global player_discard
    dest_city = None
    move_player = None
    while dest_city not in city_list or move_player < 0 or move_player > num_players - 1:
        move_player = int(input('who would you like to move (0-3): '))
        dest_city = str(input('where are they going (city name): '))
    dest_city_info = range(0)
    player = range(0)
    moving_player = range(0)
    dest_city_num = city2num(dest_city)
    dest_city_info = city_board[dest_city_num]
    player = players[current_player]
    moving_player = players[move_player]
    current_player_city = city_board[player[0]]
    moving_player_city = city_board[moving_player[0]]
    #are you moving yourself?
    i = 0
    player_locs = range(0)
    while i < num_players:
        test_player = range(0)
        test_player = player[i]
        player_locs[i] = city_list[test_player[0]]
        i += 1
    if move_player == current_player:
        #are you the operations manager and have you done this action this turn already?
        #if yes and no, discard a card to go to any city, and current city has a research station,
        if player[1] == "operations manager" and player[4] == False and current_player_city[3] == True:
            player[0] = dest_city_num
            player[2] -= 1
            player[4] = True
            players[current_player] = player
            if dest_player_city[3] == False:
                discard()
            else:
                pass
        elif player[1] == "dispatcher":
            if dest_city in player_locs and dest_city != player[0]:
                moving_player[0] = dest_city_num
                player[2] -= 1
                players[current_player] = player
            else:
                print "invalid move"
        else: 
            print "invalid move"
    else:
        if player[1] == "dispatcher":
            dispatcher_hand = range(0)
            dispatcher_hand = player_hands[current_player]
            if dest_city in player_locs and dest_city != moving_player[0]:
                moving_player[0] = dest_city_num
                player[2] -= 1
                players[current_player] = player
                players[move_player] = moving_player
                check_player_loc()
            elif dest_city in moving_player and dest_city != moving_player[0]:
                moving_player[0] = dest_city_num
                player[2] -= 1
                players[current_player] = player
                players[move_player] = moving_player
                check_player_loc()
            elif moving_player_city[2] == True and dest_city_info[2] == True:
                moving_player[0] = dest_city_num
                player[2] -= 1
                players[current_player] = player
                players[move_player] = moving_player
                check_player_loc()
            elif dest_city in moving_player == False and dest_city != moving_player[0]:
                if dest_city_num in dispatcher_hand or moving_player_city[0] in dispatcher_hand:
                    moving_player[0] = dest_city_num
                    player[2] -= 1
                    players[current_player] = player
                    players[move_player] = moving_player
                    check_player_loc()
                    discard()
                else:
                    print "invalid option, you have neither the destination nor the starting location card."
            else: 
                print "invalid move option"
        else:
            print "you cannot do this"
    return player_discard, players, player_hands

#start a player's turn	
def player_turn(curr_player):
    global players
    global current_player
    current_player = curr_player
    player = players[current_player]
    action = None
    action_list = ["ferry", "direct", "charter", "shuttle", "give", "take", "cure", "treat", "build"]
    while player[2] > 0:
        while action not in action_list:
            #ask for input for action.
            action = str(input('what would you like to do (ferry, direct, charter, shuttle, give, take, cure, treat, build): '))
        if action_list.index(action) == 0:
            ferry()
            action = None
        elif action_list.index(action) == 1:
            direct()
            action = None
        elif action_list.index(action) == 2:
            charter()
            action = None
        elif action_list.index(action) == 3:
            shuttle()
            action = None
        elif action_list.index(action) == 4:
            give_card()
            action = None
        elif action_list.index(action) == 5:
            take_card()
            action = None
        elif action_list.index(action) == 6:
            find_cure()
            action = None
        elif action_list.index(action) == 7:
            treat_1()
            action = None
        else:
            build()
        players[current_player] = player
        print player[2]
    else: 
        end_of_turn()
    return players, current_player
    
def city_list_setup():
    global city_list
    global city_board
    i = 0
    while i < 48:
        city = range(0)
        city = city_board[i]
        city_list[i] = city[0]
        i += 1
    return city_list
    
def city2num(city):
    global city_list
    global city_num
    city_num = city_list.index(city)
    return city_num
    
def city_num2color(city_num):
    global city_color
    if city_num < 12:
        city_color = "yellow"
    elif city_num < 24:
        city_color = "black"
    elif city_num < 36:
        city_color = "blue"
    elif city_num < 48:
        city_color = "red"
    else:
        print "not a valid city"
    return city_color

setup()

## Test revision control in GitHub, Jing edit