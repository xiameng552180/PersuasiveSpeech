<template>
    <!-- <div class="input-group">
        <div class="input-group-prepend">
            <span class="input-group-text">Input</span>
        </div>
            <textarea class="form-control" aria-label="With textarea" style="height:240px"></textarea>
    </div> -->
    <div>
        <textarea class="form-control" id="userInput" style="height:240px" placeholder="Input your text here" aria-label="With textarea">qqq</textarea>
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
      //var inputContent = document.getElementById("userInput").value;
    // NetService.uploadInput("hello");
    // this.updateInput();
    NetService.uploadInput({name: "hello"}, (x)=>{console.log(x)});
    
  },
  methods: {
    initialize() {},
    updateInput: function (event) {
        var inputContent = document.getElementById("userInput").value;
        this.backdata = NetService.uploadInput(inputContent);
        console.log(this.backdata);
        // NetService.uploadInput(inputContent => {
        //   console.log(inputContent);
        // });
      

      }
    },
   
  };

</script>