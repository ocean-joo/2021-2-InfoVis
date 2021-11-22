import { autoType } from "d3-dsv";

const schoolNameList = {
  snu: "Seoul National University",
  kaist: "KAIST",
  postech: "POSTECH",
  yonsei: "Yonsei University",
  korea: "Korea University",
};

const DetailSideBar = (props) => {
  // props -> confDetail, flag
  // confDetail attrib: title, impactScore
  // flag -> 0 for labDetail, 1 for confDetail, 2 for nothing selected

  // dummy define
  var flag = 0 ;
  var confInformation = {
    title: "RTSS: ...",
    impactScore: 10,
  };
  
  var labInformation = props.labDetail.selectedLabDetail;
  var listItem ;
  var paperlist = "";

  if ('selectedLabDetail' in props.labDetail) {
    listItem = labInformation.paper.map((obj) =>
      <li>
        {obj.title}
        <a href={obj.link}>[link]</a>
      </li>
    );
    if (labInformation.paper.length !== 0) {
      paperlist = "Paper List";
    }
  } else {
    listItem = "";
    labInformation = {};
  }

  // nothing selected
  if (!('selectedLabDetail' in props.labDetail)) {
    return (
      <div
      style={{
        width: "400px",
        height: "710px",
        marginLeft: 20,
        padding: 20,
        outline: "thin dashed black",
        overflow: "scroll",
      }}
      ></div>
    );
  }

  if (flag == 0) {
    return (
      <div
        style={{
          width: "400px",
          height: "710px",
          marginLeft: 20,
          padding: 20,
          outline: "thin dashed black",
          overflow: "scroll",
        }}
      >
        <h1>
          {labInformation.name}
        </h1>
        <h2>
          Information
        </h2>
        <text>
          {labInformation.prof_name}, {schoolNameList[labInformation.school]} <br />
          <b>E - mail</b>: {labInformation.email} <br />
          <b>Interest</b>: {labInformation.description} <br />
          <b>Lab link</b>: {labInformation.href}
        </text>
        <h2>
          {paperlist}
        </h2>
        <ul>{listItem}</ul>
      </div>
    );
  } else if (flag == 1) {
    return (
      <div
        style={{
          width: "400px",
          height: "710px",
          marginLeft: 20,
          padding: 20,
          outline: "thin dashed black",
          overflow: "scroll",
        }}
      >
        <h1>
          {confInformation.title}
        </h1>
        <h2>
          Information
        </h2>
        <text>
          <b>Impact Score</b>: {confInformation.impactScore} <br />
        </text>
      </div>
    );
  }
  
};

export default DetailSideBar;