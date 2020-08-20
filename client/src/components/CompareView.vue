<template>
  <div class="row">
    <!--select strategies-->
    <div class="col-lg-1">
      <div class="form-group">
        <label for="exampleFormControlInput1">Strategies</label>
        <select id="strategy" class="selectpicker show-menu-arrow form-control" multiple>
          <option value="0">Logical</option>
          <option value="1">Storytelling</option>
          <option value="2">Authoritative</option>
          <option value="3">Evidence</option>
          <option value="4">Relevance</option>
          <option value="5">New ideas</option>
          <option value="6">Specific</option>
          <option value="7">Fluent</option>
        </select>
      </div>
    </div>

    <div class="col-lg-11">
      <!--summary view-->
      <div class="col-lg-4" style="height: 400px;  overflow-x: hidden;">
        
      </div>
      <!--rose chart view-->
      <div class="col-lg-4">
        <div id="CircleSVG" style="height: 400px;  overflow-x: hidden;"></div>
      </div>
      <!--bar view-->
      <div class="col-lg-4">
        <div id="RadarSVG" style="height: 220px; width: 220px; margin:auto;"></div>
        <div id="BarChartSVG" style="height: 240px; overflow-x: hidden;"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";

import input from "../input.json";
import labelSum from "../label_summary.json"
import dating_pos from "../dating-pos.json"

