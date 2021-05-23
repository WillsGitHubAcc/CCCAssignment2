import dateutil.parser
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sanitise_v1_result(line_dict):
    """
    sanitise_v1_result takes the raw result fetched from the v1.1 API (realtime
    streaming API and v1.1 search) and returns a cleaned tweet dict
    """
    out_dict = {}

    # get creation time as timestamp in seconds
    datestring = line_dict['created_at']
    timestamp = dateutil.parser.parse(datestring).timestamp()
    out_dict['created_at'] = timestamp
    out_dict['created_at_hour_utc'] = datetime.datetime.utcfromtimestamp(timestamp).strftime("%H")
    out_dict['created_at_hour_aest'] = datetime.datetime.fromtimestamp(timestamp).strftime("%H")

    # get id, source, geo, entities, lang, place directly
    out_dict['id'] = str(line_dict['id'])
    out_dict['geo'] = line_dict['geo']
    out_dict['source'] = line_dict['source']
    out_dict['lang'] = line_dict['lang']
    out_dict['place'] = line_dict['place']
    out_dict['entities'] = line_dict['entities']

    # check if truncated and get full text
    if line_dict['truncated']:
        # if using search, even if truncated, the tweets might not have the extended field.
        # Can make it search and get the full text, or we just ignore it and use the truncated (easier)
        if 'extended_tweet' in line_dict:
            out_dict['text'] = line_dict['extended_tweet']['full_text']
        else:
            out_dict['text'] = line_dict['text']
    else:
        out_dict['text'] = line_dict['text']

    # using the text we just got, calculate sentiment score
    analyser = SentimentIntensityAnalyzer()
    out_dict['sentiment'] = analyser.polarity_scores(out_dict['text'])['compound']

    # get user fields
    user_dict = {}
    user_dict['id'] = str(line_dict['user']['id'])
    user_dict['username'] = line_dict['user']['screen_name']
    user_dict['location'] = line_dict['user']['location']
    user_dict['verified'] = line_dict['user']['verified']
    user_dict['followers_count'] = line_dict['user']['followers_count']
    user_dict['friends_count'] = line_dict['user']['friends_count'] 
    user_dict['statuses_count'] = line_dict['user']['statuses_count']
    user_dict['lang'] = line_dict['lang']

    out_dict['user'] = user_dict

    return out_dict

def sanitise_v2_result(line_dict):
    """
    sanitise_v2_result takes the raw result fetched from the v2 API (timeline
    search API, search recent and all) based off a user ID and returns a list of cleaned tweet dicts
    """
    out_dicts = []
    user_dict = {}
    places = []

    # get user fields from end of query
    user_dict['id'] = line_dict['includes']['users'][0]['id']
    user_dict['username'] = line_dict['includes']['users'][0]['username']
    user_dict['verified'] = line_dict['includes']['users'][0]['verified']
    user_dict['followers_count'] = line_dict['includes']['users'][0]['public_metrics']['followers_count']
    user_dict['friends_count'] = line_dict['includes']['users'][0]['public_metrics']['following_count']
    user_dict['statuses_count'] = line_dict['includes']['users'][0]['public_metrics']['tweet_count']

    # these fields might not be included
    if "lang" in line_dict['includes']['users'][0]:
        user_dict['lang'] = line_dict['includes']['users'][0]['lang']
    else:
        user_dict['lang'] = None
    
    if "location" in line_dict['includes']['users'][0]:
        user_dict['location'] = line_dict['includes']['users'][0]['location']
    else:
        user_dict['location'] = None

    # extract places (might not be included)
    if 'places' in line_dict['includes']:
        for place in line_dict['includes']['places']:
            places.append(place)

    # create analyser to use for text sentiment analysis on all tweets
    analyser = SentimentIntensityAnalyzer()

    # iterate through each tweet fetched
    for tweet in line_dict['data']:
        out_dict = {}
        # start by checking if this tweet has any location data. If not, then skip
        if "geo" in tweet:
            if "coordinates" in tweet['geo']:
                geo_dict = tweet['geo']['coordinates']
                out_dict['geo'] = geo_dict
            else:
                out_dict['geo'] = None

            # get place by looking up id with list of places
            place_id = tweet['geo']['place_id']

            for place in places:
                if place['id'] == place_id:
                    out_dict['place'] = place
                    break
                else:
                    out_dict['place'] = None
            
        else:
            out_dict['geo'] = None
            out_dict['place'] = None


        # get id
        out_dict['id'] = tweet['id']
        
        # get timestamp
        datestring = tweet['created_at']
        timestamp = dateutil.parser.parse(datestring).timestamp()
        out_dict['created_at'] = timestamp
        out_dict['created_at_hour_utc'] = datetime.datetime.utcfromtimestamp(timestamp).strftime("%H")
        out_dict['created_at_hour_aest'] = datetime.datetime.fromtimestamp(timestamp).strftime("%H")

        # get text, source, lang directly
        out_dict['text'] = tweet['text']
        out_dict['source'] = tweet['source']
        out_dict['lang'] = tweet['lang']
        
        # using the text we just got, calculate sentiment score
        out_dict['sentiment'] = analyser.polarity_scores(out_dict['text'])['compound']

        # get entities (might not be included)
        if "entities" in tweet:
            out_dict['entities'] = tweet['entities']
        else:
            out_dict['entities'] = []

        out_dict['user'] = user_dict

        out_dicts.append(out_dict)
    
    return out_dicts