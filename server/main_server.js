'use strict';

const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const fs = require('fs');
const path = require('path');
const mime = require('mime');

const PORT_NUMBER = 8088;

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Endpoint to reload the server
app.post('/reload-server', (req, res) => {
  console.log('Reloading server...');
  // Perform any necessary cleanup or tasks before restarting the server
  // For example, stop any running processes or connections

  // Restart the server
  restartServer(() => {
    console.log('Server restarted successfully.');
    res.status(200).send('Server reload initiated.');
  });
});

// Endpoint to reload static content
app.post('/reload-static', (req, res) => {
  console.log('Reloading static content...');
  // Perform any necessary tasks for reloading static content

  // Respond with success
  res.status(200).send('Static content reload initiated.');
});

// Start the server
http.listen(PORT_NUMBER, () => {
  console.log(`Server listening on port ${PORT_NUMBER}`);
  startServer(); // Start the WebSocket and UDP servers when Express server starts
});

// Your WebSocket and other server setup here...

// Function to restart the server 
function restartServer(callback) {
  // Restart the server by executing the batch script
  
  // Callback to indicate completion
    if (typeof callback === 'function') {
      callback();
    }
}

// Function to start the WebSocket and UDP servers
function startServer() {
  // Code to initialize and start your server, including WebSocket and other dependencies
  var webServer = require('./lib/server_udp')(io); // Pass the WebSocket server instance to the UDP server
}
