<template>
  <div class="card-body overflow-auto">
    <ul class="list-group" id="examplelist">
      <li
        class="list-group-item d-flex justify-content-between align-items-center"
        v-for="item in items"
        :key="item.content"
      >
        {{item.content}}
        <div class="row col-2">
          <span class="badge badge-primary m-1" v-if="item.logos!=='0'">L</span>
          <span class="badge badge-secondary m-1" v-if="item.pathos!=='0'">P</span>
          <span class="badge badge-success m-1" v-if="item.ethos!=='0'">P</span>
          <span class="badge badge-danger m-1" v-if="item.evidence!=='0'">Ev</span>
          <span class="badge badge-info m-1" v-if="item.relevance!=='0'">R</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import json from "../dating-16.json";
export default {
  name: "SelectView",
  data() {
    return {
      items: json["Dating-16"][0]["reply-info"][0]["reply_contents"],
    };
  },
  mounted() {
    this.initialize();
  },
  methods: {
    initialize() {
      console.log(json["Dating-16"][0]["reply-info"][0]["reply_contents"]);
      console.log(this.items);
    },
  },
};
</script>

<style scoped>
/* .badge-primary {
  background-color: antiquewhite;
} */
</style>