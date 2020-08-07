<template>
  <div class="container-fluid">
    <div class="row mt-5">
      <div class="col-lg-5">
        <div id="InputView" class="card border-light ml-3 shadow-sm" style="height:400px">
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Input Text
          </h5>
          <div class="card-body">
            <div class="input-group">
              <div class="input-group-prepend">
                <span class="input-group-text">Input</span>
              </div>
              <textarea class="form-control" aria-label="With textarea"></textarea>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-7">
        <div id="ExampleView" class="card border-light mr-3 shadow-sm" style="height:400px">
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Example View
          </h5>
          <example-view></example-view>
        </div>
      </div>
    </div>

    <div class="row mt-5">
      <div class="col-lg-5">
        <div id="SelectView" class="card border-light ml-3 shadow-sm">
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Select View
          </h5>
          <div class="card-body">
            <select-view></select-view>
          </div>
        </div>
      </div>

      <div class="col-lg-7">
        <div id="CompareView" class="card border-light mr-3 shadow-sm">
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
import CompareView from "./components/CompareView";
import ExampleView from "./components/ExampleView";
import InputView from "./components/InputView";

// import DataService from './services/data-service';
// import PipeService from './services/pipe-service';

export default {
  name: "App",
  components: {
    loginView,
    SelectView,
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
      console.log("hello world");
    },
  },
};
</script>

<style scoped></style>
