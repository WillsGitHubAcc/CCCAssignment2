from requests_oauthlib import OAuth1Session
import couchdb
import requests
import json
import time
import dateutil.parser
import datetime
import argparse
import sys

from tweet_sanitisers import *

class TwitterHarvester():
    def __init__(self, credentials, config):
        self.creds = credentials
        self.config = config

        self.load_twitter_api_info()
        self.connect_to_db()        
        
    # initialisation methods
    def load_twitter_api_info(self):
        """
        load_twitter_api_info loads in api keys and credentials from the creds json
        """
        # load in twitter api key stuff from creds
        self.key = self.creds["twitter"]["twitter_key"]
        self.secret = self.creds["twitter"]["twitter_secret"]
        self.token = self.creds["twitter"]["twitter_token"]
        self.token_secret = self.creds["twitter"]["twitter_token_secret"]
        self.bearer = self.creds["twitter"]["twitter_bearer"]

    def connect_to_db(self):
        """
        connect_to_db loads in couchdb credentials and info from config and creds
        and creates a 'connection' to the database specified in the config
        """
        # load in couchdb stuff from config and creds
        db_config = self.config["DB"]
        db_user = self.creds["database"]["user"]
        db_pw = self.creds["database"]["pword"]
        db_host = self.creds["database"]["host"]
        db_port = self.creds["database"]["port"]

        db_url = "http://" + db_user + ":" + db_pw+ "@" + db_host + ":" + db_port + "/"
        
        self.couchserver = couchdb.Server(db_url)

        db_name = db_config["db_name"]
        user_db_name = db_config["user_db_name"]

        # load database connection. if database doesn't exist, create one
        if db_name in self.couchserver:
            self.db = self.couchserver[db_name]
        else:
            self.db = self.couchserver.create(db_name)

        if user_db_name in self.couchserver:
            self.user_db = self.couchserver[user_db_name]
        else:
            self.user_db = self.couchserver.create(user_db_name)
            # create index
            idx = self.user_db.index()
            idx['ddoc_crawled_idx', 'crawled_idx'] = ['crawled']

    # tweet fetching methods
    def get_tweets_from_filtered_stream(self):
        """
        get_tweets_from_filtered_stream pulls tweets from the v1.1 Twitter
        filtered streaming API and inputs them into the couchDB
        """
        location_str = self.get_bounds_from_config(config)

        params = {
            'locations': location_str
        }

        print("Getting tweets in box: {}".format(location_str))

        # this will be continuously called while the session is open
        while True:
            try:
                # initialise session with streaming API
                s = OAuth1Session(self.key, client_secret=self.secret, resource_owner_key=self.token, resource_owner_secret=self.token_secret)
                r = s.get(self.config["URLs"]["filter_stream"], params=params, stream=True)

                for line in r.iter_lines():
                    # when a tweet has been received
                    if line:
                        # TODO: do some processing before inserting into db
                        line_dict = json.loads(line)

                        cleaned_result = sanitise_v1_result(line_dict)

                        # insert tweet and user to database
                        self.insert_tweet_to_db(cleaned_result)
                        self.insert_user_to_db(cleaned_result["user"]["id"], cleaned_result["user"]["username"])
            except:
                # something went wrong, go back and try again
                print("Something went wrong! Trying again")

    def get_tweets_from_users(self):
        """
        get_tweets_from_users gets a batch of user ids from user server and runs
        get_tweets_from_user_timeline for each user_id returned.
        Will continually run to ensure it continues crawling as new ids are added
        """
        while True:
            # get batch of user ids from user server
            user_id_queue = []
            r = requests.post("http://" + self.creds["user_server"]["ip"] + ":" + self.creds["user_server"]["port"])
            r_json = json.loads(r.text)
            for user_id in r_json["user_ids"]:
                user_id_queue.append(user_id)
            
            print("{} user ids in queue".format(len(user_id_queue)))
            # wait timer if no user ids are in the queue so it
            # doesn't thrash the database and compute resources
            if len(user_id_queue) == 0:
                time.sleep(30)
                continue

            for user_id in user_id_queue:
                self.get_tweets_from_user_timeline(user_id)



    def get_tweets_from_user_timeline(self, user_id):
        """
        get_tweets_from_user_timeline pulls tweets from a user's timeline (all
        tweets posted by them), given the user's id, and inputs them into the
        couchDB
        """
        print("\nPulling tweets from {}".format(user_id))

        # immediately mark user as being crawled
        self.mark_user_as_crawled(user_id, "CRAWLING")

        # get timeline crawling config
        timeline_config = self.config["timeline_config"]

        # get list of time periods to crawl (in ISO 8601 format)
        periods = self.get_time_periods(timeline_config["start_time"], 
                                        timeline_config["end_time"], 
                                        timeline_config["period_length"])

        headers = {
            'Authorization': 'Bearer ' + self.bearer
        }

        params = self.config["timeline_params"]

        for period in periods:
            params["start_time"] = period[0]
            params["end_time"] = period[1]

            n_counted = 0

            # loop for pagination
            more_pages = True
            while more_pages and n_counted < timeline_config["n_tweets_per_period"]:
                # note that the user_id param in the url has been stored with a {} so we 
                # can use the python default string format function to add the user_id
                r = requests.get(self.config["URLs"]["user_timeline"].format(user_id), headers=headers, params=params)

                # using pagination, continue pulling tweets with pagination token
                # tweet results are given from most recent to least, so next page
                # will go back in time

                try:
                    line_dict = json.loads(r.text)
                except json.JSONDecodeError:
                    print("JSONDecodeError in get_tweets_from_user_timeline")
                    print("r.text")

                if "meta" in line_dict:
                    if "next_token" in line_dict["meta"]:
                        # set next token in params
                        params["pagination_token"] = line_dict["meta"]["next_token"]
                        # print("more pages!")
                    else:
                        # no more pages
                        more_pages = False
                        # print("no more pages")
                    
                    # check number of results. If there were no results, move on
                    # by breaking out of the pagination loop and move onto next period
                    if "result_count" in line_dict["meta"]:
                        if line_dict["meta"]["result_count"] == 0:
                            # print("no results for specified user/period")
                            print("In period {}, counted {} tweets".format(period, 0), end='\r')
                            break
                        else:
                            n_counted += line_dict["meta"]["result_count"]
                            print("In period {}, counted {} tweets".format(period, n_counted), end='\r')
                else:
                    more_pages = False

                try:
                    cleaned_tweets = sanitise_v2_result(line_dict)
                except KeyError:
                    print("Key Error!")
                    print(line_dict)

                for tweet in cleaned_tweets:
                    self.insert_tweet_to_db(tweet)
            
            # add this time period to user db
            self.mark_user_as_crawled(user_id, "CRAWLING", period)
        
        # finished crawling this user's tweets: set as crawled in db
        self.mark_user_as_crawled(user_id, "CRAWLED", (timeline_config["start_time"], timeline_config["end_time"]))

    def get_tweets_from_search_v1(self):
        """
        get_tweets_from_search_v1 uses the Twitter v1.1 API to perform a search
        on a given query, and inputs them into the CouchDB. The query is 
        specified as a parameter in the config file. Note that this endpoint is
        available with the standard API, but is limited to the last 7 days.
        """
        params = self.config["search1_params"]

        print("Using v1.1 API with query: {}".format(params['q']))

        s = OAuth1Session(self.key, client_secret=self.secret, resource_owner_key=self.token, resource_owner_secret=self.token_secret)
        r = s.get(self.config["URLs"]["tweet_search_1.1"], params=params)

        try:
            line_dict = json.loads(r.text)
        except json.JSONDecodeError:
            print("JSONDecodeError in get_tweets_from_search_v1")
            print("r.text")
        # print(r.text)

        for tweet in line_dict['statuses']:
            cleaned_tweet = sanitise_v1_result(tweet)
            self.insert_tweet_to_db(cleaned_tweet)
            self.insert_user_id_to_db(cleaned_tweet["user"]["id"])


    def get_tweets_from_search_v2_recent(self):
        """
        get_tweets_from_search_v2_recent uses the Twitter v2 API to perform a search
        on a given query, and inputs them into the CouchDB. The query is 
        specified as a parameter in the config file. Note that this endpoint 
        is available with the standarad API, but is limited to the last 7 days.
        """
        params = self.config["search2recent_params"]

        print("Using v2 API for RECENT search with query: {}".format(params['query']))

        headers = {
            'Authorization': 'Bearer ' + self.bearer
        }

        # continue looping for paginated results
        more_pages = True
        while more_pages:
            r = requests.get(self.config["URLs"]["tweet_search_2_recent"], headers=headers, params=params)

            # check for rate limit
            while r.status_code == 429:
                self.handle_rate_limit(r)
                # request again
                r = requests.get(self.config["URLs"]["tweet_search_2_recent"], headers=headers, params=params)

            try:
                line_dict = json.loads(r.text)
            except json.JSONDecodeError:
                print("JSONDecodeError in get_tweets_from_search_v2_recent")
                print("r.text")

            if "meta" in line_dict:
                if "next_token" in line_dict["meta"]:
                    # set next token in params
                    params["next_token"] = line_dict["meta"]["next_token"]
                    print("more pages!")
                else:
                    # no more pages
                    more_pages = False
                    print("no more pages")
            else:
                more_pages = False

            cleaned_tweets = sanitise_v2_result(line_dict)

            for tweet in cleaned_tweets:
                self.insert_tweet_to_db(tweet)
                self.insert_user_to_db(tweet["user"]["id"], tweet["user"]["username"])

    def get_tweets_from_search_v2_all(self):
        """
        get_tweets_from_search_v2_recent uses the Twitter v2 API to perform a search
        on a given query, and inputs them into the CouchDB. The query is 
        specified as a parameter in the config file. Note that this endpoint 
        is only available for the academic research track.
        """
        params = self.config["search2all_params"]

        print("Using v2 API for ALL search with query: {}".format(params['query']))

        headers = {
            'Authorization': 'Bearer ' + self.bearer
        }

        # continue looping for paginated results
        more_pages = True
        while more_pages:
            r = requests.get(self.config["URLs"]["tweet_search_2_all"], headers=headers, params=params)

            # check if authorised
            if r.status_code == 403:
                print("Unauthorised endpoint access -- only available to Academic Research track")
                exit()

            # check for rate limit
            while r.status_code == 429:
                self.handle_rate_limit(r)
                # request again
                r = requests.get(self.config["URLs"]["tweet_search_2_recent"], headers=headers, params=params)

            try:
                line_dict = json.loads(r.text)
            except json.JSONDecodeError:
                print("JSONDecodeError in get_tweets_from_search_v2_recent")
                print("r.text")

            if "meta" in line_dict:
                if "next_token" in line_dict["meta"]:
                    # set next token in params
                    params["next_token"] = line_dict["meta"]["next_token"]
                    print("more pages!")
                else:
                    # no more pages
                    more_pages = False
                    print("no more pages")
            else:
                more_pages = False

            cleaned_tweets = sanitise_v2_result(line_dict)

            for tweet in cleaned_tweets:
                self.insert_tweet_to_db(tweet)
                self.insert_user_to_db(tweet["user"]["id"], tweet["user"]["username"])

    def get_id_from_username(self, username):
        """
        get_id_from_username takes in a unique twitter handle and returns
        the user's unique id. Uses the v2 API. Will return False if no id is found
        """
        # start by checking if the username is in the database already
        user_ids = []
        for doc in self.user_db.find({'selector': {'username': username}}):
            user_ids.append(doc['_id'])

        if len(user_ids) != 0:
            return user_ids[0]

        # otherwise, ask Twitter for user id
        headers = {
            'Authorization': 'Bearer ' + self.bearer
        }

        r = requests.get(self.config["URLs"]["user_lookup"].format(username), headers=headers)
        
        # check for rate limit
        while r.status_code == 429:  
            self.handle_rate_limit(r)
            # request again
            r = requests.get(self.config["URLs"]["user_lookup"].format(username), headers=headers)

        try:
            line_dict = json.loads(r.text)
        except json.JSONDecodeError:
            print("JSON decode error!")
            print(r.text)

        if "data" in line_dict:    
            return line_dict["data"]["id"]
        else:
            print("id not found for username {}".format(username))
            return False

    def handle_rate_limit(self, r):
        # get remaining time until window resets
        reset_time = int(r.headers["x-rate-limit-reset"])
        time_left = reset_time - time.time()
        print("Rate limited for another {} seconds".format(time_left))

        # wait until time_left
        time.sleep(time_left)

    # communicating with database
    def insert_tweet_to_db(self, cleaned_tweet_dict):
        """
        insert_tweet_to_db inserts the cleaned_tweet_dict into the couchDB
        """
        # print(cleaned_tweet_dict)

        # check if tweet is already in db
        doc = self.db.get(cleaned_tweet_dict['id'], default=False)

        # if tweet is not found, then add it
        if doc == False:
            print("Inserting new tweet {}".format(cleaned_tweet_dict['id']))
            # get all @mention's ids to add to user_ids 
            if "entities" in cleaned_tweet_dict:
                # for v1.1 api, it's 'user_mentions'
                if "user_mentions" in cleaned_tweet_dict["entities"]:
                    for user in cleaned_tweet_dict["entities"]["user_mentions"]:
                        self.insert_user_to_db(user["id"], user["screen_name"])
                # for v2 api, it's 'mentions'
                elif "mentions" in cleaned_tweet_dict["entities"]:
                    for user in cleaned_tweet_dict["entities"]["mentions"]:
                        user_id = self.get_id_from_username(user["username"])

                        if user_id != False:
                            self.insert_user_to_db(user_id, user["username"])

            # insert into database as new document with id set to tweet id
            cleaned_tweet_dict['_id'] = cleaned_tweet_dict['id']
            self.db.save(cleaned_tweet_dict)

    def insert_user_to_db(self, user_id, username):
        """
        insert_user_to_db checks if a user id has been added to the db first,
        then inserts the user_id into the db if it hasn't, alongside its 'crawled' status
        (which is False if it's the first time we're considering this user id). 
        """

        # will try to get the doc with the user id (as doc id). If it's not found
        # (desired), will return False
        doc = self.user_db.get(user_id, default=False)

        if doc == False:
            user_dict = {
                "_id": user_id,
                "crawled": "NOT_CRAWLED",
                "username": username,
                "crawled_periods": [],
                "crawling_periods": []
            }

            self.user_db.save(user_dict)

    def mark_user_as_crawled(self, user_id, status, crawled_period=None):
        """
        mark_user_as_crawled marks a user id's status as "crawled" after
        their timeline has been crawled. The user id should always be found.
        Also adds the period of time in which the user's tweets have been crawled 
        (tuple of timestamps (start, end))
        """
        
        # will try to get the doc with the user id (as doc id). If it's not found,
        # (undesired), will defaultly return False
        doc = self.user_db.get(user_id, default=False)

        if doc != False:
            doc["crawled"] = status
            if crawled_period != None:
                # convert to timestamps
                start_timestamp = dateutil.parser.parse(crawled_period[0]).timestamp()
                end_timestamp = dateutil.parser.parse(crawled_period[1]).timestamp()

                if status == "CRAWLED":
                    # add to doc
                    curr_periods = doc["crawled_periods"]
                    curr_periods.append((start_timestamp, end_timestamp))
                    doc["crawled_periods"] = curr_periods

                    # remove crawling periods
                    doc["crawling_periods"] = []
                elif status == "CRAWLING":
                    # add to doc
                    curr_periods = doc["crawling_periods"]
                    curr_periods.append((start_timestamp, end_timestamp))
                    doc["crawling_periods"] = curr_periods

            self.user_db.save(doc)

    # util methods
    def get_bounds_from_config(self, config):
        """
        get_bounds_from_config converts the list of bounds inside the config 
        to the desired locations string that the Twitter API would like
        """
        # load bounding boxes from config
        location_str = ""
        for box in self.config["bounds"]:
            location_str = location_str + box + ","

        # remove trailing comma
        location_str = location_str[:-1]

        return location_str

    def get_time_periods(self, start_time, end_time, period_length):
        """
        get_time_periods takes in a time period (start date, end date) in ISO 8601
        and a period length (in seconds) and outputs a list of ISO 8601 tuples 
        making up that time period, each of length period_length. Rounds up
        """
        periods = []

        # get start time/end time in epoch time
        start_timestamp = dateutil.parser.parse(start_time).timestamp()
        end_timestamp = dateutil.parser.parse(end_time).timestamp()

        time_cursor = start_timestamp
        while time_cursor < end_timestamp:
            period_start = datetime.datetime.utcfromtimestamp(time_cursor).isoformat() + 'Z'
            period_end = datetime.datetime.utcfromtimestamp(time_cursor + period_length).isoformat() + 'Z'

            period = (period_start, period_end)

            periods.append(period)

            time_cursor = time_cursor + period_length

        return periods

