import React, { useRef, useEffect } from "react";
import * as d3 from "d3";

import graph from "../data/graph.json"

const CommunityGraph = (props) => {
  const comGraph = useRef(null);
  const sideBar = useRef(null);

  const width = 960;
  const height = 750;
  const sideBarWidth = 300;
  const sideBarHeight = 750;

  const width_padding = 0;
  var dur = 600;

  useEffect(() => {
    const nodes = graph.nodes;
    const links = graph.links;

    // separation between same-color circles
    const padding = 10;
    // separation between different-color circles
    const clusterPadding = padding * 15;

    var maxRadius = -1;
    const defaultRadius = 4;

    var centered;
    const scaleFactor = 1.2;
    var polygon, centroid;
    var valueline = d3.line()
                      .x(function(d) { return d[0]; })
                      .y(function(d) { return d[1]; })
                      .curve(d3.curveCatmullRomClosed);

    const z = d3.scaleOrdinal(d3.schemeCategory10);

    // total number of nodes
    const n = nodes.length;

    nodes.forEach(function (node) {
      // node.r = defaultRadius;

      // node size is mapped to "scale" property
      if (maxRadius < node.scale / 2) {
        maxRadius = node.scale / 2;
      }
      node.r = node.scale / 2;
    });
    // console.log('maxRadius', maxRadius);

    // collect clusters from nodes
    const clusters = {};
    nodes.forEach((node) => {
      const clusterID = node.cluster;
      if (!clusters[clusterID]) {
        clusters[clusterID] = node;
      }
    });
    // console.log('clusters', clusters);

    // side bar
    var bar = d3.select(sideBar.current);
    var barSvg = bar
      .attr("style", "outline: thin dashed black;")
      .attr('height', sideBarHeight)
      .attr('width', sideBarWidth)
      .attr('transform', `translate(10,0)`);
    


    // community graph
    var cur = d3.select(comGraph.current);

    var svg = cur
      .attr("style", "outline: thin dashed black;")
      .attr('height', height)
      .attr('width', width)
      .attr('transform', `translate(${width_padding}, 0)`)

      // graph
      .append('g')
        .attr('transform', `translate(${width / 2} , ${height / 2})`)
        .attr("style", "outline: thin solid black;");

    // link popup 
    var div = d3.select('body')
      .append("div")	
      .attr("class", "tooltip")				
      .style("opacity", 0);

    // for grouping
    var groups = svg.append('g')
                    .attr('class', 'groups');
    
    var groupIds = Array.from(new Set(nodes.map(function(n) { return +n.cluster; })))
                    .map( function (groupId) {
                      return {
                        groupId : groupId,
                        count : nodes.filter(function(n) { return +n.cluster == groupId; }).length
                      };
                    });

    // console.log('groupIds', groupIds);

    var paths = groups.selectAll('.path_placeholder')
                      .data(groupIds, function(d) {return +d})
                      .enter()
                      .append('g')
                      .attr('class', 'path_placeholder')
                      .append('path')
                      .attr('stroke', d => z(d))
                      .attr('fill', d => z(d))
                      .attr('opacity', 0)
                      .on('click', cluster_clicked);
        
    paths
      .transition()
      .duration(200)
      .attr('opacity', 1);

    
    // link
    let link = svg.selectAll('line')
      .data(links)
      .enter().append('line');

    link
      .attr('class', 'link')
      .style('stroke', 'darkgray')
      .style('stroke-width', '6px')  
      .attr('opacity', 0)    
      .on('click', link_clicked);
      // .on('click', node_clicked);

    // nodes
    const circles = svg.append('g')
      .datum(nodes)
      .selectAll('.circle')
      .data(d => d)
      .enter().append('circle')
        .attr('r', d => d.r)
        .attr('fill', d => z(d.cluster))
        .attr('stroke', 'black')
        .attr('stroke-width', 0.3)
        .attr('opacity', 0)   // initially invisible
        .call(d3.drag()
        .on('start', function(event, d) {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on('drag', function(event, d) {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on('end', function(event, d) {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        })
        )
        .on('click', node_clicked);

    
    const simulation = d3.forceSimulation(nodes)
      .nodes(nodes)
      .velocityDecay(0.2)
      .force('cluster', clustering)
      .force('collide', collide)
      .force('link', d3.forceLink())
      .on('tick', ticked);
  
    simulation.force('link')
      .links(graph.links)
      .distance(function(d) {return d.weight*2;}).strength(0.1);
      // .distance([85]);
  

    // helper functions
    function cluster_clicked(event, d) {
      var node;
      nodes.forEach(function(n) {
        // TODO : lighter? 
        if (n.cluster == d.groupId) {
          node = n;
        }
      });
      node_clicked(event, node);
    }

    function link_clicked(event, d) {
      if (d && link_clicked !== d) {
        div.transition()		
          .duration(200)		
          .style("opacity", .9);	

        div.html(d.id + "<br/>" + d.source_lab + "<br/>" + d.target_lab)
          .style("left", (event.pageX) + "px")		
          .style("top", (event.pageY - 28) + "px");

        link_clicked = d;
      } else {
        div.transition()  
        .duration(500)
        .style("opacity", 0);
    
        link_clicked = null;
      }
      
    }

    function node_clicked(event, d) {
      var x, y, k;

      // they are magic numbers...
      const x_offset = 120;
      const y_offset = 100;
  
      if (d && centered !== d) {
        // console.log('cenetered is not d');
        x = d.x;
        y = d.y;
        k = 4;
        centered = d;

      groups.transition()
        .attr('opacity', 0);

      circles.transition()
      .duration(dur)
      .attr('opacity', 1)
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + (-x-x_offset) + "," + (-y-y_offset) + ")")
  
      circles.classed('active', centered && function(d) { return d === centered; });

      link.transition()
          .duration(dur)
          .attr('opacity', 1)
          .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + (-x-x_offset) + "," + (-y-y_offset) + ")");    

      } else {
        // if clicked again, restore
        x = width / 2 - x_offset;
        y = height / 2 - y_offset;
        k = 1;
        centered = null;

          
        groups.transition()
          .duration(dur)
          .attr('opacity', 1);

        circles.transition()
        .duration(dur)
        .attr('opacity', 0)
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + (-x-x_offset) + "," + (-y-y_offset) + ")")
      
        circles.classed('active', centered && function(d) { return d === centered; });

        link.transition()
            .duration(dur)
            .attr('opacity', 0)
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + (-x-x_offset) + "," + (-y-y_offset) + ")");    
    
      }
      div.transition()  
        .duration(dur)
        .style("opacity", 0);

      }

  
    function ticked() {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
  
      circles
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);

      updateGroups();
    }

    // These are implementations of the custom forces
    function clustering(alpha) {
      nodes.forEach((d) => {
        const cluster = clusters[d.cluster];
        if (cluster === d) return;
        let x = d.x - cluster.x;
        let y = d.y - cluster.y;
        let l = Math.sqrt((x * x) + (y * y));
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
      const quadtree = d3.quadtree()
        .x(d => d.x)
        .y(d => d.y)
        .addAll(nodes);
  
      nodes.forEach((d) => {
        const r = d.r + maxRadius + Math.max(padding, clusterPadding);
        const nx1 = d.x - r;
        const nx2 = d.x + r;
        const ny1 = d.y - r;
        const ny2 = d.y + r;
        quadtree.visit((quad, x1, y1, x2, y2) => {
          if (quad.data && (quad.data !== d)) {
            let x = d.x - quad.data.x;
            let y = d.y - quad.data.y;
            let l = Math.sqrt((x * x) + (y * y));
            const r = d.r + quad.data.r + (d.cluster === quad.data.cluster ? padding : clusterPadding);
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

    var polygonGenerator = function(groupId) {
      var node_coords = circles
                          .data()
                          .filter(function(d) { return d.cluster == groupId.groupId; })
                          .map(function(d) { return [d.x, d.y];});
      return d3.polygonHull(node_coords);
      // return roundedHull(d3.polygonHull(node_coords));
    }

    function updateGroups() {
      groupIds.forEach( function(groupId) {
        var path = paths.filter(function (d) { return d == groupId; })
                        .attr('transform', 'scale(1) translate(0,0)')
                        .attr('d', function(d) {
                          polygon = polygonGenerator(d);
                          centroid = d3.polygonCentroid(polygon);

                          return valueline(
                            polygon.map(function(point) {
                              return [ point[0] - centroid[0], point[1] - centroid[1] ];
                            })
                          );
                        });
        d3.select(path.node().parentNode)
          .attr('transform', 'translate(' + centroid[0] + ',' + centroid[1] + `) scale(` + scaleFactor + ')')
      })
    }

  }, []);

  return (
    <div>
      <svg ref={comGraph} width={width} height={height}>
      </svg>
      <svg ref={sideBar} width={sideBarWidth} height={sideBarHeight}> 
			</svg>

    </div>    
  )
};

export default CommunityGraph;