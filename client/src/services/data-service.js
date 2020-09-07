// import GlobalConfig from './global-config';

let instance = null;
class Service {
  constructor() {
    if (!instance) {
      instance = this;
    }

    this.counter = 0;
    this.ex_id = "";
    this.examples = [];
    //this.inputdata = [];
    this.selectIDarray = [];
    this.selectIDIndex = [];
    this.selectTopic = '';
    this.selectTopicNum = '';
    this.examplesum = {
      logos: 0,
      pathos: 0,
      ethos: 0,
      evidence: 0,
      relevance: 0,
      is_claim: 0,
      eloquence: 0,
    };
    this.linkData= [],
    this.nodeData= [],
    this.inputLabels = {
      "input": [
        { feature: "logos", label: 0 },
        { feature: "pathos", label: 0 },
        { feature: "ethos", label: 0 },
        { feature: "evidence", label: 0 },
        { feature: "relevance", label: 0 },
        { feature: "is_claim", label: 0 },
        { feature: "eloquence", label: 0 }
      ]};
    //this.inputRelationship = [];

    return instance;
  }

  getServerVideoUrl() {
    return this.serverVideoUrl;
  }

  setUserId(data) {
    this.userId = data;
  }

  getUserId() {
    return this.userId;
  }
}

const DataService = new Service();
export default DataService;
