# Tournament project

## Project files
File                | Purpose
------------------- | -------------------------------------------------------
tournament.sql      | Contains database schema
tournament.py       | Contains all the methods required for the project.
tournament_test.py  | Contains unit tests for all the methods in the project


## Methods in tournament module
Function        | Purpose
--------------- | -------------------------------------------------------
connect         | Meant to connect to the database.
deleteMatches   | Remove all the matches records from the database.
deletePlayers   | Remove all the player records from the database.
countPlayers    | Returns the number of players currently registered
registerPlayer  | Adds a player to the tournament database.
playerStandings | Returns a list of the players and their win records, sorted
                | by wins.
reportMatch     | This is to simply populate the matches table and record the
                | winner and loser as (winner,loser) in the insert statement.
swissPairings   | Returns a list of pairs of players for the next round of a
                | match. Here all we are doing is the pairing of alternate
                | players from the player standings table, zipping them up and
                | appending them to a list with values:(id1, name1, id2, name2)


## Method input(s)/ouput(s)
* connect(database_name="tournament")
    * arguments
        * database_name: a string containing the name of the database
    returns
        * a tuple in the form: db, cursor
        * db: a database connection object
        * cursor: a database cursor object

* deleteMatches(tournament_id=1)
    * arguments
        * tournament_id: id number of the tournament
    returns
        None

* countPlayers(tournament_id=1)
    * arguments
        * tournament_id: id number of the tournament
    returns
        * the number of players in the tournament

* registerTournament(name)
    * arguments
        * name: name of the tournament
    returns
        * None

* registerPlayer(name, tournament_id=1)
    * arguments
        * name: the player's full name
        * tournament_id: id number of the tournament
    returns
        * None

* playerStandings(tournament_id=1)
    * arguments
        * tournament_id: id number of the tournament
    returns
        * A list of tuples, each of which contains (id, name, wins, matches):
        * id: the player's unique id (assigned by the database)
        * name: the player's full name (as registered)
        * wins: the number of matches the player has won
        * matches: the number of matches the player has played

* reportMatch(winner, loser, tournament_id=1)
    * arguments
        * the id number of the winner
        * the id number of the loser
        * tournament_id: id number of the tournament
    returns
        * None

* swissPairings(tournament_id=1)
    * arguments
        * tournament_id: id number of the tournament
    * returns
        * A list of tuples, each of which contains (id1, name1, id2, name2)
        * id1: the first player's unique id
        * name1: the first player's name
        * id2: the second player's unique id
        * name2: the second player's name

How to run the tournament project.
* Install Vagrant and VirtualBox
* Launch the Vagrant VM
    1. Enter the vagrant folder: cd ../vagrant
    2. Start the vagrant box: vagrant up
* Login to the vagrant box
    1. vagrant ssh
4. Enter the application folder : cd /vagrant/tournament
5. Login to postgresql: psql
6. Create the database and necessary tables: \i tournament.sql
7. Import module tournament into your code in order use this project.