export default {
  name: "CompareView",
  data() {
    return {
      svg: null,
      svg1: null,
      pos: {},
      margin: { top: 30, right: 0, bottom: 0, left: 30 },
      svg2: null,
      labelRadar: labelSum["label_summary"][1]["dating"],

      examples: null,
      ex_id: "",
    };
  },
  mounted() {
    
    this.initialize();
    this.drawRadar(this.svg2, this.labelRadar);

    PipeService.$on(PipeService.UPDATE_COMPAREVIEW, () => {
      //console.log("---ok---");
      this.ex_id = DataService.ex_id;
      this.examples = DataService.examples;
      this.svg1.selectAll("*").remove();
      // this.svg.selectAll("*").remove();
      this.drawBar(this.svg1);
      this.drawRose(this.svg);
      //filtering val
      //console.log($("#strategy").val());
    });
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

      this.width2 = d3.select("#RadarSVG").node().getBoundingClientRect().width;
      this.height2 = d3
        .select("#RadarSVG")
        .node()
        .getBoundingClientRect().height;
      this.svg2 = d3
        .select("#RadarSVG")
        .append("svg")
        .attr("class", "d3SVG")
        .attr("width", this.width1)
        .attr("height", this.height1);
      2;
    },
    drawRadar(svgNode, d) {
      var cfg = {
        radius: 5,
        w: 160,
        h: 160,
        factor: 1,
        factorLegend: 0.6,
        levels: 5,
        maxValue: 150, //hard code
        radians: 2 * Math.PI,
        opacityArea: 0.5,
        ToRight: 5,
        TranslateX: 30, //margin left
        TranslateY: 30,  //margin top
        ExtraWidthX: 50,
        ExtraWidthY: 50,
        color: d3.scaleOrdinal().range(["#6F257F", "#CA0D59"]),
      };

      if ("undefined" !== typeof options) {
        for (var i in options) {
          if ("undefined" !== typeof options[i]) {
            cfg[i] = options[i];
          }
        }
      }
      var maxValue = Math.max(cfg.maxValue, d3.max(d, function(i){return d3.max(i.map(function(o){return o.value;}))}));
      //cfg.maxValue = 200; //??

      var allAxis = d[0].map(function (i, j) {
        return i.area;
      });
      var total = allAxis.length; //6
      
      var radius = cfg.factor * Math.min(cfg.w / 2, cfg.h / 2);
      var Format = d3.format("%");
      d3.select("#RadarSVG").select("svg").remove();


      var g = d3
        .select("#RadarSVG")
        .append("svg")
        .attr("width", cfg.w +  cfg.ExtraWidthX)
        .attr("height", cfg.h + cfg.ExtraWidthY)
        .append("g")
        .attr(
          "transform",
          "translate(" + cfg.TranslateX + "," + cfg.TranslateY + ")"
        );

      var tooltip;

      //Circular segments
      for (var j = 0; j < cfg.levels; j++) {
        var levelFactor = cfg.factor * radius * ((j + 1) / cfg.levels);
        g.selectAll(".levels")
          .data(allAxis)
          .enter()
          .append("svg:line")
          .attr("x1", function (d, i) {
            return (
              levelFactor *
              (1 - cfg.factor * Math.sin((i * cfg.radians) / total))
            );
          })
          .attr("y1", function (d, i) {
            return (
              levelFactor *
              (1 - cfg.factor * Math.cos((i * cfg.radians) / total))
            );
          })
          .attr("x2", function (d, i) {
            return (
              levelFactor *
              (1 - cfg.factor * Math.sin(((i + 1) * cfg.radians) / total))
            );
          })
          .attr("y2", function (d, i) {
            return (
              levelFactor *
              (1 - cfg.factor * Math.cos(((i + 1) * cfg.radians) / total))
            );
          })
          .attr("class", "line")
          .style("stroke", "grey")
          .style("stroke-opacity", "0.75")
          .style("stroke-width", "0.5px")
          .attr(
            "transform",
            "translate(" +
              (cfg.w / 2 - levelFactor) +
              ", " +
              (cfg.h / 2 - levelFactor) +
              ")"
          );
      }

      //Text indicating at what % each level is
      for (var j = 0; j < cfg.levels; j++) {
        var levelFactor = cfg.factor * radius * ((j + 1) / cfg.levels);
        g.selectAll(".levels")
          .data([1]) //dummy data
          .enter()
          .append("svg:text")
          .attr("x", function (d) {
            return levelFactor * (1 - cfg.factor * Math.sin(0));
          })
          .attr("y", function (d) {
            return levelFactor * (1 - cfg.factor * Math.cos(0));
          })
          .attr("class", "legend")
          .style("font-family", "sans-serif")
          .style("font-size", "10px")
          .attr(
            "transform",
            "translate(" +
              (cfg.w / 2 - levelFactor + cfg.ToRight) +
              ", " +
              (cfg.h / 2 - levelFactor) +
              ")"
          )
          .attr("fill", "#737373")
          .text(((j + 1) * cfg.maxValue) / cfg.levels);  //axis  maxValue
      }

      var series = 0;

      var axis = g
        .selectAll(".axis")
        .data(allAxis)
        .enter()
        .append("g")
        .attr("class", "axis");

      axis
        .append("line")
        .attr("x1", cfg.w / 2)
        .attr("y1", cfg.h / 2)
        .attr("x2", function (d, i) {   
          return (
            (cfg.w / 2) * (1 - cfg.factor * Math.sin((i * cfg.radians) / total))
          );
          
        })
        .attr("y2", function (d, i) {
          return (
            (cfg.h / 2) * (1 - cfg.factor * Math.cos((i * cfg.radians) / total))
          );
        })
        .attr("class", "line")
        .style("stroke", "grey")
        .style("stroke-width", "1px");

      
      axis
        .append("text")
        .attr("class", "legend")
        .text(function (d) {
          return d;
        })
        .style("font-family", "sans-serif")
        .style("font-size", "11px")
        .attr("text-anchor", "middle")
        .attr("dy", "1.2em")
        .attr("transform", function (d, i) {
          return "translate(0, -10)";
        })
        .attr("x", function (d, i) {
          return (
            (cfg.w / 2) *(1 - cfg.factorLegend * Math.sin((i * cfg.radians) / total)) -
            60 * Math.sin((i * cfg.radians) / total)
          );
        })
        .attr("y", function (d, i) {
          return (
            (cfg.h / 2) * (1 - Math.cos((i * cfg.radians) / total)) -
            20 * Math.cos((i * cfg.radians) / total)
          );
        });

      var dataValues = []; //add
      d.forEach(function (y, x) {
        g.selectAll(".nodes").data(y, function (j, i) {
          dataValues.push([
            (cfg.w / 2) *
              (1 -
                (parseFloat(Math.max(j.value, 0)) / cfg.maxValue) *
                  cfg.factor *
                  Math.sin((i * cfg.radians) / total)),
            (cfg.h / 2) *
              (1 -
                (parseFloat(Math.max(j.value, 0)) / cfg.maxValue) *
                  cfg.factor *
                  Math.cos((i * cfg.radians) / total)),
          ]);
        });
        dataValues.push(dataValues[0]);
        g.selectAll(".area")
          .data([dataValues])
          .enter()
          .append("polygon")
          .attr("class", "radar-chart-serie" + series)
          .style("stroke-width", "1px")
          .style("stroke", cfg.color(series))
          .attr("points", function (d) {
            var str = "";
            for (var pti = 0; pti < d.length; pti++) {
              str = str + d[pti][0] + "," + d[pti][1] + " ";
            }
            return str;
          })
          .style("fill", function (j, i) {
            return cfg.color(series);
          })
          .style("fill-opacity", cfg.opacityArea);
        // .on('mouseover', function (d){
        //           z = "polygon."+d3.select(this).attr("class");
        //           g.selectAll("polygon")
        //           .transition(200)
        //           .style("fill-opacity", 0.1);
        //           g.selectAll(z)
        //           .transition(200)
        //           .style("fill-opacity", .7);
        //           })
        // .on('mouseout', function(){
        //           g.selectAll("polygon")
        //           .transition(200)
        //           .style("fill-opacity", cfg.opacityArea);
        // });
        series++;
      });
      series = 0;

      // var tooltip = d3
      //   .select("#RadarSVG")
      //   .append("div")
      //   .attr("class", "toolTip");
      // d.forEach(function (y, x) {
      //   g.selectAll(".nodes")
      //     .data(y)
      //     .enter()
      //     .append("svg:circle")
      //     .attr("class", "radar-chart-serie" + series)
      //     .attr("r", cfg.radius)
      //     .attr("alt", function (j) {
      //       return Math.max(j.value, 0);
      //     })
      //     .attr("cx", function (j, i) {
      //       dataValues.push([
      //         (cfg.w / 2) *
      //           (1 -
      //             (parseFloat(Math.max(j.value, 0)) / cfg.maxValue) *
      //               cfg.factor *
      //               Math.sin((i * cfg.radians) / total)),
      //         (cfg.h / 2) *
      //           (1 -
      //             (parseFloat(Math.max(j.value, 0)) / cfg.maxValue) *
      //               cfg.factor *
      //               Math.cos((i * cfg.radians) / total)),
      //       ]);
      //       return (
      //         (cfg.w / 2) *
      //         (1 -
      //           (Math.max(j.value, 0) / cfg.maxValue) *
      //             cfg.factor *
      //             Math.sin((i * cfg.radians) / total))
      //       );
      //     })
      //     .attr("cy", function (j, i) {
      //       return (
      //         (cfg.h / 2) *
      //         (1 -
      //           (Math.max(j.value, 0) / cfg.maxValue) *
      //             cfg.factor *
      //             Math.cos((i * cfg.radians) / total))
      //       );
      //     })
      //     .attr("data-id", function (j) {
      //       return j.area;
      //     })
      //     .style("fill", "#fff")
      //     .style("stroke-width", "2px")
      //     .style("stroke", cfg.color(series))
      //     .style("fill-opacity", 0.9)
      //     .on("mouseover", function (d) {
      //       console.log(d.area);
      //       tooltip
      //         .style("left", d3.event.pageX - 40 + "px")
      //         .style("top", d3.event.pageY - 80 + "px")
      //         .style("display", "inline-block")
      //         .html(d.area + "<br><span>" + d.value + "</span>");
      //     })
      //     .on("mouseout", function (d) {
      //       tooltip.style("display", "none");
      //     });

      //   series++;
      // });
    }, //RadarChart

    drawBar(svgNode) {
      var width = this.width1,
        height = this.height1;
      var svg = svgNode.append("g");

      var index = this.examples.map((d) => d.id).indexOf(this.ex_id);

      if (this.ex_id !== "") {
        var exampledata = this.examples.map((d) => d.content)[index]
          .reply_contents;
        console.log("exampledata:");
        console.log(exampledata);

        var examplesum = {
          logos: 0,
          pathos: 0,
          ethos: 0,
          evidence: 0,
          relevance: 0,
          concreteness: 0,
          eloquence: 0,
        };
        exampledata.forEach((element) => {
          examplesum["logos"] += parseInt(element["logos"]);
          examplesum["pathos"] += parseInt(element["pathos"]);
          examplesum["ethos"] += parseInt(element["ethos"]);
          examplesum["evidence"] += parseInt(element["evidence"]);
          examplesum["relevance"] += parseInt(element["relevance"]);
          examplesum["concreteness"] += element["concreteness"];
          examplesum["eloquence"] += element["eloquence"];
        });
        // console.log(examplesum);

        var data = input["input"].map((d) => {
          // console.log(examplesum[d.feature] - d.label);
          return {
            feature: d.feature,
            label: examplesum[d.feature] - d.label,
          };
        });
        // console.log(data);

        data = data.sort((a, b) => d3.descending(a.label, b.label));
        // set the ranges
        var y = d3
          .scaleBand()
          .range([height - 40, 40])
          .padding(0.1);

        var x = d3.scaleLinear().range([40, width - 40]);

        // Scale the range of the data in the domains
        x.domain([
          d3.min(data, function (d) {
            return d.label;
          }),
          d3.max(data, function (d) {
            return d.label;
          }),
        ]);
        y.domain(
          data.map(function (d) {
            return d.feature;
          })
        );

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
          .attr("transform", "translate(0," + (height - 40) + ")")
          .call(d3.axisBottom(x));
        // add the y Axis
        svg
          .append("g")
          .attr("transform", "translate(" + x(0) + ",0)")
          .call(d3.axisLeft(y));
      }
      else {
        //var tempSum = this.labelRadar[0][1]["value"];
        //console.log("barSum", tempSum["area"]);

        // compute eloquenceSum & concretenessSum
        var eloquenceSum = 0;
        var concretenessSum = 0;
        this.examples.forEach((element) => {    //num of reply
          var tempElement = element.content.reply_contents;
          tempElement.forEach((d) =>{
            //console.log("this:", d.eloquence);
            eloquenceSum += parseInt(d.eloquence);
            concretenessSum += parseInt(d.concreteness);
          });
        });

        var barSum = {
          logos: this.labelRadar[0][1]["value"],
          pathos: this.labelRadar[0][2]["value"],
          ethos: this.labelRadar[0][3]["value"],
          evidence: this.labelRadar[0][4]["value"],
          relevance: this.labelRadar[0][5]["value"],
          concreteness: concretenessSum,
          eloquence: eloquenceSum,
        };
        //console.log("barSum", barSum);
        var dataInput = input["input"].map((d) => {
          // console.log(examplesum[d.feature] - d.label);
          return {
            feature: d.feature,
            label: barSum[d.feature] - d.label,
          };
        });
        //console.log("sum-input", dataInput);
        // sort for barChart show
        dataInput = dataInput.sort((a, b) => d3.descending(a.label, b.label));

        //draw Sumbar
        var y = d3
          .scaleBand()
          .range([height - 40, 40])
          .padding(0.1);

        var x = d3.scaleLinear().range([40, width - 40]);

        // Scale the range of the data in the domains
        x.domain([
          d3.min(dataInput, function (d) {
            return d.label;
          }),
          d3.max(dataInput, function (d) {
            return d.label;
          }),
        ]);
        y.domain(
          dataInput.map(function (d) {
            return d.feature;
          })
        );

        // append the rectangles for the bar chart
        svg
          .selectAll(".bar")
          .data(dataInput)
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
          .data(dataInput)
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
          .attr("transform", "translate(0," + (height - 40) + ")")
          .call(d3.axisBottom(x));
        // add the y Axis
        svg
          .append("g")
          .attr("transform", "translate(" + x(0) + ",0)")
          .call(d3.axisLeft(y));

      }

    },

    drawRose(svg) {
      // transform dating_pos
      var i = 0;
      dating_pos["16"].forEach((d) => {
        this.pos["dating-16-" + i] = d;
        i++;
      });
      var i = 0;
      dating_pos["17"].forEach((d) => {
        this.pos["dating-17-" + i] = d;
        i++;
      });
      var i = 0;
      dating_pos["19"].forEach((d) => {
        this.pos["dating-19-" + i] = d;
        i++;
      });
      var i = 0;
      dating_pos["20"].forEach((d) => {
        this.pos["dating-20-" + i] = d;
        i++;
      });
      var i = 0;
      dating_pos["21"].forEach((d) => {
        var id = "dating-21-" + i;
        this.pos["dating-21-" + i] = d;
        i++;
      });
      var i = 0;
      dating_pos["22"].forEach((d) => {
        this.pos["dating-22-" + i] = d;
        i++;
      });
      var i = 0;
      dating_pos["23"].forEach((d) => {
        this.pos["dating-23-" + i] = d;
        i++;
      });
      var i = 0;
      dating_pos["25"].forEach((d) => {
        this.pos["dating-25-" + i] = d;
        i++;
      });
      var i = 0;
      dating_pos["26"].forEach((d) => {
        this.pos["dating-26-" + i] = d;
        i++;
      });
      console.log(this.pos);

      // x, y scale
      var xdomain = Object.values(this.pos).map((d) => d[0]),
        ydomain = Object.values(this.pos).map((d) => d[1]),
        outerRdomain = this.examples.map((d) =>
          parseInt(d.content["reply_delta_num"])
        ),
        height = this.height - this.margin.bottom - this.margin.top,
        width = this.width - this.margin.right - this.margin.left;

      var xScale = d3
        .scaleLinear()
        .domain(d3.extent(xdomain))
        .range([this.margin.left, width - this.margin.right]);

      var yScale = d3
        .scaleLinear()
        .domain(d3.extent(ydomain))
        .range([this.margin.top, height - this.margin.bottom]);
      // background r scale
      var outerRScale = d3
        .scaleLinear()
        .domain(d3.extent(outerRdomain)) // depends on delta
        .range([20, 40]);
      var examples = this.examples;

      // draw rose
      function drawFrontRose(d, id, pos) {
        var exampledata = d.content["reply_contents"];
        // console.log(exampledata);
        var examplesum = [
          { feature: "is_claim", label: 0 },
          { feature: "logos", label: 0 },
          { feature: "pathos", label: 0 },
          { feature: "ethos", label: 0 },
          { feature: "evidence", label: 0 },
          { feature: "relevance", label: 0 },
        ];
        exampledata.forEach((element) => {
          examplesum[0].label += parseInt(element["is_claim"]);
          examplesum[1].label += parseInt(element["logos"]);
          examplesum[2].label += parseInt(element["pathos"]);
          examplesum[3].label += parseInt(element["ethos"]);
          examplesum[4].label += parseInt(element["evidence"]);
          examplesum[5].label += parseInt(element["relevance"]);
        });
        examplesum = examplesum.map((d) => {
          return {
            feature: d.feature,
            label: d.label,
            radius: Math.sqrt(d.label) / Math.PI,
          };
        });

        // examplesum = examplesum.sort((a, b) => d3.descending(a.label, b.label));


        var total_label = 0;
        examplesum.forEach((element) => {
          total_label += element.label;
        });

        // console.log(examplesum);

        var total_r = Math.sqrt(total_label) / Math.PI;

        // set inner radius scale:
        var outerR = outerRScale(d.content["reply_delta_num"]);
        var innerRdomain = examplesum.map((d) => d.radius);
        var innerRScale = d3
          .scaleLinear()
          .domain([d3.min(innerRdomain), total_r])
          .range([0, outerR]);

        // Compute the position of each group on the pie:
        var pie = d3.pie().value(function (d) {
          return 1; // equal arc
        });
        var data_ready = pie(d3.entries(examplesum));

        // set color scale:
        var color = d3
          .scaleOrdinal()
          .domain([
            "logos",
            "pathos",
            "ethos",
            "relevance",
            "evidence",
            "is_claim",
          ])
          .range([
            "#7eb6e4",
            "#8cd390",
            "#8f91fc",
            "#e05c5c",
            "#fa8cad",
            "#b6034d",
          ]);

        // set tooltips
        var div = d3
          .select("body")
          .append("div")
          .attr("class", "tooltip")
          .style("opacity", 0);

        svg
          .selectAll("whatever")
          .data(data_ready)
          .enter()
          .append("path")
          .attr("transform", () => {
            return (
              "translate(" + xScale(pos[id][0]) + "," + yScale(pos[id][1]) + ")"
            );
          })
          .attr(
            "d",
            d3
              .arc()
              .innerRadius(0)
              .outerRadius((d) => {
                return innerRScale(d.data.value.radius);
              })
          )
          .attr("fill", (d) => {
            return color(d.data.value.feature);
          })
          .attr("stroke", "black")
          .style("stroke-width", "1px")
          .style("opacity", 0.7)
          .on("mouseover", (d) => {
            div.transition().duration(200).style("opacity", 0.7);
            div
              .html(d.data.value.feature + ":" + d.data.value.label)
              .style("left", d3.event.pageX + "px")
              .style("top", d3.event.pageY - 28 + "px");
          })
          .on("mouseout", function (d) {
            div.transition().duration(500).style("opacity", 0);
            // d3.selectAll(".tooltip").remove();
          });
      }

      // background pie
      function drawBackRose(r, id, pos) {
        var pie = d3.pie().value(function (d) {
          return 1; // equal arc
        });
        var data_ready = pie(d3.entries(d3.range(6)));
        svg
          .selectAll("whatever")
          .data(data_ready)
          .enter()
          .append("path")
          .attr("transform", () => {
            return (
              "translate(" + xScale(pos[id][0]) + "," + yScale(pos[id][1]) + ")"
            );
          })
          .attr("d", d3.arc().innerRadius(0).outerRadius(r))
          .attr("fill", "lightblue")
          .attr("stroke", "black")
          .style("stroke-width", "1px")
          .style("opacity", 0.7);
      }

      // combine pie and rose
      var circles = svg
        .selectAll("circle")
        .data(this.examples)
        .enter()
        .each((d, i) =>
          drawBackRose(
            outerRScale(d.content["reply_delta_num"]),
            d.id,
            this.pos
          )
        )
        .append("circle")
        .attr("class", "pie")
        .attr("cx", (d, i) => {
          return xScale(this.pos[d.id][0]);
        })
        .attr("cy", (d, i) => yScale(this.pos[d.id][1]))
        .attr("r", (d) => outerRScale(d.content["reply_delta_num"]))
        .style("opacity", 0.7)
        .style("fill", "white")
        // .on("mouseover", (d, i) => {
        //   // d3.select(this).style("fill","red");
        //   d3.selectAll(".pie")
        //     .filter((circle, index) => {
        //       console.log(d);
        //       console.log(i);

        //       return i === index;
        //     })
        //     .style("fill", "red")
        //     .attr("class", "highlightCircle");
        //   // .classed("highlightCircle", true); ???
        // })
        // .on("mouseout", (d, i) => {
        //   d3.selectAll(".highlightCircle")
        //     .style("fill", "white")
        //     // .filter((circle, index) => i === index)
        //     .classed("highlightCircle", false);
        // })
        .on("click", (d) => {
          //muliple select

          DataService.ex_id = d.id;
          PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
          PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
          PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
        })
        .each((d) => drawFrontRose(d, d.id, this.pos));
    },
  },
};
</script>

<style scoped></style>
