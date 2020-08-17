// import GlobalConfig from './global-config';

let instance = null;
class Service {
  constructor() {
    if (!instance) {
      instance = this;
    }

    this.counter = 0;
    this.ex_order = 0;
    this.examples = [];
    //this.inputdata = [];
    

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
