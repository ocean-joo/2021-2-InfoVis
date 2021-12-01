import { autoType } from "d3-dsv";

const schoolNameList = {
  snu: "Seoul National University",
  kaist: "KAIST",
  postech: "POSTECH",
  yonsei: "Yonsei University",
  korea: "Korea University",
};

const DetailSideBar = (props) => {
  // props -> labDetail, confDetail, shouldVisualizeConf(flag)
  // confDetail attrib: title, impactScore
  // flag -> 0 for labDetail, 1 for confDetail, 2 for nothing selected

  var labInformation = props.labDetail.selectedLabDetail;
  var confInformation = props.confDetail.selectedConfDetail;
  var listItem ;
  var paperlist = "";

  if ('selectedLabDetail' in props.labDetail) {
    listItem = labInformation.paper.map((obj, i) =>
      <li key={i}>
        <b>{obj.title}</b> <br />
        <i>{obj.apa}</i>
        <a href={obj.href}>[link]</a>
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
  // TODO: more general condition to show nothing
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

  if (props.shouldVisualizeConf) {
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
        <b>Impact Score</b>: {confInformation.impactScore} <br />
        <b>Website     </b>: <a href={confInformation.website}>[link]</a><br />
      </div>
    );
  } else {
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
        {labInformation.prof_name}, {schoolNameList[labInformation.school]} <br />
        <b>E - mail</b>: {labInformation.email} <br />
        <b>Interest</b>: {labInformation.description} <br />
        <b>Lab link</b>: <a href={labInformation.href}>{labInformation.href}</a>
        <h2>
          {paperlist}
        </h2>
        <ul>{listItem}</ul>
      </div>
    );
  }
  
};

export default DetailSideBar;