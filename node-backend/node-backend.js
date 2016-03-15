console.log("\nJack, David, & Tyler's Robot\n");

var jayson = require('jayson');

var client = jayson.client.http({
	port: 1337
});

var express = require('express');
var app = express();

var button = [0,0,0,0,0,0,0,0,0,0,0];
var axis = [0,0,0];
var arrow = [false,false,false,false];

var joystick = new (require('joystick'))(0, 500, 10);
if(joystick) {
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
function updateAPI(err, res) {
	if(err) throw err;

	if(res) {
		console.log(res.result);
	}

	var packet = [];
	packet[0] = axis;
	packet[1] = button;
	packet[2] = arrow;

	client.request(
		'update',
		packet,
		updateAPI
	);
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
