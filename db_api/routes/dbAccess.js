const axios = require('axios');
const Mutex = require('async-mutex').Mutex;
const lock = new Mutex();
const express = require('express');
const router = express.Router();

axios.defaults.baseURL =
  "http://dbuser:dibhd59lka@"
    + ("172.26.129.177")
    + ":5984";


// axios.defaults.baseURL =
//   "http://www.google.com"

/* GET bookings */
router.get('/', (req, res) => {
  // if we don't have a query
  console.log(req);
  if (Object.keys(req.query).length === 0) {
    axios.get("/users/3362312849")
      .then((response) => {
        res.send(response.data);
      }).catch(e => console.log(e));
      
  }else {
    // validate and convert query
    var query = {}
    var skip = req.query.skip == null ? 0 : parseInt(req.query.skip);
    var limit = req.query.limit == null ? 25 : parseInt(req.query.limit);
    if (req.query.flight_num != null) query.flight_num = req.query.flight_num;
    if (req.query.origin != null) query.origin = req.query.origin;
    if (req.query.dest != null) query.dest = req.query.dest;
    if (req.query.departure != null) query.departure = req.query.departure;
    if (req.query.arrival != null) query.arrival = req.query.arrival;
    if (req.query.price != null) query.price = req.query.price;

    // send query off
    axios.post("/flights/_find", data = {"selector": query, "skip": skip, "limit": limit}
      ).then((response) => {
        res.send(response.data.docs);
      }).catch(e => console.log(e));
  }
});

module.exports = router;
