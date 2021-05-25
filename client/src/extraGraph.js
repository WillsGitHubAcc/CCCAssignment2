import React from 'react';
import Plotly from "plotly.js-basic-dist";
import createPlotlyComponent from "react-plotly.js/factory";
import * as aurin_pets from "./aurin_pets.json";
import * as aurin_elect from "./aurin_elect.json";
import * as aurin_sleep from "./data/Victoria_sleep_study.json";


export default function SpacingGrid(props) {
  var scenario = props.scenario;
  const Plot = createPlotlyComponent(Plotly);

if(scenario==="pet"){
  return (
    <Plot data={aurin_pets.default.data} layout={aurin_pets.default.layout} frames={aurin_pets.default.frames} />
  );
}

if(scenario==="elect"){
    return (
      <Plot data={aurin_elect.default.data} layout={aurin_elect.default.layout} frames={aurin_elect.default.frames} />
    );
  }
if(scenario==="sleep"){
    return (
      <Plot data={aurin_sleep.default.data} layout={aurin_sleep.default.layout} frames={aurin_sleep.default.frames} />
    );
  }

return(
    <div></div>
)
}
