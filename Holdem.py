from PokerObject import Hand
from PokerObject import Card
from PokerObject import Deck
from PokerHand import PokerHand
from itertools import combinations
from Range import Range
import copy
import random
import math

class Holdem:
    @classmethod
    def compare_two_hand(self,IP_hand,OOP_hand,board):
        IP_strongest = self.strongest_combo(IP_hand,board)
        OOP_strongest = self.strongest_combo(OOP_hand,board)
        cmp_result = PokerHand.compare_PokerHand(IP_strongest,OOP_strongest)
        if cmp_result == IP_strongest:
            return IP_hand
        elif cmp_result == OOP_strongest:
            return OOP_hand
        else:
            return cmp_result
    @classmethod
    def strongest_combo(self,hand,board):
        cards = board + hand.cards
        combos = list(combinations(cards,5))
        strongest = PokerHand(combos[0])
        for comb in combos[1:]:
            PH_comb = PokerHand(comb)
            cmp_result = PokerHand.compare_PokerHand(strongest,PH_comb)
            if cmp_result != None:
                strongest = cmp_result
        return strongest

class EquityExplorer:
    def __init__(self,IP_range,OOP_range,board) -> None:
        self.IP_range = copy.deepcopy(IP_range)
        self.OOP_range = copy.deepcopy(OOP_range)
        self.board = board
        self.IP_results = []
        self.OOP_results = []
        self.adjust_range()

    def adjust_range(self):
        for b in self.board:
            self.IP_range.remove_card(b)
            self.OOP_range.remove_card(b)

    def get_results(self):
        time = len(self.IP_range.hands)+len(self.OOP_range.hands)
        for ip_hand in self.IP_range.hands:
            rst = self.range_battle(Range(ip_hand.get_name()),self.OOP_range,times=100)
            self.IP_results.append(CompareResult(ip_hand,self.OOP_range,rst))
            time -= 1
            print(time)
        for oop_hand in self.OOP_range.hands:
            rst = self.range_battle(Range(oop_hand.get_name()),self.IP_range,times=100)
            self.OOP_results.append(CompareResult(oop_hand,self.IP_range,rst))
            time -= 1
            print(time)
        return self.IP_results,self.OOP_results
        
    @classmethod
    def range_battle(cls,IP_range,OOP_range,board=[],times = 15000):
        ip_win = 0
        oop_win = 0
        draw = 0
        for i in range(times):
            ip_hand = random.choice(IP_range.hands)
            oop_hand = random.choice(OOP_range.hands)
            if EquityExplorer._check_repeated_card(ip_hand,oop_hand,board):
                continue
            deck = Deck()
            deck.remove_cards(ip_hand.cards+oop_hand.cards+board)
            draw_cards = deck.draw(5-len(board))
            rst = Holdem.compare_two_hand(ip_hand,oop_hand,board+draw_cards)
            if rst == ip_hand:
                ip_win += 1
            elif rst == oop_hand:
                oop_win += 1
            else:
                draw += 1
        return (ip_win+draw/2)/(ip_win+oop_win+draw)
    #檢查兩個手牌與牌面有沒有重複的牌
    @classmethod
    def _check_repeated_card(cls,ip_hand,oop_hand,board):
        cards = ip_hand.cards + oop_hand.cards + board
        cards_name = []
        for card in cards:
            cards_name.append(card.name)
        if len(cards_name) == len(set(cards_name)):
            return False
        return True    
    
