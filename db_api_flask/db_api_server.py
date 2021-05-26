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

        # connect to database
        
        db_user = creds["database"]["user"]
        db_pwd = creds["database"]["pword"]
        db_host = creds["database"]["host"]
        db_port = creds["database"]["port"]

        db_url = "http://" + db_user + ":" + db_pwd + "@" + db_host + ":" + db_port + "/"

        DataStore.cs = couchdb.Server(db_url)

        DataStore.graph_db_name = "graphs"
        DataStore.graph_db = DataStore.cs[DataStore.graph_db_name]

@app.route("/", methods=['GET'])
def get_graphs():
    doc_dict = {}
    for doc in DataStore.graph_db.view('_all_docs'):
        doc_dict[doc.id] = DataStore.graph_db[doc.id]

    return doc_dict

def get_args():
    parser = argparse.ArgumentParser(description='Run user id dispatch server',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-k', '--keys', metavar='keys', type=str, required=True,
                        help='Specify (path to and incl.) credentials/keys file')

    return vars(parser.parse_args())

if __name__ == '__main__':
    args = get_args()

    DataStore(args)
    with open(args['keys']) as creds_json:
        creds = json.load(creds_json)
        port = creds["db_server"]["port"]
        
    app.run(port=port, host="0.0.0.0")