console.log("\nJack's \n");

var jayson = require('jayson');

var client = jayson.client.http({
	port: 1337
});

var express = require('express');
var app = express();

var button = [0,0,0,0,0,0,0,0,0,0,0];
var axis = [0,0,0];

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

var io = require('socket.io').listen(app.listen(2424));

function updateAPI(err, res) {
	if(err) console.log(err);

	var packet = [];
	packet[0] = axis;
	packet[1] = button;

	client.request(
		'update',
		packet,
		updateAPI
	);

	try {
		resp = res.result;
		console.log(resp);
	} catch(err) {
		console.log(err);
	}
}
updateAPI(undefined, { result: 'init' });

console.log("[%] Web Interface @ 127.0.0.1:2424");
console.log("-----------------------------------\n");
