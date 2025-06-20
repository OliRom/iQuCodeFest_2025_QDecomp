from player_slot_class import PlayerSlot
from card_generator import generate_state

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = [PlayerSlot() for _ in range(4)]

        for card in self.hand:
            card.set_state(generate_state())

    def calculate_points(self):
        """
        Calculates the total points of the player based on the cards in its hand.

        Returns:
            int: The total points of the player.
        """
        points = 0
        for slot in self.hand:
            points += slot.measure_all()

        return points    
