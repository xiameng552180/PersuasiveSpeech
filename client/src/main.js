// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
// import VueMaterial from "vue-material";
import Vue from "vue";
// import VueToggles from 'vue-toggles';
import App from "./app";
import $ from 'jquery';


// import { BootstrapVue } from "bootstrap-vue";
// Vue.use(BootstrapVue);

/* eslint-disable no-new */
new Vue({
  el: "#app" /* To match the corresponding id in index.html*/,
  template: "<App/>",
  components: { App },
});
