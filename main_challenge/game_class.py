from player_class import Player
from card_generator import *


class QDutch:
    def __init__(self):
        self.players = None
        self.dutch_player = None
        self.active_player = None

    def start_game(self, nb_players=4):
        """
        Initializes the game with a specified number of players.

        Args:
            nb_players (int): The number of players in the game.
        """
        self.end_game_flag = False
        self.dutch_player = None
        self.active_player = 0
        self.players = [Player(f"Player {i + 1}") for i in range(nb_players)]
    
    def init_routine(self):
        """
        Initializes the game routine, setting up the players and their hands.
        """
        for player in self.players:
            for card in player.hand:
                card.set_state(generate_state())
    
    def play_a_turn(self, player_no):
        """
        Executes a turn for the specified player.

        Args:
            player_no (int): The index of the player taking the turn.
        """
        self.player_turn(player_no)

    def end_routine(self):
        pass

    def check_end_game(self):
        """
        Checks if the game has ended.

        Returns:
            bool: True if the game has ended, False otherwise.
        """        
        return self.active_player == self.dutch_player

    def _call_dutch(self):
        self.dutch_player = self.active_player

    def _draw_cards(self):
        """
        Draw 2 cards from the deck.
        """
        card1 = generate_card()
        card2 = generate_card()

        return card1, card2
    
    def _apply_operator_card(self, player_no, card_no, operator):
        """
        Allows a player to apply  an operator card.

        Args:
            player_no (int): The index of the player picking a card.
            card_no (int): The index of the card to apply.
            operator (list[str]): The operator to apply.

        Returns:
            int | None: The result of the measurement if the operator is a Measurement card, otherwise None.
        """
        # Check the operator type
        if operator.type not in ["Operator", "Measurement"]:
            raise ValueError(f"The card to apply can only be an Operator or Measurement card. Got {operator.type}.")
        
        # Apply the operator card
        if operator.type == "Measurement":
            return self.players[player_no].measure(operator.data)
        
        elif operator.type == "Operator":
            self.players[player_no].hand[card_no].apply_operator(operator.data)
            return None

    def _apply_state_card(self, card_no, card):
        """
        Allows a player to change one of its cards.

        Args:
            card_no (int): The index of the card to change.
            card (Card): The new card.
        """
        if card.type != "State":
            raise ValueError(f"The card to change can only be a State card. Got {card.type}.")
        
        self.players[self.active_player].hand[card_no].set_state(card.data)
    
    def next_player(self):
        """
        Moves to the next player in the game.
        """
        self.active_player = (self.active_player + 1) % len(self.players)
