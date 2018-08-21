'''
By pressing 'Deal' buttone --> 
-deal random No of hands(2-10)
-evaluate who won(can be more than 1)
-print in the middle winning players and winning combination
'''

from tkinter import *
import random
import os # works with filesystem
import tempfile # works with temp directory

# setting up the current working folder for unpacked picks, when compiled to .exe
for direct in os.listdir(tempfile.gettempdir()):
    if '_MEI' in direct:
        os.chdir(tempfile.gettempdir() + '\u005C' + direct)

# define globals for cards
SUITS = ('c', 's', 'h', 'd')
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')

# define globals for length size of the cards & coordinates of starting draw point
A = 100
B = 145
START_POINT = [80, 80]

# define globals for player's seats number:
SEATS_NUMBERS = [[START_POINT[0] + 3.26 * A, START_POINT[1] + 2.6 * B + 2.96 * A + 30],
                 [START_POINT[0] + 6.01 * A, START_POINT[1] + 2.6 * B + 2.96 * A + 30],
                 [START_POINT[0] + 8.66 * A, START_POINT[1] + 2.6 * B + 2.96 * A + 30],
                 [START_POINT[0] + 11.96 * A + 30, START_POINT[1] + 2.7 * A + 1.2 * B],
                 [START_POINT[0] + 11.96 * A + 30, START_POINT[1] + 1.7 * A + .4 * B],
                 [START_POINT[0] + 8.66 * A, START_POINT[1] - 30],
                 [START_POINT[0] + 6.01 * A, START_POINT[1] - 30],
                 [START_POINT[0] + 3.26 * A, START_POINT[1] - 30],
                 [START_POINT[0] - 30, START_POINT[1] + 1.7 * A + .4 * B],
                 [START_POINT[0] - 30, START_POINT[1] + 2.7 * A + 1.2 * B]]

# define classes
class Card:
    '''
    Card with rank and suit and images(small and big), can be drawn
    '''
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
        self.image_board = PhotoImage(file= os.getcwd() + '\pics_board\u005C' + rank + suit + ".png")
        self.image_hand = PhotoImage(file= os.getcwd() + '\pics_hand\u005C' + rank + suit + ".png")

    def __str__(self):
        return self.rank + self.suit

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, size = True): #size default board picture(bigger), if need small change to False
        if size:
            which_image = self.image_board
        else:
            which_image = self.image_hand
        canvas.create_image(pos[0], pos[1], image = which_image, anchor=NW)
        #canvas.create_image(pos[0], pos[1], image = self.image_board, anchor=NW)

