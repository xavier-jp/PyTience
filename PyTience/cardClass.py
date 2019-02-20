class Card():

    def __init__(self, suit, value, face): #suit, value and face passed from Game() class instance
        self.suit = suit
        self.value = value
        self.face = face

        self.gameAttributes = {'Suits':['H','C','S','D'],'Values':['A','2','3','4','5','6','7','8','9','T','J','Q','K']}
        self.valueIndex = self.gameAttributes['Values'].index(self.value) #used to compare card values when moving cards

        if self.suit == 'H' or self.suit == 'D': #sets card colour based on suit
            self.colour = 'red'
        else:
            self.colour = 'black'

    def changeFace(self):
        if self.face == False:
            self.face = True
        else:
            self.face = False

    def showCard(self): #uses self.face to return the card value or an X depending on whether card is face up (True) or face down (False)
        if self.face == False:
            return 'X'
        else:
            return self.value+self.suit