<template>
  <div>
  <input v-model="userid" placeholder="input user id">
    <div class="row">
      <div class="col-lg-12">
        <label>Claim: </label> 
        <div contenteditable="true" id="userInputDiv" 
        @input="changeDivText($event)"
        style="height:260px; font-size: 20px">{{ inputContent }}</div>
      </div>
      <!-- <div contenteditable="true" id="userInputDiv" 
      style="height:200px;">from an algorithmic perspective, it becomes increasingly difficult. but we can solve it! You can't know what death is, and you can't know how you'll grow and adapt in Prison.</div> -->
      <!-- <div class="col-lg-2">
        <div class="inputSummary" style="height:260px;"></div>
      </div> -->
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
        //console.log(this.editText);
    },

    updateInput: function (event) {
        //this.inputContent = document.getElementById("userInputDiv").innerHTML;  old version
        //console.log("t1", typeof(document.getElementById("userInput1").value));
        this.inputContent = this.editText;
        //console.log("t2", typeof(this.inputContent));
        this.editText = event.target.innerHTML;
        if (this.inputContent.length != 0){ 
          NetService.uploadInput({"content": this.inputContent, "userid": this.userid}, (x)=>{
            this.backdata = x.data.results; //processing result
            this.inputRelationship = x.data.relationships;
            //this.oriDataEdit = this.backdata;
            console.log("from backend: ", this.backdata);
            console.log("backend relationship:", this.inputRelationship, this.inputRelationship.length);
            var inputKeys = Object.keys(this.backdata);
            this.inputS = []; //clear
            this.highlightWords = {}; //clear
            var currentErrWords = "";
            //console.log("sentence number: ", inputKeys.length);
            this.callRelationship(this.backdata, this.inputRelationship)
            console.log("I have run callrelatinship");
            


            this.backdata.forEach((i, index) => {
                console.log("each sentence: ", index, i['content']);
                this.eloquenceScore += parseInt(i['eloquence']);
                // if (i['content'].length > 2){
                //   console.log("null???", i);
                //   this.inputS.push(i['content']);
                //   this.oriDataEdit.push(i);
                // }else{
                //   console.log("bad sentence.");
                // }
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
                  currentErrWords = i['content'].substring(this.startErrIndex, this.endErrIndex + 1);
                  this.highlightWords[index] = i['content'].substring(this.startErrIndex, this.endErrIndex+1);
                }
                //console.log("inputLabels inputview:", this.inputLabels);
                //update input
                PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
                PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
                PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
                PipeService.$emit(PipeService.UPDATE_NODEVIEW);
                //console.log("current Err Words:", currentErrWords);

            }); //end cycle
              
            

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

              //console.log("error:", this.highlightWords);
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
              //console.log("1111111",this.inputS);
              // var sentenceList = JSON.stringify(this.inputS);
              // var items = sentenceList.split(",");
              // sentenceList = items.join("");
              // sentenceList = sentenceList.replace(/[\n]/g,"");
              // sentenceList = sentenceList.replace("[", "");
              // sentenceList = sentenceList.replace("]", "");             
              // sentenceList = sentenceList.substring(0, sentenceList.length-2)
              // sentenceList = sentenceList.replace(/\"/g, "");
              // console.log("s", sentenceList);
              // this.resultSentence = sentenceList.split(/[\.]/);//分句子
              this.resultSentence = this.inputS;
              // console.log("here1", resultSentence);
              // var resultSentence = this.backdata.map(data => data.content)

              // step 2 got label and highlight content
              console.log("sentenceNum:", this.resultSentence.length);
              //console.log("each sentence label: ", this.eachSentenceLabel);
              this.allHighlightTxt = ""; //clear
              this.inputContent = this.inputContent.replace();
              console.log("here2", this.resultSentence);
              //console.log("here3 inputContent:", this.inputContent);
              this.resultSentence.forEach((e, ind) => {
                //console.log("test", e, ind);
                var eachSentenceHighlight = "";
                if (e.length > 1){ //is it a sentence?
                  //claim?
                  if (this.eachSentenceLabel[ind][5] != 0){ //claim
                    var strTemp = "<span style =\'background-color: #90ee8f\'>" + e + "</span>" + "  ";
                    //var claimType = this.eachSentenceLabel[ind][5] 
                    eachSentenceHighlight = strTemp;
                    // console.log("add Claim!", allHighlightTxt);
                  }
                  else { //premise
                    var strTemp = "<span style = \'background-color: #ffd701\'>" + e + "</span>" + "  ";
                    //var claimType = this.eachSentenceLabel[ind][5] 
                    eachSentenceHighlight = strTemp;
            
                  }

                }//cycle
                else{// length<1
                  eachSentenceHighlight = e;
                }

                ///
                if (ind in this.errSentenceIndex) {
                      //console.log("found err!");
                      eachSentenceHighlight = eachSentenceHighlight.replace(this.highlightWords[ind], 
                      "<u style=\"text-decoration-color: red; text-decoration-style: wavy;\">" + this.highlightWords[ind] + "</u>");
                  }
                this.allHighlightTxt += eachSentenceHighlight; //add each sentence to set
              });
          
              
              document.getElementById("userInputDiv").innerHTML = "";
              this.inputContent = "";
              document.getElementById("userInputDiv").innerHTML = this.allHighlightTxt;



              PipeService.$emit(PipeService.UPDATE_INPUTVIEW);
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
        this.linkData = [];
        data.forEach((es) => {
          this.nodeData.push(es);
        });
        relationship.forEach((re) => {
          var tmpLink = {"source": data[re[1]], "target": data[re[0]]};
          this.linkData.push(tmpLink);
        })
        

        var claimNum = relationship[0][0]; //the first is claim/ default
        if (claimNum != 0){
          console.log("claimN:", claimNum);
          this.nodeData[claimNum]['is_claim'] = "1";
          this.nodeData[claimNum]['logos'] = 0;
          this.nodeData[claimNum]['evidence'] = 0;
        }
        else{
          this.nodeData[0]['is_claim'] = "1";
          this.nodeData[0]['logos'] = 0;
          this.nodeData[0]['evidence'] = 0;
        }
        
        console.log("node data1:", this.nodeData);
        console.log("link data1:", this.linkData);



        //update to node view
        DataService.nodeData = this.nodeData;
        DataService.linkData = this.linkData;
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