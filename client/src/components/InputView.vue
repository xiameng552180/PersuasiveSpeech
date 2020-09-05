<template>
  <div>
    <div class="row">
      <div class="col-lg-10">
        <label>Claim: </label> 
        <div contenteditable="true" id="userInputDiv" 
        @input="changeDivText($event)"
        style="height:200px;">{{ inputContent }}</div>
      </div>
      <!-- <div contenteditable="true" id="userInputDiv" 
      style="height:200px;">from an algorithmic perspective, it becomes increasingly difficult. but we can solve it! You can't know what death is, and you can't know how you'll grow and adapt in Prison.</div> -->
      <div class="col-lg-2">
        <div class="inputSummary"></div>
      </div>
    </div>
    <br />
    <button type="button" class="btn btn-primary" v-on:click="updateInput">Upload</button>
      &nbsp;&nbsp;&nbsp;
  <label id="eloquenceScore">eloquence: 0</label> <p id="errorMess"></p>

  </div>
</template>


<script>
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";
import axios from 'axios';
import { highlightTextarea } from "../../static/jquery.highlighttextarea.js"


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
      highlightWords: [], //high light words list
      inputLabels: {
      "input": [
        { feature: "logos", label: 0 },
        { feature: "pathos", label: 0 },
        { feature: "ethos", label: 0 },
        { feature: "evidence", label: 0 },
        { feature: "relevance", label: 0 },
        { feature: "concreteness", label: 0 },
        { feature: "eloquence", label: 0 }
      ]},
      inputRelationship: [],
      eachSentenceLabel: {},
      editText: null,
      svgInput: null,
      widthInput: null,
      heightInput: null,
    };
  },
  mounted() {
    this.initialize() 
  },
  methods: {
    initialize() {
      this.inputLabels = DataService.inputLabels;
      //console.log("input:", this.inputLabels['input'][0]['label']);
      
        this.svgInput = d3
          .select(".inputSummary")
          .append("svg")
          .attr("width", 100)
          .attr("height", 200);
    },

    changeDivText(event) {
        this.editText = event.target.innerText;
        //console.log(this.editText);
    },



    updateInput: function (event) {
        //this.inputContent = document.getElementById("userInputDiv").innerHTML;  old version
        //console.log("t1", typeof(document.getElementById("userInput1").value));
        this.inputContent = this.editText;
        console.log("t2", typeof(this.inputContent));
        this.editText = event.target.innerHTML;
        if (this.inputContent.length != 0){ 
          NetService.uploadInput(this.inputContent, (x)=>{
            this.backdata = x.data.results; //processing result
            this.inputRelationship = x.data.relationships;

            console.log("from backend: ", this.backdata);
            console.log("backend relationship:", this.inputRelationship);
            var inputKeys = Object.keys(this.backdata);
            //console.log("sentence number: ", inputKeys.length);
            
            this.backdata.forEach((inputSentence, index) => {
                //console.log("each sentence: ", inputSentence['content']);
                this.eloquenceScore += parseInt(inputSentence['eloquence']);
                this.inputS.push(inputSentence['content']);
                
                //console.log("eachS: ", inputSentence);
                //this.lengthSentenList.push(inputSentence['content'].length);
                // inpthis.errorStartIndexList.push(inputSentence['elo_info'][2][0]['contextoffset']); //highlight start
                // this.errorEndIndexList.push(inputSentence['elo_info'][2][0]['errorlength']); //highlight end
                // label add
                var inputLabelAll = 0;
                this.inputLabels['input'][0]['label'] += parseInt(inputSentence['logos']);
                inputLabelAll += parseInt(inputSentence['logos']);
                this.inputLabels['input'][1]['label'] += parseInt(inputSentence['pathos']);
                inputLabelAll += parseInt(inputSentence['pathos']);
                this.inputLabels['input'][2]['label'] += parseInt(inputSentence['ethos']);
                inputLabelAll += parseInt(inputSentence['ethos']);
                this.inputLabels['input'][3]['label'] += parseInt(inputSentence['evidence']);
                inputLabelAll += parseInt(inputSentence['evidence']);
                this.inputLabels['input'][4]['label'] += parseInt(inputSentence['relevance']);
                inputLabelAll += parseInt(inputSentence['relevance']);
                this.inputLabels['input'][5]['label'] += parseInt(inputSentence['is_claim']);
                this.inputLabels['input'][6]['label'] += parseInt(inputSentence['eloquence']);
                
                
                // get each sentence lits
                var tempLabelList = [];
                tempLabelList.push(parseInt(inputSentence['logos']));
                tempLabelList.push(parseInt(inputSentence['pathos']));
                tempLabelList.push(parseInt(inputSentence['ethos']));
                tempLabelList.push(parseInt(inputSentence['evidence']));
                tempLabelList.push(parseInt(inputSentence['relevance']));
                tempLabelList.push(parseInt(inputSentence['is_claim']));
                tempLabelList.push(parseInt(inputSentence['claim_type']));
                this.eachSentenceLabel[index] = tempLabelList;
                
                
                console.log("each sentenceLabel:", index, this.inputLabels['input']);
                // compute persentage
                if (inputLabelAll != 0){
                  this.inputLabels['input'][0]['label'] = Math.round(this.inputLabels['input'][0]['label']/inputLabelAll);
                  this.inputLabels['input'][1]['label'] = Math.round(this.inputLabels['input'][1]['label']/inputLabelAll);
                  this.inputLabels['input'][2]['label'] = Math.round(this.inputLabels['input'][2]['label']/inputLabelAll);
                  this.inputLabels['input'][3]['label'] = Math.round(this.inputLabels['input'][3]['label']/inputLabelAll);
                  this.inputLabels['input'][4]['label'] = Math.round(this.inputLabels['input'][4]['label']/inputLabelAll);                 
                }
                else {
                  this.inputLabels['input'][0]['label'] /= 1;
                  this.inputLabels['input'][1]['label'] /= 1;
                  this.inputLabels['input'][2]['label'] /= 1;
                  this.inputLabels['input'][3]['label'] /= 1;
                  this.inputLabels['input'][4]['label'] /= 1;
                }
                
                if (inputSentence['elo_info'][2].length == 0) {
                  $('#errorMess').text("ERROR ");
                }else{
                  this.eloquenceErrorList.push(inputSentence['elo_info'][2][0]['message']); //error message
                  var startTemp = inputSentence['elo_info'][2][0]['contextoffset'];
                  var endTemp = inputSentence['elo_info'][2][0]['errorlength'];
                  this.highlightWords.push(inputSentence['content'].substring(startTemp, endTemp+1));
                }
                //console.log("inputLabels inputview:", this.inputLabels);
                //update input
                PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
                PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
                PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
                PipeService.$emit(PipeService.UPDATE_NODEVIEW);
                
            }); //end cycle
              
              //draw summary
              console.log("input summary", this.inputLabels);
              var jsonCircles = [
                {"x_axis":30,"y_axis":40,"radius":this.inputLabels['input'][0]['label'], "color":"#7eb6e4"},
                {"x_axis":30,"y_axis":70,"radius":this.inputLabels['input'][1]['label'],"color":"#8cd390"},
                {"x_axis":30,"y_axis":100,"radius":this.inputLabels['input'][2]['label'],"color":"#8f91fc"},
                {"x_axis":30,"y_axis":130,"radius":this.inputLabels['input'][3]['label'],"color":"#fa8cad"},
                {"x_axis":30,"y_axis":160,"radius":this.inputLabels['input'][4]['label'],"color":"#e05c5c"},
                {"x_axis":30,"y_axis":190,"radius":this.inputLabels['input'][5]['label'],"color":"#b6034d"}
              ];
              
              var circles = this.svgInput
                  .selectAll("circle")
                  .data(jsonCircles)
                  .enter()
                  .append("circle");

              circles.attr("cx", function(d){return d.x_axis})
                      .attr("cy", function(d){return d.y_axis})
                      .attr("r", function(d){return d.radius*5 + 5;})
                      .style("fill", function(d){return d.color;});

              var circleTxt = this.svgInput
                  .selectAll("circle")
                  .append("text")
                        .attr('x', 60)
                        .attr('y', function(d){return d.y_axis})
                        .style('color', "black")
                        .text(this.inputLabels['input'][5]['feature']);
                    

              // step0 highlight error
              //elo score
              $('#eloquenceScore').text("eloquence:" + this.eloquenceScore);
              
              // console.log("eloquenceScore:", this.eloquenceScore, this.eloquenceErrorList);
              // console.log("highlight words: ", this.highlightWords);
              if (this.eloquenceErrorList.length == 0) {
                $('#errorMess').text("no error");
              }else{
                $('#errorMess').text("ERROR ");
                this.eloquenceErrorList.forEach((er, index) => {
                  $('#errorMess').append(this.highlightWords[index] + ": " + er + ". ");
                });
              }

              console.log("error:", this.highlightWords);
              //highlight
              // var wordList = [];
              // for(var i in this.highlightWords){
              //   wordList.push(this.highlightWords[i]);
              // }
              // console.log(wordList);
              // $('#userInputDiv').highlightTextarea({
              //     words: wordList,
              //     color:"yellow",          
              // });
            

              //return highlight
              // step 1 process sentences
              var sentenceList = JSON.stringify(this.inputS);
              var items = sentenceList.split(",");
              sentenceList = items.join("");
              sentenceList = sentenceList.replace(/[\n]/g,"");
              sentenceList = sentenceList.replace("[", "");
              sentenceList = sentenceList.replace("]", "");             
              sentenceList = sentenceList.substring(0, sentenceList.length-2)
              sentenceList = sentenceList.replace(/\"/g, "")
              //console.log("s", sentenceList);
              var resultSentence = sentenceList.split(/[\.!\?]/);//分句子
              
              // step 2 got label and highlight content
              console.log("sentenceNum:", resultSentence.length);
              console.log("each sentence label: ", this.eachSentenceLabel);
              var allHighlightTxt = "";
              console.log("here");
              resultSentence.forEach((e, ind) => {
                //console.log("test", e, ind);
                var eachSentenceHighlight = "";
                if (e.length > 1){ //is it a sentence?
                  var colorTxt = "";
                  //console.log("inner sentence", ind, e);
                  //console.log("returnLabel: ", ind, this.eachSentenceLabel[ind]);
                  
                  var logoFlag = 0;
                  var pathoFlag = 0;
                  var ethoFlag = 0;
                  var evidenceFlag = 0;
                  
                  //claim?
                  if (this.eachSentenceLabel[ind][5] != 0){
                    var strTemp = "<span style=\"background-color: #b6034d; color: white\">Claim </span>";
                    var claimType = this.eachSentenceLabel[ind][6] 
                    eachSentenceHighlight = strTemp + claimType + resultSentence[ind];
                    //console.log("add Claim!", allHighlightTxt);
                  }
                  else { //premise
                    //logos?
                    if (this.eachSentenceLabel[ind][0] == 1)
                    {
                      logoFlag = 1; 
                      var strTemp = "<span style=\"background-color: #7eb6e4;\">Logos </span>"; 
                      eachSentenceHighlight = strTemp + resultSentence[ind];
                      //console.log("add logos!", allHighlightTxt);
                    }
                    //pathos?
                    if (this.eachSentenceLabel[ind][1] == 1){
                      if (logoFlag == 1){
                        pathoFlag = 1; //multiple label
                        var strTemp = "<span style=\"background-color: #7eb6e4;\">Pathos&Logos </span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind]; //
                      //console.log("add pathos!", allHighlightTxt);
                      }
                      else {
                        pathoFlag = 1; //multiple label
                        var strTemp = "<span style=\"background-color: #8cd390;\">Pathos </span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                      }
                    }
                    //evidence?
                    if (this.eachSentenceLabel[ind][3] == 1){
                      if (logoFlag == 0 && pathoFlag == 0){ //single evidence
                        evidenceFlag = 1;
                        var strTemp = "<span style=\"background-color: #fa8cad;\">Evidence</span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                        //console.log("add evidence!", allHighlightTxt);
                      }
                      else if(logoFlag == 1 && pathoFlag == 1){ //3 labels
                        evidenceFlag = 1;
                        var strTemp = "<span style=\"background-color: #7eb6e4;\">Pathos&Logos&Evidence</span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                      }
                      else if(logoFlag == 1 && pathoFlag == 0){ //2 labels
                        evidenceFlag = 1;
                        var strTemp = "<span style=\"background-color: #7eb6e4;\">Logos&Evidence</span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                      }
                      else if(logoFlag == 0 && pathoFlag == 1){ //2 labels
                        evidenceFlag = 1;
                        var strTemp = "<span style=\"background-color: #8cd390;\">Pathos&Evidence</span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                      }
                    }
                    //ethos?
                    if (this.eachSentenceLabel[ind][2] == 1){
                      if (logoFlag == 0 && pathoFlag == 0 && evidenceFlag == 0){
                      var strTemp = "<span style=\"background-color: #8f91fc;\">Ethos</span>";
                      eachSentenceHighlight = strTemp + resultSentence[ind];
                      //console.log("add ethos!", allHighlightTxt);
                      }
                      else if(logoFlag == 1 && pathoFlag == 0 && evidenceFlag == 0){ //logo+etho
                        var strTemp = "<span style=\"background-color: #8f91fc;\">Ethos&Logos </span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                      }
                      else if(logoFlag == 1 && pathoFlag == 0 && evidenceFlag == 1){ //logo+etho
                        var strTemp = "<span style=\"background-color: #8f91fc;\">Ethos&Logos&Evi </span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                      }
                      else if(logoFlag == 0 && pathoFlag == 0 && evidenceFlag == 1){ //logo+etho
                        var strTemp = "<span style=\"background-color: #8f91fc;\">Ethos&Evi </span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                      }
                      // no other situations
                    }
                    //relevance?
                    if (this.eachSentenceLabel[ind][4] == 1){
                      if (logoFlag == 0 && pathoFlag == 0 && evidenceFlag == 0 && ethoFlag == 0){
                        var strTemp = "<span style=\"background-color: #e05c5c;\">Relevance </span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                        //console.log("add relevance!", allHighlightTxt);
                      }
                      else if(logoFlag == 1 && pathoFlag == 0 && evidenceFlag == 1 && ethoFlag == 0){
                        var strTemp = "<span style=\"background-color: #e05c5c;\">Logos&Evi&Rele </span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                      }
                      else if(logoFlag == 1 && pathoFlag == 0 && evidenceFlag == 0 && ethoFlag == 0){
                        var strTemp = "<span style=\"background-color: #e05c5c;\">Logos&Rele </span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                      }
                      else if(logoFlag == 0 && pathoFlag == 0 && evidenceFlag == 1 && ethoFlag == 0){
                        var strTemp = "<span style=\"background-color: #e05c5c;\">Rele&Evi </span>";
                        eachSentenceHighlight = strTemp + resultSentence[ind];
                      }
                      //no other situations
                    }
                  }
                  
                  allHighlightTxt += eachSentenceHighlight; //add each sentence to set
                }//cycle
              });
              this.highlightWords.forEach((err) =>{
                console.log("eachError:", err);
                allHighlightTxt = allHighlightTxt.replace(err, 
                  "<u style=\"text-decoration-color: red; text-decoration-style: wavy;\">" + err + "</u>");
              })
              
              document.getElementById("userInputDiv").innerHTML = "";
              document.getElementById("userInputDiv").innerHTML = allHighlightTxt;

          });
        }
        else {console.log("NULL input");}  
        
      },
    },

    
  };

</script>

<style scoped>
  #userInputDiv{
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
</style>
