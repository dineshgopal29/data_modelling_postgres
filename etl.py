import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import random
import string


def process_song_file(cur, filepath):
    
    """
     process_song_file(cur, filepath), takes in JSON log filepath and parse the data for each file and stores it ina dataframe. 
     The dataframe is then used to insert into song and artist tables
    """
    
    # open song file
    df= pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    
    """
     process_log_file(cur, filepath)
     takes in JSON log filepath and parse the data for each file and stores it ina dataframe
     
     The dataframe is then used to insert into user,time and songsplay tables
    """
        
    # open log file
    df= pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    ## pandas recognizes your format
    df['date'] =  pd.to_datetime(df['ts']) 
    #df['time'] = df['date'].dt.time
    df['time'] = df['date']
    df['hour'] = df['date'].dt.hour
    df['day'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.weekofyear
    df['month'] = df['date'].dt.month
    df['year_from_ts'] = df['date'].dt.year
    df['weekday'] = df['date'].dt.weekday
    
    
    
    t = df[['ts','date','time','hour','day','weekofyear','month','year_from_ts','weekday']]
    
    # insert time data records
    #time_data = 
    #column_labels = 
    time_df = t[['date','hour','day','weekofyear','month','year_from_ts','weekday']]

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.time,row.userId, row.level,songid, artistid,row.sessionId, row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    
    """
     process_data(cur, conn, filepath, func)
     takes in the databse cursor, connection and root folder path
     and loops through the folder directory 
     and get the file paths for all the JSON log files
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()