import React, { Fragment } from "react";
import Forms from "./forms";
import Notes from "./notes";
export default function Dashboards() {
  return (
    <div>
      <Fragment>
        <Forms />
        <Notes />
      </Fragment>
    </div>
  );
}
