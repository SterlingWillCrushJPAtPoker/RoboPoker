import hand_helpers as hands
import globals
import time
import Bots.bot_helpers as b


class Actions:
    fold = 0
    call = 1
    bet = 2
    check = 3
    allin = 4


class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.busted = False
        self.folded = False
        self.all_in = False
        self.hand = hands.Hand(self.name)
        self.type = self.bot_type()
        self.stats = b.Stats(self.chips)
        self.chips_in_pot = 0

    def new_hand(self):
        self.folded = False
        self.hand = hands.Hand(self.name)
        self.chips_in_pot = 0
        if self.chips <= 0:
            self.bust()
        else:
            self.all_in = False

    def bust(self):
        self.busted = True
        self.hand = None

    def fold(self):
        self.folded = True
        return None

    def act(self, bet, my_bet, table=None, actions=None, pot=None):
        if bet - my_bet > 50:
            return None
        else:
            return bet - my_bet

    def outer_act(self, bet, my_bet, table, actions, pot, forced=0):
        if globals.USER_PLAYING:
            time.sleep(1)
        if forced == 0:
            new_bet = self.act(bet, my_bet, table, actions, pot)
        else:
            new_bet = forced
        if new_bet:
            new_bet = new_bet
            if new_bet >= self.chips:
                self.all_in = True
                new_bet = round(self.chips)
                self.chips = 0
                if globals.USER_PLAYING:
                    print(self.name + " goes all in with " + str(new_bet + my_bet))
                self.chips_in_pot += new_bet
                return new_bet
            new_bet = round(new_bet)
            self.chips -= new_bet
            self.chips_in_pot += new_bet
        if globals.USER_PLAYING:
            if new_bet is 0:
                print(self.name + " checks")
            elif new_bet:
                print(self.name + " bets " + str(new_bet + my_bet))
        return new_bet

    def add_card(self, card, table=None):
        self.hand.add_card(card, table)

    def status(self, table):
        self.show_hand(table)
        print(self.bot_type())
        print(self.chips)

    def show_hand(self, table, print_now=False):
        if print_now:
            print(self.hand.show(table))
        if self.hand:
            return self.hand.show(table)
        return ""

    def bot_type(self):
        return "base_player"

    def get_hand_value(self):
        if self.hand:
            return self.hand.get_value()
        return 0

    def get_num_cards(self):
        if self.hand:
            return len(self.hand.cards)
        return 0

    def update_stats(self):
        if self.stats.busted:
            return
        if self.folded:
            self.stats.folded(self.chips)
        else:
            self.stats.update(self.chips)
        if self.busted:
            self.stats.busted = True
