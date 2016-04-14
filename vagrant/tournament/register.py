import sys
from tournament import registerPlayer

if len(sys.argv) == 2:
    player = sys.argv[1]
    registerPlayer(player)
