

/*
 * Respond to commands over a websocket to do math
 */
var dgram = require('dgram');
var fs = require('fs');
var client = dgram.createSocket('udp4');

var message_maze = false;
var message_path = false;

var actual_message_path = false;

var server_socket;
// Create an HTTP server
  var http = require('http');
  var server = http.createServer();

let pythonProcess = null;


// Export a function that takes the 'io' WebSocket server instance as an argument
module.exports = function (io) {
	
  
	
	client.on('listening', function () {
			var address = client.address();
			console.log('UDP Client: listening on ' + address.address + ":" + address.port);
	});

	
	client.on('message', function (message, remote) {
		if(message == "generate_path_complete") {
			server_socket.emit("generate_path_complete", "Finished");
		} else if (message == "restart_maze_complete") {
			server_socket.emit("restart_maze_complete", "Finished");
		}
		else if (message == "maze_message") {
			message_maze = true;
			message_path = false;
			actual_message_path = false;
		} else if(message == "path_message") {
			message_path = true;
			message_maze = false;
			actual_message_path = false;
		} else if(message == "actual_path_message") {
			message_path = false;
			message_maze = false;
			actual_message_path = true;
		}
		else if(message_maze) {
			const twoDArray = JSON.parse(message.toString());
			server_socket.emit("maze", twoDArray);
			message_maze = false;

		} else if(message_path) {
			const path = JSON.parse(message.toString());
			server_socket.emit("path", path);
			message_path = false;
		} else if(actual_message_path) {
			const path = JSON.parse(message.toString());
			server_socket.emit("actual_path", path);
			actual_message_path = false;
		}
	});



io.on('connection', function (socket) {
    server_socket = socket;
	
    // Kill the existing Python process if it exists
    if (pythonProcess) {
        pythonProcess.kill();
    }

    // Run the Python script when a new WebSocket connection is established
    const { spawn } = require('child_process');
    pythonProcess = spawn('python', ['../main.py']);

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python stderr: ${data}`);
    });
    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python stdout: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });

    handleCommands(socket);
});
  // Listen on a specific port
  server.listen(8089, function () {
    console.log('Server is running on port 8089');
  });
}

// Handles all the UDP communications to the Python program
function handleCommands(socket) {
	

	// Add listener on WebSocket to indicate node js is running
	socket.on('isNodeJsUp', function(data) {
		socket.emit("nodeJsACK", "I'm here");
	});

	socket.on('kill_python', function(data) {
		if (pythonProcess) {
        	pythonProcess.kill();
    	}
	});

	socket.on('clicked_coordinates', function(data) {

		// Info for connecting to the local process via UDP
		var PORT = 12345;
		var HOST = '127.0.0.1';
		//console.log(data)
		var dataString = JSON.stringify(data);
		var buffer = Buffer.from(dataString);

		// Send user command to Python program
		
		client.send(buffer, 0, buffer.length, PORT, HOST, function(err, bytes) {
			if (err) 
				throw err;
		});
	});

	socket.on('generate_path', function(data) {

		// Info for connecting to the local process via UDP
		var PORT = 12345;
		var HOST = '127.0.0.1';
		//console.log(data)
		
		var buffer = Buffer.from(data);

		// Send user command to Python program
		
		client.send(buffer, 0, buffer.length, PORT, HOST, function(err, bytes) {
			if (err) 
				throw err;
		});
	});

	socket.on('reset_maze', function(data) {

		// Info for connecting to the local process via UDP
		var PORT = 12345;
		var HOST = '127.0.0.1';
		//console.log(data)
		
		var buffer = Buffer.from(data);

		// Send user command to Python program
		
		client.send(buffer, 0, buffer.length, PORT, HOST, function(err, bytes) {
			if (err) 
				throw err;
		});
	});

	socket.on('info_client', function(data) {

		// Info for connecting to the local process via UDP
		var PORT = 12345;
		var HOST = '127.0.0.1';
		//console.log(data)
		var dataString = JSON.stringify(data);
		var buffer = Buffer.from(dataString);

		// Send user command to Python program
		
		client.send(buffer, 0, buffer.length, PORT, HOST, function(err, bytes) {
			if (err) 
				throw err;
		});
	});
	
};