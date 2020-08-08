<template>
  <div>
    <div class="form-group">
      <label for="exampleFormControlSelect1">Topic</label>
      <select class="form-control" id="exampleFormControlSelect1">
        <option>Dating</option>
        <option>Abortion</option>
        <option>Marriage</option>
      </select>
    </div>

    <div class="form-group">
      <label for="exampleFormControlInput1">Background</label>
      <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="e.g. ..." />
    </div>

    <div class="form-group">
      <label for="exampleFormControlInput1">Prefer Style</label>
      <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="e.g. ..." />
    </div>

    <div class="form-group">
      <div class="row">
        <label for="formControlRange" class="col-10">Easygoing</label>
        <label for="formControlRange">Stubborn</label>
      </div>
      <input type="range" class="form-control-range" id="formControlRange" />
    </div>

    <button type="submit" class="btn btn-primary my-1" v-on:click="addCounter">Submit</button>
    <p>Count: {{counter}}</p>
  </div>
</template>

<script>
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";

import json16 from "../../../server/dataset/posts_new/dating-16_new.json";
import json17 from "../../../server/dataset/posts_new/dating-17_new.json";
import json19 from "../../../server/dataset/posts_new/dating-19_new.json";

export default {
  name: "SelectView",
  data() {
    return {
      counter: null,
    };
  },
  mounted() {
    this.addExamples();
    PipeService.$on(PipeService.UPDATE_SELECTVIEW, () => {
      this.counter = DataService.counter;
    });
  },

  methods: {
    addExamples() {
      json16["dating-16"][0]["reply-info"].forEach((item) =>
        DataService.examples.push(item)
      );
      json17["dating-17"][0]["reply-info"].forEach((item) =>
        DataService.examples.push(item)
      );
      json19["dating-19"][0]["reply-info"].forEach((item) =>
        DataService.examples.push(item)
      );
      //   console.log(DataService.examples);
      PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
      PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
      PipeService.$emit(PipeService.UPDATE_COMPAREVIEW);
    },
    addCounter: function (event) {
      DataService.counter += 1;
      PipeService.$emit(PipeService.UPDATE_SELECTVIEW);
      PipeService.$emit(PipeService.UPDATE_EXAMPLEVIEW);
      console.log(this.counter);
    },
  },
};
</script>