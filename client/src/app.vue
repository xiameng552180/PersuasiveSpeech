<template>
  <div class="container-fluid">
    <div class="row mt-5">
      <div class="col-lg-5">
        <div id="loginView" class="card border-light ml-3 shadow-sm">
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Input Text
          </h5>
          <div class="card-body">
            <div class="input-group">
              <div class="input-group-prepend">
                <span class="input-group-text">Input</span>
              </div>
              <textarea
                class="form-control"
                aria-label="With textarea"
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-7">
        <div id="loginView" class="card border-light mr-3 shadow-sm">
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Example View
          </h5>
          <div class="card-body">
            <ul class="list-group">
              <li
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                Example 1
                <span class="badge badge-primary badge-pill">14</span>
              </li>
              <li
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                Example 2
                <span class="badge badge-primary badge-pill">2</span>
              </li>
              <li
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                Example 3
                <span class="badge badge-primary badge-pill">1</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-5">
      <div class="col-lg-5">
        <div id="loginView" class="card border-light ml-3 shadow-sm">
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Select View
          </h5>
          <div class="card-body">
            <p class="card-text">Please enter ...</p>
          </div>
        </div>
      </div>

      <div class="col-lg-7">
        <div id="loginView" class="card border-light mr-3 shadow-sm">
          <h5 class="card-header">
            <i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Compare View
          </h5>
          <div class="card-body"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import loginView from "./components/login/loginView";
import inputView from "./components/login/inputView";

// import DataService from './services/data-service';
// import PipeService from './services/pipe-service';

export default {
  name: "App",
  components: {
    loginView,
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

<style scoped>
.window {
  margin: 8px 4px 0px 4px;
  padding: 0px 0px 0px 0px;
  box-shadow: 0px 1px 1px #666;
  background-color: #a9cefc4b;
  border-color: #ffffff;
  border-width: 1px;
  border-style: solid;
  border-radius: 2px;
}

.window .title {
  padding: 1px 2px 1px 2px;
  font-size: 16px;
  color: #000;
  border-color: rgb(250, 249, 249);
  border-style: solid;
  font-weight: 600;
  border-width: 0px 0px 1px 0px;
}
</style>
