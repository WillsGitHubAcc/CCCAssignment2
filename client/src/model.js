import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Modal from '@material-ui/core/Modal';
import Backdrop from '@material-ui/core/Backdrop';
import Fade from '@material-ui/core/Fade';
import TextField from '@material-ui/core/TextField';

import FlightTakeoffIcon from '@material-ui/icons/FlightTakeoff';
import FlightLandIcon from '@material-ui/icons/FlightLand';
import HotelIcon from '@material-ui/icons/Hotel';

import ListItemText from '@material-ui/core/ListItemText';
import Box from '@material-ui/core/Box';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import Button from '@material-ui/core/Button';

import { Alert, AlertTitle } from '@material-ui/lab';

import { v4 as uuidv4 } from 'uuid';

const useStyles = makeStyles((theme) => ({
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  paper: {
    backgroundColor: theme.palette.background.paper,
    border: '2px solid #000',
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3),
  },
  root: {
    width: '100%',
    maxWidth: 700,
    backgroundColor: theme.palette.background.paper,
  },
  table: {
    minWidth: 650,
  },
}));

export default function TransitionsModal(props) {

  const classes = useStyles();
  const [open, setOpen] = React.useState(false);
  var allData = props.allData;
  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setFetchResponse(null);
  };

  
const [fetchResponse, setFetchResponse] = React.useState();
const [clicked, setClicked] = React.useState();
const [firstTime, setFirstTime] = React.useState(true);



  React.useEffect(() => {
    if(!firstTime){
      console.log("SEDNING BOOKING");
      var totalFlightCost = 0;
      var totalHotelCost = 0;
      var jsonBody = {};
      jsonBody["tripID"] = uuidv4();
  
      if(allData["flightsData"]["price"] >0){
        jsonBody["departFlight"] = {};
        jsonBody["departFlight"]["id"]= uuidv4().replace("-", "");
        jsonBody["departFlight"]["user"] = accountID;
        jsonBody["departFlight"]["flight"] = allData["flightsData"]["id"];
        totalFlightCost = totalFlightCost+allData["flightsData"]["price"]
      }
  
  
      if(allData["accomData"]["price"] >0){
        jsonBody["returnFlight"] = {};
        jsonBody["returnFlight"]["id"]= uuidv4().replace("-", "");
        jsonBody["returnFlight"]["user"] = accountID;
        jsonBody["returnFlight"]["flight"] = allData["accomData"]["id"];
        totalFlightCost = totalFlightCost+allData["accomData"]["price"]
      }
  
  
      if(allData["transData"]["price"] >0){
        jsonBody["hotel"] = {};
        jsonBody["hotel"]["bookingid"]= uuidv4().replace("-", "");
        jsonBody["hotel"]["name"] = accountID;
  
        jsonBody["hotel"]["hotelid"] = allData["transData"]["id"];
        jsonBody["hotel"]["start"] = allData["transData"]["date"];
        jsonBody["hotel"]["finish"] = allData["transData"]["returnDate"];
        totalHotelCost = totalHotelCost+allData["transData"]["price"]
      }
  
      jsonBody["payment"] = {};
      jsonBody["payment"]["source"] = accountID;
      jsonBody["payment"]["destinations"] = [];
      
      if(allData["transData"]["price"] >0){
        jsonBody["payment"]["destinations"].push({
          "destinationid": "hotel",
          "amount": totalHotelCost
        });
      }
      if(allData["accomData"]["price"] >0 || allData["flightsData"]["price"] >0){
        jsonBody["payment"]["destinations"].push(      {
          "destinationid": "flight",
          "amount": totalFlightCost
        });
      }

      fetch("http://127.0.0.1:5000" ,{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonBody)
      })
      .then(response => response.json())
      .then(data => setFetchResponse(data));
    }
    else{
      console.log("First time rendering so dont send booking ");
      setFirstTime(false);
    }
  },[clicked])



  const submitBooking = (accountID,destinationAccountID,allData) => {
    setClicked(uuidv4());    
}
if(fetchResponse){
  console.log("Modal fetch response");
  console.log(fetchResponse);
  
}
  

  const [accountID, setAccountID] = React.useState();
  const [destinationAccountID, setDestinationAccountID] = React.useState();
  const [departingDate, setDepartingDate] = React.useState("None");
  const [departingDesc, setDepartingDesc] = React.useState("None Selected");
  const [departingPrice, setDepartingPrice] = React.useState("None");
  const [returningDate, setReturningDate] = React.useState("None");
  const [returningDesc, setReturningDesc] = React.useState("None Selected");
  const [returningPrice, setReturningPrice] = React.useState("None");

  const [accomDesc, setAccomDesc] = React.useState(0);
  const [accomStartDate, setAccomStartDate] = React.useState("None");
  const [accomReturnDate, setAccomReturnDate] = React.useState("None");
  const [accomPrice, setAccomPrice] = React.useState(0);

  const [total, setTotal] = React.useState(0);

  React.useEffect(() => {
    
    
    setDepartingDate(allData["flightsData"]["date"]);
    setDepartingDesc(allData["flightsData"]["type"]);
    
    setReturningDate(allData["accomData"]["date"]);
    setReturningDesc(allData["accomData"]["type"]);
  
    setAccomDesc(allData["transData"]["type"]);
    setAccomStartDate(allData["transData"]["date"]);
    setAccomReturnDate(allData["transData"]["returnDate"]);
  
    if(allData["flightsData"]["price"] === 0){
      setDepartingPrice("");
    }
    else{
      setDepartingPrice("$" + allData["flightsData"]["price"]);
    }

    if(allData["accomData"]["price"] === 0){
      setReturningPrice("");
    }
    else{
      setReturningPrice("$"+allData["accomData"]["price"]);
    }
    if(allData["transData"]["price"] === 0){
      setAccomPrice("");
    }
    else{
      setAccomPrice("$"+allData["transData"]["price"]);
    }
  
    setTotal("$" +(allData["flightsData"]["price"] + allData["accomData"]["price"] + allData["transData"]["price"]))

  },[allData])  

  return (
    <div>
      <button type="button" onClick={handleOpen}>
        Checkout
      </button>
      <Modal
        aria-labelledby="transition-modal-title"
        aria-describedby="transition-modal-description"
        className={classes.modal}
        open={open}
        onClose={handleClose}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
        }}
      >
        <Fade in={open}>
          <div className={classes.paper} >
            <h2 id="transition-modal-title">Summary</h2>
            Enter an Account Id to make booking from: <TextField id="outlined-basica" label="Account ID" variant="outlined" value={accountID} onChange={(e) => setAccountID(e.target.value)}/>
            <Box m={3}> </Box>
            {/* Enter an Destination Account Id to make booking from: <TextField id="outlined-basic" label="Destination Account ID" variant="outlined" value={destinationAccountID} onChange={(e) => setDestinationAccountID(e.target.value)}/> */}

            <p id="transition-modal-description">
                <Box m={3}> </Box>
                <TableContainer component={Paper}>
                <Table className={classes.table} size="small" aria-label="a dense table">
                  <TableHead>
                    <TableRow>
                      <TableCell>Flight</TableCell>
                      <TableCell align="right">Flight Date</TableCell>
                      <TableCell align="right">Details</TableCell>
                      <TableCell align="right">Price</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    
                      <TableRow key={"depart"}>
                        <TableCell component="th" scope="row">
                        <FlightTakeoffIcon /><ListItemText primary="Departing Flight"  />
                        </TableCell>
                        <TableCell align="right">{departingDate}</TableCell>
                        <TableCell align="right">{departingDesc}</TableCell>
                        <TableCell align="right">{departingPrice}</TableCell>
                        
                      </TableRow>
                      <TableRow key={"return"}>
                        <TableCell component="th" scope="row">
                        <FlightLandIcon /><ListItemText primary="Returning Flight"  />
                        </TableCell>
                        <TableCell align="right">{returningDate}</TableCell>
                        <TableCell align="right">{returningDesc}</TableCell>
                        <TableCell align="right">{returningPrice}</TableCell>
                      
                      </TableRow>

                  </TableBody>
                </Table>
              </TableContainer>

              <Box m={3}> </Box>

              <TableContainer component={Paper}>
                <Table className={classes.table} size="small" aria-label="a dense table">
                  <TableHead>
                    <TableRow>
                      <TableCell>Accomodation</TableCell>
                      <TableCell align="right">Date From</TableCell>
                      <TableCell align="right">Date To</TableCell>
                      <TableCell align="right">Details</TableCell>
                      <TableCell align="right">Price</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                      <TableRow key={"accom"}>
                        <TableCell component="th" scope="row">
                        <HotelIcon /><ListItemText primary="Accomodation"  />
                        </TableCell>
                        <TableCell align="right">{accomStartDate}</TableCell>
                        <TableCell align="right">{accomReturnDate}</TableCell>
                        <TableCell align="right">{accomDesc}</TableCell>
                        <TableCell align="right">{accomPrice}</TableCell>
                      </TableRow>
                    
                  </TableBody>
                </Table>
              </TableContainer>
              <Box m={3}> </Box>
              total = {total}    
              {/* <Button onClick={() => {submitBooking(accountID,destinationAccountID,allData)}} variant="contained" color="primary" disabled={ accountID == null || accountID == "" ||destinationAccountID == null || destinationAccountID == "" || (accomPrice > 0 && (accomStartDate == "" || accomReturnDate == "") )}> */}
              <Button onClick={() => {submitBooking(accountID,destinationAccountID,allData)}} variant="contained" color="primary" disabled={ accountID == null || accountID == "" || (accomPrice > 0 && (accomStartDate == "" || accomReturnDate == ""||accomStartDate == null || accomReturnDate == null ))}>
                Book
              </Button>
              <Box m={3}> </Box>
              {fetchResponse && fetchResponse["ok"]===false && <Alert severity="error">
                <AlertTitle>Error</AlertTitle>
                There was an error making your booking — <strong>Ensure details are correct</strong>
              </Alert>}
              {!fetchResponse && <Alert severity="info">
                <AlertTitle>Info</AlertTitle>
                No Booking Made Yet
              </Alert>}
              {fetchResponse &&  fetchResponse["ok"]===true && <Alert severity="success">
                <AlertTitle>Success</AlertTitle>
                <strong>Booking Successfully Completed!</strong>
              </Alert>}

            </p>
          </div>
        </Fade>
      </Modal>
    </div>
  );
}


