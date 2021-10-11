import axios from 'axios';
import qs from 'qs'
// import GlobalConfig from './global-config';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

const devApiUrl = 'http://baselineb.s20.hkustvis.org'; // for local testing

const GET_REQUEST = 'get';
const POST_REQUEST = 'post';

function request(url, params, type, callback) {
    console.log(callback)
    let config = {
      headers:{
        // 'Content-Type':'application/x-www-form-urlencoded'
      }
    }
    if (type === GET_REQUEST) {
      for(let key in config){
        params[key] = config[key]
      }
      axios.get(url, params).then((response) => {
        if (response.status === 200) {
          callback(response);
        } else {
          console.error(response);
        }
      }).catch((error) => {
        console.error(error);
      });
    } else if (type === POST_REQUEST) {
      axios.post(url, params, config).then((response) => {
        if (response.status === 200) {
          callback(response);
        } else {
          console.error(response);
        }
      }).catch((error) => {
        console.log(error);
      });
    }
  }

function getLoginData(userName, password, callback) {
    const url = `${devApiUrl}/auth/login`;
    // const params = { userName: userName, password: password };
    const params = { userName, password };
    request(url, params, POST_REQUEST, callback);
}

function uploadInput(input, callback) {
    const url = `${devApiUrl}/uploadInput`;
    var params = { input };
    console.log(url, params);
    request(url, params, POST_REQUEST, callback);
}

// function uploadInput(input, callback) {
//   const url = `${devApiUrl}/uploadInput`;
//   var params = { input };
//   console.log(url, params);
//   request(url, params, GET_REQUEST, callback);
// }

export default {
    getLoginData,
    uploadInput,
};

