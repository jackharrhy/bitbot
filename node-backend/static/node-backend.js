function randInt(min, max) {
	return Math.floor(Math.random() * max) + min;
}

var axis = [0,0,0];
var button = [0,0,0,0,0,0,0,0,0,0,0];

var socket = io();
socket.on('button', function(data) { button[data.number] = data.value; });
socket.on('axis', function(data) { axis[data.number] = data.value / 32767; });

function iRect(color, x,y, w,h) {
	i.fillStyle = color;
	i.fillRect(x,y,w,h);
}

var iCanvas = document.getElementById('iCanvas');
var i = iCanvas.getContext('2d');
i.font = '20px Arial';
iCanvas.width  = window.innerHeight - 10;
iCanvas.height = window.innerHeight - 10;

var frame = -1;

var colors = {
	backdrop: 'white',
	dot: 'black',
	unlit: 'black',
	lit: 'blue',
	ring: 'orange'
};

offset = 50;

function loop() {
	frame++;

	// Background
	iRect(colors.backdrop,0,0,iCanvas.width,iCanvas.height);

	// Main Axis Dot
	iRect(colors.dot,
					axis[0] * (iCanvas.width - offset)/3 + iCanvas.width/2 - 5/2,
					axis[1] * (iCanvas.width - offset)/3 + iCanvas.width/2 - 5/2,
					9,
					9);

	// Secondary Axis Backdrop
	iRect(colors.unlit,
				iCanvas.width - offset,
				0,
				offset,
				iCanvas.height);

	// Secondary Axis
	iRect(colors.lit,
				iCanvas.width - offset,
				iCanvas.height / 2,
				offset,
				axis[2] * iCanvas.height/2);

	// Buttons
	for(var key in button) {
		if(button[key] === 1) {
			iRect(colors.lit,
						key * (iCanvas.width - offset)/button.length,
						iCanvas.height - 30,
						(iCanvas.width - offset)/button.length,
						30);
		} else {
			iRect(colors.unlit,
						key * (iCanvas.width - offset)/button.length,
						iCanvas.height - 30,
						(iCanvas.width - offset)/button.length,
						30);
		}
	}

	requestAnimationFrame(loop);
}
loop();
