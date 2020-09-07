<template>
  <div>
    <div class="row">
      
      <div class="col-lg-10" >
        <input v-model="userid" placeholder="input user id"/>
        </br>
        <label>Claim: </label> 
        <div contenteditable="true" id="userInputDiv" 
        @input="changeDivText($event)"
        style="height:260px; font-size: 20px">{{ inputContent }}</div>
      </div>
      <!-- <div contenteditable="true" id="userInputDiv" 
      style="height:200px;">from an algorithmic perspective, it becomes increasingly difficult. but we can solve it! You can't know what death is, and you can't know how you'll grow and adapt in Prison.</div> -->
      <div class="col-lg-2">
        <!-- <div class="inputSummary" style="height:260px;"></div> -->
      </div>
    </div>
    <br />
    <button type="button" class="btn btn-primary" v-on:click="updateInput">Upload</button>
      &nbsp;&nbsp;&nbsp;
  <label id="eloquenceScore">eloquence: 0</label> <p id="errorMess" overflow:scroll></p>

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
      highlightWords: {}, //high light words list
      inputLabels: {},
      inputRelationship: [],
      nodeData: [],
      eachSentenceLabel: {},
      editText: null,
      svgInput: null,
      widthInput: null,
      heightInput: null,
      userid: "",
      allHighlightTxt: "",
      resultSentence: null,
      startErrIndex: null,
      endErrIndex: null,
      errSentenceIndex: [],
    };
  },
  mounted() {
    this.initialize() 
  },
  methods: {
    initialize() {
      this.inputLabels = DataService.inputLabels;
      
        this.svgInput = d3
          .select(".inputSummary")
          .append("svg")
          .attr("width", 180)
          .attr("height", 250);
    },

    changeDivText(event) {
        this.editText = event.target.innerText;
        //console.log("changeTxt:", this.editText);
        //多次upload 去掉label hard processing
        // if (this.editText.search("Claim") != -1){
        //   this.editText = this.editText.replace("[Claim]", "");
        // }
        if (this.editText.search("[Claim]") != -1){
          this.editText = this.editText.replace(/\[Claim[[\d]*\]/g, "");
        }
        if (this.editText.search("[Logos]") != -1){
          this.editText = this.editText.replace(/\[Logos[[\d]*\]/g, "");
        }
        if (this.editText.search("[Pathos]") != -1){
          this.editText = this.editText.replace(/\[Pathos[[\d]*\]/g, "");
        }
        if (this.editText.search("Ethos") != -1){
          this.editText = this.editText.replace(/\[Ethos[[\d]*\]/g, "");
        }
        if (this.editText.search("Evidence") != -1){
          this.editText = this.editText.replace(/\[Evidence[[\d]*\]/g, "");
        }
        if (this.editText.search("Relevance") != -1){
          this.editText = this.editText.replace(/\[Relevance[[\d]*\]/g, "");
        }

    },

    updateInput: function (event) {
        //this.inputContent = document.getElementById("userInputDiv").innerHTML;  old version
        //console.log("t1", typeof(document.getElementById("userInput1").value));
        //remove label tag
        // var obj = document.getElementsByClassName("addLabelTag");
        // obj.innerHTML = "";//删除div内容

        this.inputContent = this.editText; 
        //console.log("jiequ1", this.inputContent.match(\span(\S*)span>\)[1]);
        console.log("changeTxt2:", this.inputContent);
        // this.editText = event.target.innerHTML;
        if (this.inputContent.length != 0){ 
          NetService.uploadInput({"content": this.inputContent, "userid": this.userid}, (x)=>{
            this.backdata = x.data.results; //processing result
            this.inputRelationship = x.data.relationships;

            console.log("from backend: ", this.backdata);
            console.log("backend relationship:", this.inputRelationship, this.inputRelationship.length);
            var inputKeys = Object.keys(this.backdata);

            /////////////////(Xingbo's try)//////////
            this.callRelationship(this.backdata, this.inputRelationship)
            console.log("I have run callrelatinship");

            /////////////////(Xingbo's try)//////////
            this.inputS = []; //clear
            this.highlightWords = {}; //clear
            var currentErrWords = "";
            //console.log("sentence number: ", inputKeys.length);
            this.backdata.forEach((i, index) => {
                
                console.log("each sentence: ", index, i['content']);
                this.eloquenceScore += parseInt(i['eloquence']);
                this.inputS.push(i['content']);
                
                //console.log("eachS: ", i);
                //this.lengthSentenList.push(i['content'].length);
                // inpthis.errorStartIndexList.push(i['elo_info'][2][0]['contextoffset']); //highlight start
                // this.errorEndIndexList.push(i['elo_info'][2][0]['errorlength']); //highlight end
                // label add
                var inputLabelAll = 0;
                this.inputLabels['input'][0]['label'] += parseInt(i['logos']);
                inputLabelAll += parseInt(i['logos']);
                this.inputLabels['input'][1]['label'] += parseInt(i['pathos']);
                inputLabelAll += parseInt(i['pathos']);
                this.inputLabels['input'][2]['label'] += parseInt(i['ethos']);
                inputLabelAll += parseInt(i['ethos']);
                this.inputLabels['input'][3]['label'] += parseInt(i['evidence']);
                inputLabelAll += parseInt(i['evidence']);
                this.inputLabels['input'][4]['label'] += parseInt(i['relevance']);
                inputLabelAll += parseInt(i['relevance']);
                this.inputLabels['input'][5]['label'] += parseInt(i['is_claim']);
                //console.log("error of [5]", this.inputLabels['input'][5]['label'])
                inputLabelAll += parseInt(i['is_claim']);

                this.inputLabels['input'][6]['label'] += parseInt(i['eloquence']);
                
                
                // get each sentence lits
                var tempLabelList = [];
                tempLabelList.push(parseInt(i['logos']));
                tempLabelList.push(parseInt(i['pathos']));
                tempLabelList.push(parseInt(i['ethos']));
                tempLabelList.push(parseInt(i['evidence']));
                tempLabelList.push(parseInt(i['relevance']));
                tempLabelList.push(parseInt(i['is_claim']));
                tempLabelList.push(parseInt(i['claim_type']));
                this.eachSentenceLabel[index] = tempLabelList;
                
                
                //console.log("each sentenceLabel:", index, this.inputLabels['input']);
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
                
                if (i['elo_info'][2].length == 0) {
                  $('#errorMess').text("ERROR ");
                }else{
                  this.errSentenceIndex.push(index);
                  this.eloquenceErrorList.push(i['elo_info'][2][0]['message']); //error message
                  this.startErrIndex = i['elo_info'][2][0]['contextoffset'];
                  this.endErrIndex = i['elo_info'][2][0]['errorlength'];
                  //highlight words of all sentence
                  currentErrWords = i['content'].substring(this.startErrIndex, this.endErrIndex + 1);
                  this.highlightWords[index] = i['content'].substring(this.startErrIndex, this.endErrIndex + 1); 
                }
                //console.log("inputLabels inputview:", this.inputLabels);
                //update input

                PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
                PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
                PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
                PipeService.$emit(PipeService.UPDATE_NODEVIEW);
                console.log("current Err Words:", currentErrWords);
            }); //end cycle
              
            
            
              // step0 highlight error
              //elo score
              $('#eloquenceScore').text("eloquence:" + this.eloquenceScore);
              
              // console.log("eloquenceScore:", this.eloquenceScore, this.eloquenceErrorList);
              
              if (this.eloquenceErrorList.length == 0) {
                $('#errorMess').text("no error");
              }else{
                $('#errorMess').text("ERROR ");
                this.eloquenceErrorList.forEach((er, index) => {
                  $('#errorMess').append(this.highlightWords[index] + ": " + er + ". "+ " ");
                });
              }
            
              //return highlight
              // step 1 process sentences
              var sentenceList = JSON.stringify(this.inputS);
              console.log("errorsentenceInd:", this.errSentenceIndex, this.highlightWords);
              var items = sentenceList.split(",");
              sentenceList = items.join("");
              
              sentenceList = sentenceList.replace(/[\n]/g,"");
              sentenceList = sentenceList.replace("[", "");
              sentenceList = sentenceList.replace("]", "");   
              //sentenceList.pop();          
              sentenceList = sentenceList.substring(0, sentenceList.length-1)
              
              sentenceList = sentenceList.replace(/\"/g, "")
              //console.log("s", sentenceList, typeof(sentenceList));
              this.resultSentence = sentenceList.split(/[\.]/);
              // console.log("here1", resultSentence);
              // var resultSentence = this.backdata.map(data => data.content)

              // step 2 got label and highlight content
              
              //console.log("sentenceNum:", this.resultSentence.length);
              //console.log("each sentence label: ", this.eachSentenceLabel);

              //clear
              this.allHighlightTxt = "";//clear
              //this.inputContent = this.inputContent.replace();
              
              
              //console.log("here2", this.resultSentence);
              //console.log("here3 inputContent:", this.inputContent);
              this.resultSentence.forEach((e, ind) => {
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
                  var errFlag = 0;
                  var errEndInd = null;
                  var newStr = "";
                  //claim?
                  //console.log("typeof Sentence", typeof(e), e); //string
                  if (this.eachSentenceLabel[ind][5] != 0){ //claim
                    var strTemp = "<span style=\"background-color: #b6034d; color: white\">[Claim]</span>";
                    eachSentenceHighlight = strTemp + e + ".";
                    
                  }
                  else { //premise
                    //logos?
                    if (this.eachSentenceLabel[ind][0] == 1)
                    {
                      logoFlag = 1; 
                      var strTemp = "<span style=\"background-color: #7eb6e4;\">[Logos]</span>"; 
                      eachSentenceHighlight = strTemp + e + ".";
                        
                      //console.log("add logos!", allHighlightTxt);
                    }
                    //pathos?
                    if (this.eachSentenceLabel[ind][1] == 1){
                      if (logoFlag == 1){
                        pathoFlag = 1; //multiple label
                        var strTemp = "<span style=\"background-color: #7eb6e4;\">[Pathos&Logos]</span>";
                        eachSentenceHighlight = strTemp + e + "."; //
                        
                      //console.log("add pathos!", allHighlightTxt);
                      }
                      else {
                        pathoFlag = 1; //multiple label
                        var strTemp = "<span style=\"background-color: #8cd390;\">[Pathos]</span>";
                        
                        eachSentenceHighlight = strTemp + e + ".";
                        
                      }
                    }
                    //evidence?
                    if (this.eachSentenceLabel[ind][3] == 1){
                      if (logoFlag == 0 && pathoFlag == 0){ //single evidence
                        evidenceFlag = 1;
                        var strTemp = "<span style=\"background-color: #fa8cad;\">[Evidence]</span>";
                        
                        eachSentenceHighlight = strTemp + e + ".";
                        
                        //console.log("add evidence!", allHighlightTxt);
                      }
                      else if(logoFlag == 1 && pathoFlag == 1){ //3 labels
                        evidenceFlag = 1;
                        var strTemp = "<span style=\"background-color: #7eb6e4;\">[Pathos&Logos&Evi.]</span>";
                          eachSentenceHighlight = strTemp + e + ".";
                        
                      }
                      else if(logoFlag == 1 && pathoFlag == 0){ //2 labels
                        evidenceFlag = 1;
                        var strTemp = "<span style=\"background-color: #7eb6e4;\">[Logos&Evi.]</span>";
                        
    
                          eachSentenceHighlight = strTemp + this.resultSentence[ind] + ".";
                        
                      }
                      else if(logoFlag == 0 && pathoFlag == 1){ //2 labels
                        evidenceFlag = 1;
                        var strTemp = "<span style=\"background-color: #8cd390;\">[Pathos&Evi.]</span>";
                        eachSentenceHighlight = strTemp + e + ".";
                        
                      }
                    }
                    //ethos?
                    if (this.eachSentenceLabel[ind][2] == 1){
                      if (logoFlag == 0 && pathoFlag == 0 && evidenceFlag == 0){
                        var strTemp = "<span style=\"background-color: #8f91fc;\">[Ethos]</span>";
                        eachSentenceHighlight = strTemp + e + ".";
                        
                      //console.log("add ethos!", allHighlightTxt);
                      }
                      else if(logoFlag == 1 && pathoFlag == 0 && evidenceFlag == 0){ //logo+etho
                        var strTemp = "<span style=\"background-color: #8f91fc;\">[Ethos&Logos]</span>";
                        eachSentenceHighlight = strTemp + e + ".";
                      }
                      else if(logoFlag == 1 && pathoFlag == 0 && evidenceFlag == 1){ //logo+etho
                        var strTemp = "<span style=\"background-color: #8f91fc;\">[Ethos&Logos&Evi.]</span>";
                        eachSentenceHighlight = strTemp + e + ".";
                      }
                      else if(logoFlag == 0 && pathoFlag == 0 && evidenceFlag == 1){ //logo+etho
                        var strTemp = "<span style=\"background-color: #8f91fc;\">[Ethos&Evi.]</span>";
                        eachSentenceHighlight = strTemp + e + ".";
                      }
                      // no other situations
                    }
                    //relevance?
                    if (this.eachSentenceLabel[ind][4] == 1){
                      if (logoFlag == 0 && pathoFlag == 0 && evidenceFlag == 0 && ethoFlag == 0){
                        var strTemp = "<span style=\"background-color: #e05c5c;\">[Relevance]</span>";
                        eachSentenceHighlight = strTemp + this.resultSentence[ind] + ".";
                        //console.log("add relevance!", allHighlightTxt);
                      }
                      else if(logoFlag == 1 && pathoFlag == 0 && evidenceFlag == 1 && ethoFlag == 0){
                        var strTemp = "<span style=\"background-color: #e05c5c;\">[Logos&Evi.&Rele.]</span>";
                        eachSentenceHighlight = strTemp + this.resultSentence[ind] + ".";
                      }
                      else if(logoFlag == 1 && pathoFlag == 0 && evidenceFlag == 0 && ethoFlag == 0){
                        var strTemp = "<span style=\"background-color: #e05c5c;\">[Logos&Rele.]</span>";
                        eachSentenceHighlight = strTemp + this.resultSentence[ind] + ".";
                      }
                      else if(logoFlag == 0 && pathoFlag == 0 && evidenceFlag == 1 && ethoFlag == 0){
                        var strTemp = "<span style=\"background-color: #e05c5c;\">[Relevance&Evi.]</span>";
                        eachSentenceHighlight = strTemp + this.resultSentence[ind] + ".";
                      }
                      //no other situations
                    }// relevance

                    
                    
                  }//is premise

                  //error underline for each sentence
                  if (ind in this.errSentenceIndex) {
                      console.log("found err!");
                      eachSentenceHighlight = eachSentenceHighlight.replace(this.highlightWords[ind], 
                      "<u style=\"text-decoration-color: red; text-decoration-style: wavy;\">" + this.highlightWords[ind] + "</u>");
                  }
                  this.allHighlightTxt += eachSentenceHighlight; //add each sentence to set
                }//cycle
              });
              
              
              // this.highlightWords.forEach((err) =>{
              //   console.log("eachError:", err, typeof(err));
              //   this.allHighlightTxt = this.allHighlightTxt.replace(err, 
              //     "<u style=\"text-decoration-color: red; text-decoration-style: wavy;\">" + err + "</u>");
              // });
              
              document.getElementById("userInputDiv").innerHTML = "";
              this.inputContent = "";
              document.getElementById("userInputDiv").innerHTML = this.allHighlightTxt;
              //PipeService.$emit(PipeService.UPDATE_INPUTVIEW);
              //call relationship
              //this.callRelationship(this.backdata, this.inputRelationship);
              //setTimeout(this.callRelationship(this.backdata, this.inputRelationship), 1000);
          });
        }
        else {console.log("NULL input");}  
        
      },
      callRelationship(data, relationship) {
        console.log("call node, relationship function:", data, relationship.length);
        this.nodeData = [];
        data.forEach((es) => {
          this.nodeData.push(es);
        });
        console.log("node data1:", this.nodeData);
        this.nodeData[0]['is_claim'] = "1";
        this.nodeData[0]['logos'] = "0";
        this.nodeData[0]['evidence'] = "0";
        // var claimNum = relationship[0][0]; //the first is claim/ default
        // console.log("claimN:", claimNum);
        // console.log("node data1:", this.nodeData);
        // console.log(this.nodeData[claimNum]);
        // this.nodeData[claimNum]['is_claim'] = 1;
        // //this.nodeData[claimNum]['claim_type'] = "disagreement";
        // this.nodeData[0]['logos'] = 0;
        // this.nodeData[0]['evidence'] = 0;
        // this.nodeData[0]['ethos'] = 0;
        // this.nodeData[0]['pathos'] = 0;
        // this.nodeData[0]['relevance'] = 0;
        // console.log("node data2:", this.nodeData);

        //update to node view
        DataService.nodeData = this.nodeData;
        PipeService.$emit(PipeService.UPDATE_NODEVIEW);
      },


    },//all methods

    

    
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