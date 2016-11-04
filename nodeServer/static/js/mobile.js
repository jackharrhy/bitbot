var socket = io();

var servoRange = document.getElementById('servoRange');
var motorRange = document.getElementById('motorRange');

var delay = 50;
var oldPacket = '';

function update() {
	var servoVal = parseInt(servoRange.value);
	var motorVal = parseInt(motorRange.value);

	if(motorVal > 140) {
		motorVal -= 140;
	}
	else if(motorVal < 100) {
		motorVal -= 100;
	}
	else {
		motorVal = 0;
	}

	motorVal *= -1;

	// TODO Servo logic

	var servos = [
		servoVal,0,0,0,0,0,0,0
	];
	var motors = [
		motorVal, motorVal
	];
	var outputs = [
		false,false,false,false,false,false,false,false
	];

	var packet = String([servos, motors, outputs]);

	if(packet !== oldPacket) {
		socket.emit('update', packet);
	}

	oldPacket = packet;

	setTimeout(update, delay);
}
update();

cameraDelay = 1000/25;
function cameraUpdate() {
	document.getElementById('cameraFeed').src = "feed.jpg#" + new Date().getTime();

	setTimeout(cameraUpdate, cameraDelay);
}
cameraUpdate();

