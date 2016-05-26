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

create table tournaments(
    tournament_id serial primary key,
    name text not null
);

create table players(
    id serial primary key,
    tournament_id integer references tournaments(tournament_id) on delete cascade,
    name text not null
);

create table matches(
    match_id serial primary key,
    tournament_id integer references tournaments(tournament_id) on delete cascade,
    winner integer references players(id),
    loser integer references players(id)
);

create view view_winners as
    select winner, count(winner) as won
    from matches
    group by winner
    order by won desc;

create view view_losers as
    select loser, count(loser) as lost
    from matches
    group by loser
    order by lost desc;

create view standings as
    select players.id, players.name, coalesce(view_winners.won,0) as wins,
    coalesce(view_winners.won,0) + coalesce(view_losers.lost,0) as matches,
    players.tournament_id
    from (players left join view_winners on players.id = view_winners.winner)
    left join view_losers on players.id = view_losers.loser
    order by wins desc;
