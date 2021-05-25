"""
COMP90024 2021 Semester 2 Assignment 2
Group 52
William Lazarus Kevin Dean 834444 Melbourne, Australia
Kenneth Huynh 992680 Melbourne, Australia
Joel Kenna 995401 Melbourne, Australia
Quinten van der Leest 1135216 Melbourne, Australia
Walter Zhang 761994 Melbourne, Australia

"""

from flask import Flask, request
import time
import couchdb
import argparse
import json

app = Flask(__name__)

# note: not thread-safe but can do because we're running with only 1 thread
# to ensure sequential processing
class DataStore():
    def __init__(self, args):
        DataStore.args = args

        with open(args['keys']) as creds_json:
            creds = json.load(creds_json)
        with open(args['config']) as config_json:
            config = json.load(config_json)
        
    
        DataStore.batch_size = args['batch_size']

        # connect to database
        
        db_user = creds["database"]["user"]
        db_pwd = creds["database"]["pword"]
        db_host = creds["database"]["host"]
        db_port = creds["database"]["port"]

        db_url = "http://" + db_user + ":" + db_pwd + "@" + db_host + ":" + db_port + "/"

        DataStore.cs = couchdb.Server(db_url)

        DataStore.user_db_name = config["DB"]["user_db_name"]

        if DataStore.user_db_name in DataStore.cs:
            DataStore.user_db = DataStore.cs[DataStore.user_db_name]
        else:
            DataStore.user_db = DataStore.cs.create(DataStore.user_db_name)

        # since we're starting up this server, anything currently marked as 'queued'
        # can be set to not crawled again (since no crawlers should be running before the server 
        # delegate ids)
        for doc in DataStore.user_db.find({'selector': {'crawled': "QUEUED"}}):
            doc["crawled"] = "NOT_CRAWLED"
            DataStore.user_db.save(doc)


@app.route("/", methods=['POST', 'GET'])
def get_user_batch():
    ret_dict = {}
    user_ids = []
    for doc in DataStore.user_db.find({'selector': {'crawled': "NOT_CRAWLED"}, 'limit': DataStore.batch_size}):
        # add user id to batch
        user_ids.append((doc['_id']))
        # set crawled to "queued" if it's a post request; otherwise we're just showing the results and not processing them
        if request.method == 'POST':
            doc["crawled"] = "QUEUED"
            DataStore.user_db.save(doc)
    
    ret_dict["user_ids"] = user_ids

    return ret_dict

def get_args():
    parser = argparse.ArgumentParser(description='Run user id dispatch server',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config', metavar='config', type=str,
                        required=True, help='Specify (path to and incl.) config file')
    parser.add_argument('-k', '--keys', metavar='keys', type=str, required=True,
                        help='Specify (path to and incl.) credentials/keys file')
    parser.add_argument('-bs', '--batch_size', metavar='batch_size', type=int, required=False, default=50,
                        help='Specify uid batch size (default 50)')

    return vars(parser.parse_args())

if __name__ == '__main__':
    args = get_args()

    DataStore(args)
    with open(args['keys']) as creds_json:
        creds = json.load(creds_json)
        port = creds["user_server"]["port"]
        
    app.run(threaded=False, port=port, host="0.0.0.0")