--Create Table--
DROP TABLE IF EXISTS spotify;
CREATE TABLE spotify (
    artist VARCHAR(255),
    track VARCHAR(255),
    album VARCHAR(255),
    album_type VARCHAR(50),
    title VARCHAR(255),
    );

-------------------EDA-------------------

--1.total count
select count(*) from spotify;

--2.How many artist?
select count(distinct artist) from spotify;

--3. How many album?
select count(distinct album) from spotify;

--4. Diiferent type of album_type?
select distinct album_type from spotify;

--5. find out maximum,minimum duration ?
-- Removed due to missing duration data

--6. Delete the song where duration is zero.
-- Removed due to missing duration data

-----------------------Easy Category-------------------

--1.List all albums along with their respective artists.
select album,artist
from spotify;

--2.Count the total number of tracks by each artist.
select count(track) as total_no_counts,artist from spotify
group by artist
order by total_no_counts desc;

--3. Lister les 10 morceaux les plus populaires
select track, popularity
from spotify
order by popularity desc
limit 10;

--4. Lister tous les morceaux d’un artiste spécifique (ex: TV Girl)
select track
from spotify
where artist = 'TV Girl';

------------------------Medium level-------------------

--3.Répartition des morceaux par année de sortie (en supposant que le champ title contient l'année ou une colonne 'release_year' existe)
-- Exemple avec colonne 'release_year'
select strftime('%Y', release_date) as year, count(*) as total_tracks
from spotify
where release_date is not null
group by year
order by year;

