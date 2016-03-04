console.log("Jack, David, & Tyler's Robot\n");

var request = require('request');

var express = require('express');
var app = express();

var button = [0,0,0,0,0,0,0,0,0,0,0];
var axis = [0,0,0];
var arrow = [false,false,false,false];

var joystick = new (require('joystick'))(0, 500, 10);
if(joystick.domain !== null) {
	joystick.on('button', function(rawButton) {
		io.sockets.emit('button', rawButton);
		button[rawButton.number] = rawButton.value;
	});
	joystick.on('axis', function(rawAxis) {
		io.sockets.emit('axis', rawAxis);
		axis[rawAxis.number] = rawAxis.value / 32767;
	});
} else {
	console.log('[!] Joystick failed to init');
}

app.use(express.static(__dirname + '/static'));

app.set('view engine', 'jade');
app.engine('jade', require('jade').__express);

app.get('/', function(req, res) {
	console.log('[|] request to /');
	res.render('index');
});

var io = require('socket.io').listen(app.listen(80));

var canRequest = true;
function url(type, val1, val2) {
	console.log(type, val1, val2);
	if(canRequest) {
		request('http://localhost:1337/'+type+'/'+val1+'/'+val2,
						function() { canRequest = true; });
	}
	canRequest = false;
}

var urlSwitch = false;
function updateAPI() {
	urlSwitch = !urlSwitch;

	if(urlSwitch && axis[1] !== 0) {
		url('axis', 1, axis[1]);
	} else if(axis[0] !== 0) {
		url('axis', 0, axis[0]);
	}

	for(var key in button) {
		if(button[key] !== 0) url('button', key, 0);
		button[key] = 0;
	}

	if(arrow[0]) {
		url('arrow', 0, 0);
	} else if(arrow[1]) {
		url('arrow', 1, 0);
	}

	if(arrow[2]) {
		url('arrow', 2, 0);
	} else if(arrow[3]) {
		url('arrow', 3, 0);
	}

	setTimeout(updateAPI, 100);
}
updateAPI();

io.sockets.on('connection', function (socket) {
	socket.on('clientControl', function(data) {
		arrow = data.arrow;
		for(var key in button) {
			if(data.button[key] !== 0) button[key] = 1;
		}
	});
});

console.log("[%] Web Interface @ 127.0.0.1:80");
console.log("--------------------------------\n");
