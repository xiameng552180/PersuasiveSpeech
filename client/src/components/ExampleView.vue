<template>
  <div class="card overflow-auto">
    <h5 class="card-header">
      <div class="btn-group btn-group-toggle" data-toggle="buttons">
        <button
          class="btn btn-sm btn-claim m-1"
          data-toggle="tooltip"
          data-placement="bottom"
          title="The category of what is being claimed"
          v-on:click="click_claim"
        >claim</button>
        <button
          class="btn btn-sm btn-logos m-1"
          v-on:click="click_logos"
          data-toggle="tooltip"
          data-placement="bottom"
          title="The use of logic, rationality, and critical reasoning to persuade"
        >logos</button>
        <button
          class="btn btn-sm btn-pathos m-1"
          v-on:click="click_pathos"
          data-toggle="tooltip"
          data-placement="bottom"
          title="The use of emotion and affect to persuade"
        >pathos</button>
        <button
          class="btn btn-sm btn-ethos m-1"
          v-on:click="click_ethos"
          data-toggle="tooltip"
          data-placement="bottom"
          title="The use of authority or credibility of the presenter to persuade"
        >ethos</button>
        <button
          class="btn btn-sm btn-evidence m-1"
          v-on:click="click_evidence"
          data-toggle="tooltip"
          data-placement="bottom"
          title="The statement decribe a concrete example"
        >evidence</button>
        <button
          class="btn btn-sm btn-relevance m-1"
          v-on:click="click_relevance"
          data-toggle="tooltip"
          data-placement="bottom"
          title="The statement revelant to the parent claim"
        >relevance</button>
        <button
          class="btn btn-sm btn-primary m-1"
          v-on:click="click_clear"
          data-toggle="tooltip"
          data-placement="bottom"
          title="The statement revelant to the parent claim"
        >clear</button>
      </div>
    </h5>
    <div class="card-body overflow-auto">
      <!--highlight text-->
      <div class="card">
        <div v-for="example in examples" :key="example.id" class="card-body">
          <h5
            class="card-title"
            :id="'h5_'+example.id"
            :ref="example.id"
          >Replyer name: {{example.content["replyer_name"]}}</h5>

          <p v-if="clear==true && ex_id !== example.id" class="card-text text-secondary">
            <span
              v-for="item in example.content.reply_contents"
              :key="item.content"
            >{{item.content+". "}}</span>
          </p>

          <!-- the selected post -->
          <p v-else-if="if_claim==true && ex_id === example.id" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-claim"
                v-if="item.is_claim!=='0' && if_claim==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p v-else-if="if_logos==true && ex_id === example.id" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-logos"
                v-if="item.logos!=='0' && if_logos==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p v-else-if="if_pathos==true && ex_id === example.id" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-pathos"
                v-if="item.pathos!=='0' && if_pathos==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p v-else-if="if_ethos==true && ex_id === example.id" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-ethos"
                v-if="item.ethos!=='0' && if_ethos==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p v-else-if="if_evidence==true && ex_id === example.id" class="card-text text-secondary">
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-evidence"
                v-if="item.evidence!=='0' && if_evidence==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>
          <p
            v-else-if="if_relevance==true && ex_id === example.id"
            class="card-text text-secondary"
          >
            <span v-for="item in example.content.reply_contents" :key="item.content">
              <mark
                class="textbg-relevance"
                v-if="item.relevance!=='0' && if_relevance==true"
              >{{item.content+". "}}</mark>
              <span v-else>{{item.content+". "}}</span>
            </span>
          </p>

          <p v-else-if="if_claim==true" class="card-text text-secondary">
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
      clear: true,
      select: null,
      example_sum: null,
    };
  },
  mounted() {
    this.initialize();
    PipeService.$on(PipeService.UPDATE_EXAMPLEVIEW, () => {
      this.ex_id = DataService.ex_id;
      this.examples = DataService.examples;
      this.examplesum = DataService.examplesum;
      //console.log("exampleview:", this.ex_id);
      this.display();
    });
  },
  methods: {
    initialize() {},
    display() {
      if (this.ex_id !== "") {
        var element = document.getElementById("h5_" + this.ex_id);
        // console.log(this.ex_id);
        // console.log(element);
        element.scrollIntoView({ behavior: "smooth" });

        //console.log("Example view examplesum:");
        //console.log(this.examplesum);

        var valuearr = Object.values(this.examplesum).map((d) => parseInt(d));
        console.log(valuearr);
        var maxvalue = Math.max(...valuearr);
        var maxindex = valuearr.indexOf(maxvalue);
        var keyarr = Object.keys(this.examplesum);
        var maxkey = keyarr[maxindex];
        console.log(maxkey);
        if (maxkey == "claim") this.click_claim();
        if (maxkey == "logos") this.click_logos();
        if (maxkey == "pathos") this.click_pathos();
        if (maxkey == "ethos") this.click_ethos();
        if (maxkey == "evidence") this.click_evidence();
        if (maxkey == "relevance") this.click_relevance();
        this.clear = true;
      }
    },
    click_claim() {
      this.if_claim = true;
      this.if_logos = false;
      this.if_pathos = false;
      this.if_ethos = false;
      this.if_evidence = false;
      this.if_relevance = false;
      this.clear = false;
    },
    click_logos() {
      this.if_claim = false;
      this.if_logos = true;
      this.if_pathos = false;
      this.if_ethos = false;
      this.if_evidence = false;
      this.if_relevance = false;
      this.clear = false;
    },
    click_pathos() {
      this.if_claim = false;
      this.if_logos = false;
      this.if_pathos = true;
      this.if_ethos = false;
      this.if_evidence = false;
      this.if_relevance = false;
      this.clear = false;
    },
    click_ethos() {
      this.if_claim = false;
      this.if_logos = false;
      this.if_pathos = false;
      this.if_ethos = true;
      this.if_evidence = false;
      this.if_relevance = false;
      this.clear = false;
    },
    click_evidence() {
      this.if_claim = false;
      this.if_logos = false;
      this.if_pathos = false;
      this.if_ethos = false;
      this.if_evidence = true;
      this.if_relevance = false;
      this.clear = false;
    },
    click_relevance() {
      this.if_claim = false;
      this.if_logos = false;
      this.if_pathos = false;
      this.if_ethos = false;
      this.if_evidence = false;
      this.if_relevance = true;
      this.clear = false;
    },
    click_clear() {
      this.if_claim = false;
      this.if_logos = false;
      this.if_pathos = false;
      this.if_ethos = false;
      this.if_evidence = false;
      this.if_relevance = false;
      this.clear = true;
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

.btn {
  font-size: 14px;
}
</style>