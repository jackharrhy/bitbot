var zerorpc = require("zerorpc");
var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

var express = require("express");
var app = express();

var morgan = require("morgan")
app.use(morgan("combined"));

app.use(express.static(__dirname + "/static"));

app.set("view engine", "pug");
app.engine("pug", require("pug").__express);

app.get("/", function(req, res) {
	res.render("index");
});

app.get("/mobile", function(req, res) {
	res.render("mobile", {
		cameraStatic: "http://192.168.1.51:81/?action=static"
	});
});

var io = require("socket.io").listen(app.listen(1337));

io.on("connection", function(socket) {

	socket.on("update", function(servos, motors, outputs) {
		client.invoke("update", String([servos, motors, outputs]));
	});

});


console.log("nodeServer @ 127.0.0.1:1337");
