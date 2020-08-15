<template>
  <div class="card-body overflow-auto">
    <p>Replyer name: {{name}}</p>
    <span>Calim type:</span>
    <span class="badge badge-claim m-1">interpretation</span>
    <span class="badge badge-claim m-1">evaluation</span>
    <span class="badge badge-claim m-1">disagreement</span>
    
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
    <br/><br/>
    <span>Concreteness (from low to high)</span>
    <span class="badge badge-concreteness m-1" style="opacity:0.2">C</span>
    <span class="badge badge-concreteness m-1" style="opacity:0.5">C</span>
    <span class="badge badge-concreteness m-1" style="opacity:1">C</span>
    <span class="ml-4">Eloquence (from low to high)</span>
    <span class="badge badge-eloquence m-1" style="opacity:0.2">El</span>
    <span class="badge badge-eloquence m-1" style="opacity:0.5">El</span>
    <span class="badge badge-eloquence m-1" style="opacity:1">El</span>

    <ul class="list-group" id="examplelist">
      <br /> 
      <li
        class="list-group-item"
        v-for="item in items"
        :key="item.content"
      >
        <div class="row">
          <div class="col-8">{{item.content}}</div>
          <div class="col-2">
            <span class="badge badge-claim m-1" v-if="item.is_claim!=='0'">{{item.claim_type}}</span>
            <span class="badge badge-logos m-1" v-if="item.logos!=='0'">L</span>
            <span class="badge badge-pathos m-1" v-if="item.pathos!=='0'">P</span>
            <span class="badge badge-ethos m-1" v-if="item.ethos!=='0'">E</span>
            <span class="badge badge-evidence m-1" v-if="item.evidence!=='0'">Ev</span>
            <span class="badge badge-relevance m-1" v-if="item.relevance!=='0'">R</span>
          </div>
          <div class="col-2">
            <span
              class="badge badge-concreteness m-1"
              v-bind:style="{opacity:((item.concreteness-0.15)*10)}"
            >C</span>
            <span class="badge badge-eloquence m-1" v-bind:style="{opacity:item.eloquence/2}">El</span>
          </div>
        <hr>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import NetService from "../services/net-service";
import DataService from "../services/data-service";
import PipeService from "../services/pipe-service";

export default {
  name: "ExampleView",
  data() {
    return {
      opacity: { opacity: 0.5 },
      name: null,
      items: null,
      //counter: null,
      examples: null,
      ex_order: null,
    };
  },
  mounted() {
    this.initialize();
    PipeService.$on(PipeService.UPDATE_EXAMPLEVIEW, () => {
      //this.counter = DataService.counter;
      this.ex_order = DataService.ex_order;
      this.examples = DataService.examples;
      this.display();
    });
  },
  methods: {
    initialize() {},
    display() {
      //   console.log(this.examples);
      this.name = this.examples[this.ex_order]["replyer_name"];
      this.items = this.examples[this.ex_order]["reply_contents"];
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
.badge-concreteness {
  background-color: rgb(1, 83, 19);
  color: white;
}
.badge-eloquence {
  background-color: rgb(1, 13, 83);
  color: white;
}
</style>