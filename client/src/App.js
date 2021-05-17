import React, { Component } from "react";
import logo from './logo.svg';
import './App.css';
import ServicePanel from './table';
class App extends Component {
  constructor(props) {
    super(props);
    this.state = { apiResponse: "" };
  }

  callAPI() {
      fetch("http://localhost:9000/walter")
          .then(res => res.text())
          .then(res => this.setState({ apiResponse: res }));
  }





  componentWillMount() {
      this.callAPI();
  }

  render(){
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">{this.state.apiResponse}</p>
        <div className="tables" style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gridGap: 20 }}>
          <ServicePanel />
          <ServicePanel />
          <ServicePanel />

        </div>
        
      </div>
    );
  }
}

export default App;
