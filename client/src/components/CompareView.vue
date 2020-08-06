<template>
  <div
    id="SelectViewSVG"
    style="height: 300px; width: 50%; overflow-x: hidden;"
  ></div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "SelectView",
  data() {
    svg: null;
  },
  mounted() {
    this.initialize();
    this.draw(this.svg);
  },
  methods: {
    initialize() {
      this.width = d3
        .select("#SelectViewSVG")
        .node()
        .getBoundingClientRect().width;
      this.height = d3
        .select("#SelectViewSVG")
        .node()
        .getBoundingClientRect().height;
      this.svg = d3
        .select("#SelectViewSVG")
        .append("svg")
        .attr("class", "d3SVG")
        .attr("width", this.width)
        .attr("height", this.height);
    },

    draw(svgNode) {
      var width = 300,
        height = 200;
      var svg = svgNode
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

      var radius = Math.min(width, height) / 2;
      var data = { a: 9, b: 20, c: 30, d: 8, e: 12 };

      // set the color scale
      var color = d3
        .scaleOrdinal()
        .domain(["a", "b", "c", "d", "e"])
        .range(["gold", "lightblue", "purple", "grey", "pink"]);

      // Compute the position of each group on the pie:
      var pie = d3
        .pie()
        .sort(null) // Do not sort group by size
        .value(function (d) {
          return d.value;
        });
      var data_ready = pie(d3.entries(data));

      // The arc generator
      var arc = d3
        .arc()
        .innerRadius(radius * 0.4) // This is the size of the donut hole
        .outerRadius(radius * 0.6);

      // Another arc that won't be drawn. Just for labels positioning
      var outerArc = d3
        .arc()
        .innerRadius(radius * 0.7)
        .outerRadius(radius * 0.7);

      // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
      svg
        .selectAll("allSlices")
        .data(data_ready)
        .enter()
        .append("path")
        .attr("d", arc)
        .attr("fill", function (d) {
          console.log(d.data.key);
          return color(d.data.key);
        })
        .attr("stroke", "white")
        .style("stroke-width", "2px")
        .style("opacity", 0.7);

      // Add the polylines between chart and labels:
      svg
        .selectAll("allPolylines")
        .data(data_ready)
        .enter()
        .append("polyline")
        .attr("stroke", "black")
        .style("fill", "none")
        .attr("stroke-width", 1)
        .attr("points", function (d) {
          var posA = arc.centroid(d); // line insertion in the slice
          var posB = outerArc.centroid(d); // line break: we use the other arc generator that has been built only for that
          var posC = outerArc.centroid(d); // Label position = almost the same as posB
          var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2; // we need the angle to see if the X position will be at the extreme right or extreme left
          posC[0] = radius * 0.95 * (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
          return [posA, posB, posC];
        });

      // Add the polylines between chart and labels:
      svg
        .selectAll("allLabels")
        .data(data_ready)
        .enter()
        .append("text")
        .text(function (d) {
          console.log(d.data.key);
          return d.data.key;
        })
        .attr("transform", function (d) {
          var pos = outerArc.centroid(d);
          var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2;
          pos[0] = radius * 0.99 * (midangle < Math.PI ? 1 : -1);
          return "translate(" + pos + ")";
        })
        .style("text-anchor", function (d) {
          var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2;
          return midangle < Math.PI ? "start" : "end";
        });
    },
  },
};
</script>
