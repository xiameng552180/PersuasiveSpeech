import axios from 'axios';
import qs from 'qs'
// import GlobalConfig from './global-config';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

const devApiUrl = 'http://127.0.0.1:5000/api'; // for local testing

const GET_REQUEST = 'get';
const POST_REQUEST = 'post';

function request(url, params, type, callback) {
    let func;
    if (type === GET_REQUEST) {
      func = axios.get;
    } else if (type === POST_REQUEST) {
      func = axios.post;
    }
  
    func(url, params)
      .then((response) => {
        if (response.status === 200) {
          callback(response);
        } else {
          console.error(response);
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }

function getLoginData(userName, password, callback) {
    const url = `${devApiUrl}/auth/login`;
    // const params = { userName: userName, password: password };
    const params = { userName, password };
    request(url, params, POST_REQUEST, callback);
}

function uploadInput(inputContent, callback) {
    const url = `${devApiUrl}/uploadInput`;
    var params = { inputContent };
    console.log(url, params);
    request(url, params, POST_REQUEST, callback);
}

export default {
    getLoginData,
    uploadInput,
};

