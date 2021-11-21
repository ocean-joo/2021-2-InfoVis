const schoolNameList = {
  snu: "Seoul National University",
  kaist: "KAIST",
  postech: "POSTECH",
  yonsei: "Yonsei University",
  korea: "Korea University",
};

const DetailSideBar = (props) => {
  console.log(props.labDetail);
  var details = props.labDetail.selectedLabDetail;
  var listItem ;

  if ('selectedLabDetail' in props.labDetail) {
    listItem = details.paper.map((obj) =>
      <li>
        {obj.apa}
        <a href=""onclick="obj.link">[link]</a>
      </li>
    );
  } else {
    listItem = "";
    details = {};
  }
  

  return (
    <div
      style={{
        width: "400px",
        marginLeft: 20,
        padding: 20,
        outline: "thin dashed black",
      }}
    >
      <h1>
        {details.name}
      </h1>
      <h2>
        Information
      </h2>
      <text>
        {details.prof_name}, {schoolNameList[details.school]} <br />
        E - mail: {details.email} <br />
        Interest: {details.description} <br />
        Lab link: {details.href}
      </text>
      <h2>
        Paper List
      </h2>
      <ul>{listItem}</ul>
    </div>
  );
};

export default DetailSideBar;