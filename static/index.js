$(document).ready(function () {
  var TYPE_IMAGE = "image";
  var TYPE_JETSON_LOG = "jetson_log";

  var HOST = location.hostname;

  let socket = new WebSocket("ws://" + HOST + ":12500");

  socket.onopen = function (e) {
    console.log("[open] Connection established");
    console.log("Sending to server");
  };

  socket.onmessage = function (event) {
    console.log(`[message] Data received from server: ${event.data}`);
    let log_data = JSON.parse(event.data);
    if (log_data.type == TYPE_IMAGE) {
      $(".img-log-container").prepend(
        "<img src=" +
          "http://" + HOST + ":8080/images/" +
          log_data.uri +
          "><p>" +
          log_data.uri +
          "</p>"
      );
    } else if (log_data.type == TYPE_JETSON_LOG) {
      let classes = ""

      if(log_data.level=="ERROR"){
        classes = '"log-error"'
      }
      $(".jetson-log-table-body").prepend(
        '<tr class=' + classes +  '><th scope="row">' +
          log_data.asctime +
          "</th><td>" +
          log_data.level +
          "</td><td>" +
          log_data.function +
          "</td><td>" +
          log_data.message +
          "</td></tr>"
      );
    } else {
      console.log("Unknown type: " + log_data.type);
    }
  };

  socket.onclose = function (event) {
    if (event.wasClean) {
      alert(
        `[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`
      );
    } else {
      alert("[close] Connection died");
    }
  };

  socket.onerror = function (error) {
    alert(`[error] ${error.message}`);
  };
});
