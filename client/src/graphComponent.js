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
// import * as aurin_pets from "./aurin_pets.json";
// import * as aurin_elect from "./aurin_elect.json";


import * as ade_sleep from  "./data/Adel_sleep_time.json"
import * as aus_sleep from  "./data/Aus_sleep_time.json"
import * as bris_sleep from  "./data/Bris_sleep_time.json"
import * as can_sleep from  "./data/canberra_sleep_time.json"
import * as dar_sleep from  "./data/darwin_sleep_time.json"
import * as hob_sleep from  "./data/hobart_sleep_time.json"
import * as melb_sleep from  "./data/melb_sleep_time.json"
import * as per_sleep from  "./data/perth_sleep_time.json"
import * as syd_sleep from  "./data/sydney_sleep_time.json"


import * as auring_sleep from  "./data/Victoria_sleep_study.json"
import * as aurin_pet from "./data/sa_cats_dogs_AURIN.json"
import * as aurin_elect from "./data/2019_elect_2pp_AURIN.json"

import * as bris_pet from "./data/bris_pet.json"
import * as syd_pet from "./data/Sydney_pet.json"
import * as per_pet from "./data/perth_pet.json"
import * as melb_pet from "./data/melb_pet.json"
import * as hob_pet from "./data/hoba_pet.json"
import * as aus_pet from "./data/aus_pet.json"
import * as can_pet from "./data/canb_pet.json"
import * as dar_pet from "./data/darw_pet.json"
import * as ade_pet from "./data/adel_pet.json"


import * as syd_elect from "./data/sydney_elect.json"
import * as per_elect from "./data/perth_elect.json"
import * as melb_elect from "./data/melb_elect.json"
import * as can_elect from "./data/canberra_elect.json"
import * as hob_elect from "./data/Hobart_elect.json"
import * as bris_elect from "./data/Bris_elect.json"
import * as aus_elect from "./data/Aus_elect.json"
import * as ade_elect from "./data/adel_elect.json"
import * as dar_elect from "./data/darwin_elect.json"

export default function BasicTextFields(props) {
  

  var state = props.type;
  var scenario = props.scenario;
  

  var chosenGraph = {"data":[],"layout":[]}
  if(state==="wa"){
    if(scenario === "sleep"){
      chosenGraph=per_sleep;
    }
    else if(scenario === "pet"){
      chosenGraph=per_pet;
    }
    else if(scenario === "elect"){
      chosenGraph=per_elect;
    }
  }
  if(state==="nt-mainland"){
    if(scenario === "sleep"){
      chosenGraph=dar_sleep;
    }
    else if(scenario === "pet"){
      chosenGraph=dar_pet;
    }
    else if(scenario === "elect"){
      chosenGraph=dar_elect;
    }
  }
  if(state==="qld-mainland"){
    if(scenario === "sleep"){
      chosenGraph=bris_sleep;
    }
    else if(scenario === "pet"){
      chosenGraph=bris_pet;
    }
    else if(scenario === "elect"){
      chosenGraph=bris_elect;
    }
  }
  if(state==="sa-mainland"){
    if(scenario === "sleep"){
      chosenGraph=ade_sleep;
    }
    else if(scenario === "pet"){
      chosenGraph=ade_pet;
    }
    else if(scenario === "elect"){
      chosenGraph=ade_elect;
    }
  }
  if(state==="nsw"){
    if(scenario === "sleep"){
      chosenGraph=syd_sleep;
    }
    else if(scenario === "pet"){
      chosenGraph=syd_pet;
    }
    else if(scenario === "elect"){
      chosenGraph=syd_elect;
    }
  }
  if(state==="vic"){
    if(scenario === "sleep"){
      chosenGraph=melb_sleep;
    }
    else if(scenario === "pet"){
      chosenGraph=melb_pet;
    }
    else if(scenario === "elect"){
      chosenGraph=melb_elect;
    }
  }
  if(state==="tas-mainland"){
    if(scenario === "sleep"){
      chosenGraph=hob_sleep;
    }
    else if(scenario === "pet"){
      chosenGraph=hob_pet;
    }
    else if(scenario === "elect"){
      chosenGraph=hob_elect;
    }
  }
  if(state==="act"){
    if(scenario === "sleep"){
      chosenGraph=can_sleep;
    }
    else if(scenario === "pet"){
      chosenGraph=can_pet;
    }
    else if(scenario === "elect"){
      chosenGraph=can_elect;
    }
  }
  if(state==="aus"){
    if(scenario === "sleep"){
      chosenGraph=aus_sleep;
    }
    else if(scenario === "pet"){
      chosenGraph=aus_pet;
    }
    else if(scenario === "elect"){
      chosenGraph=aus_elect;
    }
  }
  state = state + "_" + scenario;
  if(scenario ==="sleep"){
    state = state +"_time";
  }


  

  const Plot = createPlotlyComponent(Plotly);
  // var [result, setResult] = React.useState();
  // const [fetchResponse, setFetchResponse] = React.useState({"data":[],"layout":[]});

  // const handleResponse = (data) => {

  //   setFetchResponse(data);
    
  //   console.log(data);

  // };

  // React.useEffect(() => {
  //   console.log("Doing request");
  //   console.log(scenario);
  //   console.log("Doing state console log");
  //   console.log(state);
  //   var fetch_string = "http://127.0.0.1:3001/dbaccess?scenario=scenario_" + scenario + "&state=" + state;
  //   console.log(fetch_string);
  //   // var fetch_string = ""
  //   fetch(fetch_string)
  //   .then(response => response.json())
  //   .then(data => handleResponse(data));
  // },[state])

  return (
    // <Plot data={graph1.default.data} layout={graph1.default.layout} frames={graph1.default.frames} />
    <Plot data={chosenGraph.default.data} layout={chosenGraph.default.layout} frames={chosenGraph.default.frames} />
  );
}