class Table:
    '''
    Table representation. board + players(max 10)
    each player has hand from 2 cards(objects Card class)
    makes show down and checks who won, gives back No of player and winning hand
    reseting the table, dealing cards
    '''
    def __init__(self):
        # create a Table object
        self.board = [] #board from 5 cards
        # dictionary with key(No of player) and value(players hand from 2 cards(objects Card class))
        self.players = {}
        self.deck = []
        self.reset_table()
        self.combinations = {1:'High Card', 2:'Pair', 3:'2 Pairs', 4:'3 of a Kind', 5:'Straight',
                             6:'Flush', 7:'Full House', 8:'4 of a Kind', 9:'Sraight Flush'}

    def __str__(self):
        """
        Return human readable table
        """
        board_string = ""
        for idx in range(5):
            board_string += str(self.board[idx]) + " "

        players_string = ""
        for key, value in self.players.items():
            players_string += ("  player No " + str(key) + ": " + str(value[0]) + str(value[1]) + "\n")

        return ("    POKER TABLE:" + "\n" +
                "BOARD: "+ board_string + "\n" +
                "      PLAYERS: " + "\n" + players_string + "\n")

    def reset_table(self):
        self.deck = []
        for rank in RANKS:
            for suit in SUITS:
                self.deck.append(Card(rank, suit))
        self.board = []
        self.players = {}

    def deal_card(self):
        # deal a card object from the deck
        if len(self.deck) > 0:
            return self.deck.pop(random.randrange(0, len(self.deck)))

    def deal_everything(self, list_of_players):
        self.reset_table()
        for idx in range(5):
            self.board.append(self.deal_card())
        for player in list_of_players:
            self.players[player] = (self.deal_card(), self.deal_card())

        # ---test case(draw)---
        # self.board.append(Card('5','s'))
        # self.board.append(Card('6', 'h'))
        # self.board.append(Card('8', 'h'))
        # self.board.append(Card('9', 's'))
        # self.board.append(Card('7', 'h'))
        # self.players[7] = (Card('2', 's'), Card('3', 'd'))
        # self.players[8] = (Card('2', 'h'), Card('3', 's'))

    def who_won(self):
        winners_score_card = (0, 0, 0, 0, 0, 0, 0)
        winners_combo = []
        winners_list = []

        for key, value in self.players.items():
            seven_cards_list = []
            seven_cards_list.append(value[0])
            seven_cards_list.append(value[1])
            seven_cards_list = seven_cards_list + self.board

            for idx in range(len(best_combo_out_of_7(seven_cards_list)[0])):
                if best_combo_out_of_7(seven_cards_list)[0][idx] < winners_score_card[idx]:
                    break
                if best_combo_out_of_7(seven_cards_list)[0][idx] > winners_score_card[idx]:
                    winners_score_card = best_combo_out_of_7(seven_cards_list)[0]
                    winners_combo = best_combo_out_of_7(seven_cards_list)[1]
                    winners_list = [key]
                    break
                if idx == len(best_combo_out_of_7(seven_cards_list)[0]) - 1:
                    winners_list.append(key)

        return (winners_list, self.combinations[winners_score_card[0]], winners_combo)

    def draw(self, canvas, pos):
        #draw board
        gap = 0
        for idx in range(len(self.board)):
            if idx >= 3:
                gap += 0.1 * A
            coord = [pos[0] + 3.18 * A + A * 1.1 * idx + gap, pos[1] + 1.48 * A + 0.8 * B]
            print(coord)
            self.board[idx].draw(canvas, coord)


        #draw hands of players[1,2,3 & 6,7,8]
        for kdx in range(2):
            gap = 0
            for ydx in range(6, 9):
                for zdx in range(2):
                    coord = [pos[0] + 2.41 * A + (0.9 * A * zdx) + gap, pos[1] + (2.96 * A + 1.8 * B) * kdx]
                    if ydx == 6 and kdx == 0:
                        adj = 2
                    elif ydx == 8 and kdx == 0:
                        adj = -2
                    if (ydx - kdx * 5 + adj) in self.players:
                        self.players[ydx - kdx * 5 + adj][zdx].draw(canvas, coord, False)
                    adj = 0
                gap += 2.7 * A

        # draw hands of players[5,4 & 9,10]
        for kdx in range(2):
            gap = 0
            list_of_2players = [9 - 4 * kdx, 10 - 6 * kdx]
            for ydx in list_of_2players:
                for zdx in range(2):
                    coord = [pos[0] + ((10.26 * A) * kdx + (0.9 * A * zdx)) , pos[1] + 1.71 * A + gap]
                    if (ydx) in self.players:
                        self.players[ydx][zdx].draw(canvas, coord, False)
                gap += A + 0.8 * B

        # draw numbers of the players
        for idx in range(10):
            canv.create_text(SEATS_NUMBERS[idx][0], SEATS_NUMBERS[idx][1], text=(idx+1),
                             font="Verdana 14", anchor=CENTER, justify=CENTER, tag="group2del")

        #draw winner
        canv.create_text(660, 560, text=('Player(s) No ' + str(self.who_won()[0]) + ' won' + '\n' + str(self.who_won()[1])),
                         font="Verdana 12", anchor=CENTER, justify=CENTER, tag="group2del")

# define functions
def check_combination(list_of_5_cards):
    '''
    checking for best combination from 5 cards
    5 cards come as a list of objects(class Card)
     returns tuple(b, a1, (a2), kicker1, ...)
     b=number of best combination // Straight-Flush=9, 4of-a-kind=8, Full-House=7, Flush=6,
                                    Straight=5, 3of-a-kind=4, 2pairs=3, pair=2, high-card=1//
     a1=how high is combination /a2 in full house a1.a1.a1.a2.a2, in 2pairs a1.a1.a2.a2/
    '''

    value_list = [] #utility list
    for card in list_of_5_cards:
        value_list.append(RANKS.index(card.get_rank()))
    value_list.sort(reverse=True) #list with sorted(max-min) values of ranks of cards ('A' - 12 / '2' - 0)

    # checking for straight and for flush
    is_straight = True
    is_flush = True
    from_5 = False #straight starting from 'A'
    for idx in range(4):
        if list_of_5_cards[idx].get_suit() != list_of_5_cards[idx + 1].get_suit():
            is_flush = False
        if (value_list[idx] - value_list[idx + 1]) != 1:
            is_straight = False
    if value_list == [12, 3, 2, 1, 0]: #[A,2,3,4,5]
        is_straight = True
        from_5 = True

    # checking for straight-flush
    if is_flush and is_straight:
        return(9, value_list[0])

    # checking for 4of a kind, full house
    pair_set = set()
    three_set = set()

    for index in value_list:
        if value_list.count(index) == 4:
            for idx in value_list:
                if idx != index:
                    kicker = idx #1kicker for 4of a kind
            return (8 , index, kicker)
        if value_list.count(index) == 3:
            if len(pair_set) == 1:
                return (7, index, pair_set.pop())
            three_set.add(index)
        if value_list.count(index) == 2:
            if len(three_set) == 1:
                return (7, three_set.pop(), index)
            pair_set.add(index)

    # if nothing yet found and returned before, return flush if exists
    if is_flush:
        return(6, value_list[0])

    # if nothing returned before, return straight if exists
    if is_straight:
        if from_5:
            return(5, 3)
        else:
            return(5, value_list[0])

    # checking for pair
    if len(pair_set) == 1:
        temp = pair_set.pop()
        kickerlist = [2, temp] #2 represents pair, temp is the pair value
        for idx in value_list:
            if idx != temp:
                kickerlist.append(idx) #adding kickers to the hand
        return tuple(kickerlist)

    # checking for 2 pairs
    elif len(pair_set) == 2:
        first = pair_set.pop()
        second = pair_set.pop()
        for idx in value_list:
            if idx != first and idx != second: #looking for kicker
                kicker = idx
        return (3, max(first, second), min(first, second), kicker)

    # checking for 3of a kind
    if len(three_set) == 1:
        temp = three_set.pop()
        kickerlist = [4, temp] #4 represents 3of a kind, temp value of the 3s
        for idx in value_list:
            if idx != temp:
                kickerlist.append(idx) #adding kickers to the hand
        return tuple(kickerlist)

    return tuple([1] + value_list)

