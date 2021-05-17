import couchdb

#connect to couchdb server
print("Connecting to CouchDB Server")
database = couchdb.Server('http://testuser:testpass@172.26.131.226:5984/')

print("create new database if necessary")
database.create('test123')

#select database
print(database)
print("Selecting Database")
tweetdb = database['test123']

#save document to database
testdoc = {'tweet_title': 'AAA', 'tweet_body': '123'}

print("Saving document to DB")
tweetdb.save(testdoc)

#create mango search query
mangoquery = {
				'fields': ['_id', 'tweet_title', 'tweet_body'], 
				'selector': {'tweet_title': {'$eq':'AAA'}}
			}
#retrieve results

print("Retrieving Results")
results = tweetdb.find(mangoquery)
for row in results:
  print(row)