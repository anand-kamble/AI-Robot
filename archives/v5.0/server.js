const express = require('express')
const app = express()
const server = require('http').Server(app)
const io = require('socket.io')(server)
const { v4: uuidV4 } = require('uuid')

app.set('view engine', 'ejs')
app.use(express.static('static'))

app.get('/',(req,res)=>{
    res.sendFile(__dirname + '/static/index.html')
})

app.get('/socket.io.min.js',(req,res)=>{
    res.sendFile(__dirname + '/static/socket.io.min.js')
})

app.get('/jquery-3.6.0.min.js',(req,res)=>{
    res.sendFile(__dirname + '/static/jquery-3.6.0.min.js')
})

app.get('/peerjs.min.js',(req,res)=>{
    res.sendFile(__dirname + '/static/peerjs.min.js')
})

app.get('/Robot top view for web.png',(req,res)=>{
    res.sendFile(__dirname + '/static/Robot top view for web.png')
})

app.get('/RobotUI',(req,res)=>{
    res.sendFile(__dirname + '/static/call.html')
})

io.on('connection',(s)=>{
    console.log('Socket Connected')
})


server.listen(3000)