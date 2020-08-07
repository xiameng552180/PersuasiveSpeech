<template>
  <div class="card-body overflow-auto">
    <p>Replyer name: {{name}}</p>
    <span>Calim type:</span>
    <span class="badge badge-claim m-1">interpretation</span>
    <span class="badge badge-claim m-1">evaluation</span>
    <span class="badge badge-claim m-1">disagreement</span>
    <br />
    <span class="badge badge-logos m-1">L</span>
    <span>Logos</span>
    <span class="badge badge-pathos m-1">P</span>
    <span>Pathos</span>
    <span class="badge badge-ethos m-1">E</span>
    <span>Ethos</span>
    <span class="badge badge-evidence m-1">Ev</span>
    <span>Evidence</span>
    <span class="badge badge-relevance m-1">R</span>
    <span>Relevance</span>

    <ul class="list-group" id="examplelist">
      <li
        class="list-group-item d-flex justify-content-between align-items-center"
        v-for="item in items"
        :key="item.content"
      >
        {{item.content}}
        <div class="row col-2">
          <span class="badge badge-claim m-1" v-if="item.is_claim!=='0'">{{item.claim_type}}</span>
          <span class="badge badge-logos m-1" v-if="item.logos!=='0'">L</span>
          <span class="badge badge-pathos m-1" v-if="item.pathos!=='0'">P</span>
          <span class="badge badge-ethos m-1" v-if="item.ethos!=='0'">E</span>
          <span class="badge badge-evidence m-1" v-if="item.evidence!=='0'">Ev</span>
          <span class="badge badge-relevance m-1" v-if="item.relevance!=='0'">R</span>
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
      name: json["Dating-16"][0]["reply-info"][0]["replyer_name"],
      items: json["Dating-16"][0]["reply-info"][0]["reply_contents"],
    };
  },
  mounted() {
    this.initialize();
  },
  methods: {
    initialize() {
      console.log(json);
      console.log(json["Dating-16"][0]["reply-info"][0]["reply_contents"]);
    },
  },
};
</script>

<style scoped>
.badge-claim {
  background-color: rgb(182, 3, 77);
  color: white;
}
.badge-logos {
  background-color: rgb(126, 182, 228);
  color: white;
}
.badge-pathos {
  background-color: rgb(140, 215, 250);
  color: white;
}
.badge-ethos {
  background-color: rgb(143, 145, 252);
  color: white;
}
.badge-evidence {
  background-color: rgb(250, 140, 173);
  color: white;
}
.badge-relevance {
  background-color: rgb(224, 92, 92);
  color: white;
}
</style>