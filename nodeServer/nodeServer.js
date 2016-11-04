var config = require("./config");

var zerorpc = require("zerorpc");
var client = new zerorpc.Client();
client.connect("tcp://"+ config.piIP +":"+ String(config.piPort));

var MjpegProxy = require('mjpeg-proxy').MjpegProxy;

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

app.get('/feed.jpg', new MjpegProxy(config.cameraAddress).proxyRequest);

app.get("/mobile", function(req, res) {
	res.render("mobile");
});

var io = require("socket.io").listen(app.listen(config.port));

io.on("connection", function(socket) {

	socket.on("update", function(packet) {
		client.invoke("update", packet);
	});

});

console.log("nodeServer @ localhost:" + String(config.port));
