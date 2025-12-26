from playset import *
from app import *

game = GameState()
agent = AgentFirst(game)
playset = Playset(agent, 500, 0, SaveConditionPointThreshold(4))
playset.run()
print(playset)

app = AppPlayset(playset.saved_history)
app.add_input_callback(app.callback_undo_redo)
app.start()