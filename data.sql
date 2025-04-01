--Create Table--
DROP TABLE IF EXISTS spotify;
CREATE TABLE spotify (
    artist VARCHAR(255),
    track VARCHAR(255),
    album VARCHAR(255),
    album_type VARCHAR(50),
    danceability FLOAT,
    energy FLOAT,
    loudness FLOAT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    duration_min FLOAT,
    title VARCHAR(255),
    channel VARCHAR(255),
    views FLOAT,
    likes BIGINT,
    comments BIGINT,
    licensed BOOLEAN,
    official_video BOOLEAN,
    stream BIGINT,
    energy_liveness FLOAT,
    most_played_on VARCHAR(50)
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
select max(duration_min) from spotify;
select min(duration_min) from spotify;

--6. Delete the song where duration is zero.
delete from spotify
where duration_min = 0;

-----------------------Easy Category-------------------

--1.Retrieve the names of all tracks that have more than 1 billion streams
select track from spotify
where stream > 1000000000;

--2.List all albums along with their respective artists.
select album,artist
from spotify;

--3.Get the total number of comments for tracks where licensed = TRUE.
select Sum(comments) as total_comment
from spotify
where licensed = True;

--4.Find all tracks that belong to the album type single.
select track from spotify
where album_type = 'single';

--5.Count the total number of tracks by each artist.
select count(track) as total_no_counts,artist from spotify
group by artist
order by total_no_counts desc

------------------------Medium level-------------------

--1.Calculate the average danceability of tracks in each album.
select album, avg(danceability) as avg_danceability from spotify
group by album
order by avg_danceability desc

--2.Find the top 5 tracks with the highest energy values.
select distinct track,energy from spotify
order by energy desc
limit 5

--3.List all tracks along with their views and likes where official_video = TRUE
select track,sum(views) as total_views,sum(likes) as total_likes
from spotify
where official_video = 'TRUE'
group by track
order by total_views desc;

--4.For each album, calculate the total views of all associated tracks.
select album,track,sum(views) as total_views
from spotify
group by album,track
order by total_views desc

--5.Retrieve the track names that have been streamed on Spotify more than YouTube.
select * from(select track,
coalesce(sum(case when most_played_on = 'Youtube' then stream END),0) as streamed_on_youtube,
coalesce(sum(case when most_played_on = 'Spotify' then stream END),0) as streamed_on_Spotify
from spotify
group by track) as t 
where streamed_on_Spotify > streamed_on_youtube
and streamed_on_youtube <> 0

--6.Find the top 3 most-viewed tracks for each artist using window functions?
with cte as (select artist,track,
sum(views) as total_views,
dense_rank() over(partition by artist order by sum(views) desc) as row_num
from spotify
group by artist ,track
order by 1,3 desc)
select artist,track,row_num
from cte
where row_num < 4;

