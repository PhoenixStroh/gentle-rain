from playset import *
from app import *

game = GameState()
agent = AgentFirst(game)
playset = Playset(agent, 100, 0, SaveConditionPointThreshold(4))
playset.run()
print(playset)

for history in playset.saved_history:
    App(history.game_state).start()