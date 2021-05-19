//Refresher on contents of keys, values, etc.
//https://stackoverflow.com/questions/11743435/what-is-in-the-reduce-function-arguments-in-couchdb


//NOTE: this view hasn't yet been tested

//map
function(doc) {

	//create keys based on date to cover the case we want to filter on date etc. later
	emit(doc.created_at, doc)
}


//reduce
function (keys, values, rereduce) {
	
	//return vals
	ret.sum = 0
	ret.count = 0
	ret.hourarray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	
	
	//re-reduction step
	if (rereduce){
	
		//sum up total time and number of entries
		for (i in values) {
			sum += values.sum
			count += values.count
			
			//sum up date distribution
			for (let j = 0; j < 24; j++) {
				ret.hourarray[j] += ret.values[j]
			}
		}
		return ret
	}else{
		for (val in values) {
			ret.sum += val.time
			ret.count += 1
			
			//NOTE, Tweets should be modified before insertion to the database to have a "created_at_hours" field that only contains the UTC hour section (normalise to melbourne time then save the hours)
			//eg. Wed Oct 10 20:19:24 +0000 2018 is reduced to 20:19:24 (NOTE: this example does not normalise to melbourne time first)
			//This "created_at_hours" field should be in int form
			ret.hourarray[tweet.created_at_hours] += 1
		}
	}
	return ret
}