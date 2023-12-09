from PokerObject import Card

class PokerHand:
    NAME_LIST = ['High Card','One Pair','Two Pair','Three of a Kind','Straight','Flush','Full House','Four of a Kind','Straight Flush']

    def __init__(self,cards):
        self.cards = cards
        type_level,num_level =self._check_type()
        self.type_level = type_level
        self.num_level = num_level
        self.name = PokerHand.NAME_LIST[type_level]

    def __str__(self) -> str:
        text = ''
        for card in self.cards:
            text += str(card) + ','
        return text

    @classmethod
    def create_PokerHand_by_text(cls,text):
        cards = []
        cards_name = text.split(',')
        for card_name in cards_name:
            cards.append(Card(card_name))
        return PokerHand(cards)
    
    #與其他PokerHand比大小
    @classmethod
    def compare_PokerHand(cls,IP,OOP):
        if IP.type_level > OOP.type_level:
            return IP
        elif IP.type_level < OOP.type_level:
            return OOP
        else:
            for i in range(len(IP.num_level)):
                if IP.num_level[i] > OOP.num_level[i]:
                    return IP
                elif IP.num_level[i] < OOP.num_level[i]:
                    return OOP
            return None

    #撲克牌型判別
    def _check_type(self):
        '''card = [num,suit]'''
        cards_num,cards_suit = self._split_num_suit(self.cards)
        
        count_rst = self._count_cards(cards_num)
        if max(count_rst[1]) == 4:
            return 7,self._sortForcompare(count_rst)+[0,0,0]
        elif max(count_rst[1]) == 3:
            if 2 in count_rst[1]:
                return 6,self._sortForcompare(count_rst)+[0,0,0]
            return 3,self._sortForcompare(count_rst)+[0,0]
        elif max(count_rst[1]) == 2:
            if len(count_rst[0]) == 3:
                return 2,self._sortForcompare(count_rst)+[0,0]
            return 1,self._sortForcompare(count_rst)+[0]
        else:
            flush_ck = self._check_flush(cards_suit)
            straight_ck = self._check_straight(count_rst[0])
            ct_rst0 = count_rst[0]
            ct_rst0.reverse()
            if flush_ck == True and straight_ck == True:
                return 8,ct_rst0
            elif flush_ck == True:
                return 5,ct_rst0
            elif straight_ck == True:
                return 4,ct_rst0
            else:
                return 0,ct_rst0

    def _count_cards(self,cards_num):
        '''ret = count_rst = [[num],[amount]]'''
        num_list = [0]*13
        for element in cards_num:
                num_list[element]+=1
        ret = [[],[]]
        for num,amount in enumerate(num_list):
            if amount != 0:
                ret[0].append(num)
                ret[1].append(amount) 
        return ret

    def _check_flush(self,cards_suit):
        for element in cards_suit:
            if element != cards_suit[0]:
                return False 
        return True

    def _check_straight(self,count_rst0):
        if count_rst0[-1]-count_rst0[0]==4 or count_rst0 == [0,1,2,3,12]:
            return True
        return False

    def _sortForcompare(self,count_rst):
        num_amount = [[], [], [], []]
        for i,amt in enumerate(count_rst[1]):
            num_amount[amt-1].append(count_rst[0][i])
        re = []
        for element in num_amount:
            if element != []:
                re = re + element
        re.reverse()
        return re

    def _split_num_suit(self,cards):
        cards_num = []
        cards_suit = []
        for card in cards:
            cards_num.append(card.number)
            cards_suit.append(card.suit)
        return cards_num,cards_suit


        
