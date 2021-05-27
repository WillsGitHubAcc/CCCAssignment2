const axios = require('axios');
const Mutex = require('async-mutex').Mutex;
const lock = new Mutex();
const express = require('express');
const router = express.Router();


    
const config = require('../src/credentials.json')
// console.log(config);

const url = "http://" + config["database"]["user"] + ":" + config["database"]["pword"] + "@" + config["database"]["host"] + ":" + config["database"]["port"]
// console.log(url);
axios.defaults.baseURL = url
// console.log(axios.defaults.baseURL);
// axios.defaults.baseURL =
//   "http://www.google.com"

/* GET bookings */
router.get('/', (req, res) => {
  // if we don't have a query
  // console.log(req);
  if (Object.keys(req.query).length === 0) {
    axios.get("/users/3362312849")
      .then((response) => {
        res.send(response.data);
      }).catch(e => console.log(e));
      
  }else {
    // validate and convert query
    var query = {}
    if (req.query.scenario != null) query.scenario = req.query.scenario;
    if (req.query.state != null) query.state = req.query.state;

    // console.log(query.state)
    // console.log(query.scenario)

    axios.get("/graphs/" + query.scenario ) 
    .then((response) => {
      // console.log(response.data);
      // console.log(response.data["hobart_elect"]);
      res.send(response.data[query.state]);
    }).catch(e => console.log(e));
    
  }
});

module.exports = router;
