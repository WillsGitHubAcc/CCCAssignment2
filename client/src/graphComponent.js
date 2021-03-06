// COMP90024 2021 Semester 2 Assignment 2
// Group 52
// William Lazarus Kevin Dean 834444 Melbourne, Australia
// Kenneth Huynh 992680 Melbourne, Australia
// Joel Kenna 995401 Melbourne, Australia
// Quinten van der Leest 1135216 Melbourne, Australia
// Walter Zhang 761994 Melbourne, Australia

import React from 'react';
import Plotly from "plotly.js-basic-dist";
import createPlotlyComponent from "react-plotly.js/factory";
import * as aurin_pets from "./aurin_pets.json";
import * as aurin_elect from "./aurin_elect.json";


export default function BasicTextFields(props) {


const config = require('./credentials.json')
// console.log(config);

const ip = config["db_server"]["ip"] ;
const port = config["db_server"]["port"] ;

  var state = props.type;
  var scenario = props.scenario;

  if(state==="wa"){
    state="perth";
  }
  if(state==="nt-mainland"){
    state="darwin";
  }
  if(state==="qld-mainland"){
    state="bris";
  }
  if(state==="sa-mainland"){
    state="adel";
  }
  if(state==="nsw"){
    state="sydney";
  }
  if(state==="vic"){
    state="melb";
  }
  if(state==="tas-mainland"){
    state="hobart";
  }
  if(state==="act"){
    state="canberra";
  }
  if(state==="aus"){
    state="aus";
  }
  state = state + "_" + scenario;
  if(scenario ==="sleep"){
    state = state +"_time";
  }

  var scenario = props.scenario;
  

  const Plot = createPlotlyComponent(Plotly);
  var [result, setResult] = React.useState();
  const [fetchResponse, setFetchResponse] = React.useState({"data":[],"layout":[]});

  const handleResponse = (data) => {
    console.log(data);
    setFetchResponse(data);
    
    console.log(data);

  };

  React.useEffect(() => {
    console.log("Doing request");
    console.log(scenario);
    console.log("Doing state console log");
    console.log(state);
    var fetch_string = "http://" + ip + ":" + port+ "/dbaccess?scenario=scenario_" + scenario + "&state=" + state;
    // var fetch_string = "http://localhost:3001/";
    // var fetch_string = ""
    fetch(fetch_string)
    .then(response => response.json())
    .then(data => handleResponse(data));
  },[state])

  return (
    // <Plot data={graph1.default.data} layout={graph1.default.layout} frames={graph1.default.frames} />
    <Plot data={fetchResponse.data} layout={fetchResponse.layout} frames={fetchResponse.frames} />
  );
}