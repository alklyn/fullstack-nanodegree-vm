-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- Use the command \i tournament.sql to import the whole file into psql at once.

drop database if exists tournament;
create database tournament;

\c tournament

drop table if exists tournaments;
create table tournaments(
    tournament_id serial primary key,
    name text
);

drop table if exists players;
create table players(
    id serial primary key,
    tournament_id integer references tournaments(tournament_id) on delete cascade,
    name text
);

drop table if exists matches;
/*
Points are awarded as follows
win: 2
loss: 0
draw: 1
*/
create table matches(
    tournament_id integer references tournaments(tournament_id) on delete cascade,
    player1_id integer references players(id) on delete cascade,
    player2_id integer references players(id) on delete cascade,
    player1_points integer check(player1_points >= 0 and player1_points <= 2),
    player2_points integer check(player2_points >= 0 and player2_points <= 2),
    primary key (tournament_id, player1_id, player2_id),
    check (player1_points + player2_points = 2)
);

drop view if exists player1_wins;
create view player1_wins as
select players.id, players.name, count(matches.player1_points) as wins
from players
left join matches on players.id = matches.player1_id
where player1_points = 2
group by players.id
order by wins desc;

drop view if exists player2_wins;
create view player2_wins as
select players.id, players.name, count(matches.player2_points) as wins
from players
left join matches on players.id = matches.player2_id
where player2_points = 2
group by players.id
order by wins desc;

drop view
drop view if exists losers;
create view losers as
select players.id, players.name, count(matches.loser) as losses
from players
left join matches on players.id = matches.loser
group by players.id
order by losses desc;

drop view if exists standings;
create view standings as
select winners.id, winners.name, winners.wins, winners.wins + losers.losses as played
from winners, losers
where winners.id = losers.id
order by winners.wins desc;
