<template>
    <div>
        <textarea class="form-control" id="userInput" style="height:240px" 
            placeholder="Input your text here" aria-label="With textarea">123</textarea>
        <br />
        <button type="button" class="btn btn-primary" v-on:click="updateInput">Upload</button>
    </div>
        
    
</template>


<script>
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";
import axios from 'axios';



export default {
  name: "InputView",
  data() {
    return {
      inputContent: null,
      backdata: null
    };
  },
  mounted() {
    this.initialize();
    
  },
  methods: {
    initialize() {},
    updateInput: function (event) {
        var inputContent = document.getElementById("userInput").value;
        //this.backdata = NetService.uploadInput(inputContent);
        NetService.uploadInput(inputContent, (x)=>{
           //console.log("callback", x);
           this.backdata = x;
           });
        console.log("from backend: ", this.backdata);
      }
    },
   
  };

</script>