from game_class import QDutch
from card_generator import Card

g = QDutch()
g.start_game(4)
g.init_routine()

print("Initial hands:")
print(g.players[0].hand[0].measure_all())
print(g.players[1].hand[0].measure_all())
print()

# Cards designed specifically for testing
op = Card(type="Operator", data=["X", "X", "X"])
ms = Card(type="Measurement", data=1)
st = Card(type="State", data=3)

print("Applying state card:")
print(g.players[0].hand[1].measure_all())  # Returns the value of the second card
g.apply_state_card(1, st)  # Apply a state card to player[0], card[1]
print(g.players[0].hand[1].measure_all())  # Returns the value of the second card

print()
print("Applying operator card:")
print(g.apply_operator_card(1, 0, op))  # Nothing is expected from an operator card
print(g.apply_operator_card(1, 0, ms))  # The qubit value is returned from a partial measurement
print(g.players[1].hand[0].measure_all())  # Returns an int corresponding to the value of the card
print()

g.next_player()
print(f"Active player: {g.active_player}")
g.call_dutch()

g.next_player()
print(g.active_player)
print(g.check_end_game())
g.next_player()
print(g.active_player)
print(g.check_end_game())
g.next_player()
print(g.active_player)
print(g.check_end_game())
g.next_player()
print(g.active_player)
print(g.check_end_game())

print()
print(g.get_ranking())
for player in g.players:
    print(f"{player.name} points: {player.calculate_points()}")
