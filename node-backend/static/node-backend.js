var axis = [0,0,1]; var button = [0,0,0,0,0,0,0,0,0,0,0];

var socket = io();
socket.on('button', function(data) { button[data.number] = data.value;         });
socket.on('axis',   function(data) { axis[data.number]   = data.value / 32767; });

var canvas = document.getElementById('canvas');
var c = canvas.getContext('2d');

var colors = {
	backdrop: '#86b9d8',
	dot: '#0d8487',
	unlit: '#175563',
	lit: '#65acc7',
	boundBox: 'white',
	specialBackdrop: '#0d8487',
	special: '#65acc7'
};

function rect(color, x,y, w,h) {
	c.fillStyle = color;
	c.strokeRect(x,y,w,h);
	c.fillRect(x,y,w,h);
}

function circ(color, x,y, r) {
	c.beginPath();
	c.arc(x,y, r, 0, 2 * Math.PI);
	c.fillStyle = color;
	c.fill();
}

function setInfo(text, id) {
	document.getElementById(id).innerHTML = text;
}

var mode = 'Nothing';
var frame = -1;

function loop() {
	canvas.width  = window.innerWidth * 0.5;
	canvas.height = window.innerHeight;

	frame++;

	rect(colors.backdrop,0,0,canvas.width,canvas.height);

	rect(colors.boundBox,
			 (-1 * canvas.width/4) + canvas.width/2,
			 (-1 * canvas.height/4) + (canvas.height/2 - canvas.height/30),
			 canvas.width/2,
			 canvas.height/2);

	circ(colors.dot,
			 (axis[0] * canvas.width/4) + canvas.width/2,
			 (axis[1] * canvas.height/4) + (canvas.height/2 - canvas.height/30),
			 canvas.height/40);

	rect(colors.specialBackdrop,
			 0,
			 canvas.height - (canvas.height / 10) * 1.25,
			 canvas.width,
			 canvas.height/40);

	rect(colors.special,
			 0,
			 canvas.height - (canvas.height / 10) * 1.25,
			 (canvas.width/2) * (axis[2] * -1 + 1),
			 canvas.height/40);

	mode = '';

	if(button[0]) {
		mode += 'Arm ';
		setInfo('Servo Pos: ' + String(Math.ceil(axis[1] * -100)), 'servoPos');
	}
	
	if(button[1]) {
		mode += 'Vertical ';
		setInfo('Motor2 0: ' + String(Math.ceil(axis[1] * -100)), 'motor20vel');
		setInfo('Motor2 1: ' + String(Math.ceil(axis[1] * -100)), 'motor21vel');
	}

	if(button[5]) {
		mode += 'Vertical-0 ';
		setInfo('Motor2 0: ' + String(Math.ceil(axis[1] * -100)), 'motor20vel');
	}
	if(button[10]) {
		mode += 'Vertical-1 ';
		setInfo('Motor2 1: ' + String(Math.ceil(axis[1] * -100)), 'motor21vel');
	}
	if(button[6]) {
		mode += 'Horizontal-0 ';
		setInfo('Motor1 0: ' + String(Math.ceil(axis[1] * -100)), 'motor10vel');
	}
	if(button[9]) {
		mode += 'Horizontal-1 ';
		setInfo('Motor1 1: ' + String(Math.ceil(axis[1] * -100)), 'motor11vel');
	}
	
	if(button[2]) {
		mode += 'Horizontal ';
		setInfo('Motor1 0: ' + String(Math.ceil(axis[1] * -100)), 'motor10vel');
		setInfo('Motor1 1: ' + String(Math.ceil(axis[1] * -100)), 'motor11vel');
	}
	
	if(button[3]) {
		mode += 'T-Left ';
		if(axis[0] <= 0) {
			setInfo('Motor1 0: ' + String(Math.ceil(axis[0] * 100)), 'motor10vel');
			setInfo('Motor1 1: ' + String(Math.ceil(axis[0] * -100)), 'motor11vel');
		}
	} else if(!button[4] && !button[2] && !button[6] && !button[9]) {
		setInfo('Motor1 0: 0', 'motor10vel');
		setInfo('Motor1 1: 0', 'motor11vel');
	}

	if(button[4]) {
		mode += 'T-Right';
		if(axis[0] >= 0) {
			setInfo('Motor1 0: ' + String(Math.ceil(axis[0] * 100)), 'motor10vel');
			setInfo('Motor1 1: ' + String(Math.ceil(axis[0] * -100)), 'motor11vel');
		}
	} else if(!button[3] && !button[2] && !button[6] && !button[9]) {
		setInfo('Motor1 0: 0', 'motor10vel');
		setInfo('Motor1 1: 0', 'motor11vel');
	}

	setInfo('Mode(s): ' + mode, 'mode');

	setInfo('x: ' + String(axis[0].toFixed(5)), 'x');
	setInfo('y: ' + String(axis[1].toFixed(5)), 'y');
	setInfo('z: ' + String(axis[2].toFixed(5)), 'z');

	setInfo('Acel: ' + String(Math.ceil(((axis[2] * -1) + 1) * 50)), 'acel');

	for(var i=0; i < button.length; i++) {
		var curColor = colors.lit;
		if(button[i] === 0) curColor = colors.unlit;

		rect(curColor,
         i * canvas.width / button.length,
				 canvas.height - canvas.height / 10,
				 canvas.width / button.length,
				 canvas.height / 10);
	}

	requestAnimationFrame(loop);
}
loop();
