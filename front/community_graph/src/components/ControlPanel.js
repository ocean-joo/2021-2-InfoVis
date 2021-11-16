import React from "react";
import { Range } from "rc-slider";
import 'rc-slider/assets/index.css';

class CustomizedRange extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            lowerBound: 0,
            upperBound: 100
        };
    }

    onLowerBoundChange = (e) => {
        if (+e.target.value < 0 || +e.target.value > this.state.upperBound) return
        this.setState({
            lowerBound: +e.target.value,
            value: [+e.target.value, this.state.upperBound]
        });
    };

    onUpperBoundChange = (e) => {
        if (+e.target.value > 100 || +e.target.value < this.state.lowerBound) return
        this.setState({
            upperBound: +e.target.value,
            value: [this.state.lowerBound, +e.target.value]
        });
    };

    onSliderChange = (value) => {
        this.setState({
            lowerBound: value[0],
            upperBound: value[1],
        });
    };

    render() {
        return (
            <div>
                <label>LowerBound: </label>
                <input type="number" value={this.state.lowerBound} onChange={this.onLowerBoundChange} />
                <label> %</label>
                <br />
                <label>UpperBound: </label>
                <input type="number" value={this.state.upperBound} onChange={this.onUpperBoundChange} />
                <label> %</label>
                <br />
                <br />
                <Range
                    allowCross={false}
                    min={0}
                    max={100}
                    value={[this.state.lowerBound, this.state.upperBound]}
                    onChange={this.onSliderChange}
                />
            </div>
        );
    }
}

const ControlPanel = (props) => {
    return (
        <div style={{ width: 400, margin: 50, display: "inline-flex" }}>
            <CustomizedRange />
        </div>
    );
};

export default ControlPanel;