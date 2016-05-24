var socket = io();

var servoRange = document.getElementById('servoRange');
var motorRange = document.getElementById('motorRange');

var delay = 50;

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

	socket.emit('update', servos, motors, outputs);

	setTimeout(update, delay);
}
update();

cameraDelay = 1000/10;
function cameraUpdate() {
	document.getElementById('cameraFeed').src = "http://192.168.1.51:81/?action=static#" + new Date().getTime();	

	setTimeout(cameraUpdate, cameraDelay);
}
cameraUpdate();
