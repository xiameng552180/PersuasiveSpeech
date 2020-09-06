<template>
<div class="row" style="height: 400px; width: 400px;">
  <svg id="nodelink" height="400"/>
</div>
</template>

<script>
import * as d3 from "d3";
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";
import dating16 from "../dating-16.json"; //for nodelink

export default {
  name: "NodeView",
  data() {
    return {
      svg3: null,
      simulation1: null,
      node: null,
      link: null,
      nodeData: [],
    }
  },
  mounted() {
    this.initialize();
    PipeService.$on(PipeService.UPDATE_NODEVIEW, () => {
      this.nodeData = DataService.nodeData;
      console.log("nodeview1: ", this.nodeData);
    //   //PipeService.$on(PipeService.UPDATE_NODEVIEW, () => {
    //   //console.log("drawNode!!!");
      this.drawNodeLink(this.svg3);
    });
    //this.drawNodeLink(this.svg3);
    // console.log("Node:", this.node);
    // console.log("Link:", this.link);
    //});

  },
  methods: {
    initialize() {
      this.nodeData = DataService.nodeData;
      console.log("nodeview12: ", this.nodeData);
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
    drawNodeLink(svgNode) {
      console.log("nodeview2:", this.nodeData);
      var arrow = svgNode
        .append("defs")
        .append("marker")
        .attr("id", "arrowhead")
        .attr("viewBox", "-0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", 0)
        .attr("orient", "auto")
        .attr("markerWidth", 5)
        .attr("markerHeight", 5)
        .attr("xoverflow", "visible")
        .append("path")
        .attr("d", "M 0,-5 L 10 ,0 L 0,5")
        .attr("fill", "black")
        .style("stroke", "black");

      this.simulation1 = d3
        .forceSimulation()
        .force(
          "link",
          d3
            .forceLink()
            .id(function (d) {
              return d.id;
            })
            .distance(100)
            .strength(1)
        )
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(this.width3 / 2, this.height3 / 2));

      var nodes = [],
        links = [];
      nodes = this.nodeData.map( 
        (d, i) => {
          d.id = i;
          return d;
        }
      );
      // console.log(nodes);
      var source = null;
      nodes.forEach((d, i) => {
        if (d.is_claim === "1") {
          source = i;
        }
        if (source != null && source !== i) {
          var newlink = {
            source: i,
            target: source,
          };
          links.push(newlink);
        }
      });
      
      this.update(links, nodes);
    },

    update(links, nodes) {
      this.link = this.svg3
        .selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("marker-end", "url(#arrowhead)")
        .attr("stroke", "black")
        .attr("stroke-width", "2px");

       // add tooltip
      var tooltip=d3.select("body")
          .append("div")
          .attr("class","tooltip")
          .style("opacity",0.0)
          .style('z-index', 10)
          .style('font-size', '12px')
          .style('color', "white")
          .style('background', "#535353")	
          .style('border-radius', "8px");

      this.node = this.svg3
        .selectAll(".node")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .call(
          d3.drag().on("start", this.dragstarted).on("drag", this.dragged)
          //.on("end", dragended)
        );

      this.node
        .append("circle")
        .attr("r", 10)
        .style("fill", function (d, i) {
          if (d.is_claim === "1") return "#90ee8f";
          // else if(d.logos == "1") return "#7eb6e4";
          // else if(d.pathos == "1") return "#8cd390";
          // else if(d.evidence == "1") return "#fa8cad";
          // else if(d.ethos == "1") return "#8f91fc";
          // else if (d.relevance == "1") return "#e05c5c";
          else return "#ffd701";
        })
        // .style("stroke", function (d, i){
        //   if (d.is_claim == "1") return "#b6034d";
        // })
        // .style("stroke-width", function (d, i){
        //   if (d.is_claim == "1") return "5";
        // })
        // .append("title")
        // .text(function(d){return d.content});
        .on("mouseover", function(d){
          tooltip
              .html(d.id +": "+ d.content+"<br/>")
              .style("left",(d3.event.pageX) +"px")
              .style("top",(d3.event.pageY +20)+"px")
              .style("opacity",1.0)
        })
        // .on('mousemove', function (d, i) {
        //   console.log("mousemove");
        //   return tooltip.style('top', (event.pageY-10)+'px').style('left',(event.pageX+10)+'px');
        // })
        .on('mouseout', function (d) {
          tooltip.style("opacity",0.0);
          //return tooltip.style('visibility', 'hidden');
        });



      this.simulation1 = d3
        .forceSimulation(nodes) // Force algorithm is applied to data.nodes
        .force(
          "link",
          d3
            .forceLink() // This force provides links between nodes
            .id(function (d) {
              return d.id;
            }) // This provide  the id of a node
            .links(links) // and this the list of links
            .distance(100)
        )
        .force(
          "charge",
          d3.forceManyBody().strength(-50).distanceMin(100).distanceMax(100)
        ) // This adds repulsion between nodes.
        .force("center", d3.forceCenter(this.width3 / 2, this.height3 / 2)); // This force attracts nodes to the center of the svg area
        //.on("tick", this.tickedNodelink);

        for (let index = 0; index < 50; index++) {
          this.simulation1.tick()
        }
        this.tickedNodelink();

    },

    tickedNodelink() {
      this.link
        .attr("x1", function (d) {
          return d.source.x;
        })
        .attr("y1", function (d) {
          return d.source.y;
        })
        .attr("x2", function (d) {
          return d.target.x;
        })
        .attr("y2", function (d) {
          return d.target.y;
        });

      this.node.attr("transform", function (d) {
        return "translate(" + d.x + ", " + d.y + ")";
      });
    },

    dragstarted(d) {
      if (!d3.event.active) this.simulation1.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    },
    dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    },
    // nodelink end//

  }
};
</script>

<style scoped>
.tooltip{
    position:absolute;
    padding:5px;
    width:120;
    height:auto;
    font-family:simsun;
    font-size:14px;
    color:black;
    background-color: rgb(255,255,255);
    border-width: 2px solid rgb(255,255,255);
    border-radius:5px;
}  

.tooltip:after{
    content: '';
    position:absolute;
    bottom:100%;
    left:20%;
    margin-left: -8px;
    width:0;
    height:0;
    border-bottom:12px solid rgb(255,255,255);
    border-right:12px solid transparent;
    border-left:12px solid transparent;
}

</style>