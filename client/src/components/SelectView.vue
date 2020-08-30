<template>
  <div>
    <div class="form-group">
      <label for="exampleFormControlSelect1">Topic</label>
      <select class="form-control" id="topicSelect" v-on:change="chooseTopic">
        <option value="0">Abortion</option>
        <option value="1" selected = "selected">Dating</option>
        <option value="2">Eugenics</option>
        <option value="3">Immortality</option>
        <option value="4">Marriage</option>
        <option value="5">Parenthood</option>
        <option value="6">Pride</option>
        <option value="7">Suicide</option>
      </select>
    </div>

    <div class="form-group">
      <label for="exampleFormControlInput1">Background</label>
      <!-- <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="e.g. ..." /> -->
      <select class="form-control" id="exampleFormControlSelect1">
        <option>Abortion</option>
        <option>Dating</option>
        <option>Immortality</option>
        <option>Marriage</option>
        <option>Parenthood</option>
        <option>Pride</option>
        <option>Suicidce</option>
      </select>
    </div>

    <!-- <div class="form-group">
      <label for="exampleFormControlInput1">Strategies</label>
      <select id="strategy" class="selectpicker show-menu-arrow form-control" multiple>
                <option value="0">Logical</option>
                <option value="1">Storytelling</option>
                <option value="2">Authoritative</option>
                <option value="3">Evidence</option>
                <option value="4">Relevance</option>
                <option value="5">New ideas</option>
                <option value="6">Specific</option>
                <option value="7">Fluent</option>
                
      </select>
    </div>-->

    <div class="form-group">
      <div class="row">
        <label for="formControlRange" class="col-10">Easygoing</label>
        <label for="formControlRange">Stubborn</label>
      </div>
      <input type="range" class="form-control-range" id="formControlRange" />
    </div>
    <button type="submit" class="btn btn-primary my-1" v-on:click="onSubmit">Submit</button>
    <!-- <p>Count: {{counter}}</p> -->
  </div>
</template>

<script>
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";

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
  name: "SelectView",
  data() {
    return {
      //counter: null,
      selectTopicNum: null,
      selectTopic: null,
      topicExamples: {
        'Abortion': abortion, 
        'Dating': dating, 
        'Eugenics': eugenics,
        'Immortality': immortality,
        'Marriage': marriage,
        'Parenthood': parenthood,
        'Pride': pride,
        'Suicide': suicide
      },
    };
  },
  mounted() {
    this.chooseTopic();
    //this.addExamples();

  },

  methods: {
    chooseTopic() {
      var topic_s = document.getElementById('topicSelect');
      var index = topic_s.selectedIndex;
      this.selectTopicNum = topic_s.options[index].value;
      this.selectTopic = topic_s.options[index].text;
      
      DataService.selectTopicNum = this.selectTopicNum;
      DataService.selectTopic = this.selectTopic;

      PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
      this.addExamples();
      //console.log("topicSelect:", this.selectTopicNum, this.selectTopic);
    },

    addExamples() {
      //console.log("Choosetest2", this.topicExamples[this.selectTopic]);
      var tempEx = this.topicExamples[this.selectTopic]
      DataService.examples = [];
      tempEx.forEach((ele) => {
        var objKey = Object.keys(ele);
        var c = 0
        ele[objKey][0]["reply-info"].forEach((item) => { 
          var new_item = {id: objKey + "-" + c, content: item};
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

    onSubmit: function (event) {

      PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
      PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
      PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
      //console.log(this.counter);
      // console.log($('#strategy').val());
    },
  },
};
</script>