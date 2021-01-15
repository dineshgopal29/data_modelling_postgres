# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""

CREATE TABLE IF NOT EXISTS songplays (
songplay_id SERIAL PRIMARY KEY, 
start_time TIMESTAMP NULL, 
user_id int NULL, 
level varchar NULL, 
song_id varchar NULL, 
artist_id varchar NULL, 
session_id int NULL, 
location varchar NULL, 
user_agent varchar NULL)


""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id int PRIMARY KEY, 
first_name varchar, 
last_name varchar, 
gender varchar, 
level varchar)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id varchar PRIMARY KEY NOT NULL, 
title varchar NOT NULL, 
artist_id varchar, 
year int, 
duration decimal
)

""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id varchar PRIMARY KEY NOT NULL, 
name varchar, 
location varchar, 
latitude decimal, 
longitude decimal)

""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time TIMESTAMP PRIMARY KEY NOT NULL, 
hour int, 
day int, 
week int, 
month int, 
year int, 
weekday int)
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time, 
user_id, 
level, 
song_id, 
artist_id, 
session_id, 
location, 
user_agent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
""")

user_table_insert = ("""
INSERT INTO users VALUES (%s, %s, %s, %s,%s) ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs VALUES (%s, %s, %s, %s,%s) ON CONFLICT (song_id) DO UPDATE SET title = EXCLUDED.title, artist_id = EXCLUDED.artist_id, \
year = EXCLUDED.year, duration = EXCLUDED.duration;
""")

artist_table_insert = ("""
INSERT INTO artists VALUES (%s, %s, %s, %s,%s) ON CONFLICT (artist_id) DO UPDATE SET name = EXCLUDED.name, location = EXCLUDED.location, \
latitude = EXCLUDED.latitude, longitude = EXCLUDED.longitude;
""")


time_table_insert = ("""
INSERT INTO time VALUES (%s, %s, %s, %s,%s,%s,%s) ON CONFLICT (start_time) DO UPDATE SET hour = EXCLUDED.hour, day = EXCLUDED.day, \
week = EXCLUDED.week, month = EXCLUDED.month,year= EXCLUDED.year,weekday= EXCLUDED.weekday;
""")

# FIND SONGS

song_select = ("""
select songs.song_id,artists.artist_id \
                FROM songs INNER JOIN artists \
                ON songs.artist_id = artists.artist_id WHERE songs.title =  %s AND artists.name = %s AND songs.duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]