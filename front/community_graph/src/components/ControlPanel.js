import React from "react";
import { Range } from "rc-slider";
import "rc-slider/assets/index.css";

const ControlPanel = (props) => {
  const onLowerBoundChange = (e) => {
    if (+e.target.value < 0 || +e.target.value > this.state.upperBound) return;

    props.setWeightRange({ min: +e.target.value, max: props.weightRange.max });
  };

  const onUpperBoundChange = (e) => {
    if (+e.target.value > 100 || +e.target.value < this.state.lowerBound)
      return;

    props.setWeightRange({ min: props.weightRange.min, max: +e.target.value });
  };

  const onSliderChange = (value) => {
    props.setWeightRange({ min: value[0], max: value[1] });
  };

  return (
    <div
      style={{
        display: "flex",
        width: 400,
        margin: "50px 50px 10px 50px",
        alignItems: "flex-end",
      }}
    >
      <div className="Slider">
        <label>LowerBound: </label>
        <input
          type="number"
          value={props.weightRange.min}
          onChange={onLowerBoundChange}
        />
        <label> %</label>
        <br />
        <label>UpperBound: </label>
        <input
          type="number"
          value={props.weightRange.max}
          onChange={onUpperBoundChange}
        />
        <label> %</label>
        <br />
        <br />
        <Range
          allowCross={false}
          min={0}
          max={100}
          value={[props.weightRange.min, props.weightRange.max]}
          onChange={onSliderChange}
        />
      </div>
    </div>
  );
};

export default ControlPanel;