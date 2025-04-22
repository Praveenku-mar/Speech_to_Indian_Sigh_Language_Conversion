function startListening() {
  if (!('webkitSpeechRecognition' in window)) {
    alert("Your browser doesn't support speech recognition.");
    return;
  }
  var recognition = new webkitSpeechRecognition();
  recognition.lang = "en-IN";
  recognition.start();

  recognition.onresult = function(event) {
    var speechResult = event.results[0][0].transcript;
    document.getElementById("result").innerText = "You said: " + speechResult;
    sendToServer(speechResult);
  };

  recognition.onerror = function(event) {
    alert("Speech recognition error: " + event.error);
  };
}

function sendToServer(text) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/process_speech", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.onload = function () {
    var response = JSON.parse(this.responseText);
    var outputDiv = document.getElementById("output");
    outputDiv.innerHTML = "";

    if (response.type === "gif") {
      outputDiv.innerHTML = "<h3>Result:</h3><img src='" + response.path + "' width='350'>";
    } else if (response.type === "alphabets") {
      response.paths.forEach(function (img) {
        outputDiv.innerHTML += "<img src='" + img + "' width='70' style='margin:5px'>";
      });
    } else {
      outputDiv.innerHTML = "<p style='color:red'>" + response.message + "</p>";
    }
  };
  xhr.send("text=" + encodeURIComponent(text));
}
