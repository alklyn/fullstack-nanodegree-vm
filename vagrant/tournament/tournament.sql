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
    name text not null
);

drop table if exists players;
create table players(
    id serial primary key,
    tournament_id integer references tournaments(tournament_id) on delete cascade,
    name text not null
);

drop table if exists results;
/*
Points are awarded as follows
win: 2
loss: 0
draw: 1
*/
create table results(
    results_id serial primary key,
    tournament_id integer references tournaments(tournament_id) on delete cascade,
    match_id integer not null,
    player_id integer references players(id) on delete cascade,
    points integer not null
);

drop view if exists stats;
create view stats as
    select player_id, sum(points) as points, count(*) as matches
    from results
    group by player_id
    order by points desc;

drop view if exists standings;
create view standings as
    select players.id, players.name, coalesce(stats.points, 0) as wins, coalesce(stats.matches, 0) as matches
    from players left join stats on players.id = stats.player_id
    order by wins desc;
