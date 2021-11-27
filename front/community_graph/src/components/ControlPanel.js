import React from "react";
import Slider, { Range } from "rc-slider";
import "rc-slider/assets/index.css";

const ControlPanel = (props) => {
  const onLowerBoundChange = (e) => {
    if (+e.target.value < 0 || +e.target.value > props.weightRange.max) return;

    props.setWeightRange({ min: +e.target.value, max: props.weightRange.max });
  };

  const onUpperBoundChange = (e) => {
    if (+e.target.value > 100 || +e.target.value < props.weightRange.min)
      return;

    props.setWeightRange({ min: props.weightRange.min, max: +e.target.value });
  };

  const onSliderChange = (value) => {
    props.setWeightRange({ min: value[0], max: value[1] });
  };

  const onScaleChange = (value) => {
    props.setScaleFactor(value);
  };

  const onScaleInputChange = (e) => {
    if (+e.target.value > 300 || +e.target.value < 5) return;

    props.setScaleFactor(+e.target.value);
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
      <div className="Range">
        <label>Zoom: </label>
        <input
          type="number"
          value={props.scaleFactor}
          onChange={onScaleInputChange}
        />
        <div className="Slider">
          <Slider
            min={5}
            max={300}
            value={props.scaleFactor}
            onChange={onScaleChange}
          />
        </div>
        <label> %</label>
        <br />
        <br />
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
