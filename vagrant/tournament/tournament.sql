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
    winner integer references players(id),
    loser integer references players(id),
    primary key (winner, loser)
);

create view winners as
select players.id, players.name, count(matches.winner) as wins
from players
left join matches on players.id = matches.winner
group by players.id
order by wins desc;

create view losers as
select players.id, players.name, count(matches.loser) as losses
from players
left join matches on players.id = matches.loser
group by players.id
order by losses desc;

create view standings as
select winners.id, winners.name, winners.wins, winners.wins + losers.losses as played
from winners, losers
where winners.id = losers.id
order by winners.wins desc;

select p.id, p.name, p.wins, p.wins + coalesce(l.losses, 0) as played from
results
(
select loser, count(loser) as losses
from matches
group by loser
) as l on p.id = l.loser;
