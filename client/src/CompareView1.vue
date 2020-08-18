<template>

  <div class="row">
    <!--select strategies-->
    <div class="col-lg-1">
        <div class="form-group" >
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
      <div class="col-lg-4" style="height: 360px;  overflow-x: hidden;">
        <div id="RadarSVG" style="height: 360px;  overflow-x: hidden;"></div>
      </div>
      <!--rose chart view-->
      <div class="col-lg-4">
          <div id="CircleSVG" style="height: 360px;  overflow-x: hidden;"></div>
      </div>
      <!-- <div id="chartholder"></div> -->
      <!--bar view-->
      <div class="col-lg-4">
          <div id="BarChartSVG" style="height: 360px; overflow-x: hidden;"></div>
      </div>
  </div>
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
      svg2: null,
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
      datingSum: [//dating summary
        {axis:"claim_num",value: 28},
        {axis:"logos_num",value: 119},
        {axis:"pathos_num",value: 41},
        {axis:"ethos_num",value: 9},
        {axis:"evidence_num",value: 97},
        {axis:"relevance_num",value: 25},
        {axis:"others",value: 186}
      ],
      margin: { top: 30, right: 30, bottom: 30, left: 30 },
      examples: null,
      ex_order: null,
    };
  },
  mounted() {
    this.initialize();
    this.drawRadar(this.svg2);
    PipeService.$on(PipeService.UPDATE_COMPAREVIEW, () => {
      console.log("---ok---");
      this.ex_order = DataService.ex_order;
      this.examples = DataService.examples;
      this.svg1.selectAll("*").remove();
      this.drawCircle(this.svg);
      this.drawBar(this.svg1);
      

      console.log($('#strategy').val());
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

      this.width2 = d3
        .select("#RadarSVG")
        .node()
        .getBoundingClientRect().width;
      this.height2 = d3
        .select("#RadarSVG")
        .node()
        .getBoundingClientRect().height;
      this.svg2 = d3
        .select("#RadarSVG")
        .append("svg")
        .attr("class", "d3SVG")
        .attr("width", this.width1)
        .attr("height", this.height1);2
    },

    drawRadar(svgNode) {
      var d = [ [//dating summary
        {area:"claim_num",value: 28},
        {area:"logos_num",value: 119},
        {area:"pathos_num",value: 41},
        {area:"ethos_num",value: 9},
        {area:"evidence_num",value: 97},
        {area:"relevance_num",value: 25},
        {area:"others",value: 186}
       ]];
      var options = {
          w: this.width2,
          h: this.height2,
          maxValue: 190,
          levels: 5,
          ExtraWidthX: 300
      }


      var cfg = {
          radius: 5,
          w: 300,
          h: 300,
          factor: 1,
          factorLegend: .85,
          levels: 3,
          maxValue: 0,
          radians: 2 * Math.PI,
          opacityArea: 0.5,
          ToRight: 5,
          TranslateX: 80,
          TranslateY: 30,
          ExtraWidthX: 100,
          ExtraWidthY: 100,
          color: d3.scaleOrdinal().range(["#6F257F", "#CA0D59"])
      };
          
      if('undefined' !== typeof options){
        for(var i in options){
        if('undefined' !== typeof options[i]){
          cfg[i] = options[i];
        }
        }
      }
        
        cfg.maxValue = 200;
        
        var allAxis = (d[0].map(function(i, j){return i.area}));
        var total = allAxis.length;
        var radius = cfg.factor*Math.min(cfg.w/2, cfg.h/2);
        var Format = d3.format('%');
        d3.select("#RadarSVG").select("svg").remove();

        var g = d3.select("#RadarSVG")
            .append("svg")
            .attr("width", cfg.w+cfg.ExtraWidthX)
            .attr("height", cfg.h+cfg.ExtraWidthY)
            .append("g")
            .attr("transform", "translate(" + cfg.TranslateX + "," + cfg.TranslateY + ")");

        var tooltip;
      
        //Circular segments
        for(var j=0; j<cfg.levels; j++){
          var levelFactor = cfg.factor*radius*((j+1)/cfg.levels);
          g.selectAll(".levels")
          .data(allAxis)
          .enter()
          .append("svg:line")
          .attr("x1", function(d, i){return levelFactor*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
          .attr("y1", function(d, i){return levelFactor*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
          .attr("x2", function(d, i){return levelFactor*(1-cfg.factor*Math.sin((i+1)*cfg.radians/total));})
          .attr("y2", function(d, i){return levelFactor*(1-cfg.factor*Math.cos((i+1)*cfg.radians/total));})
          .attr("class", "line")
          .style("stroke", "grey")
          .style("stroke-opacity", "0.75")
          .style("stroke-width", "0.3px")
          .attr("transform", "translate(" + (cfg.w/2-levelFactor) + ", " + (cfg.h/2-levelFactor) + ")");
        }

        //Text indicating at what % each level is
        for(var j=0; j<cfg.levels; j++){
          var levelFactor = cfg.factor*radius*((j+1)/cfg.levels);
          g.selectAll(".levels")
          .data([1]) //dummy data
          .enter()
          .append("svg:text")
          .attr("x", function(d){return levelFactor*(1-cfg.factor*Math.sin(0));})
          .attr("y", function(d){return levelFactor*(1-cfg.factor*Math.cos(0));})
          .attr("class", "legend")
          .style("font-family", "sans-serif")
          .style("font-size", "10px")
          .attr("transform", "translate(" + (cfg.w/2-levelFactor + cfg.ToRight) + ", " + (cfg.h/2-levelFactor) + ")")
          .attr("fill", "#737373")
          .text((j+1)*200/cfg.levels); //100
        }

        var series = 0;

        var axis = g.selectAll(".axis")
            .data(allAxis)
            .enter()
            .append("g")
            .attr("class", "axis");

        axis.append("line")
          .attr("x1", cfg.w/2)
          .attr("y1", cfg.h/2)
          .attr("x2", function(d, i){return cfg.w/2*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
          .attr("y2", function(d, i){return cfg.h/2*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
          .attr("class", "line")
          .style("stroke", "grey")
          .style("stroke-width", "1px");

        axis.append("text")
          .attr("class", "legend")
          .text(function(d){return d})
          .style("font-family", "sans-serif")
          .style("font-size", "11px")
          .attr("text-anchor", "middle")
          .attr("dy", "1.5em")
          .attr("transform", function(d, i){return "translate(0, -10)"})
          .attr("x", function(d, i){return cfg.w/2*(1-cfg.factorLegend*Math.sin(i*cfg.radians/total))-60*Math.sin(i*cfg.radians/total);})
          .attr("y", function(d, i){return cfg.h/2*(1-Math.cos(i*cfg.radians/total))-20*Math.cos(i*cfg.radians/total);});

        var dataValues = [];
        d.forEach(function(y, x){
          
          g.selectAll(".nodes")
          .data(y, function(j, i){
            dataValues.push([
            cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total)), 
            cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total))
            ]);
          });
          dataValues.push(dataValues[0]);
          g.selectAll(".area")
                .data([dataValues])
                .enter()
                .append("polygon")
                .attr("class", "radar-chart-serie"+series)
                .style("stroke-width", "2px")
                .style("stroke", cfg.color(series))
                .attr("points",function(d) {
                  var str="";
                  for(var pti=0;pti<d.length;pti++){
                    str=str+d[pti][0]+","+d[pti][1]+" ";
                  }
                  return str;
                  })
                .style("fill", function(j, i){return cfg.color(series)})
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
        series=0;   
        
    var tooltip = d3.select("#RadarSVG").append("div").attr("class", "toolTip");
        d.forEach(function(y, x){
          g.selectAll(".nodes")
          .data(y).enter()
          .append("svg:circle")
          .attr("class", "radar-chart-serie"+series)
          .attr('r', cfg.radius)
          .attr("alt", function(j){return Math.max(j.value, 0)})
          .attr("cx", function(j, i){
            dataValues.push([
            cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total)), 
            cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total))
          ]);
          return cfg.w/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total));
          })
          .attr("cy", function(j, i){
            return cfg.h/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total));
          })
          .attr("data-id", function(j){return j.area})
          .style("fill", "#fff")
          .style("stroke-width", "2px")
          .style("stroke", cfg.color(series)).style("fill-opacity", .9)
          .on('mouseover', function (d){
            console.log(d.area)
                tooltip
                  .style("left", d3.event.pageX - 40 + "px")
                  .style("top", d3.event.pageY - 80 + "px")
                  .style("display", "inline-block")
                  .html((d.area) + "<br><span>" + (d.value) + "</span>");
                })
            .on("mouseout", function(d){ tooltip.style("display", "none");});

          series++;
        });
        

    },//RadarChart



  
    drawCircle(svgNode) {
      var xdomain = this.pos.map((d) => d[0]),
        ydomain = this.pos.map((d) => d[1]),
        rdomain = this.examples.map((d) => parseInt(d["reply_delta_num"])),
        height = this.height - this.margin.bottom - this.margin.top,
        width = this.width;


      var xScale = d3
        .scaleLinear()
        .domain(d3.extent(xdomain))
        .range([this.margin.left, width - this.margin.right]);

      var yScale = d3
        .scaleLinear()
        .domain(d3.extent(ydomain))
        .range([this.margin.top, height]);
      
    var rScale = d3.scaleLinear().domain(d3.extent(rdomain)).range([10, 20]);

    // svgNode
      //   .append("g")
      //   .attr("transform", "translate(" + this.margin.left + ")")
      //   .call(d3.axisLeft(yScale));

      // svgNode
      //   .append("g")
      //   .attr("transform", "translate(30," + height + ")")
      //   .call(d3.axisBottom(xScale));

      var circles = svgNode
        .selectAll("circle")
        .data(this.examples)
        .enter()
        .append("circle")
        .attr("class", "pie")
        .attr("cx", (d, i) => xScale(this.pos[i][0]))
        .attr("cy", (d, i) => yScale(this.pos[i][1]))
        .attr("r", (d) => rScale(d["reply_delta_num"]))
        .style("opacity", 0.7)
        .style("fill", "orange")
        .on("mouseover", (d, i) => {
          d3.selectAll("circle")
            .filter((circle, index) => i === index)
            .style("fill", "red")
            .attr("class", "highlightCircle");
          // .classed("highlightCircle", true); ???
        })
        .on("mouseout", (d, i) => {
          d3.selectAll(".highlightCircle")
            .style("fill", "orange")
            // .filter((circle, index) => i === index)
            .classed("highlightCircle", false);
        })
        .on("click", (d, i) => {
          DataService.ex_order = i;
          PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
          PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
          PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
        });

    },

    drawBar(svgNode) {
      var width = this.width1,
        height = this.height1;
      var svg = svgNode.append("g");

      var exampledata = this.examples[this.ex_order]["reply_contents"];
      //console.log(exampledata);
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
      console.log(examplesum);

      var data = input["input"].map((d) => {
        console.log(examplesum[d.feature] - d.label);
        return {
          feature: d.feature,
          label: examplesum[d.feature] - d.label,
        };
      });
      console.log(data);

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
.axis {
	font: 15px sans-serif;
}
.axis path,
.axis line {
  fill: none;
  stroke: #D4D8DA;
  stroke-width: 2px;
  shape-rendering: crispEdges;
}
#chart {
	position: absolute;
	top: 50px;
	left: 100px;
}
  
  .toolTip {
  pointer-events: none;
	position: absolute;
    display: none;
  min-width: 50px;
  height: auto;
  background: none repeat scroll 0 0 #ffffff;
  padding: 9px 14px 6px 14px;
  border-radius: 2px;
  text-align: center;
  line-height: 1.3;
  color: #5B6770;
  box-shadow: 0px 3px 9px rgba(0, 0, 0, .15);
}
.toolTip:after {
  content: "";
  width: 0;
  height: 0;
  border-left: 12px solid transparent;
  border-right: 12px solid transparent;
  border-top: 12px solid white;
  position: absolute;
  bottom: -10px;
  left: 50%;
  margin-left: -12px;
}  
.toolTip span {
	font-weight: 500;
  color: #081F2C;
}
</style>
