-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- Use the command \i tournament.sql to import the whole file into psql at once.

/*
create table tournaments(
    id serial primary key,
    name text,
    start_date date,
    end_date date
);
*/

create table players(
    id serial primary key,
    name text
);

create table matches(
    player1_id integer references players(id),
    player2_id integer references players(id),
    player1_score integer,
    player2_score integer,
    primary key (player1_id, player2_id)
);
