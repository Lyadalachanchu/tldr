    document.getElementById("myButton").addEventListener("click", getSummary);
    document.getElementById("myButtonAsk").addEventListener("click", askQuestion);

    chrome.storage.session.get(["key"]).then((result) => {
        func(result)
      });

    function func(result) {
        dataDiv = document.getElementById('answer-container');
        dataDiv.innerHTML = result.key;
    }
    
    var xhr = null;
    var user_id = null;
    chrome.storage.session.get(["user"]).then((result) => {
        user_id = result.user
      });

    if(user_id == null){
        user_id = uuidv4()
        console.log(user_id);
        chrome.storage.session.set({ user: user_id }).then(() => {
            console.log(user_id);
        });
    }

    getXmlHttpRequestObject = function () {
        if (!xhr) {
            // Create a new XMLHttpRequest object 
            xhr = new XMLHttpRequest();
        }
        return xhr;
    };

    function uuidv4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });
    }

    function sendDataCallback() {
        // Check response is ready or not
        if (xhr.readyState == 4 && xhr.status == 201) {
            console.log("Data received!");
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
    function getSummary() {
        console.log("Get users...");
        dataDiv = document.getElementById('result-container');
        dataDiv.innerHTML = "thinking...";
        dataToSend = ""
        chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
            dataToSend = tabs[0].url;
            xhr = getXmlHttpRequestObject();
            xhr.onreadystatechange = sendDataCallback;
            // asynchronous requests
            xhr.open("POST", "http://tldr.pythonanywhere.com/summary", true);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            // Send the request over the network
            xhr.send(JSON.stringify({"data": dataToSend, "id": user_id}));
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
        console.log(user_id)
        xhr.send(JSON.stringify({"data": dataToSend, "id": user_id}));
    }