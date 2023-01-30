# Created by Yuan Liu at 11:23 29/01/2023 using PyCharm
# -*- coding: utf-8 -*-

import random


class Card:

    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank
        if self.rank in ['J', 'Q', 'K', 'Joker']:
            self.val = 0.5
        elif self.rank == 'A':
            self.val = 1
        else:
            self.val = int(self.rank)
        self.name = self.suit + ' ' + self.rank

    def __repr__(self):
        return f'Card(\'{self.name}\', Value: {self.val})'

    def __str__(self):
        return f"You've got a '{self.name}' with value {self.val}."

    def show(self):
        print(self.__repr__())

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, suit):
        if suit.capitalize() in ['Diamonds', 'Clubs', 'Hearts', 'Spades', '']:
            self._suit = suit.capitalize()
        else:
            raise Exception('The suit is INVALID!')
        return self._suit

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, rank):
        valid_rank = [str(i) for i in list(range(2, 11))] + ['J', 'Q', 'K', 'A', 'Joker']
        if str(rank) in valid_rank:
            self._rank = str(rank)
        else:
            raise Exception('The rank is INVALID!')
        return self._rank


class JokerCard(Card):
    def __init__(self, colour):
        self.colour = colour
        super().__init__('', "Joker")
        self.name = f'Joker {self.colour}'

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, colour):
        if colour.capitalize() in ['Red', 'Black']:
            self._colour = colour.capitalize()
        else:
            raise Exception('The colour is INVALID!')
        return self._colour


class Deck:

    def __init__(self):
        self.cards = []
        self.count = 0
        self.populate()
        self.shuffle()

    def __repr__(self):
        return f"Deck({self.count} cards)"

    def __len__(self):
        return len(self.cards)

    def populate(self):
        card_suits = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
        card_ranks = [str(i) for i in list(range(2, 11))] + ['J', 'Q', 'K', 'A']
        self.cards = [Card(card_suit, card_rank) for card_suit in card_suits for card_rank in card_ranks]
        self.cards.extend([JokerCard('Red'), JokerCard('Black')])  # add two jokers
        self.count = len(self.cards)

    def show(self):
        for card in self.cards:
            card.show()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        card_drawn = self.cards.pop()
        card_drawn.show()
        self.count -= 1
        return card_drawn


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.status = True  # if the player is still in the game
        self.score = 0

    def __repr__(self):
        return f"{self.name} (cards)"

    def draw(self, deck):
        print(f"{self.name} is drawing a card...")
        self.hand.append(deck.deal())
        self.show_hand()
        self.calculate_score()
        if self.score > 11:
            self.status = False
            self.score = 0  # reset score to 0
            print(f"{self.name} busts and is out with final score 0. Better luck next time.")

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand}")

    def calculate_score(self):
        self.score = sum(card.val for card in self.hand)

    def wants_card(self):
        while True:
            cont_to_play = input(f"{self.name}, do you want another card? (Y/N)").lower()
            if cont_to_play == 'y':
                print(f"{self.name} wants another card.")
                return True
            elif cont_to_play == 'n':
                self.status = False
                self.calculate_score()
                print(f"{self.name} does not want any more cards. {self.name}'s score is {self.score}.")
                self.show_hand()
                return False
            else:
                print('The choice is not defined! Please try again.')
                continue


def play_game(player_names: list = ["Alex", "Peppa"]) -> dict:
    """
    This is a simple poker game.
    The game's rules are as follows: We deal one card to each player at a time in turn. The value of Jack, Queen, King
    and Joker worth 0.5 while other cards worth their face value. The player can decide if he/she wants another card or
    not. When the sum of all cards is greater than 11, the player busts and his score is set to  0. The game continues
    till only one player is left or nobody wants more cards. Then we calculate the scores and print the final results.
    :param player_names: a list of players' names
    :return: a dictionary of players' final scores
    """
    if (type(player_names) == str) or (len(player_names) < 2) or (len(player_names) > 6):
        raise Exception("This game is designed for 2-6 players. Please try again with valid number of players")

    # set up the game
    deck = Deck()
    players = [Player(name) for name in player_names]
    losers = []

    # start the game by giving each player one card
    print("The game has started".center(72, '-'))
    print(f"There are {len(players)} players in this game: {', '.join(player_names)}.")
    for player in players:
        player.draw(deck)

    # carry on playing till there is no more player
    while len(players) > 0:
        for player in players:
            if not player.status:
                losers.append(player)
                players.remove(player)
                continue
            else:
                if player.wants_card():
                    player.draw(deck)

    # calculate the leaderboard and take into account when there is a tie
    scores = {player.name: player.score for player in (players + losers)}
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    max_score = sorted_scores[0][1]
    winner = {k: v for k, v in sorted_scores if v == max_score}

    # end the game and print the results
    print(f"Here is the leaderboard: \n {dict(sorted_scores)}")
    print(f"The {'winner is' if len(winner)==1 else 'winners are'} {', '.join(list(winner.keys()))}! Congrats!")
    print("The game has ended".center(72, '-'))

    return sorted_scores


if __name__ == "__main__":
    player_list = ["Alex", "Bob", "Charlie"]
    play_game(player_list)
