from flask import Flask, request
import time
import couchdb
import json

app = Flask(__name__)

# note: not thread-safe but can do because we're running with only 1 thread
# to ensure sequential processing
class DataStore():
    batch_size = 50

    # connect to database
    with open("credentials.json") as creds_json:
        creds = json.load(creds_json)
    with open("config.json") as config_json:
        config = json.load(config_json)
    
    
    db_user = creds["database"]["user"]
    db_pwd = creds["database"]["pword"]
    db_host = creds["database"]["host"]
    db_port = creds["database"]["port"]

    db_url = "http://" + db_user + ":" + db_pwd + "@" + db_host + ":" + db_port + "/"

    cs = couchdb.Server(db_url)

    user_db_name = config["DB"]["user_db_name"]

    if user_db_name in cs:
        user_db = cs[user_db_name]
    else:
        user_db = cs.create(user_db_name)


@app.route("/", methods=['POST', 'GET'])
def get_user_batch():
    ret_dict = {}
    user_ids = []
    for doc in DataStore.user_db.find({'selector': {'crawled': "NOT_CRAWLED"}, 'limit': DataStore.batch_size}):
        # add user id to batch
        user_ids.append(int(doc['_id']))
        # set crawled to "queued" if it's a post request; otherwise we're just showing the results and not processing them
        if request.method == 'POST':
            doc["crawled"] = "QUEUED"
            DataStore.user_db.save(doc)
    
    ret_dict["user_ids"] = user_ids

    return ret_dict

if __name__ == '__main__':
    DataStore()
    with open("credentials.json") as creds_json:
        creds = json.load(creds_json)
        port = creds["user_server"]["port"]
        
    app.run(threaded=False, port=port)