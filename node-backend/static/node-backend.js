"use strict";

function randInt(min, max) {
	return Math.floor(Math.random() * max) + min;
}

var button = [0,0,0,0,0,0,0,0,0,0,0];
var axis = [0,0,0];

var socket = io();
socket.on('button', function(data) { button[data.number] = data.value; });
socket.on('axis', function(data) { axis[data.number] = data.value / 32767; });

var usingJS = false;
function iRect(color, x,y, w,h) {
	i.fillStyle = color;
	i.fillRect(x,y,w,h);
}

var iCanvas = document.getElementById('iCanvas');
var i = iCanvas.getContext('2d');
iCanvas.width  = 300;
iCanvas.height = 300;

var frame = -1;
function loop() {
	frame++;

	// Background
	iRect('#feffef',0,0,iCanvas.width,iCanvas.height);

	if(usingJS) {
		// Main Axis Dot
		iRect('#56848d',
						axis[0] * (iCanvas.width - 35)/2 + iCanvas.width/2 - 5/2,
						axis[1] * (iCanvas.width - 35)/2 + iCanvas.width/2 - 5/2,
						9,
						9);

		// Secondary Axis Backdrop
		iRect('#446880',
					iCanvas.width - 10,
					0,
					10,iCanvas.height);

		// Secondary Axis
		iRect('#87bed9',
					iCanvas.width - 10,
					iCanvas.height / 2,
					10,
					axis[2] * iCanvas.height/2);

		// Buttons
		for(var key in button) {
			if(button[key] === 1) {
				iRect('#87bed9',
							key * (iCanvas.width - 10)/button.length,
							iCanvas.height - 10,
							(iCanvas.width - 10)/button.length,15);
			} else {
				iRect('#446890',
							key * (iCanvas.width - 10)/button.length,
							iCanvas.height - 5,
							(iCanvas.width - 10)/button.length,15);
			}
		}
	} else {
		for(var key in button) {
			iRect('#446890',key * iCanvas.width / button.length,0,(iCanvas.width - 10)/button.length,(iCanvas.width - 10)/button.length);
		}
	}

	requestAnimationFrame(loop);
}
loop();

function slowLoop() {
	socket.emit('client-update', { axis: axis, button: button });
	setTimeout(slowLoop, 100);
}
slowLoop();
