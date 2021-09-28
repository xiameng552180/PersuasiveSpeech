<template>
  <div class="container-fluid">
    <div class="row mt-5">
      <div class="col-lg-6">
        <div
          id="InputView"
          class="card border-light ml-3 shadow-sm"
          style="height: 500px"
        >
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Input Text
          </h5>
          <div class="card-body">
            <input-view></input-view>
          </div>
        </div>
      </div>

      <div class="col-lg-6">
        <div
          id="ExampleView"
          class="card border-light mr-3 shadow-sm"
          style="height: 500px"
        >
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Example View
          </h5>
          <example-view></example-view>
        </div>
      </div>
    </div>

    <div class="row mt-5 mb-5">
      <!-- <div class="col-lg-2">
        <div
          id="SelectView"
          class="card border-light ml-3 shadow-sm"
          style="height: 500px"
        >
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Select View
          </h5>
          <div class="card-body">
            <select-view></select-view>
          </div>
        </div>
      </div> -->
      <div class="col-lg-4">
        <div
          id="NodeView"
          class="card border-light mr-3 shadow-sm"
          style="height: 500px"
        >
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Node View
          </h5>
          <div class="card-body">
            <node-view></node-view>
          </div>
        </div>
      </div>
      <div class="col-lg-8">
        <div
          id="CompareView"
          class="card border-light mr-3 shadow-sm"
          style="height: 500px"
        >
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Compare View
          </h5>
          <div class="card-body">
            <compare-view></compare-view>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import loginView from "./components/loginView";
import SelectView from "./components/SelectView";
import NodeView from "./components/NodeView";
import CompareView from "./components/CompareView";
import ExampleView from "./components/ExampleView";
import InputView from "./components/InputView";
import NetService from "./services/net-service";
import DataService from "./services/data-service";
import PipeService from "./services/pipe-service";

export default {
  name: "App",
  components: {
    loginView,
    SelectView,
    NodeView,
    CompareView,
    ExampleView,
    InputView,
  },
  data() {
    return {
      mainViewMode: [
        "DashBoard",
        "KidsList",
        "Upload",
        "KidDetails",
        "VideoLabeling",
      ],
      defaultViewMode: 0, // default is 0
      curViewMode: 0, // default is 0
      isLogin: true, // make sure it is true first.
    };
  },
  mounted() {
    this.$nextTick(function foo() {
      this.initialize();
    });
  },
  methods: {
    initialize() {
      // console.log("hello world");
    },
  },
};
</script>

<style scoped></style>
