#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    query = "delete from matches;"
    cur.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    query = "delete from players;"
    cur.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    query = "select count(*) from players;"
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    return row[0]


def registerPlayer(name, tournament_id = 1):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    query = "insert into players(tournament_id, name) values(%s, %s);"
    cur.execute(query, (tournament_id, name))
    conn.commit()
    conn.close()


def playerStandings(tournament_id = 1):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    query = "select * from standings;"
    cur.execute(query)
    data = cur.fetchall()
    conn.close()
    return data

def new_match_id():
    """Generate a new match id for saving match results"""
    conn = connect()
    cur = conn.cursor()
    query = "select coalesce(max(match_id), 0) + 1 as new_match_id from results;"
    cur.execute(query)
    data = cur.fetchone()
    conn.close()
    return data[0]



def reportMatch(winner, loser, tournament_id = 1):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    match_id = new_match_id()
    conn = connect()
    cur = conn.cursor()
    query = "insert into results(tournament_id, match_id, player_id, points) values(%s, %s, %s, %s);"
    cur.execute(query, (tournament_id, winner, loser, 2, 0))
    conn.commit()
    conn.close()



def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cur = conn.cursor()
    query = "select id, name from standings;"
    cur.execute(query)
    temp = cur.fetchall()
    conn.close()
    data = list()
    for index in range(0, len(temp), 2):
        data.append(temp[index] + temp[index + 1])
    return data
