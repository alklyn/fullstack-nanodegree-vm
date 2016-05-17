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

drop view if exists player1_points;
create view player1_points as
select players.id, players.name, coalesce(matches.player1_points, 0) as points
from players
left join matches on players.id = matches.player1_id
order by player1_points desc;

drop view if exists player2_points;
create view player2_points as
select players.id, players.name, coalesce(matches.player2_points, 0) as points
from players
left join matches on players.id = matches.player2_id
order by player2_points desc;

drop view if exists totals;
create view totals as
select player1_points.id, player1_points.name, player1_points.points + player2_points.points as totals
from player1_points inner join
player2_points on player1_points.id = player2_points.id
order by totals desc;
