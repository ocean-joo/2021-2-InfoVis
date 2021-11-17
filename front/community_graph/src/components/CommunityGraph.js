import React, { useRef, useEffect, useState } from "react";
import * as d3 from "d3";

import DetailSideBar from "./DetailSideBar";
import ControlPanel from "./ControlPanel";

import link_json from "../data/link.json";
import conf_json from "../data/conf.json";
import lab_json from "../data/lab.json";

const CommunityGraph = (props) => {
  const [labDetail, setLabDetail] = useState({});
  const [isLabView, setLabView] = useState(false);
  // it's percentage. should divide by 100 in below code
  const [weightRange, setWeightRange] = useState({ min: 0, max: 100 });

  const onChangeWeightRange = (e) => {
    setWeightRange(e);

    if (!isLabView) return;
    const filteredLabLink = d3
      .selectAll("line")
      .filter((d) => d.weight > weightRange.min && d.weight < weightRange.max);
    const TransparentLabLink = d3
      .selectAll("line")
      .filter((d) => d.weight < weightRange.min || d.weight > weightRange.max);

    console.log(weightRange, filteredLabLink.size(), TransparentLabLink.size());

    filteredLabLink.attr("opacity", 1);
    TransparentLabLink.attr("opacity", 0);
  };

  const schoolNameArray = [
    "Seoul National University",
    "KAIST",
    "POSTECH",
    "Yonsei University",
    "Korea University",
  ];
  const schoolList = {
    snu: { id: 0, name: "Seoul National University" },
    kaist: { id: 1, name: "KAIST" },
    postech: { id: 2, name: "POSTECH" },
    yonsei: { id: 3, name: "Yonsei University" },
    korea: { id: 4, name: "Korea University" },
  };
  const comGraph = useRef(null);
  const detailSideBar = useRef(null);

  // parameters for community graph location
  const comGraphWidth = 960;
  const comGraphHeight = 750;
  const comGraphWidthOffset = 80;
  const comGraphHeightOffset = 0;

  const comGraphWidthPadding = 0;
  var dur = 600;

  const detailSideBarWidth = 300;
  const detailSideBarHeight = 750;

  useEffect(() => {
    const nodes = lab_json;
    const links = link_json;

    // separation between same-color circles
    const nodePadding = 73;
    // separation between different-color circles
    const clusterPadding = nodePadding * 2;

    var maxRadius = 30;
    const defaultRadius = 4;

    var centered;
    const scaleFactor = 1.2;
    var polygon, centroid;
    var valueline = d3
      .line()
      .x(function (d) {
        return d[0];
      })
      .y(function (d) {
        return d[1];
      })
      .curve(d3.curveCatmullRomClosed);

    const schoolScale = d3.scaleOrdinal(d3.schemeCategory10);

    // total number of nodes
    const nodeNum = nodes.length;

    nodes.forEach(function (node) {
      node.r = defaultRadius;

      // node size is mapped to "scale" property
      // if (maxRadius < node.scale / 2) {
      // maxRadius = node.scale / 2;
      // }
      // node.r = node.scale / 2;
    });
    // console.log('maxRadius', maxRadius);

    // collect clusters from nodes
    const clusters = {};
    nodes.forEach((node) => {
      const clusterID = schoolList[node.school]["id"];
      if (!clusters[clusterID]) {
        clusters[clusterID] = node;
      }
    });
    // console.log('clusters', clusters);

    // side bar
    var detailSideBarSVG = d3
      .select(detailSideBar.current)
      .attr("style", "outline: thin dashed black;")
      .attr("height", detailSideBarHeight)
      .attr("width", detailSideBarWidth)
      .attr("transform", `translate(10,0)`);

    // TODO : Add paper info
    var detailSideBarText = detailSideBarSVG
      .selectAll("text")
      // [name, school, prof_name, email, description, href]
      .data(["", "", "", "", "", ""])
      .enter()
      .append("text")
      .text(function (d) {
        return d;
      })
      .attr("x", function (d, i) {
        return 30;
      })
      .attr("y", function (d, i) {
        return 30 * (i + 1);
      })
      .attr("font-family", "sans-serif")
      .attr("font-size", "11px")
      .attr("fill", "black")
      .attr("text-anchor", "middle")
      .attr("class", "detail_text");

    // community graph
    var comGraphSVG = d3
      .select(comGraph.current)
      .attr("style", "outline: thin dashed black;")
      .attr("height", comGraphHeight)
      .attr("width", comGraphWidth)
      .attr("transform", `translate(${comGraphWidthPadding}, 0)`)
      // graph
      .append("g")
      .attr(
        "transform",
        `translate(${comGraphWidth / 2 + comGraphWidthOffset} , ${comGraphHeight / 2 + comGraphHeightOffset
        })`
      );
    // .attr("style", "outline: thin solid black;");

    // link popup
    var linkPopup = d3
      .select("body")
      .append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);

    // for grouping
    var schoolNode = comGraphSVG.append("g").attr("class", "schoolNode");

    var schoolNodeData = Array.from(
      new Set(
        nodes.map(function (n) {
          return +schoolList[n.school]["id"];
        })
      )
    ).map(function (groupId) {
      return {
        groupId: groupId,
        count: nodes.filter(function (n) {
          return +schoolList[n.school]["id"] === groupId;
        }).length,
        x: 0,
        y: 0,
      };
    });

    var schoolNodeEdge = schoolNode
      .selectAll(".path_placeholder")
      .data(schoolNodeData, function (d) {
        return +d;
      })
      .enter()
      .append("g")
      .append("path")
      .attr("stroke", (d) => schoolScale(d))
      .attr("fill", (d) => schoolScale(d))
      .attr("opacity", 0)
      .on("click", cluster_clicked);

    schoolNodeEdge.transition().duration(200).attr("opacity", 1);

    var schoolText = schoolNode
      .selectAll(".path_placeholder")
      .data(schoolNodeData, function (d) {
        return +d;
      })
      .enter()
      .append("g")
      .append("text")
      .attr("font-family", "sans-serif")
      .attr("font-size", "13px")
      .attr("fill", "black")
      .attr("text-anchor", "middle")
      .attr("opacity", 1)
      .text((d, i) => {
        return schoolNameArray[i];
      });

    // link for lab
    let labLink = comGraphSVG
      .selectAll("line")
      .data(links)
      .enter()
      .append("line");

    labLink
      .attr("class", "link")
      .style("stroke", "darkgray")
      .style("stroke-width", "0.3px")
      .attr("opacity", 0)
      .on("click", link_clicked);
    // .on('click', node_clicked);

    // node for lab
    const labNode = comGraphSVG
      .append("g")
      .datum(nodes)
      .selectAll(".circle")
      .data((d) => d)
      .enter()
      .append("circle")
      .attr("r", (d) => d.r)
      .attr("fill", (d) => schoolScale(schoolList[d.school]["id"]))
      .attr("stroke", "black")
      .attr("stroke-width", 0.3)
      .attr("opacity", 0) // initially invisible
      .call(
        d3
          .drag()
          .on("start", function (event, d) {
            if (!event.active) simulation.alphaTarget(0.005).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", function (event, d) {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", function (event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      )
      .on("click", node_clicked);

    var labText = comGraphSVG
      .append("g")
      .datum(nodes)
      .selectAll(".text")
      .data((d) => d)
      .enter()
      .append("text")
      .attr("font-family", "sans-serif")
      .attr("font-size", "4px")
      .attr("fill", "black")
      .attr("text-anchor", "middle")
      .attr("opacity", 0)
      .text((d) => {
        if (d.name == "_") return "";
        else return d.name;
      });

    const simulation = d3
      .forceSimulation(nodes)
      .nodes(nodes)
      .velocityDecay(0.2)
      .force("cluster", clustering)
      .force("collide", collide)
      .force("link", d3.forceLink())
      .on("tick", ticked);

    simulation
      .force("link")
      .links(link_json)
      .distance(function (d) {
        return d.weight * 2;
      })
      .strength(0.1);
    // .distance([85]);

    // helper functions
    function cluster_clicked(event, d) {
      var node;
      nodes.forEach(function (n) {
        // TODO : lighter?
        if (schoolList[n.school]["id"] === d.groupId) {
          node = n;
        }
      });
      node_clicked(event, node);
    }

    function link_clicked(event, d) {
      if (d && link_clicked !== d) {
        linkPopup.transition().duration(200).style("opacity", 0.9);

        linkPopup
          .html(d.source.name + "<br/>" + d.target.name)
          .style("left", event.pageX + "px")
          .style("top", event.pageY - 28 + "px");

        link_clicked = d;
      } else {
        linkPopup.transition().duration(500).style("opacity", 0);

        link_clicked = null;
      }
    }

    function node_clicked(event, d) {
      var x, y, k;

      // they are magic numbers...
      const x_offset = 120;
      const y_offset = 100;

      if (d && centered !== d) {
        setLabView(true);

        // TODO : thicker stroke for the links in d's cluster
        x = d.x;
        y = d.y;
        k = 4;
        centered = d;

        schoolNode.transition().attr("opacity", 0);

        labText
          .transition()
          .duration(dur)
          .attr("opacity", 1)
          .attr(
            "transform",
            "translate(" +
            comGraphWidth / 2 +
            "," +
            comGraphHeight / 2 +
            ")scale(" +
            k +
            ")translate(" +
            (-x - x_offset) +
            "," +
            (-y - y_offset) +
            ")"
          );

        labNode
          .transition()
          .duration(dur)
          .attr("opacity", 1)
          .attr(
            "transform",
            "translate(" +
            comGraphWidth / 2 +
            "," +
            comGraphHeight / 2 +
            ")scale(" +
            k +
            ")translate(" +
            (-x - x_offset) +
            "," +
            (-y - y_offset) +
            ")"
          );

        labNode.classed(
          "active",
          centered &&
          function (d) {
            return d === centered;
          }
        );

        labLink
          .transition()
          .duration(dur)
          .attr("opacity", 1)
          .attr(
            "transform",
            "translate(" +
            comGraphWidth / 2 +
            "," +
            comGraphHeight / 2 +
            ")scale(" +
            k +
            ")translate(" +
            (-x - x_offset) +
            "," +
            (-y - y_offset) +
            ")"
          );

        // set lab detail info
        // TODO : Add paper Info
        var selectedLabDetail = {
          name: d.name,
          school: d.school,
          prof_name: d.prof_name,
          email: d.email,
          description: d.description,
          href: d.href,
        };
        setLabDetail(selectedLabDetail);
      } else {
        // if clicked again, restore
        setLabView(false);
        setLabDetail({});

        x = comGraphWidth / 2 - x_offset;
        y = comGraphHeight / 2 - y_offset;
        k = 1;
        centered = null;

        schoolNode.transition().duration(dur).attr("opacity", 1);

        labText
          .transition()
          .duration(dur)
          .attr("opacity", 0)
          .attr(
            "transform",
            "translate(" +
            comGraphWidth / 2 +
            "," +
            comGraphHeight / 2 +
            ")scale(" +
            k +
            ")translate(" +
            (-x - x_offset) +
            "," +
            (-y - y_offset) +
            ")"
          );

        labNode
          .transition()
          .duration(dur)
          .attr("opacity", 0)
          .attr(
            "transform",
            "translate(" +
            comGraphWidth / 2 +
            "," +
            comGraphHeight / 2 +
            ")scale(" +
            k +
            ")translate(" +
            (-x - x_offset) +
            "," +
            (-y - y_offset) +
            ")"
          );

        labNode.classed(
          "active",
          centered &&
          function (d) {
            return d === centered;
          }
        );

        labLink
          .transition()
          .duration(dur)
          .attr("opacity", 0)
          .attr(
            "transform",
            "translate(" +
            comGraphWidth / 2 +
            "," +
            comGraphHeight / 2 +
            ")scale(" +
            k +
            ")translate(" +
            (-x - x_offset) +
            "," +
            (-y - y_offset) +
            ")"
          );
      }
      linkPopup.transition().duration(dur).style("opacity", 0);

      detailSideBarText
        .data([
          d.name,
          schoolList[d.school]["name"],
          d.prof_name,
          d.email,
          d.description,
          d.href,
        ])
        .text(function (d) {
          return d;
        })
        .attr("x", function (d, i) {
          return 150;
        })
        .attr("y", function (d, i) {
          return 30 * (i + 1);
        })
        .attr("font-family", "sans-serif")
        .attr("font-size", "11px")
        .attr("fill", "black")
        .attr("text-anchor", "middle");
    }

    function ticked() {
      labLink
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      labNode.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

      labText.attr("x", (d) => d.x).attr("y", (d) => d.y - 5);

      schoolText.attr("x", (d) => d.x).attr("y", (d) => d.y);

      updateGroups();
    }

    // These are implementations of the custom forces
    function clustering(alpha) {
      nodes.forEach((d) => {
        const cluster = clusters[schoolList[d.school]["id"]];
        if (cluster === d) return;
        let x = d.x - cluster.x;
        let y = d.y - cluster.y;
        let l = Math.sqrt(x * x + y * y);
        const r = d.r + cluster.r;
        if (l !== r) {
          l = ((l - r) / l) * alpha;
          d.x -= x *= l;
          d.y -= y *= l;
          cluster.x += x;
          cluster.y += y;
        }
      });
    }

    function collide(alpha) {
      const quadtree = d3
        .quadtree()
        .x((d) => d.x)
        .y((d) => d.y)
        .addAll(nodes);

      nodes.forEach((d) => {
        const r = d.r + maxRadius + Math.max(nodePadding, clusterPadding);
        const nx1 = d.x - r;
        const nx2 = d.x + r;
        const ny1 = d.y - r;
        const ny2 = d.y + r;
        quadtree.visit((quad, x1, y1, x2, y2) => {
          if (quad.data && quad.data !== d) {
            let x = d.x - quad.data.x;
            let y = d.y - quad.data.y;
            let l = Math.sqrt(x * x + y * y);
            const r =
              d.r +
              quad.data.r +
              (schoolList[d.school]["id"] === schoolList[quad.data.school]["id"]
                ? nodePadding
                : clusterPadding);
            if (l < r) {
              l = ((l - r) / l) * alpha;
              d.x -= x *= l;
              d.y -= y *= l;
              quad.data.x += x;
              quad.data.y += y;
            }
          }
          return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
        });
      });
    }

    var polygonGenerator = function (groupId) {
      var node_coords = labNode
        .data()
        .filter(function (d) {
          return schoolList[d.school]["id"] === groupId.groupId;
        })
        .map(function (d) {
          return [d.x, d.y];
        });
      return d3.polygonHull(node_coords);
      // return roundedHull(d3.polygonHull(node_coords));
    };

    function updateGroups() {
      schoolNodeData.forEach(function (groupId) {
        var path = schoolNodeEdge
          .filter(function (d) {
            return d === groupId;
          })
          .attr("transform", "scale(1) translate(0,0)")
          .attr("d", function (d) {
            polygon = polygonGenerator(d);
            centroid = d3.polygonCentroid(polygon);

            return valueline(
              polygon.map(function (point) {
                return [point[0] - centroid[0], point[1] - centroid[1]];
              })
            );
          });
        d3.select(path.node().parentNode).attr(
          "transform",
          "translate(" +
          centroid[0] +
          "," +
          centroid[1] +
          `) scale(` +
          scaleFactor +
          ")"
        );

        groupId.x = centroid[0];
        groupId.y = centroid[1];
      });
    }
  }, []);

  return (
    <div style={{ display: "flex" }}>
      <ControlPanel
        weightRange={weightRange}
        setWeightRange={onChangeWeightRange}
      />
      <svg ref={comGraph} width={comGraphWidth} height={comGraphHeight} />
      <svg
        ref={detailSideBar}
        width={detailSideBarWidth}
        height={detailSideBarHeight}
      />
      <DetailSideBar
        labDetail={labDetail}
        ConfDetail={null}
        shouldVisualizeConf={false}
      />
    </div>
  );
};

export default CommunityGraph;