<template>
  <div class="row">
    <!--select strategies-->
    <div class="col-lg-2">
      <div id="RadarSVG" style="width:100px;margin-left:10px;"></div>
      <!-- <div class="form-group">
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
      </div>-->
      
    </div>

    <div class="col-lg-10">
      <!--summary view-->
      <!-- <div class="col-lg-3" style="height: 400px;  overflow-x: hidden;">
        <svg id="nodelink" height="400"/>
      </div>-->
      <!--rose chart view-->
      <div class="col-lg-5">
        <div id="CircleSVG" style="height: 400px; width: 420px; overflow-auto;"></div>
        <div class="row" id="multiSelectDiv">
          <input type="checkbox" id="multipleS" v-on:click="mulipleSelect" data-toggle="toggle" /> &nbsp;
          <label id="cbTxt">Select is disabled</label>&nbsp;
          <p id="selectInd"></p>
          <!-- <button class="btn btn-primary" id = "genBar" v-on:click="sumbitArray" style="display:none;">yes</button> -->
        </div>
      </div>
      <!--bar view-->
      <div class="col-lg-5">
        
        <div id="BarChartSVG"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";

// import input from "../input.json";
import labelSum from "../label_summary_persent.json";
import dating_pos from "../dating-pos.json";
// import dating16 from "../dating-16.json"; //for nodelink
//pos test
import abortionPos from "../pos_data/abortion-pos.json";
import datingPos from "../pos_data/dating-pos.json";
import eugenicsPos from "../pos_data/eugenics-pos.json";
import immortalityPos from "../pos_data/immortality-pos.json";
import marriagePos from "../pos_data/marriage-pos.json";
import parenthoodPos from "../pos_data/parenthood-pos.json";
import pridePos from "../pos_data/pride-pos.json";
import suicidePos from "../pos_data/suicide-pos.json";

