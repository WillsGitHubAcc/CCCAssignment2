import React from "react";
import ReactDOM from "react-dom";
import australia from "./australia";
import { SVGMap } from "react-svg-map";
import "react-svg-map/lib/index.css";

import { makeStyles } from '@material-ui/core/styles';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import Switch from '@material-ui/core/Switch';

import Button from '@material-ui/core/Button';
import PropTypes from 'prop-types';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

export default function CustomMap(props) {
  const classes = useStyles();
  var sendDataToParent = props.sendDataToParent;

  const [value, setValue] = React.useState('awakeBC');

  const [prettyValue, setPrettyValue] = React.useState('Australia');


  const handleChange = (event) => {
    setValue(event.target.value);
    sendDataToParent(event.target.value);
  };

  const func = (event) => {
    const clickedLocation = event.target.id;
    setPrettyValue(event.target.attributes.name.value);
    sendDataToParent(clickedLocation);
  }

  return(
        <div className={classes.root}>
        <SVGMap map={australia} onLocationClick={func} 				/>

              <Button variant="contained" color="primary" onClick={() => {setPrettyValue("Australia");setValue("australia");  }} > 
              Reset to Australia
             </Button>

             <div className="examples__block__info__item">
					  	Selected location: {prettyValue}
					  </div>
        </div>  
  );
}

