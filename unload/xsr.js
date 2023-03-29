    document.getElementById("myButton").addEventListener("click", getUsers);
    document.getElementById("myButtonAsk").addEventListener("click", askQuestion);

    chrome.storage.session.get(["key"]).then((result) => {
        func(result)
      });

    function func(result) {
        dataDiv = document.getElementById('answer-container');
        dataDiv.innerHTML = result.key;
    }
    
    var xhr = null;

    getXmlHttpRequestObject = function () {
        if (!xhr) {
            // Create a new XMLHttpRequest object 
            xhr = new XMLHttpRequest();
        }
        return xhr;
    };

    function sendDataCallback() {
        // Check response is ready or not
        if (xhr.readyState == 4 && xhr.status == 201) {
            console.log("User data received!");
            dataDiv = document.getElementById('result-container');
            // Set current data text
            dataDiv.innerHTML = xhr.responseText;
            dataDiv.innerHTML = xhr.responseText;
        }
    }
    function sendDataCallbackAsk() {
        // Check response is ready or not
        if (xhr.readyState == 4 && xhr.status == 201) {
            console.log("answer received!");
            dataDiv = document.getElementById('answer-container');
            // Set current data text
            chrome.storage.session.set({ key: xhr.responseText }).then(() => {
                console.log("Value is set");
              });
            //   chrome.storage.session.get(["key"]).then((result) => {
            //     dataDiv.innerHTML = result.key;
            //   });
            dataDiv.innerHTML = xhr.responseText;
        }
    }
    function getUsers() {
        console.log("Get users...");
        dataDiv = document.getElementById('result-container');
        dataDiv.innerHTML = "thinking...";
        dataToSend = ""
        chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
            dataToSend = tabs[0].url;
            xhr = getXmlHttpRequestObject();
            xhr.onreadystatechange = sendDataCallback;
            // asynchronous requests
            xhr.open("POST", "http://tldr.pythonanywhere.com/users", true);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            // Send the request over the network
            xhr.send(JSON.stringify({"data": dataToSend}));
        });
    }
    function askQuestion() {
        console.log("Get users...");
        dataDiv = document.getElementById('answer-container');
        dataDiv.innerHTML = "thinking...";
        dataToSend = document.getElementById('data-input').value
        xhr = getXmlHttpRequestObject();
        xhr.onreadystatechange = sendDataCallbackAsk;
        // asynchronous requests
        xhr.open("POST", "http://tldr.pythonanywhere.com/ask", true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        // Send the request over the network
        xhr.send(JSON.stringify({"data": dataToSend}));
    }