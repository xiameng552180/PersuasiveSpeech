<template>
  <div class="card overflow-auto">
    <h5 class="card-header">
      <div class="btn-group btn-group-toggle" data-toggle="buttons">
        <button class="btn btn-sm btn-claim m-1" v-on:click="click_claim">claim</button>
        <button class="btn btn-sm btn-logos m-1" v-on:click="click_logos">logos</button>
        <button class="btn btn-sm btn-pathos m-1" v-on:click="click_pathos">pathos</button>
        <button class="btn btn-sm btn-ethos m-1" v-on:click="click_ethos">ethos</button>
        <button class="btn btn-sm btn-evidence m-1" v-on:click="click_evidence">evidence</button>
        <button class="btn btn-sm btn-relevance m-1" v-on:click="click_relevance">relevance</button>
      </div>
    </h5>
    <div class="card-body overflow-auto">
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
      <br />
      <br />
      <span>Concreteness (from low to high)</span>
      <span class="badge badge-concreteness m-1" style="opacity:0.2">C</span>
      <span class="badge badge-concreteness m-1" style="opacity:0.5">C</span>
      <span class="badge badge-concreteness m-1" style="opacity:1">C</span>
      <span class="ml-4">Eloquence (from low to high)</span>
      <span class="badge badge-eloquence m-1" style="opacity:0.2">El</span>
      <span class="badge badge-eloquence m-1" style="opacity:0.5">El</span>
      <span class="badge badge-eloquence m-1" style="opacity:1">El</span>

      <br />

      <!--highlight text-->
      <div class="card">
        <div v-for="example in examples" :key="example.id" class="card-body">
          <h5
            class="card-title"
            :id="example.id"
            :ref="example.id"
          >Replyer name: {{example.content["replyer_name"]}}</h5>
          <p v-if="if_claim==true" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-claim"
                v-if="item.is_claim!=='0' && if_claim==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p v-else-if="if_logos==true" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-logos"
                v-if="item.logos!=='0' && if_logos==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p v-else-if="if_pathos==true" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-pathos"
                v-if="item.pathos!=='0' && if_pathos==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p v-else-if="if_ethos==true" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-ethos"
                v-if="item.ethos!=='0' && if_ethos==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p v-else-if="if_evidence==true" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-evidence"
                v-if="item.evidence!=='0' && if_evidence==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p v-else-if="if_relevance==true" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-relevance"
                v-if="item.relevance!=='0' && if_relevance==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p v-else class="card-text text-secondary">
            <span
              v-for="item in example.content.reply_contents"
              :key="item.content"
            >{{item.content+". "}}</span>
          </p>
        </div>
      </div>
    </div>
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
      if_claim: false,
      if_logos: false,
      if_pathos: false,
      if_ethos: false,
      if_evidence: false,
      if_relevance: false,
      examples: null,
      ex_id: "",
    };
  },
  mounted() {
    this.initialize();
    PipeService.$on(PipeService.UPDATE_EXAMPLEVIEW, () => {
      this.ex_id = DataService.ex_id;
      this.examples = DataService.examples;
      this.display();
    });
  },
  methods: {
    initialize() {},
    display() {
      if (this.ex_id !== "") {
        var element = document.getElementById(this.ex_id);
        console.log(this.ex_id);
        console.log(document.getElementById(this.ex_id));

        element.scrollIntoView({ behavior: "smooth" });
      }
    },
    click_claim() {
      this.if_claim = true;
      this.if_logos = false;
      this.if_pathos = false;
      this.if_ethos = false;
      this.if_evidence = false;
      this.if_relevance = false;
    },
    click_logos() {
      this.if_claim = false;
      this.if_logos = true;
      this.if_pathos = false;
      this.if_ethos = false;
      this.if_evidence = false;
      this.if_relevance = false;
    },
    click_pathos() {
      this.if_claim = false;
      this.if_logos = false;
      this.if_pathos = true;
      this.if_ethos = false;
      this.if_evidence = false;
      this.if_relevance = false;
    },
    click_ethos() {
      this.if_claim = false;
      this.if_logos = false;
      this.if_pathos = false;
      this.if_ethos = true;
      this.if_evidence = false;
      this.if_relevance = false;
    },
    click_evidence() {
      this.if_claim = false;
      this.if_logos = false;
      this.if_pathos = false;
      this.if_ethos = false;
      this.if_evidence = true;
      this.if_relevance = false;
    },
    click_relevance() {
      this.if_claim = false;
      this.if_logos = false;
      this.if_pathos = false;
      this.if_ethos = false;
      this.if_evidence = false;
      this.if_relevance = true;
    },
  },
};
</script>

<style scoped>
/* for text bg color */
.textbg-claim {
  background-color: #b6034d;
  color: white;
}
.textbg-logos {
  background-color: #7eb6e4;
  color: white;
}
.textbg-pathos {
  background-color: #8cd390;
  color: white;
}
.textbg-ethos {
  background-color: #8f91fc;
  color: white;
}
.textbg-evidence {
  background-color: #fa8cad;
  color: white;
}
.textbg-relevance {
  background-color: #e05c5c;
  color: white;
}
.textbg-concreteness {
  background-color: rgb(1, 83, 19);
  color: white;
}
.textbg-eloquence {
  background-color: rgb(1, 13, 83);
  color: white;
}

/* for button */
.btn-claim {
  background-color: rgb(182, 3, 77);
  color: white;
}
.btn-logos {
  background-color: rgb(126, 182, 228);
  color: white;
}
.btn-pathos {
  background-color: #8cd390;
  color: white;
}
.btn-ethos {
  background-color: rgb(143, 145, 252);
  color: white;
}
.btn-evidence {
  background-color: rgb(250, 140, 173);
  color: white;
}
.btn-relevance {
  background-color: rgb(224, 92, 92);
  color: white;
}

/* for badge */
.badge-claim {
  background-color: rgb(182, 3, 77);
  color: white;
}
.badge-logos {
  background-color: rgb(126, 182, 228);
  color: white;
}
.badge-pathos {
  background-color: #8cd390;
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