// COMP90024 2021 Semester 2 Assignment 2
// Group 52
// William Lazarus Kevin Dean 834444 Melbourne, Australia
// Kenneth Huynh 992680 Melbourne, Australia
// Joel Kenna 995401 Melbourne, Australia
// Quinten van der Leest 1135216 Melbourne, Australia
// Walter Zhang 761994 Melbourne, Australia

import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import BasicTextFields from "./graphComponent";

import Typography from '@material-ui/core/Typography';
import CustomMap from "./CustomMap";
import SpacingGrid from "./extraGraph";

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

export default function CenteredGrid(props) {
  const classes = useStyles();
  // const Plot = createPlotlyComponent(Plotly);
  
  var [graphName, setGraphName] = React.useState("aus");
  var scenario = props.scenario;

  console.log(scenario)

  const sendDataToParent = (graphType) => {
    console.log(graphType)
    setGraphName(graphType);

  }
  
  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={3}>
          <Paper className={classes.paper}>
            
            
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
          
            <BasicTextFields type={graphName} scenario={scenario}/>
            <SpacingGrid scenario={scenario}/>
           
          
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}
