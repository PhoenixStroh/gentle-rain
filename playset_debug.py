from playset import *
from app import *

game = GameState()
agent = AgentFirst(game)
playset = Playset(agent, 100, 0, SaveConditionPointThreshold(4))
playset.run()
print(playset)

for history in playset.saved_history:
    app = App(history.game_state, history)
    app.add_input_callback(app.callback_undo_redo)
    app.start()