import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import BasicTextFields from "./graphComponent";

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

export default function CenteredGrid(props) {
  const classes = useStyles();
  // const Plot = createPlotlyComponent(Plotly);
  
  var [graphName, setGraphName] = React.useState("aus");
  var scenario = props.scenario;
  console.log("I AM WALTER")
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
           
          
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}
