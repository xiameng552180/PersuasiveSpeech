<template>
    <div>
        <!-- <div class="highlighter">
          <span v-for="item in inputSentences"
          class="markError">
          {{ item }}
          </span> 
        </div> -->
        <textarea class="form-control" id="userInput" style="height:240px" 
            placeholder="Input your text here" aria-label="With textarea">from an algorithmic perspective, it becomes increasingly difficult. but we can solve it!
        </textarea>
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
      inputSentences: [], //all input sentences
      // lengthSentenList: [],//lenfth of each sentence
      highlightWords: [], //high light words list
      inputLabels: {},
    };
  },
  mounted() {
    this.initialize();
    
    
  },
  methods: {
    initialize() {
      this.inputLabels = DataService.inputLabels;
      //console.log("input:", this.inputLabels['input'][0]['label']);
    },
    updateInput: function (event) {
        var inputContent = document.getElementById("userInput").value;
        //this.backdata = NetService.uploadInput(inputContent);
        if (inputContent.length != 0){ 
          NetService.uploadInput(inputContent, (x)=>{
            this.backdata = x.data.results; //processing result
            console.log("from backend: ", this.backdata);
            var inputKeys = Object.keys(this.backdata);
            console.log("sentence number: ", inputKeys.length);
            
            this.backdata.forEach((inputSentence) => {
                //console.log("each sentence: ", inputSentence['content']);
                this.eloquenceScore += parseInt(inputSentence['eloquence']);
                this.inputSentences.push(inputSentence['content']);
                // this.lengthSentenList.push(inputSentence['content'].length);
                // inpthis.errorStartIndexList.push(inputSentence['elo_info'][2][0]['contextoffset']); //highlight start
                // this.errorEndIndexList.push(inputSentence['elo_info'][2][0]['errorlength']); //highlight end

                // label add
                this.inputLabels['input'][0]['label'] += parseInt(inputSentence['logos']);
                this.inputLabels['input'][1]['label'] += parseInt(inputSentence['pathos']);
                this.inputLabels['input'][2]['label'] += parseInt(inputSentence['ethos']);
                this.inputLabels['input'][3]['label'] += parseInt(inputSentence['evidence']);
                this.inputLabels['input'][4]['label'] += parseInt(inputSentence['relevance']);
                this.inputLabels['input'][5]['label'] += parseInt(inputSentence['concreteness']);
                this.inputLabels['input'][6]['label'] += parseInt(inputSentence['eloquence']);

                if (inputSentence['elo_info'][2].length == 0) {
                  $('#errorMess').text("ERROR ");
                }else{
                  this.eloquenceErrorList.push(inputSentence['elo_info'][2][0]['message']); //error message
                  var startTemp = inputSentence['elo_info'][2][0]['contextoffset'];
                  var endTemp = inputSentence['elo_info'][2][0]['errorlength'];
                  this.highlightWords.push(inputSentence['content'].substring(startTemp, endTemp+1));
                
                }
                //console.log("inputLabels:", this.inputLabels);
                //update input
                PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
                PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
                PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
                
              });
              //elo score
              $('#eloquenceScore').text("eloquence:" + this.eloquenceScore);
              // console.log("inputS: ", this.inputSentences);
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
              
              //highlight
              var wordList = [];
              for(var i in this.highlightWords){
                wordList.push(this.highlightWords[i]);
              }
              console.log(wordList);
              $('#userInput').highlightTextarea({
                  words: wordList,
                  color:"yellow",          
              });
          });
        }
        else {console.log("NULL input");}  
        
      },
    },

    
  };

</script>
