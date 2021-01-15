# Project: Data Modeling with Postgres

## Problem Statement
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Project Description
In this project, you'll apply what you've learned on data modeling with Postgres and build an ETL pipeline using Python. To complete the project, you will need to define fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.

## Project Goal
The goal is to create a datastore for Sparkify analytics team to help them perform analytics to track listening patterns to understand their customers and songs trends and to help them improve the app.

## Project Steps

### Step 1: Data Review
Sparkify collects two types of data in JSON format
* Song Metadata
* User Activity Metadata

Upon review, the collected data can be divided into high level categories like 
* User Related Data - User activity, location, action performed, user type etc...
* Song Related Data - Duration, title, albums etc..
* Artist Related Data - Name, song title, location etc.. 

The high level categories will be used as reference for approaching the data modelling tasks

### Step 2: Data Model and Desing

We will be using the **STAR Schema** to perform our data model and design. The **Fact table** will be focused on the queries that will be requried for the analytics team for their analysis. We will desing the table in a way where the team can get the requried data and also will be able to access the related information. The Fact table will contain the keys to other dimension tables that can further be used by the anlytics team for their queries. The dimension tables will be designed and created based on the different categories identified in Step 1 during the initial analysis phase.

Final List of Tables will be as follows:
* songplay Table -  Will be used for analytical queries, will contain a snapshot of user activity and song detials 
* users Table - Will contain all user related details 
* songs Table - Will contain all songs related details 
* artists Table - Will contain all artist related details 
* time Table - Will have timestamp, data, year, week  etc... 


### Step 3: Create ETL Pipeline and Store Data
Once we have the data model created, we will move on to get the data from the log files to the database tables for querying the information. 

The log files are of two types:
* songs data
* user data

#### Data Description
**songs_data** JSON log files contain metadata information of all the songs listened using the apps. Sample format below

{
"num_songs": 1,
"artist_id": "ARJIE2Y1187B994AB7",
"artist_latitude": null,
"artist_longitude": null,
"artist_location": "",
"artist_name": "Line Renaud",
"song_id": "SOUPIRU12A6D4FA1E1",
"title": "Der Kleine Dompfaff",
"duration": 152.92036,
"year": 0
}

**user_log_data** JSON log files contain metadata information of all the songs listened using the apps. Sample format below

{
  "artist": "Survivor",
  "auth": "Logged In",
  "firstName": "Jayden",
  "gender": "M",
  "itemInSession": 0,
  "lastName": "Fox",
  "length": 245.36771,
  "level": "free",
  "location": "New Orleans-Metairie, LA",
  "method": "PUT",
  "page": "NextSong",
  "registration": 1541033612796,
  "sessionId": 100,
  "song": "Eye Of The Tiger",
  "status": 200,
  "ts": 1541110994796,
  "userAgent": "\"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36\"",
  "userId": "101"
}


#### ETL Pipeline Process
The database tables created in the step above will be used to store the information retrieved from the log files. We will create a python script using panda libraries to extract the data from the log files.

##### ETL Script Process Flow
* Retreive the file path for the log files
* Parse the data from the JSON log file
* Store the data in a pandas dataframe
* Create database connection and cursor objects
* Inser the data parsed from the log file
* Repeat the process for all the files

The fact table contains information about songs, artist and the metadata related to the user type and song duration. We will be using JOINS on songs and artisits tables to get iDs and other data based on the name, duration and title of the song as they are the common data avaibale in the user activity logs that can be used to match the song details.

We will be using a combination of the data set and JOIN queries to get the data for songplay table which will be used by the analytics team.


### Step 4: Run Analytical Queries
Using the **songsplay table**, the analytics team can run analysis on the user activity to identify the songs trending among the customer base. Some of the queries can be as follows

* Most popular song amoung the user base 
* Song trends or popularity by location
* User activity profile
* Most popular artist, alumbums 
* Song trends depending on the month or day of the year 