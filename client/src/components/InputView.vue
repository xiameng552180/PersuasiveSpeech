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
      lengthSentenList: [],//lenfth of each sentence
      highlightWords: [], //high light words list
    };
  },
  mounted() {
    this.initialize();
    
    
  },
  methods: {
    initialize() {
      
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
                this.lengthSentenList.push(inputSentence['content'].length);
                
                this.eloquenceErrorList.push(inputSentence['elo_info'][2][0]['message']); //error message
                // inpthis.errorStartIndexList.push(inputSentence['elo_info'][2][0]['contextoffset']); //highlight start
                // this.errorEndIndexList.push(inputSentence['elo_info'][2][0]['errorlength']); //highlight end
                var startTemp = inputSentence['elo_info'][2][0]['contextoffset'];
                var endTemp = inputSentence['elo_info'][2][0]['errorlength'];
                this.highlightWords.push(inputSentence['content'].substring(startTemp, endTemp+1));
                //console.log("highlight:", inputSentence['content'].substring(startTemp, endTemp+1));
                //console.log(inputSentence['content'].length);
                //console.log("error:", inputSentence['elo_info'][2][0]['message']);
              });
              $('#eloquenceScore').text("eloquence:" + this.eloquenceScore);
              console.log("inputS: ", this.inputSentences);
              console.log("eloquenceScore:", this.eloquenceScore, this.eloquenceErrorList);
              console.log("highlight: ", this.highlightWords);

              if (this.eloquenceErrorList.length == 0) {
                $('#errorMess').text("no error");
              }else{
                $('#errorMess').text("error: ");
                this.eloquenceErrorList.forEach((er, index) => {
                  $('#errorMess').append(index + ':' + er + ".");
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
