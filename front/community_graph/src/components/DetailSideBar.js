const schoolNameList = {
    snu: "Seoul National University" ,
    kaist: "KAIST" ,
    postech: "POSTECH",
    yonsei: "Yonsei University",
    korea: "Korea University",
  };

const DetailSideBar = (props) => {
  return (
    <div
      style={{
        width: "200px",
        marginLeft: 20,
        padding: 20,
        outline: "thin dashed black",
      }}
    >
    <h1>
      {props.labDetail.name}
    </h1>
    <text>
      {schoolNameList[props.labDetail.school]} <br />
      {props.labDetail.prof_name} <br />
      {props.labDetail.email} <br />
      {props.labDetail.description} <br />
      {props.labDetail.href}
    </text>
    </div>
  );
};

export default DetailSideBar;