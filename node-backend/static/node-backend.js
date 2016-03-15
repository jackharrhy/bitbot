var axis = [0,0,0];
var button = [0,0,0,0,0,0,0,0,0,0,0];
var arrow = [false,false,false,false];

var socket = io();
socket.on('button', function(data) { button[data.number] = data.value; });
socket.on('axis', function(data) { axis[data.number] = data.value / 32767; });

var canvas = document.getElementById('canvas');
var c = canvas.getContext('2d');
c.font = '20px Arial';

// 15801
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

var frame = -1;
function loop() {
	canvas.width  = window.innerWidth;
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
			 15);

	rect(colors.specialBackdrop,
			 0,
			 canvas.height - (canvas.height / 10) * 1.25,
			 canvas.width,
			 canvas.height/40);

	rect(colors.special,
			 canvas.width/2,
			 canvas.height - (canvas.height / 10) * 1.25,
			 (canvas.width/2) * axis[2],
			 canvas.height/40);

	var curColor = colors.lit;
	if(!arrow[0]) curColor = colors.unlit;
	rect(curColor,
			 canvas.width / 2 - canvas.width / 40,
			 canvas.height - ((canvas.height / 4.5) + (canvas.height/30)),
			 canvas.width / 20,
			 canvas.height / 20);
	curColor = colors.lit;
	if(!arrow[1]) curColor = colors.unlit;
	rect(curColor,
			 canvas.width / 2 - canvas.width / 40,
			 canvas.height - ((canvas.height / 4.5) - (canvas.height/40)),
			 canvas.width / 20,
			 canvas.height / 20);

	curColor = colors.lit;
	if(!arrow[2]) curColor = colors.unlit;
	rect(curColor,
			 canvas.width / 2 - ((canvas.width / 40) + (canvas.height/13)),
			 canvas.height - ((canvas.height / 4.5) - (canvas.height/40)),
			 canvas.width / 20,
			 canvas.height / 20);

	curColor = colors.lit;
	if(!arrow[3]) curColor = colors.unlit;
	rect(curColor,
			 canvas.width / 2 - ((canvas.width / 40) - (canvas.height/13)),
			 canvas.height - ((canvas.height / 4.5) - (canvas.height/40)),
			 canvas.width / 20,
			 canvas.height / 20);


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

Mousetrap.bind({
	'1': function() { button[0]  = 1 },
	'2': function() { button[1]  = 1 },
	'3': function() { button[2]  = 1 },
	'4': function() { button[3]  = 1 },
	'5': function() { button[4]  = 1 },
	'6': function() { button[5]  = 1 },
	'7': function() { button[6]  = 1 },
	'8': function() { button[7]  = 1 },
	'9': function() { button[8]  = 1 },
	'0': function() { button[9]  = 1 },
	'-': function() { button[10] = 1 },

	'up':    function() { arrow[0] = true },
	'down':  function() { arrow[1] = true },
	'left':  function() { arrow[2] = true },
	'right': function() { arrow[3] = true }

}, 'keydown');

Mousetrap.bind({
	'1': function() { button[0]  = 0 },
	'2': function() { button[1]  = 0 },
	'3': function() { button[2]  = 0 },
	'4': function() { button[3]  = 0 },
	'5': function() { button[4]  = 0 },
	'6': function() { button[5]  = 0 },
	'7': function() { button[6]  = 0 },
	'8': function() { button[7]  = 0 },
	'9': function() { button[8]  = 0 },
	'0': function() { button[9]  = 0 },
	'-': function() { button[10] = 0 },

	'up':    function() { arrow[0] = false },
	'down':  function() { arrow[1] = false },
	'left':  function() { arrow[2] = false },
	'right': function() { arrow[3] = false }
}, 'keyup');

function updateServer() {
	socket.emit('clientControl', {
		arrow: arrow,
		button: button
	});

	setTimeout(updateServer, 50);
}
updateServer();
