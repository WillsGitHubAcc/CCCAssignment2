import React from "react";
import ReactDOM from "react-dom";
import australia from "./australia";
import { SVGMap } from "react-svg-map";
import "react-svg-map/lib/index.css";

class CustomMap extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return <SVGMap map={australia} />;
  }
}

// ReactDOM.render(<App />, document.getElementById("app"));
export default CustomMap