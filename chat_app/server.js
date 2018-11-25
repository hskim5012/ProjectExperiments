// require is similar to import in Python
// express is a framework that we will import.
var express    = require('express'),
    // app is going to be how we use express to add routes, find templates, etc.
    app        = express(),
    // path lets us easily combine variables and string to form a file path
    path       = require('path');
    // port       = 8000;
var dateFormat = require('dateformat');
var session = require('express-session');
// app.use(session({
//   secret: 'noneofyourdamnbusiness',
//   resave: false,
//   saveUninitialized: true,
//   cookie: { maxAge: 60000 }
// }));

var app = require('express')(),
  server  = require("http").createServer(app),
  io = require("socket.io")(server),
  session = require("express-session")({
    secret: "my-secret",
    resave: true,
    saveUninitialized: true
  }),
  sharedsession = require("express-socket.io-session");

// var handshake = require('socket.io-handshake');
server.listen(1337);
app.use(session);
io.use(sharedsession(session));
var storage = [];
io.on('connection', function (socket) { //2
  // io.use(handshake(config.session));

  console.log(socket.id);
    socket.emit('greeting', { msg: 'Greetings, from server Node, brought to you by Sockets! -Server'}); //3
    socket.on('thankyou', function (data) { //7
        console.log(data.msg); //8 (note: this log will be on your server's terminal)
    });
    socket.on('user_name', function (data) { //7
        console.log(data);
        socket.handshake.session.name = data.name;
        socket.handshake.session.save();
        console.log(socket.handshake.session.name);
        socket.broadcast.emit('new_user', {msg: `${data.name} has joined the Hootenanny`});
        socket.emit('chat_history', {storage: storage, msg: `${data.name} has joined the Hootenanny`});
    });
    socket.on('send', function (data) { //7
      var now = new Date();
      date = dateFormat(now);
      msg = data.msg

      storage.push(`<p><span class='text-danger'>${date} - ${socket.handshake.session.name}</span>: ${msg}</p>`);

      socket.broadcast.emit('send_all', {msg: msg, name: socket.handshake.session.name, color: 'text-danger', date: date});
      socket.emit('send_all', {msg: msg, name: socket.handshake.session.name, color: 'text-primary', date: date});
      socket.emit('clear_message_box');
    });
    socket.on('green_click', function () { //7
      color = 'set_green'
      io.emit('set_green');
    });

});


// Tell express where our static files are
app.use(express.static(path.join(__dirname, 'static')));

// Tell express where our views are
app.set(path.join('views', __dirname, 'views'));

// Now lets set the view engine itself so that express knows that we are using
// ejs as opposed to another templating engine like jade
app.set('view engine', 'ejs');

// We create this file, it contains all of our routes. Think urls.py in Django
// and routes.rb in ruby.
require('./config/routes.js')(app);

// app.listen(port, function() {
//     console.log(`listening on port ${port}`);
// })