def get_args():
    """
    get_args uses the argparse library to parse command line arguments. Returns
    a dictionary with argument name as key, value as provided value on command line
    """
    parser = argparse.ArgumentParser(description='Pull tweets using the Twitter API',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-m', '--mode', metavar='mode', type=str, default="stream",
                        help='Specify harvesting mode: stream, users, search1, search2recent, search2all')    

    return vars(parser.parse_args())

def main(credentials, config, args):
    th = TwitterHarvester(credentials, config)

    if args['mode'] == 'stream':
        th.get_tweets_from_filtered_stream()
    elif args['mode'] == 'users':
        # th.get_tweets_from_user_timeline(65869538)
        # th.get_tweets_from_user_timeline(17587297)
        th.get_tweets_from_users()
    elif args['mode'] == 'search1':
        th.get_tweets_from_search_v1()
    elif args['mode'] == 'search2recent':
        th.get_tweets_from_search_v2_recent()
    elif args['mode'] == 'search2all':
        th.get_tweets_from_search_v2_all()
    else:
        # invalid mode
        print("Invalid harvesting mode specified")
        # print("{}".format(th.get_time_periods("2011-01-01T00:00:01Z", "2011-02-07T00:00:01Z", 604800)))


if __name__ == '__main__':
    # read in command line arguments
    args = get_args()

    # load config variables
    with open('config.json') as json_file:
        config = json.load(json_file)
    
    # load credentials
    with open('credentials.json') as json_file:
        credentials = json.load(json_file)

    main(credentials, config, args)