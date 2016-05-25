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

drop view if exists view_winners cascade;
create view view_winners as
    select results.player_id, coalesce(count(results.player_id), 0) as wins
    from results
    where results.points = 2
    group by results.player_id
    order by wins desc;

drop view if exists view_losers cascade;
create view view_losers as
    select results.player_id, coalesce(count(results.player_id), 0) as losses
    from results
    where results.points = 0
    group by results.player_id
    order by losses desc;

drop view if exists view_draws cascade;
create view view_draws as
    select results.player_id, coalesce(count(results.player_id), 0) as draws
    from results
    where results.points = 1
    group by results.player_id
    order by draws desc;

drop view if exists standings; 
create view standings as
    select players.id, players.name, coalesce(view_winners.wins, 0) as wins,
    coalesce(view_winners.wins, 0) + coalesce(view_losers.losses, 0) as matches
    from (players left join view_winners on players.id = view_winners.player_id)
    left join view_losers on players.id = view_losers.player_id
    order by wins desc;
