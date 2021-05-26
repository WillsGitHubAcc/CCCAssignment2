// COMP90024 2021 Semester 2 Assignment 2
// Group 52
// William Lazarus Kevin Dean 834444 Melbourne, Australia
// Kenneth Huynh 992680 Melbourne, Australia
// Joel Kenna 995401 Melbourne, Australia
// Quinten van der Leest 1135216 Melbourne, Australia
// Walter Zhang 761994 Melbourne, Australia

import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
// import App from './App';
import reportWebVitals from './reportWebVitals';

import TabPanel from "./tabs";


ReactDOM.render(
  <React.StrictMode>
    <TabPanel />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
