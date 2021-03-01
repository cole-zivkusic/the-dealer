# helper functions to be used by extensions
import random


'''
shuffles 6 decks worth of cards created by a following function
params : none
return : a list of the shuffled deck (312 cards)
'''
def shuffle_cards():
    # create a deck using
    deck = create_deck()
    # combine 6 decks into one
    full_deck = all_decks(deck)
    card_order = []

    for i in range(312):
        card = random.choice(full_deck)
        card_order.append(card)

    return card_order


'''
orders the card values of a given deck
param deck : 6 decks worth of pre-shuffled cards
return : a list of the params card values in the same order
'''
def value_order(deck):
    values = []
    for i in deck:
        value = card_value(i)
        values.append(value)

    return values


'''
creates a deck of 52 cards
return : a list of said 52 cards, not shuffled
'''
def create_deck():
    return ["Ace of Hearts ❤️", "Ace of Spades ♠️", "Ace of Diamonds ♦️", "Ace of Clubs ♣️",
            "Two of Hearts ❤️", "Two of Spades ♠️", "Two of Diamonds ♦️", "Two of Clubs ♣️",
            "Three of Hearts ❤️", "Three of Spades ♠️", "Three of Diamonds ♦️", "Three of Clubs ♣️",
            "Four of Hearts ❤️", "Four of Spades ♠️", "Four of Diamonds ♦️", "Four of Clubs ♣️",
            "Five of Hearts ❤️", "Five of Spades ♠️", "Five of Diamonds ♦️", "Five of Clubs ♣️",
            "Six of Hearts ❤️", "Six of Spades ♠️", "Six of Diamonds ♦️", "Six of Clubs ♣️",
            "Seven of Hearts ❤️", "Seven of Spades ♠️", "Seven of Diamonds ♦️", "Seven of Clubs ♣️",
            "Eight of Hearts ❤️", "Eight of Spades ♠️", "Eight of Diamonds ♦️", "Eight of Clubs ♣️",
            "Nine of Hearts ❤️", "Nine of Spades ♠️", "Nine of Diamonds ♦️", "Nine of Clubs ♣️",
            "Ten of Hearts ❤️", "Ten of Spades ♠️", "Ten of Diamonds ♦️", "Ten of Clubs ♣️",
            "Jack of Hearts ❤️", "Jack of Spades ♠️", "Jack of Diamonds ♦️", "Jack of Clubs ♣️",
            "Queen of Hearts ❤️", "Queen of Spades ♠️", "Queen of Diamonds ♦️", "Queen of Clubs ♣️",
            "King of Hearts ❤️", "King of Spades ♠️", "King of Diamonds ♦️", "King of Clubs ♣️"]


