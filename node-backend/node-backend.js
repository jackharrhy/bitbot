var request = require('request');

var express = require('express');
var app = express();

var joystick = new (require('joystick'))(0, 100, 10);
var button = [0,0,0,0,0,0,0,0,0,0,0];
joystick.on('button', function(rawButton) {
	io.sockets.emit('button', 
	button[rawButton.number] = rawButton.value;
});
var axis = [0,0,0];
joystick.on('axis', function(rawAxis) {
	axis[rawAxis.number] = rawAxis.value / 32767;
});

app.use(express.static(__dirname + '/static'));

app.set('views', __dirname + '/tpl');
app.set('view engine', 'jade');
app.engine('jade', require('jade').__express);

app.get('/', function(req, res){
	res.render('index');
});

var io = require('socket.io').listen(app.listen(80));

var canRequest = true;
function url(curAxis, axisValue) {
	console.log(curAxis, axisValue);
	if(canRequest) {
		request('http://localhost:1337/'+curAxis+'/'+axisValue,
						function(e,r,b) {
							canRequest = true;			 
						});
	}
	canRequest = false;
}

var urlSwitch = false;
function updateAPI() {
	urlSwitch = !urlSwitch;

	if(urlSwitch) {
		if(axis[1] < -0.01) {
			url(1, axis[1]);
		} else if(axis[1] > 0.01) {
			url(1, axis[1]);
		}
	}

	if(axis[0] < -0.01) {
		url(0, axis[0]);
	} else if(axis[0] > 0.01) {
		url(0, axis[0]);
	}

	setTimeout(updateAPI, 100);

	//console.log(axis, button);
}
updateAPI();

io.sockets.on('connection', function (socket) {
	socket.on('something', function(data) {
		//
	});
});

console.log("============================");
console.log("Web Interface @ 127.0.0.1:80");
