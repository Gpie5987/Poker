import random
class Card:
    NUM = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    SUIT = ['c','d','h','s']
    def __init__(self,card_name):
        self.name = card_name
        self.number,self.suit = None,None
        self.text2card()
        
    def __str__(self) -> str:
        return self.name

    def text2card(self):
        if self.name[0] == self.NUM[12]:
            self.number = 12
        elif self.name[0] == self.NUM[11]:
            self.number = 11
        elif self.name[0] == self.NUM[10]:
            self.number = 10
        elif self.name[0] == self.NUM[9]:
            self.number = 9
        elif self.name[0] == self.NUM[8]:
            self.number = 8
        else:
            self.number = int(self.name[0])-2
        if self.name[1] == 's':
            self.suit = 3
        elif self.name[1] == 'h':
            self.suit = 2
        elif self.name[1] == 'd':
            self.suit = 1
        elif self.name[1] == 'c':
            self.suit = 0

class Hand:
    def __init__(self,card1,card2):
        self.cards = [card1,card2]
    
    def __str__(self) -> str:
        return self.get_name()

    @classmethod
    def create_hand_by_text(cls,text):
        return Hand(Card(text[0:2]),Card(text[2:4]))
    
    def get_name(self):
        return self.cards[0].name + self.cards[1].name

    def search_card(self,card):
        for self_card in self.cards:
            if card.name == self_card.name:
                return True
        return False
class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = []
        for n in Card.NUM:
            for s in Card.SUIT:
                self.cards.append(Card(n+s))
    
    def draw(self,times):
        retn = []
        for i in range(times):
            card = random.choice(self.cards)
            retn.append(card)
            self.cards.remove(card)
        return retn
    
    def remove_cards(self,remove_cards):
        discards = []
        for re_card in remove_cards:
            for de_card in self.cards:
                if re_card.name == de_card.name:
                    discards.append(de_card)
        for d in discards:
            if d in self.cards:
                self.cards.remove(d)

    def search_card(self,card):
        for self_card in self.cards:
            if card.name == self_card.name:
                return True
        return False