def gen_permutations(outcomes, length):
    """
    Iterative function that generates set of permutations of
    outcomes of length num_trials. No repeated outcomes allowed
    (0,1) (1,0) is ok, length 2    // (0,0) not ok
    """
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                if item not in seq:
                    new_seq = list(seq)
                    new_seq.append(item)
                    temp.add(tuple(new_seq))
        ans = temp
    return ans

def gen_sorted_permutations(outcomes, length):
    """
    Function that creates all sorted sequences via permutations
    from permutations reduces/cancels (0,1) and (1,0) to one tuple
    """
    all_sequences = gen_permutations(outcomes, length)
    sorted_sequences = [tuple(sorted(sequence)) for sequence in all_sequences]
    return set(sorted_sequences)

def best_combo_out_of_7(list_of_7_cards):
    '''
    takes list of 7 cards(objects/class Card) and finds the highest combination from 5 cards
      returns value representation(evaluation) of this best combination + 5 cards of this combination
    '''
    card_dict = dict(list(enumerate(list_of_7_cards))) #creating dictionary {0:card0, 1:card1, ..., 6:card6}
    sequences = gen_sorted_permutations(card_dict.keys(), 5) #generates all sorted permutable sequences for keys of dictionary

    # creating list of lists, 21 sorted permutable sequences(no repetiton, order doesn't matter) of values from dictionary(objects/class Card)
    list_of_combinations = []
    for sequence in sequences:
        temp_list = []
        for idx in range(5):
            temp_list.append(card_dict[sequence[idx]])
        list_of_combinations.append(temp_list)


    # finding the best possible hand form list_of_combinations(from 21 combination)
    max_score_list = (0, 0, 0, 0, 0, 0)
    best_hand = []

    for temp_list in list_of_combinations: # iterating over the 21 hands, to evaluate which is better
        score_list = check_combination(temp_list) # checking the score of the hand
        for idx in range(len(score_list)): # iterating over the digits in the score(2, 3, 12, 1, 0), compairing each with max
            if score_list[idx] < max_score_list[idx]:
                break
            if score_list[idx] > max_score_list[idx]:
                max_score_list = score_list # if bigger than max, overwriting max
                best_hand = list(temp_list) # combination from 5 cards(class Card)
                break

    return (max_score_list, best_hand) # (evaluation representation of the combination (2, 4, 8, ...), list of cards in combination)

def reset_button():
    '''
    randomly takes 2-10 players and deals them cards
     draws the table
    '''
    global test_table
    canv.delete('group2del')
    fish_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # removes 1-8 players
    for idx in range(random.randrange(0, 9)):
        fish_list.pop()
    test_table.deal_everything(fish_list) # deals for 2-10 players
    test_table.draw(canv, START_POINT)

# create window
root = Tk()
root.title("POKER TABLE")
root.minsize(width=1600, height=900)
root.maxsize(width=1600, height=900)
root.resizable(width=False, height=False)

# create canvas
canv = Canvas(root, width=1650, height=900, bg="lightblue")
canv.pack()

# draw numbers of the players
for idx in range(10):
    canv.create_text(SEATS_NUMBERS[idx][0], SEATS_NUMBERS[idx][1], text=(idx + 1),
                     font="Verdana 14", anchor=CENTER, justify=CENTER, tag="group2del")

# creating object table
test_table = Table()

# create button on canvas
but = Button(canv, text='Deal', command=reset_button, height = 10, width = 20, anchor=CENTER)
canv.create_window(1450, 415, window=but)

root.mainloop()