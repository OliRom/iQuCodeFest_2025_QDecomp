from player_slot_class import PlayerSlot

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = [PlayerSlot() for _ in range(4)]

    def points(self):
        points = 0
        for slot in self.hand:
            points += slot.measure_all()
            self.points
        return points
    
            

    def play_a_turn(self):
        pass
