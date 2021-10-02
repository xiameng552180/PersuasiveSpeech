<template>
  <div>
    <div class="row">
      <div class="col-lg-10" style="overflow: scroll">
        <!-- <input v-model="userid" placeholder="input user id" /> -->
        <!-- <br /> -->
        <div class="form-group">
          <label for="exampleFormControlSelect1" style="font-size: 16px"
            >Topic</label
          >
          <select
            class="form-control"
            id="topicSelect"
            v-on:change="chooseTopic"
            style="height: 40px; font-size: 18px"
          >
            <option value="none" selected disabled hidden style="color: gray">
              -- Select a topic --
            </option>
            <option value="0">Abortion</option>
            <option value="1">Dating</option>
            <option value="2">Eugenics</option>
            <option value="3">Immortality</option>
            <option value="4">Marriage</option>
            <option value="5">Parenthood</option>
            <option value="6">Pride</option>
            <option value="7">Suicide</option>
          </select>
        </div>

        <label>Claim: </label>
        <div
          contenteditable="true"
          id="userInputDiv"
          @input="changeDivText($event)"
          style="height: 240px; font-size: 18px"
        >
          {{ inputContent }}
        </div>
      </div>
      <!-- <div contenteditable="true" id="userInputDiv" 
      style="height:200px;">from an algorithmic perspective, it becomes increasingly difficult. but we can solve it! You can't know what death is, and you can't know how you'll grow and adapt in Prison.</div> -->
      <div class="col-lg-2">
        <div class="inputSummary" style="height: 260px"></div>
      </div>
    </div>
    <br />
    <button type="button" class="btn btn-primary" v-on:click="updateInput">
      Upload
    </button>
    <input
      id="arglabel"
      type="checkbox"
      checked
      data-toggle="toggle"
      data-size="lg"
    />
    <span style="color: gray">Argument Labels</span>
    &nbsp;&nbsp;&nbsp;
    <label id="eloquenceScore" style="opacity: 0"></label>
    <p id="errorMess" style="overflow: scroll"></p>
  </div>
</template>


<script>
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";
import axios from "axios";
import { highlightTextarea } from "../../static/jquery.highlighttextarea.js";
//topic
import abortion from "../topic_file/abortion.json";
import dating from "../topic_file/dating.json";
import eugenics from "../topic_file/eugenics.json";
import immortality from "../topic_file/immortality.json";
import marriage from "../topic_file/marriage.json";
import parenthood from "../topic_file/parenthood.json";
import pride from "../topic_file/pride.json";
import suicide from "../topic_file/suicide.json";

