#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.
    Returns a database connection and a cursor.
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except Exception as e:
        print(e)
        exit()


def deleteTournaments():
    """Remove all the tournament records from the database."""
    conn, cur = connect()
    query = "delete from tournaments;"
    cur.execute(query)
    conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    conn, cur = connect()
    query = "delete from matches;"
    cur.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cur = connect()
    query = "delete from players;"
    cur.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cur = connect()
    query = "select count(*) from players;"
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    return row[0]


def registerTournament(name):
    """Adds a tournament to the database.
    Args:
      name: the the name of the tournament.
    """
    conn, cur = connect()
    query = "insert into tournaments(name) values(%s);"
    cur.execute(query, (name, ))
    conn.commit()
    conn.close()


def registerPlayer(name, tournament_id=1):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, cur = connect()
    query = "insert into players(tournament_id, name) values(%s, %s);"
    cur.execute(query, (tournament_id, name))
    conn.commit()
    conn.close()


def playerStandings(tournament_id=1):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, cur = connect()
    query = """
    select id, name, wins, matches
    from standings
    where tournament_id = %s;
    """
    cur.execute(query, (tournament_id,))
    standings = cur.fetchall()
    conn.close()
    return standings


def reportMatch(winner, loser, tournament_id=1):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the winner
      loser:  the id number of the loser
      tournament_id: id number of the current tournament

    """
    conn, cur = connect()
    query = """
    insert into matches(tournament_id, winner, loser) values(%s, %s, %s);
    """
    cur.execute(query, (tournament_id, winner, loser))
    conn.commit()
    conn.close()


def swissPairings(tournament_id=1):
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
    standings = playerStandings()
    pairings = list()
    for index in range(0, len(standings), 2):
        pairings.append([
            standings[index][0], standings[index][1],
            standings[index + 1][0], standings[index + 1][1]])
    return pairings
