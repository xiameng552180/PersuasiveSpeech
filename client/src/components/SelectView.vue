<template>
  <div>
    <div class="form-group">
      <label for="exampleFormControlSelect1">Topic</label>
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
    <button type="submit" class="btn btn-primary my-1" v-on:click="addCounter">Submit</button>
    <!-- <p>Count: {{counter}}</p> -->
  </div>
</template>

<script>
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";

import json16 from "../../../server/dataset/dating/dating-16.json";
import json17 from "../../../server/dataset/dating/dating-17.json";
import json19 from "../../../server/dataset/dating/dating-19.json";
import json20 from "../../../server/dataset/dating/dating-20.json";
import json21 from "../../../server/dataset/dating/dating-21.json";
import json22 from "../../../server/dataset/dating/dating-22.json";
import json23 from "../../../server/dataset/dating/dating-23.json";
import json25 from "../../../server/dataset/dating/dating-25.json";
import json26 from "../../../server/dataset/dating/dating-26.json";

export default {
  name: "SelectView",
  data() {
    return {
      counter: null,
    };
  },
  mounted() {
    this.addExamples();
  },

  methods: {
    addExamples() {
      var i = 0;
      json16["dating-16"][0]["reply-info"].forEach((item) => {
        var new_item = { id: "dating-16-" + i, content: item };
        DataService.examples.push(new_item);
        i++;
      });

      var i = 0;
      json17["dating-17"][0]["reply-info"].forEach((item) => {
        var new_item = { id: "dating-17-" + i, content: item };
        DataService.examples.push(new_item);
        i++;
      });

      var i = 0;
      json19["dating-19"][0]["reply-info"].forEach((item) => {
        var new_item = { id: "dating-19-" + i, content: item };
        DataService.examples.push(new_item);
        i++;
      });

      var i = 0;
      json20["dating-20"][0]["reply-info"].forEach((item) => {
        var new_item = { id: "dating-20-" + i, content: item };
        DataService.examples.push(new_item);
        i++;
      });

      var i = 0;
      json21["dating-21"][0]["reply-info"].forEach((item) => {
        var new_item = { id: "dating-21-" + i, content: item };
        DataService.examples.push(new_item);
        i++;
      });

      var i = 0;
      json22["dating-22"][0]["reply-info"].forEach((item) => {
        var new_item = { id: "dating-22-" + i, content: item };
        DataService.examples.push(new_item);
        i++;
      });

      var i = 0;
      json23["dating-23"][0]["reply-info"].forEach((item) => {
        var new_item = { id: "dating-23-" + i, content: item };
        DataService.examples.push(new_item);
        i++;
      });

      var i = 0;
      json25["dating-25"][0]["reply-info"].forEach((item) => {
        var new_item = { id: "dating-25-" + i, content: item };
        DataService.examples.push(new_item);
        i++;
      });

      var i = 0;
      json26["dating-26"][0]["reply-info"].forEach((item) => {
        var new_item = { id: "dating-26-" + i, content: item };
        DataService.examples.push(new_item);
        i++;
      });

      // sort by delta
      DataService.examples = DataService.examples.sort((a, b) =>
        d3.descending(
          parseInt(a.content.reply_delta_num),
          parseInt(b.content.reply_delta_num)
        )
      );

      console.log(DataService.examples);
      PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
      // PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
      // PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
    },
    addCounter: function (event) {
      // DataService.counter += 1;
      PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
      PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
      PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
      //console.log(this.counter);
      // console.log($('#strategy').val());
    },
  },
};
</script>