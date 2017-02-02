var verbose = true;
var screens = [];

var main = function() {
	// this function is for use in --> $(document).ready(main)
	// TODO: remove all these calls for all the spawn functions, they only exist right now for dev purposes
	spawnHomeScreen();
	spawnMusicScreen();
	spawnCameraScreen();
};

var spawnHomeScreen = function() {
	/*
	Create the default startup screen
	*/
	var body = document.body;
	var homescreen = document.createElement("div");
	homescreen.id = "homescreen";
	homescreen.className = "screen";
	var title = document.createElement("span");
	title.innerHTML = "HOMESCREEN";
	homescreen.appendChild(title);
	body.appendChild(homescreen);
	screens += ["homescreen"];
};

var spawnMusicScreen = function() {
	/*
	Create the music screen
	*/
	var body = document.body;
	var musicscreen = document.createElement("div");
	musicscreen.id = "musicscreen";
	musicscreen.className = "screen";
	var title = document.createElement("span");
	title.innerHTML = "MUSICSCREEN";
	musicscreen.appendChild(title);
	body.appendChild(musicscreen);
	screens += ["musicscreen"];
};

var spawnCameraScreen = function() {
	/*
	Create the camera screen
	*/
	var body = document.body;
	var camerascreen = document.createElement("div");
	camerascreen.id = "camerascreen";
	camerascreen.className = "screen";
	var title = document.createElement("span");
	title.innerHTML = "CAMERASCREEN";
	camerascreen.appendChild(title);
	body.appendChild(camerascreen);
	screens += ["camerascreen"];
};

var drawTelemetry = function(data) {
	/*
	Update the center console based on new data
	*/
	console.log("received telemetry");
	console.log(data);
};

var spawnNavbar = function(tabArray) {
	/*
	Create a navbar with N items
	*/
};

/*================================================
	Websocket IO Framework
================================================*/
var ws = new WebSocket("ws://localhost:1234/ws");

ws.onopen = function() {
	/*
	WebSocket Open Event
	*/

};

ws.onclose = function(ev) {
	/*
	WebSocket Close Event
	*/

};

ws.onerror = function(ev) {
	/*
	WebSocket Error Event
	*/

};

ws.onmessage = function(ev) {
	/*
	WebSocket Receive Message Event
	*/

	var jsonraw = JSON.parse(ev.data);

	for (var key in jsonraw) {
		value = jsonraw[key];
		switch(key) {
			// case "spawnHomeScreen":
			// 	if (verbose) { console.log("spawnHomeScreen"); }
			// 	spawnHomeScreen();
			// 	break;
			// case "spawnMusicScreen":
			// 	if (verbose) { console.log("spawnMusicScreen"); }
			// 	spawnMusicScreen();
			// 	break;
			// case "spawnCameraScreen":
			// 	if (verbose) { console.log("spawnCameraScreen"); }
			// 	spawnCameraScreen();
			// 	break;
			case "drawTelemetry":
				if (verbose) { console.log("drawTelemetry"); }
				drawTelemetry(value[0]);
				break;
		}
	}
};

sendmsg = function(key, value) {
	/*
	WebSocket Send Message
	*/
	var fleeb = {};
	fleeb[key] = value;
	ws.send(JSON.stringify(fleeb));
};


$(document).ready(main);