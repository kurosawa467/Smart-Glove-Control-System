message_queue = '';

current_color = 7;
current_brightness = 100;

// Called after form input is processed
function startConnect() {
    // Generate a random client ID
    clientID = "clientID-" + parseInt(Math.random() * 100);

    // Fetch the hostname/IP address and port number from the form
    host = document.getElementById("host").value;
    port = document.getElementById("port").value;

    // Print output for the user in the messages div
    message_queue += '<span>Connecting to: ' + host + ' on port: ' + port + '</span><br/>';
    message_queue += '<span>Using the following client value: ' + clientID + '</span><br/>';
    updateMessage();

    // Initialize new Paho client connection
    client = new Paho.MQTT.Client(host, Number(port), clientID);

    // Set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // Connect the client, if successful, call onConnect function
    client.connect({
        onSuccess: onConnect,
        onFailure: onFailure,
        userName: "mosquitto",
        password: "mosquitto",

    });
}

// Called when the client connects
function onConnect() {
    // Fetch the MQTT topic from the form
    topic = document.getElementById("topic").value;

    // Print output for the user in the messages div
    message_queue += '<span>Subscribing to: ' + topic + '</span><br/>';
    updateMessage();

    // Subscribe to the requested topic
    client.subscribe(topic);
    setImagePanel();
}

function onFailure(){
    console.log('Failed');

}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    message_queue += '<span>ERROR: Connection lost</span><br/>';
    if (responseObject.errorCode !== 0) {
        message_queue += '<span>ERROR: ' + + responseObject.errorMessage + '</span><br/>';
    }
    updateMessage();
    resetForm();
}

// Called when a message arrives
function onMessageArrived(message) {
    console.log("onMessageArrived: " + message.payloadString);
    message_queue += '<span>Message: ' + message.payloadString + ' = ' + decodeMessage(message.payloadString) + '</span><br/>';
    apply(message.payloadString);
    console.log(current_color)
    console.log(current_brightness)
    setImagePanel();
    updateMessage();
}

// Called when the disconnection button is pressed
function startDisconnect() {
    client.disconnect();
    message_queue += '<span>Disconnected</span><br/>';
    updateMessage();
    resetForm();
}

function updateMessage(){
    document.getElementById("messages").innerHTML = '<span>' + message_queue + '</span>';
}

function resetForm(){
    document.getElementById("connection-form").innerHTML = "<h1>Subscriber</h1>" +
        "        <form id=\"connection-information-form\">" +
        "            <b>Hostname or IP Address:</b>" +
        "            <input id=\"host\" type=\"text\" name=\"host\" value=\"192.168.178.27\"><br>" +
        "            <b>Port:</b>" +
        "            <input id=\"port\" type=\"text\" name=\"port\" value=\"1884\"><br>" +
        "            <b>Topic:</b>" +
        "            <input id=\"topic\" type=\"text\" name=\"topic\" value=\"JS_APP\"><br><br>" +
        "            <input type=\"button\" onclick=\"startConnect()\" value=\"Connect\">" +
        "        </form>" +
        "        <div id=\"messages\"></div>";
    document.getElementById("image-panel").innerHTML = "<span> </span>";
    updateMessage();
}
function setImagePanel(){
    document.getElementById("connection-form").innerHTML = "<span> </span>";
    document.getElementById("image-panel").innerHTML = '<div id="panel" style="background-color: '+getColor(current_color,current_brightness)+'"><img src="lightBuld.png" height="550px "></div><br>'+//'<div id="panel" style="background-color: ' + getColor(current_color,current_brightness)+ '"><img src="lightBuld.png" height="550px "></div><br>' +
        '<input type="button" onClick="startDisconnect()" value="Disconnect"><br>' +
        '<div id="messages"></div>';
}

function decodeMessage(c){
    switch(c) {
        case '1':
            return 'next color';
        case '2':
            return 'previous color';
        case '3':
            return 'lower brightness';
        case '4':
            return 'higher brightness';
        default:
            return 'Error worng command!!!';
    }
}

function apply(c){
    switch(c) {
        case '1':
            current_color = (current_color +1)%8;

            break;
        case '2':
            current_color = (current_color -1);
            if (current_color<0)
                current_color += 8;
            break;
        case '3':
            current_brightness = (current_brightness +10)%110;
            break;
        case '4':
            current_brightness = (current_brightness -10);
            if (current_brightness<0)
                current_brightness += 100;
            break;
        default:
            break;
    }
}

function getColor(color,brightness) {
    blue = color % 2 == 1 ? 255 : 0;
    color = color >> 1;
    green = color % 2 == 1 ? 255 : 0;
    color = color >> 1;
    red = color % 2 == 1 ? 255 : 0;
    console.log('red:' + red + ", green:" + green + ', blue:' + blue);
    return "rgba(" + red + ", " + green + ", " + blue + "," + brightness / 100 + ")";
}
