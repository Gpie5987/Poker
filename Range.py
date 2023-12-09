from PokerObject import Card
from PokerObject import Hand
class Range:
    def __init__(self,range_txt):
        self.hands = []
        self.text2range(range_txt)

    #刪除含指定牌的手牌
    def remove_card(self,card):
        original_hands = self._copy_hands()
        for hand in original_hands:
            if hand.search_card(card):
                self.hands.remove(hand)

    '''文字範圍轉成類別Range'''
    def text2range(self,text):
        self.hands = []
        hands = text.split(',')
        for hand in hands:
            if '+' in hand:
                self._plus_in_text(hand)
            elif '-' in hand:
                self._minus_in_text(hand)
            elif len(hand) == 3:
                self._add_cards([hand[:2]],hand)
            elif len(hand) == 2:
                self._all_pair(hand)
            else:
                self.hands.append(Hand.create_hand_by_text(hand))

    #有+的範圍，例如:99+,86o+
    def _plus_in_text(self,split_text):
        second_card_index = Card.NUM.index(split_text[0])
        start,end = split_text, split_text[0]+Card.NUM[second_card_index-1]
        cards_num = self._start2end(start,end)
        self._add_cards(cards_num,split_text)

    #有-的範圍，例如:KK-66,A7o-A3o
    def _minus_in_text(self,split_text):
        end,start = split_text.split('-')
        cards_num = self._start2end(start,end)
        self._add_cards(cards_num,split_text)

    #根據開始的數字與結束的數字得出數字清單，例如start = AJ,end = A9得出[AJ,AT,A9]
    def _start2end(self,start,end):
        cards_num = []
        switch = False
        for num in Card.NUM:
            if num == start[1]:
                switch = True
            if switch:
                if start[0] == start[1]:
                    cards_num.append(num+num)
                else:
                    cards_num.append(start[0]+num)
            if  num == end[1]:
                switch = False
        return cards_num
    
    #將數字清單根據三種類型pair,suit,offsuit輸入進屬性self.hands
    def _add_cards(self,cards_num,split_text):
         for num in cards_num:
            if num[0] == num[1]:
                self._all_pair(num)
            elif split_text[2] == 's':
                self._all_suit(num)
            else:
                self._all_offsuit(num)

    def _all_suit(self,hand_num):
        for s in Card.SUIT:
            self.hands.append(Hand.create_hand_by_text(hand_num[0]+s + hand_num[1]+s))
    
    def _all_offsuit(self,hand_num):
        for s in Card.SUIT:
            for s2 in Card.SUIT:
                hand = hand_num[0]+s + hand_num[1]+s2
                if s == s2:
                    continue
                self.hands.append(Hand.create_hand_by_text(hand))

    def _all_pair(self,hand_num):
        cards = []
        for s in Card.SUIT:
            cards.append(hand_num[0]+s)
        for i in range(3):
            for j in range(i+1,4):
                self.hands.append(Hand.create_hand_by_text(cards[i]+cards[j]))

    '''類別Range轉文字(未完成):step1.offsuit,suit,pair分別合併, step2.分成高張A~2低張高到低, step3.檢查清單大小>2與低張相減數量判斷可合併,step4.合併成+或-'''
    def range2text(self):
        merger_hands = self._copy_hands()
        self._suit_merger(merger_hands)
        for hand in merger_hands:
            print(hand)

    #將suit與offsuit組合分別合併
    def _suit_merger(self,merger_hands):
        number_combos = {}
        for hand in merger_hands:
            hand_txt = hand.get_hand()
            if hand_txt[1] == hand_txt[3]:
                suited = 's'
            elif hand_txt[0] == hand_txt[2]:
                suited = ''
            else:
                suited = 'o'
            num_type = hand_txt[0] + hand_txt[2] + suited
            if num_type not in number_combos:
                number_combos[num_type] = [hand]
            else:
                number_combos[num_type].append(hand)
            
        for key in number_combos.keys():
            if len(number_combos[key]) == 4 or len(number_combos[key]) == 12 or (len(number_combos[key]) == 6 and key[0] == key[1]):
                for removal_hand in number_combos[key]:
                    merger_hands.remove(removal_hand)
                merger_hands.append(key)
    
    #依高張排序進清單
    def _sort_ace_to_two(self,merger_hands):
        sort_result_suit = []
        sort_result_offsuit = []
        #for hand in merger_hands:
            #if type(hand) != Hand:
                #if 'o' in hand:
    #深度複製範圍                
    def _copy_hands(self):
        copy_hands = []
        for hand in self.hands:
            copy_hands.append(hand)
        return copy_hands
    

