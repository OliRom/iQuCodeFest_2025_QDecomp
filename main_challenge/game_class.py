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

    def end_routine(self):
        pass

    def check_end_game(self):
        """
        Checks if the game has ended.

        Returns:
            bool: True if the game has ended, False otherwise.
        """        
        return self.active_player == self.dutch_player or self.end_game_flag

    def call_dutch(self):
        self.dutch_player = self.active_player

    def draw_cards(self):
        """
        Draw 2 cards from the deck.
        """
        card1 = generate_card()
        card2 = generate_card()

        return card1, card2
    
    def apply_operator_card(self, player_no, card_no, operator):
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
            return self.players[player_no].hand[card_no].measure(operator.data)
        
        elif operator.type == "Operator":
            self.players[player_no].hand[card_no].apply_operator(operator.data)
            return None

    def apply_state_card(self, card_no, card):
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

    def get_ranking(self):
        """
        Returns the ranking of the players based on their scores.

        The player with the lowest score wins. In case of a tie, the player that called "Dutch" is
        ranked first. In case of an other tie, 

        The ranking is determined as follows:
        1. Player with the lowest score is ranked first.
        2. Player that called "Dutch" is ranked first.
        3. The player with the smallest card is ranked first.
        4. In case of a tie, both players are ranked equally.

        Returns:
            list[list]: A list of players sorted by their scores in descending order.
        """
        temp_list = [(player, self.get_score(player)) for player in self.players]
        temp_list.sort(key=lambda x: x[1])

        ranking_list = [[player.name, player.calculate_points(), i+1] for i, (player, _) in enumerate(temp_list)]
        for i in range(1, len(ranking_list)):
            if temp_list[i][1] == temp_list[i-1][1]:  # If scores are equal, they share the same rank
                ranking_list[i][2] = ranking_list[i-1][2]

        return ranking_list
    
    def get_score(self, player):
        """
        Function to help ranking the players.

        The ranking is determined as follows:
        1. Player with the lowest score is ranked first.
        2. Player that called "Dutch" is ranked first.
        3. The player with the smallest card is ranked first.
        4. In case of a tie, both players are ranked equally.

        Args:
            player (Player): The player to get the score from.

        Returns:
            float: The score of the player.
        """
        points = player.calculate_points()

        # The player that called "Dutch" wins in case of a tie
        if self.dutch_player == self.players.index(player):
            points -= 0.5

        # The player with the smallest card wins in case of a tie
        points += 0.01 * min([card.measure_all() for card in player.hand])

        return points
