import React from 'react';
import Plotly from "plotly.js-basic-dist";
import createPlotlyComponent from "react-plotly.js/factory";
import * as aurin_pets from "./aurin_pets.json";
import * as aurin_elect from "./aurin_elect.json";


export default function BasicTextFields(props) {
  

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

    setFetchResponse(data);
    
    console.log(data);

  };

  React.useEffect(() => {
    console.log("Doing request");
    console.log(scenario);
    console.log("Doing state console log");
    console.log(state);
    var fetch_string = "http://127.0.0.1:3001/dbaccess?scenario=scenario_" + scenario + "&state=" + state;
    console.log(fetch_string);
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