<template>
  <div class="row">
    <div id="CircleSVG" style="height: 400px; width: 50%; overflow-x: hidden;"></div>
    <!-- <div id="chartholder"></div> -->

    <div id="BarChartSVG" style="height: 400px; width: 50%; overflow-x: hidden;"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";

import json from "../ideal.json";
import input from "../input.json";

export default {
  name: "CompareView",
  data() {
    return {
      svg: null,
      svg1: null,
      pos: [
        [-122.181656, -387.4932],
        [65.003456, -162.4631],
        [-313.18588, 91.801956],
        [-225.66704, -151.02963],
        [163.1909, -408.45877],
        [355.8698, -196.94835],
        [164.89957, 282.22745],
        [-22.538868, 57.171097],
      ],
      margin: { top: 10, right: 30, bottom: 30, left: 30 },
      examples: null,
      ex_order: null,
    };
  },
  mounted() {
    this.initialize();
    console.log("---ok---before on");
    PipeService.$on(PipeService.UPDATE_COMPAREVIEW, () => {
    console.log("---ok---");
    this.ex_order = DataService.ex_order;
    this.examples = DataService.examples;
    this.drawCircle(this.svg);
    console.log(this.examples);
    this.drawBar(this.svg1);
    });
    // this.drawRose();
  },
  methods: {
    initialize() {
      this.width = d3.select("#CircleSVG").node().getBoundingClientRect().width;
      this.height = d3
        .select("#CircleSVG")
        .node()
        .getBoundingClientRect().height;
      this.svg = d3
        .select("#CircleSVG")
        .append("svg")
        .attr("class", "d3SVG")
        .attr("width", this.width)
        .attr("height", this.height);

      this.width1 = d3
        .select("#BarChartSVG")
        .node()
        .getBoundingClientRect().width;
      this.height1 = d3
        .select("#BarChartSVG")
        .node()
        .getBoundingClientRect().height;
      this.svg1 = d3
        .select("#BarChartSVG")
        .append("svg")
        .attr("class", "d3SVG")
        .attr("width", this.width1)
        .attr("height", this.height1);
    },

    drawCircle(svgNode) {
      var xdomain = this.pos.map((d) => d[0]),
        ydomain = this.pos.map((d) => d[1]),
        height = this.height - this.margin.bottom,
        width = this.width - this.margin.right;

      var xScale = d3
        .scaleLinear()
        .domain(d3.extent(xdomain))
        .range([this.margin.left, width]);

      var yScale = d3
        .scaleLinear()
        .domain(d3.extent(ydomain))
        .range([height, this.margin.top]);

      svgNode
        .append("g")
        .attr("transform", "translate(" + this.margin.left + ")")
        .call(d3.axisLeft(yScale));

      svgNode
        .append("g")
        .attr("transform", "translate(30," + height + ")")
        .call(d3.axisBottom(xScale));

      for (var i = 0; i < this.pos.length; i++) {
        // var circles = d3
        // .selectAll("circle")
        // .data(this.examples)
        // .enter()
        svgNode
          .append("circle")
          .attr("class", "pie")
          // .attr("cx", (d, i) => xScale(this.pos[i][0]))
          // .attr("cy", (d, i) => yScale(this.pos[i][1]))
          .attr("cx", () => xScale(this.pos[i][0]))
          .attr("cy", () => yScale(this.pos[i][1]))
          .attr("r", 10)
          .style("opacity", 0.7)
          .style("fill", "orange");
        // .on("click", (d, i) => {
        // d3.select(this).style("stroke", "red");

        // DataService.ex_order = i;
        // });
      }
    },

    drawBar(svgNode) {
      var width = 300,
        height = 200;
      var svg = svgNode.append("g");

      //data
      var data = [
        { feature: "logos", label: 5 },
        { feature: "pathos", label: -1 },
        { feature: "ethos", label: 1 },
        { feature: "evidence", label: 2 },
        { feature: "relevance", label: 4 },
        { feature: "concreteness", label: 0.04 },
        { feature: "eloquence", label: -1 },
      ];

      data = data.sort((a, b) => d3.descending(a.label, b.label));

      // set the ranges
      var y = d3.scaleBand().range([height, 0]).padding(0.1);

      var x = d3.scaleLinear().range([0, width]);

      // Scale the range of the data in the domains
      x.domain([
        -50,
        d3.max(data, function (d) {
          return d.label;
        }),
      ]);
      y.domain(
        data.map(function (d) {
          return d.feature;
        })
      );
      //y.domain([0, d3.max(data, function(d) { return d.label; })]);

      // append the rectangles for the bar chart
      svg
        .selectAll(".bar")
        .data(data)
        .enter()
        .append("rect")
        // .attr("class", (d) => {
        //   return "bar-" + (d.label < 0 ? "neg" : "pos");
        // })
        .style("fill", (d) => (d.label > 0 ? "lightblue" : "#f0a2a2"))
        .attr("width", (d) => {
          return Math.abs(x(d.label) - x(0));
        })
        .attr("x", (d) => {
          return x(Math.min(0, d.label));
        })
        .attr("y", function (d) {
          return y(d.feature);
        })
        .attr("height", y.bandwidth());

      svg
        .selectAll("text")
        .data(data)
        .enter()
        .append("text")
        .text((d) => d.label)
        .attr("x", (d) => x(d.label))
        .attr("y", function (d) {
          return y(d.feature) + y.bandwidth() / 2;
        })
        .attr("text-anchor", (d) => (d.label < 0 ? "end" : "start"))
        .style("fill", (d) => (d.label < 0 ? "darkred" : "darkblue"));

      // add the x Axis
      svg
        .append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

      // add the y Axis
      svg
        .append("g")
        .attr("transform", "translate(" + x(0) + ",0)")
        .call(d3.axisLeft(y));
    },

    /*
    drawRose() {
      console.log(json);
      d3.json("../ideal.json").then(function (json) {
        console.log(json);
        var colors = ["lightblue", "orange"];
        var chart = d3.ez.chart.roseChart().colors(colors);
        var legend = d3.ez.component.legend().title("Causes of Mortality");
        var title = d3.ez.component
          .title()
          .mainText(
            "Diagram of the Causes of Mortality in the Army in The East"
          )
          .subText("April 1854 to March 1855");

        // Convert json to d3-ez data format

        var data = d3
          .nest()
          .key(function (d) {
            return d.feature;
          })
          .entries(json)
          .map(function (obj) {
            console.log(obj);

            var rec = obj.values[0];
            var scalar = 0.3;

            var values = {
              key: rec.feature,
              values: [
                {
                  key: "Example",
                  value: Math.sqrt(rec.example * scalar) / Math.PI,
                },
                {
                  key: "Input",
                  value: Math.sqrt(rec.input * scalar) / Math.PI,
                },
              ],
            };

            console.log(values);
            return values;
          });

        console.log(data);

        // Create chart base
        var myChart = d3.ez
          .base()
          .width(700)
          .height(400)
          .chart(chart)
          .legend(legend)
          //   .title(title)
          .on("customValueMouseOver", function (d) {
            d3.select("#message").text(d.value);
          });

        // Add to page
        d3.select("#chartholder").datum(data).call(myChart);
      });
    },
    */
  },
};
</script>

<style scoped>
.bar-pos {
  fill: lightblue;
}
.bar-neg {
  fill: rgb(240, 162, 162);
}
text {
  font-family: "Trebuchet MS", "Lucida Sans Unicode", "Lucida Grande",
    "Lucida Sans", Arial, sans-serif;
  font-size: 2em;
}
</style>
