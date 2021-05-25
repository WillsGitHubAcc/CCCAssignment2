# CCC Assignment 2 - Twitter Harvester
## Execution
``` 
python twitter_harvester.py -m <stream/users/search1/search2all/search2recent>
```

TwitterHarvester class has a method for each mode of tweet harvesting specified, with configuration available in the ```config.json``` file. Credentials are stored in ```credentials.json``` which has the following format:


```credentials.json```:
```
{
    "twitter": {
        "twitter_key": <insert API key>,
        "twitter_secret": <insert API key secret>,
        "twitter_token": <insert token>,
        "twitter_token_secret": <insert token secret>,
        "twitter_bearer": <insert bearer token> 
    },
    "database": {
        "user": <insert username>,
        "pword": <insert password>,
        "host": <insert host ip>,
        "port": <insert host port> 
    },
    "user_server" {
        "ip": <insert user dispatch server host ip>,
        "port": <insert user host port>
    }
}
```

Returned responses from the API are sanitised/processed in ```tweet_sanitisers.py``` into the desired format for insertion into the database.

Also stored in this folder is the user dispatch server, which has to be running in order for user timeline crawling to work. It uses Flask to host a HTTP server which allows for the user timeline crawlers to 'POST' to in order to obtain a batch of user ids to crawl. Can be run just as a standalone python script, i.e.
```
python user_dispatch_server.py
```

## Configuration
Notes about ```config.json```:
- ```bounds``` = list of bounding boxes used for filtering real time stream
- ```
    "timeline_config": {
        "n_tweets_per_period": <number of tweets we want per sub-period,
        "period_length": <length (in seconds) of sub-period>,
        "start_time": "2011-01-01T00:00:01Z" <i.e. start time in ISO 8601>,
        "end_time": "2011-05-05T00:00:01Z" <i.e. end time in ISO 8601>
    },
    ```
- search params: ```q``` = ```query``` = query used for search
    - ```geocode``` = specify centre coordinate and radius around it to get tweets
    - query uses operators defined on twitter api docs. Note that we are limited to standard operators (i.e. can't use location filtering)
- ```
    "DB": {
        "db_name": <name of document collection to deposit tweets into>,
        "user_db_name": <name of document collection to deposit user/ids/crawl history into>
    }
    ```
## Requirements
Non-standard Python libraries:
```
couchdb
Flask
```

## TODO
- get proper bounding boxes and test
- add index for user db --> username and crawled
- test geolocation filtering on user timeline crawled tweets
- containerise

## Done
- get tweets from a user's timeline
- get tweets from filtered real-time stream
- input data into database
- update the config with proper query stuff we want 
- process incoming tweet data into a format that we want to store as
- implement method to pull tweets with search queried terms via API
    - options: v1.1 search (not exhaustive), v2 search standard (past 6-9 days only), v2 search academic (all time, big load)
- command line argument specifying operation mode
- implemented separate database of userids
    - all user mentions are also added to this database
- implemented queueing and pulling system for user ids and user timeline crawling
- implement pagination for user timelines/search results
- rate limit handling -- just waits until rate limit period elapses
- test pagination for user timelines/search results
- set user timeline crawling to pull each (period length) over a time period instead of every tweet
- now using creds.json instead of .env for easier ansible vault integration
- should now only save tweets from user timelines that include geolocation
- user id dispatch server built and tested
- now pulls user id queue from user id dispatch server, which is not threaded meaning no duplication of user ids to crawl if multiple instances of user crawlers are running concurrently

## Assumptions/Things to note
- no longer pulling retweets (as they truncate tweets) from user history
- tweet creation time is saved as timestamp in seconds
- entities are not being parsed (the raw object is being submitted into the db)
- v2 with location field requires academic research account
    - specified in the query like ```'place_country:AU'```
- v1 uses location in query as a centre coordinate + radius

## Considerations/Notes
- bounding boxes around each major city or entire states?
- scenario: someone tweets 100 tweets a day. We want to get a sample of their tweets over a 2 month period. Problem: that's like 6000 tweets. Solution: we take the first 100 per week = 700 instead. Is this ok? Won't be representative but hopefully not everyone is a chronic tweeter
- dont have an academic research account -- most of our tweets should therefore be from user crawling
- location data is quite sparse -- don't think we can get down to the suburb level
- since search is probably not going to be used, the implementation isn't fully fleshed out
- not a lot of error handling has been written 
- probably should have used like tweepy but i didnt think about it when i started, oops sorry :(
- sorry that the code is messy hahah could use a refactor but probably not the highest priority