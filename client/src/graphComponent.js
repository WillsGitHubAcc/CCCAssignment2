import React from 'react';

import Plotly from "plotly.js-basic-dist";
import createPlotlyComponent from "react-plotly.js/factory";
import * as graph1 from "./Australia_awake_hist_BC.json";

import * as graph2 from "./data/Adel_sleep_time.json";
import * as graph3 from "./data/Aus_sleep_time.json";
import * as graph4 from "./data/Bris_sleep_time.json";
import * as graph5 from "./data/canberra_sleep_time.json";
import * as graph6 from "./data/darwin_sleep_time.json";
import * as graph7 from "./data/hobart_sleep_time.json";
import * as graph8 from "./data/melb_sleep_time.json";
import * as graph9 from "./data/perth_sleep_time.json";


export default function BasicTextFields(props) {
  

  var state = props.type;
  var scenario = props.scenario;
  var [graphChoice, setGraphChoice] = React.useState(graph1);

  const Plot = createPlotlyComponent(Plotly);
  var [result, setResult] = React.useState();
  const [fetchResponse, setFetchResponse] = React.useState();

  const handleResponse = (data) => {

    setFetchResponse(data);
    if(state === "wa"){
      setGraphChoice(graph9);
    }
    else if(state === "nt-mainland"){
      setGraphChoice(graph6);
    }
  };

  React.useEffect(() => {
    console.log("Doing request");
    var fetch_string = "http://127.0.0.1:3001/bookings"
    // var fetch_string = ""
    fetch(fetch_string)
    .then(response => response.json())
    .then(data => handleResponse(data));
  },[state])


  // if(fetchResponse){
  //   console.log(fetchResponse);
  //   if(state === "wa"){
  //     setGraphChoice(graph9);
  //   }

  // }
      
  //   switch(state){
  //     case "australia":
  //       setGraphChoice(graph3);
  //       break;
  //     case "wa":
  //       setGraphChoice(graph9);
  //       break;
  //     case "nt-mainland":
  //       setGraphChoice(graph6);
  //       break;
  //     case "qld-mainland":
  //       setGraphChoice(graph4);
  //       break;
  //     case "sa-mainland":
  //       setGraphChoice(graph2);
  //       break;
  //     case "nsw":
  //       // error
  //       setGraphChoice(graph5);
  //       break;
  //     case "vic":
  //       setGraphChoice(graph8);
  //       break;
  //     case "tas-mainland":
  //       setGraphChoice(graph7);
  //       break;
  //     default:
  //       setGraphChoice(graph3);
  //       break;
  //   }
  // }
  return (
    <Plot data={graphChoice.default.data} layout={graphChoice.default.layout} frames={graphChoice.default.frames} />
  );
}