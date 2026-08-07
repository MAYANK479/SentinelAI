const SockJS = require('sockjs-client');
try {
  new SockJS('https://sentinel-backend-d1qo.onrender.com/ws');
  console.log("SUCCESS");
} catch (e) {
  console.log("CAUGHT", e.message);
}
