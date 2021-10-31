import React, { useRef, useEffect } from "react";
import * as d3 from "d3";

import graph from "../data/graph.json"

const CommunityGraph = (props) => {
  const comGraph = useRef(null);

  const width = 960;
  const height = 500;

  useEffect(() => {
    console.log('graph', graph);
    const nodes = graph.nodes;
    const links = graph.links;

    // separation between same-color circles
    const padding = 4;

    // separation between different-color circles
    const clusterPadding = 16;

    const maxRadius = 20;

    const z = d3.scaleOrdinal(d3.schemeCategory10);

    // total number of nodes
    const n = nodes.length;

    const defaultRadius = 10;
    nodes.forEach(function (node) {
      node.r = defaultRadius;
    });

    // collect clusters from nodes
    const clusters = {};
    nodes.forEach((node) => {
      const radius = node.r;
      const clusterID = node.cluster;
      if (!clusters[clusterID] || (radius > clusters[clusterID].r)) {
        clusters[clusterID] = node;
      }
    });
    console.log('clusters', clusters);

    const svg = d3.select(comGraph.current)
      // .attr("style", "outline: thin solid black;")
      .attr('height', height)
      .attr('width', width)
      .append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`)
        // .attr("style", "outline: thin solid black;");

    let link = svg.selectAll('line')
      .data(links)
      .enter().append('line');

    link
      .attr('class', 'link')
      .style('stroke', 'darkgray')
      .style('stroke-width', '2px');

    const circles = svg.append('g')
      .datum(nodes)
      .selectAll('.circle')
      .data(d => d)
      .enter().append('circle')
        .attr('r', d => d.r)
        .attr('fill', d => z(d.cluster))
        .attr('stroke', 'black')
        .attr('stroke-width', 0.3)
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
      );

        
    const simulation = d3.forceSimulation(nodes)
      .nodes(nodes)
      .velocityDecay(0.2)
      .force('cluster', clustering)
      .force('collide', collide)
      // .force('collide', d3.forceCollide().strength(1).radius((d) => d.r + padding))
      .force('link', d3.forceLink())
      .on('tick', ticked);

    simulation.force('link')
      .links(links)
      .distance(function(d) {return d.weight*2;}).strength(0.1);
      // .distance([85]);
  
    function ticked() {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
  
      circles
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
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

    function centroid(nodes) {
      let x = 0;
      let y = 0;
      let z = 0;
      for (const d of nodes) {
        let k = d.r ** 2;
        x += d.x * k;
        y += d.y * k;
        z += k;
      }
      return {x: x / z, y: y / z};
    }

    function forceCluster() {
      const strength = 0.2;
      let nodes;

      function force(alpha) {
        const centroids = d3.rollup(nodes, centroid, d => d.cluster);
        const l = alpha * strength;
        for (const d of nodes) {
          const {x: cx, y: cy} = centroids.get(d.cluster);
          d.vx -= (d.x - cx) * l;
          d.vy -= (d.y - cy) * l;
        }
      }

      force.initialize = _ => nodes = _;

      return force;
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

  }, []);

  return (
    <div>
      <svg ref={comGraph} width={width} height={height}>
      </svg>
    </div>    
  )
};

export default CommunityGraph;