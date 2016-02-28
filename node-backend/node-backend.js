var request = require('request');

var express = require('express');
var app = express();

/*
var joystick = new (require('joystick'))(0, 100, 10);

joystick.on('button', function(button) {
	io.emit('button', button);
});
joystick.on('axis', function(axis) {
	io.emit('axis', axis);
});
*/

app.use(express.static(__dirname + '/static'));

app.set('views', __dirname + '/tpl');
app.set('view engine', 'jade');
app.engine('jade', require('jade').__express);

app.get('/', function(req, res){
	res.render('index');
});

app.get('/otto', function(req, res){
	res.render('otto');
});

var io = require('socket.io').listen(app.listen(80));

var canRequest = true;
function url(d,t,s) {
	canRequest = false;
	request('http://localhost:1337/'+d+'/'+String(t)+'/'+String(s),
					function(e,r,b) {
						canRequest = true;			 
					});
}

function parseClientUpdate(axis, button) {
	if(axis[0] > 0.25) {
		url('f', 0.25, axis[0]);
	} else if(axis[0] < -0.25) {
		
	}
}

io.sockets.on('connection', function (socket) {
	socket.on('client-update', function(data) {
		parseClientUpdate(data.axis, data.button);
	});
});

console.log("\n\
\
            Jack'n' David 'n' Tyler's\n\
\
      .-.              .               \n\
      (_) )-.        /           /   \n\
      /   \\  .-._. /-.  .-._.---/--- \n\
     /     )(   ) /   )(   )   /     \n\
  .-/ ----'  `-'.'`--'`-`-'   /      \n\
 (_/     `-._)   \n\
\n\
Web Interface @ ::80\n\
--------------------\n\
\
");
