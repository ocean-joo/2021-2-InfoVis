import React from "react";
import { Range } from "rc-slider";
import 'rc-slider/assets/index.css';

class CustomizedRange extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            lowerBound: 20,
            upperBound: 40,
            value: [20, 40],
        };
    }

    onLowerBoundChange = (e) => {
        this.setState({ lowerBound: +e.target.value });
    };

    onUpperBoundChange = (e) => {
        this.setState({ upperBound: +e.target.value });
    };

    onSliderChange = (value) => {
        this.setState({
            value,
        });
    };

    handleApply = () => {
        const { lowerBound, upperBound } = this.state;
        this.setState({ value: [lowerBound, upperBound] });
    };

    render() {
        return (
            <div>
                <label>LowerBound: </label>
                <input type="number" value={this.state.lowerBound} onChange={this.onLowerBoundChange} />
                <br />
                <label>UpperBound: </label>
                <input type="number" value={this.state.upperBound} onChange={this.onUpperBoundChange} />
                <br />
                <button type="button" onClick={this.handleApply}>
                    Apply
          </button>
                <br />
                <br />
                <Range allowCross={false} value={this.state.value} onChange={this.onSliderChange} />
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