export default {
  name: "InputView",
  data() {
    return {
      inputContent: null,
      backdata: null, // origin data from backend processing results
      eloquenceScore: null, // sum of eloquence score of all sentences
      eloquenceErrorList: [], //all error tooltip of input sentences
      // errorStartIndexList: [],// all input highlight starts
      // errorEndIndexList: [], //all input highlight ends
      inputS: [], //all input sentences
      // lengthSentenList: [],//lenfth of each sentence
      highlightWords: {}, //high light words list
      inputLabels: {},
      inputRelationship: [],
      nodeData: [],
      linkData: [],
      eachSentenceLabel: {},
      editText: null,
      svgInput: null,
      widthInput: null,
      heightInput: null,
      userid: "1",
      allHighlightTxt: "",
      resultSentence: null,
      startErrIndex: null,
      endErrIndex: null,
      errSentenceIndex: [],
      inputLabelAll: null,
      selectTopicNum: null,
      selectTopic: null,
      topicExamples: {
        Abortion: abortion,
        Dating: dating,
        Eugenics: eugenics,
        Immortality: immortality,
        Marriage: marriage,
        Parenthood: parenthood,
        Pride: pride,
        Suicide: suicide,
      },
      //label toggle
      labelTag: true,
    };
  },
  mounted() {
    this.initialize();
    // this.chooseTopic();
    const _this = this;
    $("#arglabel").click(function () {
      _this.labelTag = !_this.labelTag;
      if (_this.labelTag == false) {
        // hide labels
        console.log("------label tag == false---------");
        console.log("input html: ", _this.editText);
        document.getElementById("userInputDiv").innerHTML = "";
        this.inputContent = "";
        document.getElementById("userInputDiv").innerHTML = _this.editText;
      } else {
        // add labels
        console.log("------label tag == true---------");
        console.log("input html: ", _this.allHighlightTxt);
        document.getElementById("userInputDiv").innerHTML = "";
        this.inputContent = "";
        document.getElementById("userInputDiv").innerHTML =
          _this.allHighlightTxt;
      }
    });
  },
  methods: {
    initialize() {
      this.inputLabels = DataService.inputLabels;

      this.svgInput = d3
        .select(".inputSummary")
        .append("svg")
        .attr("width", 100)
        .attr("height", 250);
    },

    chooseTopic() {
      var topic_s = document.getElementById("topicSelect");
      var index = topic_s.selectedIndex;
      this.selectTopicNum = topic_s.options[index].value;
      this.selectTopic = topic_s.options[index].text;

      DataService.selectTopicNum = this.selectTopicNum;
      DataService.selectTopic = this.selectTopic;
      console.log("selectTopicNum", this.selectTopicNum);
      console.log("selectTopic", this.selectTopic);

      this.addExamples();
      console.log("after add examples");
      PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);

      //console.log(this.persuasiveLevel[this.selectTopic]);
      // if (this.persuasiveLevel[this.selectTopic].length > 3){
      //   $('#persuasiveText').text("ratio:0%");
      // }
      // console.log("tttt", this.persuasiveLevel[this.selectTopic]);
      // $("#persuasiveStyle").css(
      //   "width",
      //   this.persuasiveLevel[this.selectTopic] + "%"
      // );
      // $("#persuasiveText").text(
      //   "ratio:" + this.persuasiveLevel[this.selectTopic] + "%"
      // );
      $("#interestTopic").text(this.selectTopic);
      console.log("topicSelect:", this.selectTopicNum, this.selectTopic);
    },

    addExamples() {
      console.log("add examples");
      console.log("selectTopic", this.selectTopic);
      console.log("topicExamples", this);
      console.log("Choosetest2", this.topicExamples[this.selectTopic]);
      var tempEx = this.topicExamples[this.selectTopic];
      DataService.examples = [];
      tempEx.forEach((ele) => {
        var objKey = Object.keys(ele);
        var c = 0;
        ele[objKey][0]["reply-info"].forEach((item) => {
          var new_item = { id: objKey + "-" + c, content: item };
          DataService.examples.push(new_item);
          //console.log("Abortion:", new_item);
          c++;
        });
      });

      // sort by delta
      DataService.examples = DataService.examples.sort((a, b) =>
        d3.descending(
          parseInt(a.content.reply_delta_num),
          parseInt(b.content.reply_delta_num)
        )
      );

      //console.log("testexamples1:", DataService.examples);

      PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
      PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
      PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
    },

    changeDivText(event) {
      this.editText = event.target.innerText;
      console.log("changeTxt:", this.editText);
      //多次upload 去掉label hard processing
      // if (this.editText.search("Claim") != -1){
      //   this.editText = this.editText.replace("[Claim]", "");
      // }
      if (this.editText.search("[Claim]") != -1) {
        this.editText = this.editText.replace(
          /\[Claim[[\d]*&*\w*\.*&*\w*\.*\]/g,
          ""
        );
      }
      if (this.editText.search("[Logos]") != -1) {
        this.editText = this.editText.replace(
          /\[Logos[[\d]*&*\w*\.*&*\w*\.*\]/g,
          ""
        );
      }
      if (this.editText.search("[Pathos]") != -1) {
        this.editText = this.editText.replace(
          /\[Pathos[[\d]*&*\w*\.*&*\w*\.*\]/g,
          ""
        );
      }
      if (this.editText.search("Ethos") != -1) {
        this.editText = this.editText.replace(
          /\[Ethos[[\d]*&*\w*\.*&*\w*\.*\]/g,
          ""
        );
      }
      if (this.editText.search("Evidence") != -1) {
        this.editText = this.editText.replace(
          /\[Evidence[[\d]*&*\w*\.*&*\w*\.*\]/g,
          ""
        );
      }
      if (this.editText.search("Relevance") != -1) {
        this.editText = this.editText.replace(
          /\[Relevance[[\d]*&*\w*\.*&*\w*\.*\]/g,
          ""
        );
      }

      console.log("changeTxt after:", this.editText);
    },

    updateInput: function (event) {
      //this.inputContent = document.getElementById("userInputDiv").innerHTML;  old version
      //console.log("t1", typeof(document.getElementById("userInput1").value));
      //remove label tag
      // var obj = document.getElementsByClassName("addLabelTag");
      // obj.innerHTML = "";//删除div内容

      this.inputContent = this.editText;
      this.eloquenceErrorList = [];
      this.inputLabels["input"][0]["label"] = 0;
      this.inputLabels["input"][1]["label"] = 0;
      this.inputLabels["input"][2]["label"] = 0;
      this.inputLabels["input"][3]["label"] = 0;
      this.inputLabels["input"][4]["label"] = 0;
      //console.log("jiequ1", this.inputContent.match(\span(\S*)span>\)[1]);
      console.log("changeTxt2:", this.inputContent);
      // this.editText = event.target.innerHTML;
      if (this.inputContent.length != 0) {
        NetService.uploadInput(
          { content: this.inputContent, userid: this.userid },
          (x) => {
            this.backdata = x.data.results; //processing result
            this.inputRelationship = x.data.relationships;

            console.log("from backend: ", this.backdata);
            console.log(
              "backend relationship:",
              this.inputRelationship,
              this.inputRelationship.length
            );
            var inputKeys = Object.keys(this.backdata);
            //call relationship
            this.callRelationship(this.backdata, this.inputRelationship);
            console.log("I have run callrelatinship");

            this.inputS = []; //clear
            this.highlightWords = {}; //clear
            var currentErrWords = "";
            this.inputLabelAll = 0;
            console.log("inputlabels", this.inputLabels);
            //console.log("sentence number: ", inputKeys.length);
            this.backdata.forEach((i, index) => {
              console.log("each sentence: ", index, i["content"]);
              this.eloquenceScore += parseInt(i["eloquence"]);
              this.inputS.push(i["content"]);

              //console.log("eachS: ", i);
              //this.lengthSentenList.push(i['content'].length);
              // inpthis.errorStartIndexList.push(i['elo_info'][2][0]['contextoffset']); //highlight start
              // this.errorEndIndexList.push(i['elo_info'][2][0]['errorlength']); //highlight end
              // label add

              this.inputLabels["input"][0]["label"] += parseInt(i["logos"]);
              this.inputLabelAll += parseInt(i["logos"]);
              this.inputLabels["input"][1]["label"] += parseInt(i["pathos"]);
              this.inputLabelAll += parseInt(i["pathos"]);
              this.inputLabels["input"][2]["label"] += parseInt(i["ethos"]);
              this.inputLabelAll += parseInt(i["ethos"]);
              this.inputLabels["input"][3]["label"] += parseInt(i["evidence"]);
              this.inputLabelAll += parseInt(i["evidence"]);
              // this.inputLabels["input"][4]["label"] += parseInt(i["relevance"]);
              // this.inputLabelAll += parseInt(i["relevance"]);
              this.inputLabels["input"][4]["label"] += parseInt(i["is_claim"]);
              //console.log("error of [5]", this.inputLabels['input'][5]['label'])
              this.inputLabelAll += parseInt(i["is_claim"]);

              // this.inputLabels["input"][6]["label"] += parseInt(i["eloquence"]);

              // get each sentence lits
              var tempLabelList = [];
              tempLabelList.push(parseInt(i["logos"]));
              tempLabelList.push(parseInt(i["pathos"]));
              tempLabelList.push(parseInt(i["ethos"]));
              tempLabelList.push(parseInt(i["evidence"]));
              // tempLabelList.push(parseInt(i["relevance"]));
              tempLabelList.push(parseInt(i["is_claim"]));
              tempLabelList.push(parseInt(i["claim_type"]));
              this.eachSentenceLabel[index] = tempLabelList;

              if (i["elo_info"][2].length == 0) {
                $("#errorMess").text("ERROR ");
              } else {
                this.errSentenceIndex.push(index);
                this.eloquenceErrorList.push(i["elo_info"][2][0]["message"]); //error message
                this.startErrIndex = i["elo_info"][2][0]["contextoffset"];
                this.endErrIndex = i["elo_info"][2][0]["errorlength"];
                //highlight words of all sentence
                currentErrWords = i["content"].substring(
                  this.startErrIndex,
                  this.endErrIndex + 1
                );
                this.highlightWords[index] = i["content"].substring(
                  this.startErrIndex,
                  this.endErrIndex + 1
                );
              }
              //console.log("inputLabels inputview:", this.inputLabels);
              //update input

              PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
              PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
              PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
              PipeService.$emit(PipeService.UPDATE_NODEVIEW);
              console.log("current Err Words:", currentErrWords);
            }); //end cycle
            console.log("inputLabelAll Num:", this.inputLabelAll);

            // compute persentage
            if (this.inputLabels["input"][4]["label"] == 0) {
              this.inputLabels["input"][4]["label"] += 1;
            }
            if (this.inputLabelAll != 0) {
              this.inputLabels["input"][0]["label"] =
                (this.inputLabels["input"][0]["label"] / this.inputLabelAll) *
                100;
              this.inputLabels["input"][1]["label"] =
                (this.inputLabels["input"][1]["label"] / this.inputLabelAll) *
                100;
              this.inputLabels["input"][2]["label"] =
                (this.inputLabels["input"][2]["label"] / this.inputLabelAll) *
                100;
              this.inputLabels["input"][3]["label"] =
                (this.inputLabels["input"][3]["label"] / this.inputLabelAll) *
                100;
              this.inputLabels["input"][4]["label"] =
                (this.inputLabels["input"][4]["label"] / this.inputLabelAll) *
                100;
              // this.inputLabels["input"][5]["label"] =
              //   (this.inputLabels["input"][5]["label"] / this.inputLabelAll) *
              //   100;
            } else {
              this.inputLabels["input"][0]["label"] = 0;
              this.inputLabels["input"][1]["label"] = 0;
              this.inputLabels["input"][2]["label"] = 0;
              this.inputLabels["input"][3]["label"] = 0;
              this.inputLabels["input"][4]["label"] = 0;
              // this.inputLabels["input"][5]["label"] = 0;
            }
            console.log("eachLabel percentage:", this.inputLabels["input"]);
            DataService.inputLabels = this.inputLabels;
            PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
            //draw summary
            ////////////draw summary/////

            var width = 80,
              height = 250; // width and height of svgInput
            // draw back rose
            var pie = d3.pie().value(function (d) {
              return 1; // equal arc
            });
            var data_ready1 = pie(d3.entries(d3.range(5)));

            this.svgInput
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
              // { feature: "relevance", label: 0 },
            ];

            Rosesum[0].label += this.inputLabels["input"][4]["label"];
            Rosesum[1].label += this.inputLabels["input"][0]["label"];
            Rosesum[2].label += this.inputLabels["input"][1]["label"];
            Rosesum[3].label += this.inputLabels["input"][2]["label"];
            Rosesum[4].label += this.inputLabels["input"][3]["label"];
            // Rosesum[5].label += this.inputLabels["input"][4]["label"];

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
            // console.log(Rosesum);

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

            this.svgInput
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

            //draw summary end

            // step0 highlight error
            //elo score
            $("#eloquenceScore").text("eloquence:" + this.eloquenceScore);

            console.log(
              "eloquenceScore:",
              this.eloquenceScore,
              this.eloquenceErrorList
            );

            if (this.eloquenceErrorList.length == 0) {
              $("#errorMess").text("no error");
            } else {
              $("#errorMess").text("ERROR ");
              this.eloquenceErrorList.forEach((er, index) => {
                $("#errorMess").append(
                  this.highlightWords[index] + ": " + er + ". " + " "
                );
              });
            }

            //return highlight
            // step 1 process sentences
            var sentenceList = this.inputS;
            // JSON.stringify(this.inputS);
            console.log("****************************");
            console.log("sentenceList: ", sentenceList);
            console.log("****************************");
            console.log(
              "errorsentenceInd:",
              this.errSentenceIndex,
              this.highlightWords
            );
            this.resultSentence = sentenceList;

            // var items = sentenceList.split(",");
            // sentenceList = items.join("");

            // sentenceList = sentenceList.replace(/[\n]/g, "");
            // sentenceList = sentenceList.replace("[", "");
            // sentenceList = sentenceList.replace("]", "");
            // //sentenceList.pop();
            // sentenceList = sentenceList.substring(0, sentenceList.length - 1);

            // sentenceList = sentenceList.replace(/\"/g, "");
            // console.log("s", sentenceList, typeof(sentenceList));
            // console.log("****************************");
            // this.resultSentence = sentenceList.split(/[\.]/);
            // console.log("here1", resultSentence);

            // var resultSentence = this.backdata.map(data => data.content)

            // step 2 got label and highlight content

            //console.log("sentenceNum:", this.resultSentence.length);
            //console.log("each sentence label: ", this.eachSentenceLabel);

            //clear
            this.allHighlightTxt = ""; //clear
            //this.inputContent = this.inputContent.replace();

            //console.log("here2", this.resultSentence);
            //console.log("here3 inputContent:", this.inputContent);
            this.resultSentence.forEach((e, ind) => {
              //console.log("test", e, ind);

              var eachSentenceHighlight = "";
              if (e.length > 1) {
                //is it a sentence?
                var colorTxt = "";
                //console.log("inner sentence", ind, e);
                //console.log("returnLabel: ", ind, this.eachSentenceLabel[ind]);

                var logoFlag = 0;
                var pathoFlag = 0;
                var ethoFlag = 0;
                var evidenceFlag = 0;
                var errFlag = 0;
                var errEndInd = null;
                var newStr = "";
                //claim?
                //console.log("typeof Sentence", typeof(e), e); //string
                if (this.eachSentenceLabel[ind][5] != 0) {
                  //claim
                  var strTemp =
                    '<span style="background-color: #b6034d; color: white">[Claim]</span>';
                  eachSentenceHighlight = strTemp + e + " ";
                } else {
                  //premise
                  //logos?
                  if (this.eachSentenceLabel[ind][0] == 1) {
                    logoFlag = 1;
                    var strTemp =
                      '<span style="background-color: #7eb6e4;">[Logos]</span>';
                    eachSentenceHighlight = strTemp + e + " ";

                    //console.log("add logos!", allHighlightTxt);
                  }
                  //pathos?
                  else if (this.eachSentenceLabel[ind][1] == 1) {
                    if (logoFlag == 1) {
                      pathoFlag = 1; //multiple label
                      var strTemp =
                        '<span style="background-color: #7eb6e4;">[Pathos&Logos]</span>';
                      eachSentenceHighlight = strTemp + e + " "; //

                      //console.log("add pathos!", allHighlightTxt);
                    } else {
                      pathoFlag = 1; //multiple label
                      var strTemp =
                        '<span style="background-color: #8cd390;">[Pathos]</span>';

                      eachSentenceHighlight = strTemp + e + " ";
                    }
                  }
                  //evidence?
                  else if (this.eachSentenceLabel[ind][3] == 1) {
                    if (logoFlag == 0 && pathoFlag == 0) {
                      //single evidence
                      evidenceFlag = 1;
                      var strTemp =
                        '<span style="background-color: #fa8cad;">[Evidence]</span>';

                      eachSentenceHighlight = strTemp + e + " ";

                      //console.log("add evidence!", allHighlightTxt);
                    } else if (logoFlag == 1 && pathoFlag == 1) {
                      //3 labels
                      evidenceFlag = 1;
                      var strTemp =
                        '<span style="background-color: #7eb6e4;">[Pathos&Logos&Evi.]</span>';
                      eachSentenceHighlight = strTemp + e + " ";
                    } else if (logoFlag == 1 && pathoFlag == 0) {
                      //2 labels
                      evidenceFlag = 1;
                      var strTemp =
                        '<span style="background-color: #7eb6e4;">[Logos&Evi.]</span>';

                      eachSentenceHighlight =
                        strTemp + this.resultSentence[ind] + " ";
                    } else if (logoFlag == 0 && pathoFlag == 1) {
                      //2 labels
                      evidenceFlag = 1;
                      var strTemp =
                        '<span style="background-color: #8cd390;">[Pathos&Evi.]</span>';
                      eachSentenceHighlight = strTemp + e + " ";
                    }
                  }
                  //ethos?
                  else if (this.eachSentenceLabel[ind][2] == 1) {
                    if (logoFlag == 0 && pathoFlag == 0 && evidenceFlag == 0) {
                      var strTemp =
                        '<span style="background-color: #8f91fc;">[Ethos]</span>';
                      eachSentenceHighlight = strTemp + e + " ";

                      //console.log("add ethos!", allHighlightTxt);
                    } else if (
                      logoFlag == 1 &&
                      pathoFlag == 0 &&
                      evidenceFlag == 0
                    ) {
                      //logo+etho
                      var strTemp =
                        '<span style="background-color: #8f91fc;">[Ethos&Logos]</span>';
                      eachSentenceHighlight = strTemp + e + " ";
                    } else if (
                      logoFlag == 1 &&
                      pathoFlag == 0 &&
                      evidenceFlag == 1
                    ) {
                      //logo+etho
                      var strTemp =
                        '<span style="background-color: #8f91fc;">[Ethos&Logos&Evi.]</span>';
                      eachSentenceHighlight = strTemp + e + " ";
                    } else if (
                      logoFlag == 0 &&
                      pathoFlag == 0 &&
                      evidenceFlag == 1
                    ) {
                      //logo+etho
                      var strTemp =
                        '<span style="background-color: #8f91fc;">[Ethos&Evi.]</span>';
                      eachSentenceHighlight = strTemp + e + " ";
                    }
                    // no other situations
                  }
                  //relevance?
                  else if (this.eachSentenceLabel[ind][4] == 1) {
                    if (
                      logoFlag == 0 &&
                      pathoFlag == 0 &&
                      evidenceFlag == 0 &&
                      ethoFlag == 0
                    ) {
                      var strTemp =
                        '<span style="background-color: #e05c5c;">[Relevance]</span>';
                      eachSentenceHighlight =
                        strTemp + this.resultSentence[ind] + " ";
                      //console.log("add relevance!", allHighlightTxt);
                    } else if (
                      logoFlag == 1 &&
                      pathoFlag == 0 &&
                      evidenceFlag == 1 &&
                      ethoFlag == 0
                    ) {
                      var strTemp =
                        '<span style="background-color: #e05c5c;">[Logos&Evi.&Rele.]</span>';
                      eachSentenceHighlight =
                        strTemp + this.resultSentence[ind] + " ";
                    } else if (
                      logoFlag == 1 &&
                      pathoFlag == 0 &&
                      evidenceFlag == 0 &&
                      ethoFlag == 0
                    ) {
                      var strTemp =
                        '<span style="background-color: #e05c5c;">[Logos&Rele.]</span>';
                      eachSentenceHighlight =
                        strTemp + this.resultSentence[ind] + " ";
                    } else if (
                      logoFlag == 0 &&
                      pathoFlag == 0 &&
                      evidenceFlag == 1 &&
                      ethoFlag == 0
                    ) {
                      var strTemp =
                        '<span style="background-color: #e05c5c;">[Relevance&Evi.]</span>';
                      eachSentenceHighlight =
                        strTemp + this.resultSentence[ind] + " ";
                    }
                    //no other situations
                  } // relevance
                  // nothing?
                  else {
                    eachSentenceHighlight = this.resultSentence[ind] + " ";
                  }
                } //is premise
              } //cycle
              else {
                // length<1
                eachSentenceHighlight = e;
              }
              //error underline for each sentence
              if (ind in this.errSentenceIndex) {
                console.log("found err!");
                eachSentenceHighlight = eachSentenceHighlight.replace(
                  this.highlightWords[ind],
                  '<u style="text-decoration-color: red; text-decoration-style: wavy;">' +
                    this.highlightWords[ind] +
                    "</u>"
                );
              }
              this.allHighlightTxt += eachSentenceHighlight; //add each sentence to set
            });

            // this.highlightWords.forEach((err) =>{
            //   console.log("eachError:", err, typeof(err));
            //   this.allHighlightTxt = this.allHighlightTxt.replace(err,
            //     "<u style=\"text-decoration-color: red; text-decoration-style: wavy;\">" + err + "</u>");
            // });

            document.getElementById("userInputDiv").innerHTML = "";
            this.inputContent = "";
            document.getElementById("userInputDiv").innerHTML =
              this.allHighlightTxt;

            // check label button
            console.log("----check label button after click update----");
            console.log("label:", $("#arglabel")[0].checked);
            if (!this.labelTag) {
              $("#arglabel")[0].checked = true;
              this.labelTag = !this.labelTag;
            }
            //PipeService.$emit(PipeService.UPDATE_INPUTVIEW);
            //call relationship
            //this.callRelationship(this.backdata, this.inputRelationship);
            //setTimeout(this.callRelationship(this.backdata, this.inputRelationship), 1000);
          }
        );
      } else {
        console.log("NULL input");
      }
    },
    callRelationship(data, relationship) {
      console.log(
        "call node, relationship function:",
        data,
        relationship.length
      );
      this.nodeData = [];
      this.linkData = [];
      data.forEach((es) => {
        this.nodeData.push(es);
      });
      relationship.forEach((re) => {
        var tmpLink = { source: data[re[1]], target: data[re[0]] };
        this.linkData.push(tmpLink);
      });

      //the first is claim/ default
      var claimNum = relationship[0][0];
      if (claimNum != 0) {
        console.log("claimN:", claimNum);
        this.nodeData[claimNum]["is_claim"] = "1";
        this.nodeData[claimNum]["logos"] = 0;
        this.nodeData[claimNum]["evidence"] = 0;
      } else {
        this.nodeData[0]["is_claim"] = "1";
        this.nodeData[0]["logos"] = 0;
        this.nodeData[0]["evidence"] = 0;
      }
      console.log("node data1:", this.nodeData);
      console.log("link data1:", this.linkData);

      //update to node view
      DataService.nodeData = this.nodeData;
      DataService.linkData = this.linkData;
      PipeService.$emit(PipeService.UPDATE_NODEVIEW);
    },
  }, //all methods
};
</script>

<style scoped>
#userInputDiv {
  border-style: groove;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  word-break: break-all;
  outline: none;
  user-select: text;
  white-space: pre-wrap;
  text-align: left;
}

.btn {
  font-size: 14px;
}
</style>