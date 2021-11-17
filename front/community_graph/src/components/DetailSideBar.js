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
        {props.labDetail.name}
      </div>
    );
  };
  
  export default DetailSideBar;