class RangeExplorer(EquityExplorer):
    def create_js_file(self):
        ip_pr,oop_pr = self.get_PR()
        ip_output,oop_output = self._output_PR(ip_pr,oop_pr)
        file_name = 'output_result.js'
        ip_output_txt = self._build_output_txt(ip_output)
        oop_output_txt = self._build_output_txt(oop_output)
        ip_myPHs = RangeExplorer.range_to_MyPH_combo(self.IP_range,self.board,player='IP')
        oop_myPHs = RangeExplorer.range_to_MyPH_combo(self.OOP_range,self.board,player='OOP')
        ip_distribution = RangeExplorer.get_card_distribution(ip_myPHs)
        oop_distribution = RangeExplorer.get_card_distribution(oop_myPHs)
        ip_distribution_txt = RangeExplorer.build_distribution_txt(ip_distribution)
        oop_distribution_txt = RangeExplorer.build_distribution_txt(oop_distribution)

        board = '['
        for card in self.board:
            board += '"' + card.name + '",'
        board = board[:-1]
        board += ']'

        js_code = """
function get_ip_rst(){
    return """
        js_code += ip_output_txt + ';}'
        js_code += """
function get_oop_rst(){
    return """
        js_code += oop_output_txt + ';}'
        js_code += """
function get_board(){
    return """
        js_code += board + ';}'
        js_code += """
function get_ip_distribution(){
    return """
        js_code += ip_distribution_txt + ';}'
        js_code += """
function get_oop_distribution(){
    return """
        js_code += oop_distribution_txt + ';}'

        with open(file_name, "w") as js_file:
            js_file.write(js_code)
    @classmethod
    def get_card_distribution(cls,poker_hands):
        card_distribution = RangeExplorer.create_ph_type_dict()
        for ph in poker_hands:
            card_distribution[ph.name] += 1
        return card_distribution
    @classmethod
    def create_ph_type_dict(cls):
        ph_dict = {}
        for ph_type in PokerHand.NAME_LIST:
            ph_dict[ph_type] = 0
        return ph_dict
    @classmethod
    def build_distribution_txt(self,distribution):
        text = '{'
        keys = list(distribution.keys())
        keys.reverse()
        for key in keys:
            text += '"' + key + '":' + str(distribution[key]) + ','
        text = text[:-1]
        text += '}'
        return text

    def _build_output_txt(self,output):
        text = '['
        for my_PHs in output:
            if my_PHs == None:
                text += 'null,'
                continue
            text += '['
            for ph in my_PHs:
                text += '"' + ph.hand.get_name() + '",'
            text = text[:-1]
            text += '],'
        text = text[:-1]
        text += ']'
        return text

    def _output_PR(self,ip_pr,oop_pr):
        ip_pr.reverse()
        oop_pr.reverse()
        ip_output = []
        oop_output = []
        while len(ip_pr)>0 or len(oop_pr)>0:
            if len(ip_pr) == 0:
                rst = oop_pr[0][0]
            elif len(oop_pr) == 0:
                rst = ip_pr[0][0]
            else:
                rst = PokerHand.compare_PokerHand(ip_pr[0][0],oop_pr[0][0])

            if len(ip_pr) != 0 and rst == ip_pr[0][0]:
                ip_output.append(ip_pr.pop(0))
                oop_output.append(None)
            elif len(oop_pr) != 0 and rst == oop_pr[0][0]:
                oop_output.append(oop_pr.pop(0))
                ip_output.append(None)
            else:
                ip_output.append(ip_pr.pop(0))
                oop_output.append(oop_pr.pop(0))
        
        return ip_output,oop_output

    def get_PR(self):
        ip_rst = RangeExplorer.range_to_MyPH_combo(self.IP_range,self.board,player='IP')
        ip_rst = RangeExplorer.sort_ranking(ip_rst)
        ip_rst = RangeExplorer.make_PR_distribution(ip_rst)
        oop_rst = RangeExplorer.range_to_MyPH_combo(self.OOP_range,self.board,player='OOP')
        oop_rst = RangeExplorer.sort_ranking(oop_rst)
        oop_rst = RangeExplorer.make_PR_distribution(oop_rst)
        return ip_rst,oop_rst
    
    @classmethod
    def make_PR_distribution(cls,PH_rank):
        '''剩餘組合/剩餘PR == size-1'''
        PokerHands_PR = []
        length = len(PH_rank)
        size = math.ceil(length / 100)
        switch = 100-(100*size-length)
        for i in range(0,switch*size,size):
            splt = PH_rank[i:i + size]
            rst = RangeExplorer.sort_ranking(splt)
            rst.reverse()
            PokerHands_PR.append(rst)
        switch = switch*size
        size -= 1
        if size != 0:
            for i in range(switch,length,size):
                splt = PH_rank[i:i + size]
                rst = RangeExplorer.sort_ranking(splt)
                rst.reverse()
                PokerHands_PR.append(rst)
        return PokerHands_PR

    @classmethod
    def sort_ranking(cls,my_poker_hands):
        rank = sorted(my_poker_hands, key=lambda x: (x.poker_hand.type_level,x.poker_hand.num_level[0],x.poker_hand.num_level[1],x.poker_hand.num_level[2],x.poker_hand.num_level[3],x.poker_hand.num_level[4]))
        return rank

    @classmethod
    def range_to_MyPH_combo(cls,range,board,player=''):
        my_poker_hands = []
        for hand in range.hands:
            my_poker_hands.append(MyPokerHand(hand,board,player))
        return my_poker_hands

class MyPokerHand:
    def __init__(self,hand,board,player=''):
        self.player = player
        self.hand = hand
        self.board = board
        self.poker_hand = Holdem.strongest_combo(hand,board)
        self.type_level = self.poker_hand.type_level
        self.num_level = self.poker_hand.num_level
        self.name = self.poker_hand.name

