import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
}));

export default function BasicTextFields(props) {
  const classes = useStyles();
  
//   const walter="walter"

  var [fromFilter, setFrom] = React.useState();
  var [toFilter, setTo] = React.useState();
  var [dateFromFilter, setDateFrom] = React.useState();
  var [dateToFilter, setDateTo] = React.useState();

//   React.useEffect(() => {
//     console.log(toFilter);
//   },[toFilter])

  
  return (  
    
      <div>
            <TextField id="outlined-basic1" label="Leaving From" variant="outlined" value={fromFilter} onChange={(e) => setFrom(e.target.value)}/>
            <TextField id="outlined-basic2" label="Going To" variant="outlined" value={toFilter} onChange={(e) => setTo(e.target.value)}/>
            <TextField id="outlined-basic3" label="Departure" variant="outlined" value={dateFromFilter} onChange={(e) => setDateFrom(e.target.value)}/>
            <TextField id="outlined-basic4" label="Returning" variant="outlined" value={dateToFilter} onChange={(e) => setDateTo(e.target.value)}/>
            
            <Button variant="contained" color="primary" size="large" onClick={() => props.setFiltersFunction(fromFilter,toFilter,dateFromFilter,dateToFilter) }>
                Search
            </Button>
            
      </div>
  
  
    
  );
}
