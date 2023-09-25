"use strict";
// After creating package.json, install modules:
//   $ npm install
//
// Launch server with:
//   $ node main_server.js
var PORT_NUMBER = 8088;

var http = require('http');
var fs   = require('fs');
var path = require('path');
var mime = require('mime');
var socketIo = require('socket.io'); // Import the socket.io module

/* 
 * Create the static web server
 */
var server = http.createServer(function(request, response) {
  var filePath = false;
  
  if (request.url == '/') {
    filePath = 'public/index.html';
  } else {
    filePath = 'public' + request.url;
  }
  
  var absPath = './' + filePath;

  serveStatic(response, absPath);
});

server.listen(PORT_NUMBER, function() {
  console.log("Backend debug - server listening on port " + PORT_NUMBER);
});

function serveStatic(response, absPath) {
  fs.exists(absPath, function(exists) {
    if (exists) {
      fs.readFile(absPath, function(err, data) {
        if (err) {
          send404(response);
        } else {
          sendFile(response, absPath, data);
        }
      });
    } else {
      send404(response);
    }
  });
}

function send404(response) {
	
  response.writeHead(404, {'Content-Type': 'text/plain'});
  response.write('Error 404: resource not found.');
  response.end();
}

function sendFile(response, filePath, fileContents) {
  var contentType = mime.getType(path.basename(filePath));

  response.writeHead(200, {
    "Content-Type": contentType || "application/octet-stream"
  });
  response.end(fileContents);
}


/*
 * Create the Web server to listen for the WebSocket
 */
var io = new socketIo.Server(server, {
  // Set log level here (0 for debug, 1 for info, 2 for warning, 3 for error)
  logger: {
    level: 1,
  },
});

var webServer = require('./lib/server_udp')(io); // Pass the WebSocket server instance to UDP server



