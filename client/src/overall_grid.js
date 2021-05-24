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
import RadioButtonsGroup from "./radioButtons";


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
    switch(graphType){
      case "awakeBC":
        setGraphChoice(graph1);
        break;
      case "awakeAC":
        setGraphChoice(graph2);
        break;
      case "other":
        setGraphChoice(graph3);
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
            <RadioButtonsGroup sendDataToParent={sendDataToParent}/>
          </Paper>
        </Grid>
        <Grid item xs={9}>
          <Paper className={classes.paper}>
            <Plot data={graphChoice.default.data} layout={graphChoice.default.layout} />
            {/* <Plot data={graphChoice.default.data} layout={graphChoice.default.layout} /> */}
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}
