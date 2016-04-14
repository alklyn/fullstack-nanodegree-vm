import sys
from tournament import reportMatch

if len(sys.argv) == 3:
    winner = int(sys.argv[1])
    loser = int(sys.argv[2])
    reportMatch(winner, loser)
