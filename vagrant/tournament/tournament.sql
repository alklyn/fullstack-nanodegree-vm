-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table tournament(
    id serial primary key,
    name text,
    start_date date,
    end_date date
)

create table players(
    id serial primary key,
    name text,
    surname text,
)

create table matches(
    tournament_id integer,
    player1_id integer,
    player2_id integer,
    player1_score integer,
    player2_score integer
)
