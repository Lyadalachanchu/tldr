    document.getElementById("myButton").addEventListener("click", getUsers);
    
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
    function getUsers() {
        console.log("Get users...");
        dataToSend = ""
        chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
            dataToSend = tabs[0].url;
            xhr = getXmlHttpRequestObject();
            xhr.onreadystatechange = sendDataCallback;
            // asynchronous requests
            xhr.open("POST", "http://localhost:6969/users", true);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            // Send the request over the network
            xhr.send(JSON.stringify({"data": dataToSend}));
        });
    }