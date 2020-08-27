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
        <label id="eloquenceScore">eloquence: 0</label>
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
      errorStartIndexList: [],// all input highlight starts
      errorEndIndexList: [], //all input highlight ends
      inputSentences: [], //all input sentences
    };
  },
  mounted() {
    this.initialize();
    $('#userInput').highlightTextarea({
        words: ['can', 'an']
    });
    
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
                this.eloquenceErrorList.push(inputSentence['elo_info'][2][0]['message']);
                this.errorStartIndexList.push(inputSentence['elo_info'][2][0]['contextoffset']);
                this.errorEndIndexList.push(inputSentence['elo_info'][2][0]['errorlength']);
                //console.log("error:", inputSentence['elo_info'][2][0]['message']);
              });
              $('#eloquenceScore').text("eloquence:" + this.eloquenceScore);
              console.log("inputS: ", this.inputSentences);
              console.log("eloquenceScore:", this.eloquenceScore, this.eloquenceErrorList);
              console.log("errorlength: ", this.errorStartIndexList, this.errorEndIndexList);

          });
          }
          else {console.log("NULL input");}       
      },
    

    },
    
  };

</script>
<style scoped>
.hwt-container {
	display: inline-block;
	position: relative;
	overflow: hidden !important;
	-webkit-text-size-adjust: none !important;
}

.hwt-backdrop {
	position: absolute !important;
	top: 0 !important;
	right: -99px !important;
	bottom: 0 !important;
	left: 0 !important;
	padding-right: 99px !important;
	overflow-x: hidden !important;
	overflow-y: auto !important;
}

.hwt-highlights {
	width: auto !important;
	height: auto !important;
	border-color: transparent !important;
	white-space: pre-wrap !important;
	word-wrap: break-word !important;
	color: transparent !important;
	overflow: hidden !important;
}

.hwt-input {
	display: block !important;
	position: relative !important;
	margin: 0;
	padding: 0;
	border-radius: 0;
	font: inherit;
	overflow-x: hidden !important;
	overflow-y: auto !important;
}

.hwt-content {
	border: 1px solid;
	background: none transparent !important;
}

.hwt-content mark {
	padding: 0 !important;
	color: inherit;
}

</style>