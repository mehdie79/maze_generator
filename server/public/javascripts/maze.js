"use strict";
// Client-side interactions with the browser.

var socket = io();

var width_maze;
var height_maze;
// Make connection to server when web page is fully loaded.
$(document).ready(function() {

	// Handle data coming back from the server
	socket.on('maze', function(result) {
		//sendUDPCommand("openSocket", "recieved");
		//console.log(result);
		showMazeImage(result);

		const page1 = document.getElementById('profile');
    const page2 = document.getElementById('maze');

        
		page1.classList.remove('active-page');
        page2.classList.add('active-page');
		
	});

	socket.on('path', function(result) {
		showPath(result);
	
	});
  socket.on('actual_path', function(result) {
		showActualPath(result);
	});

    $('#stop').click(function(){
		sendUDPCommand("singleUserCommand", "stop");
	});
	

	socket.on('commandReplySong', function(result) {
		$('#modeid').text(result);
	});
	
});

  document.getElementById('myForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            const width = document.getElementById('width').value;
            const height = document.getElementById('height').value;
            const algorithm = document.getElementById('algorithm').value;

			 if (width < 5 || width > 30 || height < 5 || height > 30) {
                event.preventDefault(); // Prevent form submission
                document.getElementById("error-message").textContent = "Width and height must be between 5 and 30";
            } else {
                document.getElementById("error-message").textContent = "";
            }

			width_maze = width;
			height_maze = height;

			const info = {
						width: width,
						height: height,
						algorithm: algorithm,	
					};
			sendUDPCommand("info_client", info);
			

});

function showActualPath(path) {
   
    const firstValue = path[0];
    const secondValue = path[1];
    const rowClass = `row${firstValue}`;
    const colClass = `col${secondValue}`;

    // Get the element with the specified row and column class
    const element = document.querySelector(`.${rowClass} .${colClass}`);

    // Create a canvas element
    const canvas = document.createElement("canvas");
    canvas.width = 30;
    canvas.height = 30;

    // Get the 2D drawing context
    const context = canvas.getContext("2d");

    // Draw a red square on the canvas
    context.fillStyle = "blue";
    context.fillRect(0, 0, 30, 30);

    // Convert the canvas to a data URL
    const dataURL = canvas.toDataURL("image/png");

    // Set the src attribute of the image element to the data URL
    element.src = dataURL;

}

function showPath(pathArray) {

  // Iterate through the arrays
  for (let i = 0; i < pathArray.length; i++) {
    const currentArray = pathArray[i];
    const firstValue = currentArray[0];
    const secondValue = currentArray[1];
    const rowClass = `row${firstValue}`;
    const colClass = `col${secondValue}`;

    // Get the element with the specified row and column class
    const element = document.querySelector(`.${rowClass} .${colClass}`);

    // Create a canvas element
    const canvas = document.createElement("canvas");
    canvas.width = 30;
    canvas.height = 30;

    // Get the 2D drawing context
    const context = canvas.getContext("2d");

    // Draw a red square on the canvas
    context.fillStyle = "green";
    context.fillRect(0, 0, 30, 30);

    // Convert the canvas to a data URL
    const dataURL = canvas.toDataURL("image/png");

    // Set the src attribute of the image element to the data URL
    element.src = dataURL;
  }
}

function showMazeImage(twoDArray) {
  // Get the number of rows and columns
  const numRows = twoDArray.length;
  const numCols = twoDArray[0].length;
  const mazeContainer = document.getElementById('maze');
  mazeContainer.classList.add('maze-container');

  if(width_maze > 22 && height_maze > 22) {
	mazeContainer.classList.remove('maze-container');
  }

  // Iterate through the 2D array using nested loops
  for (let i = 0; i < numRows; i++) {
    const row = document.createElement('div'); // Create a row container
    const rowClass = `row${i}`; // Unique class for the row
    row.classList.add(rowClass);

    for (let j = 0; j < numCols; j++) {
      // Access the element at row 'i' and column 'j'
      const element = twoDArray[i][j];

      // Generate a unique class name for each column
      const colClass = `col${j}`; // Unique class for the column
      const imgClass = `${colClass}`; // Combine row and column classes

      // Set the element's style based on the array value
      let mazeElement;
      if (element === ' ') {
        mazeElement = `<img class="${imgClass}" src="./Images/floor.png" style="width: 30px; height: 30px;margin-bottom:-4px;" alt="Floor">`;
      } else if (element === '#') {
        mazeElement = `<img class="${imgClass}" src="./Images/wall.png" style="width: 30px; height: 30px;margin-bottom:-4px;" alt="Wall">`;
      } else if (element === 'O' || element === 'X') {
        mazeElement = `<img class="${imgClass}" src="./Images/floor.png" style="width: 30px; height: 30px;margin-bottom:-4px;" alt="Floor">`;
      }


      row.innerHTML += mazeElement;
    }

    mazeContainer.appendChild(row);
  }

  // Append the maze container to the document body or a specific HTML element
  document.body.appendChild(mazeContainer);
}


function sendUDPCommand(command, message) {
	socket.emit(command, message);
}


function replaceAll(str, find, replace) {
	return str.replace(new RegExp(find, 'g'), replace);
}