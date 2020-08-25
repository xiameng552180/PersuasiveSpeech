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
      concreteness: 0,
      eloquence: 0,
    };

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