export default {
  name: "CompareView",
  data() {
    return {
      svg: null,
      svg1: null,
      pos: {},
      margin: { top: 30, right: 0, bottom: 0, left: 30 },
      svg2: null,
      //svg3: null, nodelink
      labelRadar: labelSum["label_summary"][0]["Abortion"],
      selectIDarray: [],
      selectIDIndex: [],
      selectTopic: "",
      selectTopicNum: "",
      examples: null,
      ex_id: "",
      //simulation1: null, nodelink
      examplesum: {
        logos: 0,
        pathos: 0,
        ethos: 0,
        evidence: 0,
        relevance: 0,
        is_claim: 0,
        eloquence: 0,
      },
      flag: 0,
      inputLabels: {},
      //node: null, nodelink
      //link: null, nodelink
      posRose: null,
    };
  },
  mounted() {
    this.initialize();
    // console.log(dating16);
    PipeService.$on(PipeService.UPDATE_COMPAREVIEW, () => {
      //console.log("---ok---");
      this.ex_id = DataService.ex_id;
      this.examples = DataService.examples;
      this.selectIDarray = DataService.selectIDarray;
      this.selectIDIndex = DataService.selectIDIndex;
      this.examplesum = DataService.examplesum;
      //filtering
      this.selectTopic = DataService.selectTopic;
      this.selectTopicNum = DataService.selectTopicNum;
      //console.log("selectview", this.selectTopicNum);

      //draw
      var numTemp = parseInt(this.selectTopicNum, 10);
      //console.log("Select topic: ",numTemp, this.selectTopic);
      //console.log(labelSum["label_summary"][numTemp][this.selectTopic]);
      //console.log("compare: ", labelSum["label_summary"][1]["Dating"]);
      this.labelRadar = labelSum["label_summary"][numTemp][this.selectTopic];

      this.svg.selectAll("*").remove();
      this.svg1.selectAll("*").remove();
      this.posRose = {
        Abortion: abortionPos,
        Dating: datingPos,
        Eugenics: eugenicsPos,
        Immortality: immortalityPos,
        Marriage: marriagePos,
        Parenthood: parenthoodPos,
        Pride: pridePos,
        Suicide: suicidePos,
      };

      // this.svg.selectAll("*").remove();
      //console.log("testpos1:", this.posRose[this.selectTopic]);

      this.drawRose(this.svg, this.posRose[this.selectTopic]);
      this.drawRadarRose(this.svg2, this.labelRadar);
      this.drawBar(this.svg1);
      //this.drawNodeLink(this.svg3); //nodelink
      //filtering val
      //console.log($("#strategy").val());
    });
  },
  methods: {
    initialize() {
      this.inputLabels = DataService.inputLabels; //input data labelsSum
      console.log("inputlabel-Compareview:", this.inputLabels);

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

      this.width1 = 500;
        //d3
        // .select("#BarChartSVG")
        // .node()
        // .getBoundingClientRect().width;
      this.height1 = 400;
        // d3
        // .select("#BarChartSVG")
        // .node()
        // .getBoundingClientRect().height;
      this.svg1 = d3
        .select("#BarChartSVG")
        .append("svg")
        .attr("class", "d3SVG")
        .attr("width", this.width1)
        .attr("height", this.height1);

      this.width2 = 100;
      //d3.select("#RadarSVG").node().getBoundingClientRect().width;
      this.height2 = 200;
        // d3
        // .select("#RadarSVG")
        // .node()
        // .getBoundingClientRect().height;
      this.svg2 = d3
        .select("#RadarSVG")
        .append("svg")
        .attr("class", "d3SVG")
        .attr("width", this.width1)
        .attr("height", this.height1);

      this.width3 = d3.select("#nodelink").node().getBoundingClientRect().width;
      this.height3 = d3
        .select("#nodelink")
        .node()
        .getBoundingClientRect().height;
      this.svg3 = d3
        .select("#nodelink")
        .attr("width", this.width3)
        .attr("height", this.height3);
    },

    mulipleSelect: function (event) {
      if ($("#cbTxt").text() == "Select is enabled") {
        //disable
        console.log("close");
        $("#selectInd").text("");
        DataService.selectIDarray = [];
        DataService.selectIDIndex = [];
        $("#cbTxt").text("Select is disabled");
        $("#genBar").css("display", "none");
      } else {
        console.log("open");
        $("#cbTxt").text("Select is enabled");
        $("#genBar").css("display", "block");
      }
    },

    drawRadarRose(svg, d) {
      var height = 200,
        width = 100;

      // draw back rose
      var pie = d3.pie().value(function (d) {
        return 1; // equal arc
      });
      var data_ready1 = pie(d3.entries(d3.range(6)));

      svg
        .selectAll("whatever")
        .data(data_ready1)
        .enter()
        .append("path")
        .attr("transform", () => {
          return "translate(" + width / 2 + "," + height / 2 + ")";
        })
        .attr("d", d3.arc().innerRadius(0).outerRadius(40))
        .attr("fill", "lightblue")
        .attr("stroke", "black")
        .style("stroke-width", "1px")
        .style("opacity", 0.7);

      // draw front rose
      var Rosesum = [
        { feature: "is_claim", label: 0 },
        { feature: "logos", label: 0 },
        { feature: "pathos", label: 0 },
        { feature: "ethos", label: 0 },
        { feature: "evidence", label: 0 },
        { feature: "relevance", label: 0 },
      ];

      Rosesum[0].label += d[0][0].value;
      Rosesum[1].label += d[0][1].value;
      Rosesum[2].label += d[0][2].value;
      Rosesum[3].label += d[0][3].value;
      Rosesum[4].label += d[0][4].value;
      Rosesum[5].label += d[0][5].value;

      Rosesum = Rosesum.map((d) => {
        return {
          feature: d.feature,
          label: d.label,
          radius: Math.sqrt(d.label) / Math.PI,
        };
      });

      var total_label = 0;
      Rosesum.forEach((element) => {
        total_label += element.label;
      });
      console.log(Rosesum);

      var total_r = Math.sqrt(total_label) / Math.PI;

      // set inner radius scale:
      var outerR = 40;
      var innerRdomain = Rosesum.map((d) => d.radius);
      var innerRScale = d3
        .scaleLinear()
        .domain([d3.min(innerRdomain), total_r])
        .range([0, outerR]);

      // Compute the position of each group on the pie:
      var pie = d3.pie().value(function (d) {
        return 1; // equal arc
      });
      var data_ready2 = pie(d3.entries(Rosesum));

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
        .data(data_ready2)
        .enter()
        .append("path")
        .attr("transform", () => {
          return "translate(" + width / 2 + "," + height / 2 + ")";
        })
        .attr(
          "d",
          d3
            .arc()
            .innerRadius(0)
            .outerRadius((d) => {
              // console.log(d);
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
    },

    drawRadar(svgNode, d) {
      var cfg = {
        radius: 5,
        w: 160,
        h: 160,
        factor: 1,
        factorLegend: 0.6,
        levels: 5,
        maxValue: 0, //decided later
        radians: 2 * Math.PI,
        opacityArea: 0.5,
        ToRight: 5,
        TranslateX: 30, //margin left
        TranslateY: 30, //margin top
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
      var maxValue = Math.max(
        cfg.maxValue,
        d3.max(d, function (i) {
          return d3.max(
            i.map(function (o) {
              return o.value;
            })
          );
        })
      );
      //console.log("radarMax:", maxValue);
      cfg.maxValue = maxValue; //??

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
        .attr("width", cfg.w + cfg.ExtraWidthX)
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
          .style("font-size", "12px")
          .attr(
            "transform",
            "translate(" +
              (cfg.w / 2 - levelFactor + cfg.ToRight) +
              ", " +
              (cfg.h / 2 - levelFactor) +
              ")"
          )
          .attr("fill", "#737373")
          .text(((j + 1) * cfg.maxValue) / cfg.levels); //axis  maxValue
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
        .style("font-size", "141px")
        .attr("text-anchor", "middle")
        .attr("dy", "1.2em")
        .attr("transform", function (d, i) {
          return "translate(0, -10)";
        })
        .attr("x", function (d, i) {
          return (
            (cfg.w / 2) *
              (1 - cfg.factorLegend * Math.sin((i * cfg.radians) / total)) -
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

      //console.log("EX.ID:", this.ex_id, this.selectIDIndex, this.flag);
      if (this.ex_id !== "") {
        if (this.selectIDIndex.length == 0) {
          //draw single data
          this.examplesum = {
            logos: 0,
            pathos: 0,
            ethos: 0,
            evidence: 0,
            relevance: 0,
            is_claim: 0,
            eloquence: 0,
          };
          var exampledata = this.examples.map((d) => d.content)[index]
            .reply_contents;
          exampledata.forEach((element) => {
            this.examplesum["logos"] += parseInt(element["logos"]);
            this.examplesum["pathos"] += parseInt(element["pathos"]);
            this.examplesum["ethos"] += parseInt(element["ethos"]);
            this.examplesum["evidence"] += parseInt(element["evidence"]);
            this.examplesum["relevance"] += parseInt(element["relevance"]);
            this.examplesum["is_claim"] += parseInt(element["is_claim"]);
            this.examplesum["eloquence"] += element["eloquence"];
          });
          console.log("examplesum:", this.examplesum);
          DataService.examplesum = this.examplesum;
          PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
        } else {
          //draw group data

          this.examplesum = {
            logos: 0,
            pathos: 0,
            ethos: 0,
            evidence: 0,
            relevance: 0,
            is_claim: 0,
            eloquence: 0,
          };
          this.selectIDIndex.forEach((ind) => {
            //all replies
            var exampledata = this.examples.map((d) => d.content)[ind]
              .reply_contents;

            exampledata.forEach((sentence) => {
              this.examplesum["logos"] += parseInt(sentence["logos"]);
              this.examplesum["pathos"] += parseInt(sentence["pathos"]);
              this.examplesum["ethos"] += parseInt(sentence["ethos"]);
              this.examplesum["evidence"] += parseInt(sentence["evidence"]);
              this.examplesum["relevance"] += parseInt(sentence["relevance"]);
              this.examplesum["is_claim"] += parseInt(sentence["is_claim"]);
              this.examplesum["eloquence"] += sentence["eloquence"];
            });
          });
        }
      } else {
        //draw all data

        // compute eloquenceSum & is_claimSum
        var eloquenceSum = 0;
        //var is_claimSum = 0;
        this.examples.forEach((element) => {
          //num of reply
          var tempElement = element.content.reply_contents;
          tempElement.forEach((d) => {
            //console.log("this:", d.eloquence);
            eloquenceSum += parseInt(d.eloquence);
            //is_claimSum += parseInt(d.is_claim);
          });
        });

        this.examplesum = {
          logos: this.labelRadar[0][1]["value"],
          pathos: this.labelRadar[0][2]["value"],
          ethos: this.labelRadar[0][3]["value"],
          evidence: this.labelRadar[0][4]["value"],
          relevance: this.labelRadar[0][5]["value"],
          is_claim: this.labelRadar[0][0]["value"],
          eloquence: eloquenceSum,
        };
        //console.log("barSum", barSum);
      }

      var data = this.inputLabels["input"].map((d) => {
        console.log("barview-input:", d.label);
        console.log("barview-data:", this.examplesum[d.feature]);
        return {
          feature: d.feature,
          label: Math.round(d.label - this.examplesum[d.feature]),
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
        .text((d) => d.label + "%")
        .attr("x", (d) => x(d.label))
        .attr("y", function (d) {
          return y(d.feature) + y.bandwidth() / 2;
        })
        .attr("text-anchor", (d) => (d.label < 0 ? "end" : "start"))
        .style("fill", (d) => (d.label < 0 ? "darkred" : "darkblue"))
        .style("font-size", 15);
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
    },

    // drawInputRose(){

    // },

    drawRose(svg, currentPos) {
      this.pos = currentPos;
      //console.log("rosePos:", this.pos);
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
        .range([12, 40]);

      //force layout test
      // var ticked = function() {
      //     circles
      //       .attr("cx", function(d) { return d.x; })
      //       .attr("cy", function(d) { return d.y; });
      //   }
      var simulation = d3
        .forceSimulation()
        .force(
          "collide",
          d3.forceCollide().radius(function (d) {
            return outerRScale(d.content["reply_delta_num"]) + 2;
          })
        )
        .force("center", d3.forceCenter(this.width / 2, this.height / 2))
        .force(
          "x",
          d3.forceX((d, i) => {
            return xScale(this.pos[d.id][0]);
          })
        )
        .force(
          "y",
          d3.forceX((d, i) => {
            return yScale(this.pos[d.id][1]);
          })
        );
      //.force("charge", d3.forceManyBody().strength(-50).distanceMin(1).distanceMax(20));

      // combine pie and rose
      var drawBackRose = this.drawBackRose;
      var drawFrontRose = this.drawFrontRose;
      //var posCurrent = this.pos;
      var circles = svg.selectAll("g").data(this.examples).enter().append("g");

      circles
        .each(function (d, i) {
          drawBackRose(
            outerRScale(d.content["reply_delta_num"]),
            d.id,
            //this.pos,
            xScale,
            yScale,
            d3.select(this)
          );
        })
        .attr(
          "transform",
          (d) =>
            `translate(${xScale(this.pos[d.id][0])},${yScale(
              this.pos[d.id][1]
            )})`
        )

        .attr("class", "pie");

      circles
        .append("circle")
        // .attr("cx", (d, i) => xScale(this.pos[d.id][0]))
        // .attr("cy", (d, i) => yScale(this.pos[d.id][1]))
        .attr("r", (d) => outerRScale(d.content["reply_delta_num"]))
        .style("opacity", 0)
        // .style("fill", "white")
        .on("mouseover", function () {
          d3.select(this).style("fill", "white").style("opacity", 0.5);
          // d3.selectAll(".pie")
          //   .filter((circle, index) => {
          //     console.log(d);
          //     console.log(i);
          //     return i === index;
          //   })
          //   .style("fill", "red")
          //   .attr("class", "highlightCircle");
          // .classed("highlightCircle", true); ???
        })
        .on("mouseout", function () {
          d3.select(this).style("fill", "white").style("opacity", 0);
        })
        .on("click", (d) => {
          //muliple select: submit and then check enabled
          if ($("#cbTxt").text() == "Select is enabled") {
            PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
            this.selectIDarray.push(d.id);
            this.selectIDIndex.push(
              this.examples.map((d) => d.id).indexOf(d.id)
            ); //d.id is consistent
            $("#selectInd").text(this.selectIDIndex);
            PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
          }
          if ($("#cbTxt").text() == "Select is disabled") {
            DataService.ex_id = d.id;
            DataService.selectIDIndex = []; // clear IDarray
            DataService.selectIDIndex = []; //clear index

            PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
            // PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
            PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
          }
          //console.log("IDARRAY: ", this.selectIDarray, this.selectIDIndex, this.examples.map((d) => d.id));
        });

      circles.each(function (d) {
        drawFrontRose(d, d.id, xScale, yScale, outerRScale, d3.select(this));
      });

      var tickedRose = function () {
        circles
          // .attr("cx", function(d) { return d.x; })
          // .attr("cy", function(d) { return d.y; });
          .attr("transform", (d) => `translate(${d.x},${d.y})`);
        //circles.exit().remove();
      };
      simulation.nodes(this.examples).alphaDecay(0.1);
      for (let index = 0; index < 2000; index++) {
        simulation.tick();
      }
      tickedRose();

      var tickedRose = function () {
        circles
          // .attr("cx", function(d) { return d.x; })
          // .attr("cy", function(d) { return d.y; });
          .attr("transform", (d) => `translate(${d.x},${d.y})`);

        circles.exit().remove();
      };
      simulation.nodes(this.examples).alphaDecay(0.1);

      for (let index = 0; index < 2000; index++) {
        simulation.tick();
      }
      tickedRose();
    },
    drawFrontRose(d, id, xScale, yScale, outerRScale, g) {
      //console.log("testpos3:", pos);
      var exampledata = d.content["reply_contents"];
      var Rosesum = [
        { feature: "is_claim", label: 0 },
        { feature: "logos", label: 0 },
        { feature: "pathos", label: 0 },
        { feature: "ethos", label: 0 },
        { feature: "evidence", label: 0 },
        { feature: "relevance", label: 0 },
      ];
      exampledata.forEach((element) => {
        Rosesum[0].label += parseInt(element["is_claim"]);
        Rosesum[1].label += parseInt(element["logos"]);
        Rosesum[2].label += parseInt(element["pathos"]);
        Rosesum[3].label += parseInt(element["ethos"]);
        Rosesum[4].label += parseInt(element["evidence"]);
        Rosesum[5].label += parseInt(element["relevance"]);
      });
      Rosesum = Rosesum.map((d) => {
        return {
          feature: d.feature,
          label: d.label,
          radius: Math.sqrt(d.label) / Math.PI,
        };
      });

      // Rosesum = Rosesum.sort((a, b) => d3.descending(a.label, b.label));
      var total_label = 0;
      Rosesum.forEach((element) => {
        total_label += element.label;
      });
      // console.log(Rosesum);

      var total_r = Math.sqrt(total_label) / Math.PI;

      // set inner radius scale:
      var outerR = outerRScale(d.content["reply_delta_num"]);
      var innerRdomain = Rosesum.map((d) => d.radius);
      var innerRScale = d3
        .scaleLinear()
        .domain([d3.min(innerRdomain), total_r])
        .range([0, outerR]);

      // Compute the position of each group on the pie:
      var pie = d3.pie().value(function (d) {
        return 1; // equal arc
      });
      var data_ready = pie(d3.entries(Rosesum));

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

      var simulation = d3
        .forceSimulation()
        .force(
          "collide",
          d3.forceCollide(function (d) {
            return outerRScale(d.content["reply_delta_num"]);
          })
        )
        .force("center", d3.forceCenter(this.width / 2, this.height / 2))
        .force(
          "y",
          d3.forceX((d, i) => {
            return yScale(pos[id][1]);
          })
        )
        .force(
          "x",
          d3.forceX((d, i) => {
            return xScale(pos[id][0]);
          })
        );
      // set tooltips
      var div = d3
        .select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
      //this.svg

      g.selectAll("whatever")
        .data(data_ready)
        .enter()
        .append("path")
        // .attr("transform", () => {
        //   return (
        //     "translate(" + xScale(pos[id][0]) + "," + yScale(pos[id][1]) + ")"
        //   );
        // })
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

      // var ticked = function() {
      //     circles
      //         .attr("cx", function(d) { return d.x; })
      //         .attr("cy", function(d) { return d.y; });
      // }

      // simulation
      //     .nodes(d)
      //     .on("tick", ticked);
    },
    drawBackRose(r, id, xScale, yScale, g) {
      var pie = d3.pie().value(function (d) {
        return 1; // equal arc
      });
      //console.log("drawbackrose:", id);
      var data_ready = pie(d3.entries(d3.range(6)));
      // this.svg

      //console.log("before", g);
      g.selectAll("whatever")
        .data(data_ready)
        .enter()
        .append("path")
        // .attr("transform", () => {
        //   return (
        //     "translate(" + xScale(pos[id][0]) + "," + yScale(pos[id][1]) + ")"
        //   );
        // })
        .attr("d", d3.arc().innerRadius(0).outerRadius(r))
        .attr("fill", "lightblue")
        .attr("stroke", "black")
        .style("stroke-width", "1px")
        .style("opacity", 0.7);
      // console.log("testtttttt:", xScale(pos[id][0]), yScale(pos[id][1]));
    },
  },
};
</script>

<style scoped>
  #multiSelectDiv{
    align-items: center;
    justify-content:center
  } 
</style>
