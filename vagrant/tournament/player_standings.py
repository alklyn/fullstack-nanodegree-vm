import sys
from tournament import playerStandings

ps = playerStandings()
for row in ps:
    print(row[0], row[1], row[2])
