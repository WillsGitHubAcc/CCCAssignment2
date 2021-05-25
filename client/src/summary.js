import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import TransitionsModal from "./model"; 

const useStyles = makeStyles({
  table: {
    minWidth: 700,
    
  },
});

function ccyFormat(num) {
  
  if(num === ""){
    return "";
  }
  return `${num.toFixed(2)}`;
}

function createRow(desc, date, returnDate,price) {
  
  return { desc, date, returnDate, price };
}

function subtotal(items) {
  return items.map(({ price }) => price).reduce((sum, i) => sum + i, 0);
}

var rows = [
  createRow('A', 100, 1.15,2),
  createRow('B', 10, 45.99,2),
  createRow('C', 2, 17.99,2),
];

var invoiceTotal = subtotal(rows);

export default function SpanningTable(all_data) {
  const classes = useStyles();
  const [fetchResponse, setFetchResponse] = React.useState();

  React.useEffect(() => {
    var flightsData = all_data["flightsData"];
    var accomData = all_data["accomData"];
    var transData = all_data["transData"];
    rows = [
      createRow(flightsData["type"], flightsData["date"],"-", flightsData["price"]),
      createRow(accomData["type"], accomData["date"], "-",accomData["price"]),
      createRow(transData["type"], transData["date"],transData["returnDate"], transData["price"]),
    ];
    invoiceTotal = subtotal(rows);
    setFetchResponse(rows);
  
  },[all_data])
  if(fetchResponse){
    rows = fetchResponse;
  }

  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="spanning table">
        <TableHead>
          <TableRow>
            <TableCell align="center" colSpan={3}>
              Details
            </TableCell>
            <TableCell align="right">Price</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Description</TableCell>
            <TableCell align="right">Date</TableCell>
            <TableCell align="right">Return Date</TableCell>
            <TableCell align="right">Price</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow key={rows[0].desc}>
              <TableCell>{rows[0].desc}</TableCell>
              <TableCell align="right">{rows[0].date}</TableCell>
              <TableCell align="right">{rows[0].returnDate}</TableCell>
              <TableCell align="right">{ccyFormat(rows[0].price)}</TableCell>
            </TableRow>
          <TableRow key={rows[1].desc}>
              <TableCell>{rows[1].desc}</TableCell>
              <TableCell align="right">{rows[1].date}</TableCell>
              <TableCell align="right">{rows[1].returnDate}</TableCell>
              <TableCell align="right">{ccyFormat(rows[1].price)}</TableCell>
          </TableRow>
          <TableRow key={rows[2].desc}>
              <TableCell>{rows[2].desc}</TableCell>
              <TableCell align="right">{rows[2].date}</TableCell>
              <TableCell align="right">{rows[2].returnDate}</TableCell>
              <TableCell align="right">{ccyFormat(rows[2].price)}</TableCell>
            </TableRow>
          <TableRow>
            <TableCell rowSpan={3} />
            <TableCell colSpan={2}>Total</TableCell>
            <TableCell align="right">{ccyFormat(invoiceTotal)}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell rowSpan={3} />
            <TableCell colSpan={2} align="right">    
            <TransitionsModal allData={all_data}/>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>

  );
  
}
