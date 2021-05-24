import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
// import html from './location.html'

import Plotly from "plotly.js-basic-dist";
import createPlotlyComponent from "react-plotly.js/factory";
import * as graph1 from "./Australia_awake_hist_BC.json";
import * as graph2 from "./Australia_awake_hist_DC.json";
import * as graph3 from "./test_plot.json";
import * as graph4 from "./Aus_sleep_time.json";
import RadioButtonsGroup from "./radioButtons";


import Typography from '@material-ui/core/Typography';
import CustomMap from "./CustomMap";
const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
}));

export default function CenteredGrid() {
  const classes = useStyles();
  const Plot = createPlotlyComponent(Plotly);
  var [graphChoice, setGraphChoice] = React.useState(graph1);

  const sendDataToParent = (graphType) => {
    console.log(graphType)
    
    switch(graphType){
      case "australia":
        setGraphChoice(graph1);
        break;
      case "wa":
        setGraphChoice(graph2);
        break;
      case "nt-mainland":
        setGraphChoice(graph3);
        break;
      case "qld-mainland":
        setGraphChoice(graph2);
        break;
      case "sa-mainland":
        setGraphChoice(graph3);
        break;
      case "nsw":
        setGraphChoice(graph2);
        break;
      case "vic":
        setGraphChoice(graph3);
        break;
      case "tas-mainland":
        setGraphChoice(graph4);
        break;
      default:
        setGraphChoice(graph1);
        break;
    }
  }
  
  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={3}>
          <Paper className={classes.paper}>
            
            {/* <RadioButtonsGroup sendDataToParent={sendDataToParent}/> */}
            <Typography variant="h4" gutterBottom>
              Select a State
            </Typography>
            <Typography variant="h6" gutterBottom>
              Default is Australia
            </Typography>
            <CustomMap sendDataToParent={sendDataToParent}/>

          </Paper>
        </Grid>
        <Grid item xs={9}>
          <Paper className={classes.paper}>
            <Plot data={graphChoice.default.data} layout={graphChoice.default.layout} frames={graphChoice.default.frames} />
            {/* <Plot data={graphChoice.default.data} layout={graphChoice.default.layout} /> */}
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}
