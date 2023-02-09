const express = require("express");
const app = express();
const server = require("http").Server(app);
const io = require("socket.io")(server);
const { v4: uuidV4 } = require("uuid");

const filesBasePath = "/UI/";

app.set("view engine", "ejs");
app.use(express.static("static"));

app.get("/", (req, res) => {
  res.sendFile(__dirname + filesBasePath + "index.html");
});

app.get("/socket.io.min.js", (req, res) => {
  res.sendFile(__dirname + filesBasePath + "socket.io.min.js");
});

app.get("/jquery-3.6.0.min.js", (req, res) => {
  res.sendFile(__dirname + filesBasePath + "jquery-3.6.0.min.js");
});

app.get("/peerjs.min.js", (req, res) => {
  res.sendFile(__dirname + filesBasePath + "peerjs.min.js");
});

app.get("/Robot top view for web.png", (req, res) => {
  res.sendFile(__dirname + filesBasePath + "Robot top view for web.png");
});

app.get("/RobotUI", (req, res) => {
  res.sendFile(__dirname + filesBasePath + "call.html");
});

io.on("connection", (s) => {
  console.log("Socket Connected");
});

server.listen(3000);
