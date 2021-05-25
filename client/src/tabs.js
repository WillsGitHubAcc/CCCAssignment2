import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';

import AutoGrid from "./overall_grid";

import appArch from "./appArch.jpeg";


function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
}));

export default function SimpleTabs() {
  const classes = useStyles();
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
          
          <Tab label="Sleep Scenario" {...a11yProps(0)} />
          <Tab label="Pets Scenario" {...a11yProps(1)} />
          <Tab label="Election Scenario" {...a11yProps(2)} />
          {/* <Tab label="General Data" {...a11yProps(3)} /> */}
          <Tab label="Application Architecture" {...a11yProps(3)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
      <AutoGrid scenario={"sleep"}/> 
      </TabPanel>
      <TabPanel value={value} index={1}>
      <AutoGrid scenario={"pet"}/> 
      </TabPanel>
      <TabPanel value={value} index={2}>
      <AutoGrid scenario={"elect"}/> 
      </TabPanel>
      {/* <TabPanel value={value} index={3}>
        <CenteredGridSingle/>
      </TabPanel> */}
      <TabPanel value={value} index={3}>
      <Typography variant="h4" gutterBottom>
            Application Architecture
            </Typography>          
            <img src={appArch} alt="Our Application Architecture"     />        
      </TabPanel>
    </div>
  );
}
