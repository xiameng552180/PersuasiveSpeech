<template>
  <div class="row">
    <!-- <div id="PieChartSVG" style="height: 300px; width: 50%; overflow-x: hidden;"></div> -->
    <!-- <div id="chartholder"></div> -->
    <!-- <br />
    <div>
      Value:
      <span id="message"></span>
    </div>-->
    <div id="BarChartSVG" style="height: 300px; width: 50%; overflow-x: hidden;"></div>
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "CompareView",
  data() {
    svg: null;
    svg1: null;
  },
  mounted() {
    this.initialize();
    // this.drawPie(this.svg);
    this.drawBar(this.svg1);
    // this.drawRose();
  },
  methods: {
    /*
    drawRose() {
      d3.json("../ideal.json").then(function (json) {
        console.log("json");
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
    initialize() {
      // this.width = d3
      //   .select("#PieChartSVG")
      //   .node()
      //   .getBoundingClientRect().width;
      // this.height = d3
      //   .select("#PieChartSVG")
      //   .node()
      //   .getBoundingClientRect().height;
      // this.svg = d3
      //   .select("#PieChartSVG")
      //   .append("svg")
      //   .attr("class", "d3SVG")
      //   .attr("width", this.width)
      //   .attr("height", this.height);

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

    drawPie(svgNode) {
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

    drawBar(svgNode) {
      var width = 300,
        height = 200;
      var svg = svgNode.append("g");

      //data
      var data = [
        { feature: "Logos", label: -33 },
        { feature: "Pathos", label: -12 },
        { feature: "Ethos", label: -41 },
        { feature: "Evidence", label: 16 },
        { feature: "Relevance", label: 59 },
        { feature: "Others", label: 38 },
      ];

      data = data.sort((a, b) => d3.descending(a.label, b.label));
      console.log(data);

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
