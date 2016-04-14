var axis = [0,0,1];
var button = [0,0,0,0,0,0,0,0,0,0,0];

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
	canvas.width  = window.innerWidth * 0.75;
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

	mode = 'Nothing';

	if(button[1]) {
		mode = 'Vertical';
		setInfo('M2 0: ' + String(Math.ceil(axis[1] * -100)), 'motor20vel');
		setInfo('M2 1: ' + String(Math.ceil(axis[1] * -100)), 'motor21vel');
	}	else if(button[2]){
		mode = 'Horizontal';
	} else if(button[3]) {
		mode = 'T-Left';
	} else if(button[4]) {
		mode = 'T-Right';
	} else {
		setInfo('M1 0: 0', 'motor10vel');
		setInfo('M1 1: 0', 'motor11vel');
		setInfo('M2 0: 0', 'motor20vel');
		setInfo('M2 1: 0', 'motor21vel');
	}
	
	setInfo('Mode: ' + mode, 'mode');

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
