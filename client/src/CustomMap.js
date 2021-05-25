import React from "react";

import australia from "./australia";
import { SVGMap } from "react-svg-map";
import "react-svg-map/lib/index.css";

import { makeStyles } from '@material-ui/core/styles';

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
    setPrettyValue("Australia");
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

              <Button variant="contained" color="primary" onClick={handleChange} > 
              Reset to Australia
             </Button>

             <div className="examples__block__info__item">
					  	Selected location: {prettyValue}
					  </div>
        </div>  
  );
}

