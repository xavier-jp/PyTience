from random import shuffle
from cardClass import Card

class Game():

    def __init__(self):
        self.gameAttributes = {'Suits':['H','C','S','D'],'Values':['A','2','3','4','5','6','7','8','9','T','J','Q','K']}
        self.stock = [] #contains all remaining cards after dealt
        self.waste = [] #contains turned over cards from stock
        self.tableaus = [[],[],[],[],[],[],[]]
        self.foundations = [[],[],[],[]]
        self.moveLocs = {'T1':self.tableaus[0], 'T2':self.tableaus[1], 'T3':self.tableaus[2], 'T4':self.tableaus[3], 'T5':self.tableaus[4], 'T6':self.tableaus[5], 'T7':self.tableaus[6], 'HF':self.foundations[0], 'CF':self.foundations[1], 'SF':self.foundations[2], 'DF':self.foundations[3]} #user input location reference assigned to actual location

        #creates instances of Card class for each suit and value in self.gameAttributes
        for suit in self.gameAttributes['Suits']:
            for value in self.gameAttributes['Values']:
                self.stock.append(Card(suit, value, False))
        shuffle(self.stock) #shuffles cards

        #assigns each tableau a number of cards equal to the tableau's index +1; for example, tableau 1 has the reference self.tableaus[0], and so will contain 0+1 cards
        for tableau in range(len(self.tableaus)):
            for noOfCards in range(tableau+1):
                self.tableaus[tableau].append(self.stock[tableau+noOfCards])
                self.stock.pop(tableau+noOfCards)

        #turns last card in each tableau face up
        for tableau in self.tableaus:
            tableau[-1].changeFace()

        #displays rules and calls play function for main game loop
        input("WELCOME TO PyTience!\n\n\nRULES:\nThere are four different pile types. To the left of the table is the stock pile.\nThis contains all the cards in the deck that are not currently in play. This is represented by the 'S'.\nWhen 'S' is entered as a move, a card is drawn from the stock pile and moved to the waste pile.\nOnly the top card may be played from the waste pile - this is shown during gameplay underneath the stock pile.\nThe next seven piles are the tableaus - these make up the main table.\nThe four rightmost piles are the foundations. These are where each suit must be built up from ace to king.\n\nEach card is represented in the form 'AB' where A is the card's value and B is the card's suit.\nCards can only be placed on top of each other in alternating colours - remember that hearts and diamonds are red, and spades and clubs are black.\n(This rule does not apply to the foundation piles.)\nIf you move a card that is embedded within a tableau, all proceeding cards will move with it.\n\nTo make a move, enter the value of the card as shown on the table followed by the location you want the card to be moved to.\nTo move a card between tableaus, enter the card value followed by 'TX' where X is the tableau number.\nTo move a card to a foundation pile, enter the card value followed by 'YF' where Y is the foundation suit.\nRemember to seperate the card reference and location with a space.\n\nPress enter or click OK to continue: ")
        self.play()

    def gameDisplay(self):
        print('    1 2 3 4 5 6 7\n') #tableau formatting
        noColumns = 0
        for tableau in self.tableaus:
            if len(tableau) > noColumns:
                noColumns = len(tableau)
        if noColumns < 4:
            noColumns = 4

        for column in range(noColumns):
            if column == 0:
                string_start = "S " #used to represent stock
            else:
                if column == 1:
                    try:
                        string_start = self.waste[-1].showCard() #checks for cards in waste and displays last card to user
                    except:
                        string_start = "  "
                else:
                    string_start = "  "
            string_middle = ""
            for i in range(len(self.tableaus)):
                try:
                    x = str(self.tableaus[i][column].showCard())
                except IndexError:
                    x = "  "
                if len(x)!= 3:
                    string_start += ' '
                string_start += x
            try:
                string_end = self.foundations[column][-1].showCard()
            except:
                try:
                    string_end = self.gameAttributes['Suits'][column]+'F' #represents foundation piles
                except:
                    string_end = ""

            final_string = string_start + string_middle + "  " + string_end #string formatting
            print(final_string)
        print('\n')

    def validMove(self):
        while True:
            try:
                move = input('Enter your move, or type \'Q\' to quit: ').upper()
                break
            except TimeoutError: #bug fix for TimeoutError being raised after inactivity
                pass

        if move == 'Q' or move == 'QUIT':
            exit()

        validCard = False
        if move == 'S':
            try:
                #drawing of card from waste
                self.waste.append(self.stock[-1])
                self.waste[-1].changeFace()
                self.stock.pop(-1)
            except:
                #reshuffling waste if there are no new cards
                for cardIdx, card in enumerate(self.waste):
                    self.stock.append(card)
                    card.changeFace()
                    self.waste.pop(cardIdx)

        else:
            moveParts = move.split()

            cardLoc = []

            #shecks if card is currently able to move
            try:
                if moveParts[0] == self.waste[-1].showCard():
                    validCard = True
            except:
                pass
            if validCard == False:
                for foundation in self.foundations:
                    try:
                        if moveParts[0] == foundation[-1].showCard():
                            validCard = True
                            break
                    except:
                        pass
            if validCard == False:
                for tableau in self.tableaus:
                    for card in tableau:
                        try:
                            if moveParts[0] == card.showCard():
                                validCard = True
                                cardLoc.append(tableau.index(card))
                                cardLoc.append(self.tableaus.index(tableau))
                        except:
                            pass

            #checks if move location is valid using self.moveLocs
            validMove = False
            for loc in self.moveLocs:
                try:
                    if moveParts[1] == loc:
                        validMove = True
                except:
                    pass

            if validCard == True and validMove == True:
                return [moveParts, cardLoc]
            else:
                return False

    def play(self):
        moveCount = 0 #counts moves to display to user at endgame

        while True:
            moveCount += 1

            #check for win
            winCheck = 0
            for foundation in self.foundations:
                try:
                    if foundation[-1].showCard()[0] == 'K':
                        winCheck += 1
                except:
                    pass
            if winCheck == 4:
                print('YOU WON!!!\nYou beat PyTience in '+str(moveCount)+' moves!')
                exit()

            #displays game board
            self.gameDisplay()

            #ensures move is valid
            while True:
                move = self.validMove()
                if move != False:
                    break

            try:
                #moves from waste and into foundation piles
                if str(move[1]) == '[]':

                    if move[0][0] == self.waste[-1].showCard():
                        if move[0][1] == 'HF' or move[0][1] == 'CF' or move[0][1] == 'SF' or move[0][1] == 'DF':
                            try:
                                if self.moveLocs[move[0][1]][-1].colour == self.waste[-1].colour:
                                    if self.moveLocs[move[0][1]][-1].valueIndex == self.waste[-1].valueIndex+1:
                                        self.moveLocs[move[0][1]].append(self.waste[-1])
                                        self.waste.pop(-1)
                                    elif move[0][0][1] == move[0][1][0]:
                                        if self.moveLocs[move[0][1]][-1].colour == self.waste[-1].colour:
                                            if self.moveLocs[move[0][1]][-1].valueIndex+1 == self.waste[-1].valueIndex:
                                                self.moveLocs[move[0][1]].append(self.waste[-1])
                                                self.waste.pop(-1)
                            except:
                                if move[0][0][1] == move[0][1][0] and move[0][0][0] == 'A':
                                    self.moveLocs[move[0][1]].append(self.waste[-1])
                                    self.waste.pop(-1)

                        else:
                            try:
                                if self.moveLocs[move[0][1]][-1].colour != self.waste[-1].colour:
                                    if self.moveLocs[move[0][1]][-1].valueIndex == self.waste[-1].valueIndex+1:
                                        self.moveLocs[move[0][1]].append(self.waste[-1])
                                        self.waste.pop(-1)
                            except IndexError:
                                self.moveLocs[move[0][1]].append(self.waste[-1])
                                self.waste.pop(-1)

                    else:
                        for foundation in self.foundations:
                            if move[0][0] == foundation[-1].showCard():
                                if self.moveLocs[move[0][1]][-1].colour != foundation[-1].colour:
                                    if self.moveLocs[move[0][1]][-1].valueIndex == foundation[-1].valueIndex+1:
                                        self.moveLocs[move[0][1]].append(foundation[-1])
                                        foundation.pop(-1)

                #movement between tableaus
                else:
                    for tableau in self.tableaus:
                        try:
                            for card in tableau:

                                try:
                                        if (move[0][0] == card.showCard() and card.showCard() != 'X') or (self.tableaus.index(tableau) == move[1][1] and tableau.index(card) > move[1][0] and card.showCard() != 'X'):
                                            if move[0][1] == 'HF' or move[0][1] == 'CF' or move[0][1] == 'SF' or move[0][1] == 'DF':
                                                try:
                                                    if self.moveLocs[move[0][1]][-1].colour == card.colour:
                                                        if self.moveLocs[move[0][1]][-1].valueIndex == card.valueIndex+1:
                                                            self.moveLocs[move[0][1]].append(card)
                                                            tableau.pop(tableau.index(card))
                                                        elif move[0][0][1] == move[0][1][0]:
                                                            if self.moveLocs[move[0][1]][-1].colour == card.colour:
                                                                if self.moveLocs[move[0][1]][-1].valueIndex+1 == card.valueIndex:
                                                                    self.moveLocs[move[0][1]].append(card)
                                                                    tableau.pop(tableau.index(card))
                                                except:
                                                    if move[0][0][1] == move[0][1][0] and move[0][0][0] == 'A':
                                                        self.moveLocs[move[0][1]].append(card)
                                                        tableau.pop(tableau.index(card))
                                            else:
                                                if tableau.index(card)+1 != len(tableau):
                                                    try:
                                                        if self.moveLocs[move[0][1]][-1].colour != card.colour:
                                                            if self.moveLocs[move[0][1]][-1].valueIndex == card.valueIndex+1:
                                                                self.moveLocs[move[0][1]].extend(tableau[tableau.index(card):])
                                                                self.tableaus[self.tableaus.index(tableau)] = tableau[:tableau.index(card)]
                                                                if self.moveLocs[move[0][1]][-1].valueIndex > self.moveLocs[move[0][1]][-2].valueIndex:
                                                                    self.moveLocs[move[0][1]].pop(-1)
                                                                break
                                                    except IndexError:
                                                        self.moveLocs[move[0][1]].extend(tableau[tableau.index(card):])
                                                        try:
                                                            self.tableaus[self.tableaus.index(tableau)] = tableau[:tableau.index(card)]
                                                            if self.moveLocs[move[0][1]][-1].valueIndex > self.moveLocs[move[0][1]][-2].valueIndex:
                                                                self.moveLocs[move[0][1]].pop(-1)
                                                        except:
                                                            self.tableaus[self.tableaus.index(tableau)] = []
                                                        break
                                                else:
                                                    try:
                                                        if self.moveLocs[move[0][1]][-1].colour != card.colour:
                                                            if self.moveLocs[move[0][1]][-1].valueIndex == card.valueIndex+1:
                                                                self.moveLocs[move[0][1]].append(card)
                                                                tableau.pop(tableau.index(card))
                                                    except IndexError:
                                                        self.moveLocs[move[0][1]].append(card)
                                                        tableau.pop(tableau.index(card))
                                except ValueError:
                                    self.moveLocs[move[0][1]].append(card)
                                    tableau.pop(tableau.index(card))
                        except:
                            pass
            except:
                pass

            for tableau in self.tableaus:
                try:
                    if tableau[-1].showCard() == 'X':
                        tableau[-1].changeFace()
                except:
                    pass

            self.moveLocs = {'T1':self.tableaus[0], 'T2':self.tableaus[1], 'T3':self.tableaus[2], 'T4':self.tableaus[3], 'T5':self.tableaus[4], 'T6':self.tableaus[5], 'T7':self.tableaus[6], 'HF':self.foundations[0], 'CF':self.foundations[1], 'SF':self.foundations[2], 'DF':self.foundations[3]}

gameInstance = Game()