'''
used for grabbing a cards value
param card : the card whomst value we are looking to return
return : an integer representing the cards value
'''
def card_value(card):
    card_database = {"Ace of Hearts ❤️": 1, "Ace of Spades ♠️": 1, "Ace of Diamonds ♦️": 1, "Ace of Clubs ♣️": 1,
                     "Two of Hearts ❤️": 2, "Two of Spades ♠️": 2, "Two of Diamonds ♦️": 2, "Two of Clubs ♣️": 2,
                     "Three of Hearts ❤️": 3, "Three of Spades ♠️": 3, "Three of Diamonds ♦️": 3,
                     "Three of Clubs ♣️": 3,
                     "Four of Hearts ❤️": 4, "Four of Spades ♠️": 4, "Four of Diamonds ♦️": 4, "Four of Clubs ♣️": 4,
                     "Five of Hearts ❤️": 5, "Five of Spades ♠️": 5, "Five of Diamonds ♦️": 5, "Five of Clubs ♣️": 5,
                     "Six of Hearts ❤️": 6, "Six of Spades ♠️": 6, "Six of Diamonds ♦️": 6, "Six of Clubs ♣️": 6,
                     "Seven of Hearts ❤️": 7, "Seven of Spades ♠️": 7, "Seven of Diamonds ♦️": 7,
                     "Seven of Clubs ♣️": 7,
                     "Eight of Hearts ❤️": 8, "Eight of Spades ♠️": 8, "Eight of Diamonds ♦️": 8,
                     "Eight of Clubs ♣️": 8,
                     "Nine of Hearts ❤️": 9, "Nine of Spades ♠️": 9, "Nine of Diamonds ♦️": 9, "Nine of Clubs ♣️": 9,
                     "Ten of Hearts ❤️": 10, "Ten of Spades ♠️": 10, "Ten of Diamonds ♦️": 10, "Ten of Clubs ♣️": 10,
                     "Jack of Hearts ❤️": 10, "Jack of Spades ♠️": 10, "Jack of Diamonds ♦️": 10,
                     "Jack of Clubs ♣️": 10,
                     "Queen of Hearts ❤️": 10, "Queen of Spades ♠️": 10, "Queen of Diamonds ♦️": 10,
                     "Queen of Clubs ♣️": 10,
                     "King of Hearts ❤️": 10, "King of Spades ♠️": 10, "King of Diamonds ♦️": 10,
                     "King of Clubs ♣️": 10, }

    return card_database[card]


'''
takes a deck and returns a larger deck, of 6
param deck : a list of non-shuffled cards
return : a list of 6 decks worth of non-shuffled cards
'''
def all_decks(deck):
    six_decks = []
    for i in range(6):
        for card in deck:
            six_decks.append(card)

    return six_decks


'''
calculates the possible hands a player or dealer can have
param cards : a list of the player or dealers cards
return bust : a two item list containing -1 at index 0, and a hand sum at index 1
return unique_values : a two item list containing either two identical hand sums or 
a low and high hand sum if there is an ace in play
'''
def possible_hands(cards):
    # holds the dealer or players two possible hand values in a list
    # if no ace is in play, both values will be identical
    unique_values = []
    # holds a -1 at index 0, and their hand sum at index 1
    # this is done to locate a bust in the main game, and be able to print their hand total in summary
    bust = []

    # return -1 in a list if the player or dealer has a bust hand
    # since aces are values as 1 at the start we don't need to worry about a non-bust hand returning a bust
    if sum(cards) > 21:
        bust.append(-1)
        bust.append(sum(cards))
        return bust

    # add the low end of what a player or dealer could have
    unique_values.append(sum(cards))

    # check if the user has an ace in play and if it can still cause their hand to have two possible combos
    if unique_values[0] + 10 < 22 and 1 in cards:
        unique_values.append(unique_values[0] + 10)
    else:
        unique_values.append(unique_values[0])

    return unique_values


'''
compares a players hand to the dealer and determines the outcome
param player : the players hand combinations (a two item list taken created by possible_hands())
param dealer : the dealers hand combinations (a two item list taken created by possible_hands())
return : the hand outcome as a string
'''
def check_winner(player, dealer):
    # grab the player and dealers "low" hand values
    p_value = player[0]
    d_value = dealer[0]

    # check to see if an ace is in play and assign a value variable to equal the higher of the two
    # hand combinations that is under 22
    if p_value < player[1] < 22:
        p_value = player[1]

    if d_value < dealer[1] < 22:
        d_value = dealer[1]

    # player win if the dealer busts
    # if the player also busts, there is a check for this in the main blackjack command
    # to still give the player a loss
    if d_value == -1:
        return "p_win"
    # dealer win
    elif d_value > p_value and 22 > d_value > 16:
        return "d_win"
    # dealer and player tie
    elif d_value == p_value and d_value > 16:
        return "push"
    # player win
    elif p_value > d_value > 16 and 22 > p_value > 16:
        return "p_win"
    # default to a dealer win to catch any mishaps (double checked in the main blackjack command)
    else:
        return "d_win"
