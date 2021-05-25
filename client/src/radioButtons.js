import React from 'react';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';



export default function RadioButtonsGroup(props) {

  var sendDataToParent = props.sendDataToParent;

  const [value, setValue] = React.useState('awakeBC');

  const handleChange = (event) => {
    setValue(event.target.value);
    sendDataToParent(event.target.value);
  };


  return (
    <FormControl component="fieldset">
      <FormLabel component="legend">Figure Type</FormLabel>
      <FormControl component="fieldset">
      
      {/* <p></p>
      
      <Switch
        defaultChecked
        color="default"
        onChange={handleChange}
        inputProps={{ 'aria-label': 'checkbox with default color' }}
      /> */}
    </FormControl>
      <p></p>
      <RadioGroup aria-label="overall" name="overall1" value={value} onChange={handleChange}>
        <FormControlLabel value="awakeBC" control={<Radio />} label="Awake Histogram Before COVID" />
        <FormControlLabel value="awakeAC" control={<Radio />} label="Awake Histogram After COVID" />
        <FormControlLabel value="other" control={<Radio />} label="TestPlot" />
        
      </RadioGroup>
    </FormControl>
  );
}