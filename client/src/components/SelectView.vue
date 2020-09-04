<template>
  <div>
    <div class="form-group">
      <label for="exampleFormControlSelect1">Topic</label>
      <select class="form-control" id="topicSelect" v-on:change="chooseTopic">
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
    <br />
    <span class="glyphicon glyphicon glyphicon-edit" aria-hidden="true"></span>
    <label>Interest topic:</label> <br />
    <li>Human Life</li>
    <li id="interestTopic">Others</li>
    <li>...</li>
    <br /><br />
    <span class="glyphicon glyphicon glyphicon-edit" aria-hidden="true"></span>
    <label>Persuasive Level:</label>
    <div class="progress">
      <div id="persuasiveStyle" class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 45%">
      </div>
    </div>
    <label id="persuasiveText">ratio:</label>
    <br /><br />
    <!-- <div class="form-group">
      <div class="row">
        <label for="formControlRange" class="col-10">Easygoing</label>
        <label for="formControlRange">Stubborn</label>
      </div>
      <input type="range" class="form-control-range" id="formControlRange" />
    </div> -->
    <button type="submit" class="btn btn-primary my-1" v-on:click="onSubmit">Submit</button>
    <!-- <p>Count: {{counter}}</p> -->
  </div>
</template>

<script>
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";
import pLevelSum from "../levelSummary.json";
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
      persuasiveLevel: {}
    };
  },
  mounted() {
    this.chooseTopic();
    //this.addExamples();

    //persuasive level
    pLevelSum.forEach((e) => {
      var key = Object.keys(e);
      this.persuasiveLevel[key] = e[key]['replyer_num']/e[key]['delta'];
      this.persuasiveLevel[key] =  Math.round(this.persuasiveLevel[key] * 900);
    });
    
    //console.log("persuasiveLevel: ", this.persuasiveLevel);
  },

  methods: {
    chooseTopic() {
      var topic_s = document.getElementById('topicSelect');
      var index = topic_s.selectedIndex;
      this.selectTopicNum = topic_s.options[index].value;
      this.selectTopic = topic_s.options[index].text;
      
      DataService.selectTopicNum = this.selectTopicNum;
      DataService.selectTopic = this.selectTopic;
      this.addExamples();
      PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
      //console.log(this.persuasiveLevel[this.selectTopic]);

      $("#persuasiveStyle").css("width", this.persuasiveLevel[this.selectTopic]+'%');
      $('#persuasiveText').text("ratio:" + this.persuasiveLevel[this.selectTopic]+'%');
      $('#interestTopic').text(this.selectTopic);
      console.log("topicSelect:", this.selectTopicNum, this.selectTopic);
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