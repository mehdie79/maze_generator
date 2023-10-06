"use strict";
// Client-side interactions with the browser.

const socket = io(); // Use the correct server URL

var width_maze;
var height_maze;
var box_checked = false;

var addPunishment = false;
var generatePath = false;
var resetMaze = false;

var current_maze;

var count_generate_path_pressered = 0;



// Make connection to server when web page is fully loaded.
$(document).ready(function() {
  

	// Handle data coming back from the server
	socket.on('maze', function(result) {
		showMazeImage(result);

		const page1 = document.getElementById('profile');
    const page2 = document.getElementById('maze');
    const page3 = document.getElementById('maze_sec');
    const page4 = document.getElementById('maze_not_customize');

        
		page1.classList.remove('active-page');
    page2.classList.add('active-page');
    if(box_checked == true) {
       page3.classList.add('active-page');
    }
    if(box_checked == false) {
       page4.classList.add('active-page');
       
    }
    
    
		
	});
  socket.on('generate_path_complete', function(result) {
    generatePath = false;
	});
  socket.on('restart_maze_complete', function(result) {
    resetMaze = false;
		
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

      var checkbox = document.getElementById("interact");
      // Check if the checkbox is checked
      if (checkbox.checked) {
          box_checked = true;
          // Checkbox is checked
          console.log("Checkbox is checked.");
      } else {
          box_checked = false;
          // Checkbox is not checked
          console.log("Checkbox is not checked.");
      }
      const info = {
						width: width,
						height: height,
						algorithm: algorithm,	
            box_checked: box_checked,
					};
      sendUDPCommand("info_client", info);
			
});
function removePunishmentImagesByClassName(rowClass , className) {
  const punishmentImgs = document.querySelectorAll(`.${rowClass} .${className}[data-punishment="true"]`);
  punishmentImgs.forEach((img) => {
    img.parentNode.removeChild(img);
  });
}


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

    const punishmentImg = document.createElement('img');
    punishmentImg.src = dataURL;
    punishmentImg.style.width = '30px';
    punishmentImg.style.height = '30px';
    punishmentImg.style.position = 'absolute';
    if(current_maze[firstValue][secondValue] == 'X' || current_maze[firstValue][secondValue] == 'O') {
      punishmentImg.style.marginLeft = "-4.5px";
      punishmentImg.style.marginRight = "-4.5px";
    }
    
    punishmentImg.classList.add(colClass);
    punishmentImg.style.border = '1px solid white';
    
    const parentElement = element.parentNode;
    const desiredClassName = colClass;
    removePunishmentImagesByClassName(rowClass,colClass)

     // Iterate through child elements of the parent
    for (let i = 0; i < parentElement.children.length; i++) {
          const child = parentElement.children[i];
          
          // Check if the child element has the desired class name
          if (child.classList.contains(desiredClassName)) {

            parentElement.insertBefore(punishmentImg, child);
            break; // Exit the loop after insertion
          }
    }
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
    const tileElement = document.querySelector(`.${rowClass} .${colClass}`);

    // Create a canvas element
    const canvas = document.createElement("canvas");
    canvas.width = 30;
    canvas.height = 30;
    const context = canvas.getContext("2d");

    // Draw a green path on the canvas
    context.fillStyle = "green"; // Green with transparency
    context.fillRect(0, 0, 30, 30);

    // Convert the canvas to a data URL
    const dataURL = canvas.toDataURL("image/png");



    const punishmentImg = document.createElement('img');
    punishmentImg.src = dataURL;
    punishmentImg.style.width = '30px';
    punishmentImg.style.height = '30px';
    punishmentImg.style.position = 'absolute';
    punishmentImg.classList.add(colClass);
    punishmentImg.setAttribute('data-punishment', 'true'); // Add a custom data attribute
    punishmentImg.style.border = '1px solid white';
    if(current_maze[firstValue][secondValue] == 'X' || current_maze[firstValue][secondValue] == 'O') {
      punishmentImg.style.marginLeft = "-4.5px";
      punishmentImg.style.marginRight = "-4.5px";
    }
    
    const parentElement = tileElement.parentNode;
    const desiredClassName = colClass;

     // Iterate through child elements of the parent
    for (let i = 0; i < parentElement.children.length; i++) {
          const child = parentElement.children[i];
          
          // Check if the child element has the desired class name
          if (child.classList.contains(desiredClassName)) {
            // Insert the punishmentImg before the found element
            parentElement.insertBefore(punishmentImg, child);
            break; // Exit the loop after insertion
          }
    }
  }
}




function showMazeImage(twoDArray) {
  // Get the number of rows and columns
  const numRows = twoDArray.length;
  const numCols = twoDArray[0].length;
  current_maze = twoDArray;
  const mazeContainer = document.getElementById('maze');
  mazeContainer.classList.add('maze-container');
  
  // Clear the existing maze by removing all child elements
  while (mazeContainer.firstChild) {
    mazeContainer.removeChild(mazeContainer.firstChild);
  }

  if(width_maze > 18 && height_maze > 18 && width_maze < 22 && height_maze < 22) {
    mazeContainer.style.marginTop = '20%';
  }

  if(width_maze > 22 || height_maze > 22) {
     mazeContainer.style.marginTop = '8%';
     mazeContainer.style.marginLeft = '18%';
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
      }
    else if (element === 'O') {
    mazeElement = `
        <span class="${imgClass} yellow-square"></span>
        <img class="${imgClass} hidden" src="./Images/floor.png" style="width: 30px; height: 30px; margin-bottom: -4px;" alt="Floor">
    `;
} else if (element === 'X') {
    mazeElement = `
        <span class="${imgClass} orange-square"></span>
        <img class="${imgClass} hidden" src="./Images/floor.png" style="width: 30px; height: 30px; margin-bottom: -4px;" alt="Floor">
    `;
}
    else if (element === 'P') { 
          mazeElement = `
            <div style="position: relative;">
              <img class="${imgClass}" src="./Images/floor.png" style="width: 30px; height: 30px; margin-bottom: -4px;" alt="Floor">
              <img class="punishment" src="./Images/punishment.png" style="position: absolute; top: 0; left: 0; width: 30px; height: 30px; margin-bottom: -4px;" alt="Punishment">
            </div>
          `;
      }


      row.innerHTML += mazeElement;
    }

    mazeContainer.appendChild(row);
  }

  

  // Append the maze container to the document body or a specific HTML element
  document.body.appendChild(mazeContainer);
  
  const mazeTiles = mazeContainer.querySelectorAll('img');


mazeTiles.forEach((tile, index) => {
  tile.addEventListener('click', function () {
    if(box_checked == false) {
      return;
    }
    // Calculate the row and column of the clicked tile
    const numRows = twoDArray.length;
    const numCols = twoDArray[0].length;
    const clickedRow = Math.floor(index / numCols);
    const clickedCol = index % numCols;

    if(current_maze[clickedRow][clickedCol] === "O" || current_maze[clickedRow][clickedCol] === "X" ||  current_maze[clickedRow][clickedCol] === "P" ) {
      return;
    }

    // Now you can use clickedRow and clickedCol to identify the clicked tile
    console.log(`Clicked tile coordinates: (${clickedRow}, ${clickedCol})`);
    console.log("Tile" + tile);
    const info = {
						row: clickedRow,
						column: clickedCol,	
            addPunishment: addPunishment,
		};

    sendUDPCommand("clicked_coordinates", info);
    if(current_maze[clickedRow][clickedCol] == " " && addPunishment == true) {
        console.log("Punishment" + tile.className);
        //Create the punishment image element
        const punishmentImg = document.createElement('img');
        punishmentImg.src = './Images/punishment.png';
        punishmentImg.style.width = '30px';
        punishmentImg.style.height = '30px';
        punishmentImg.style.position = 'absolute';
        punishmentImg.classList.add(tile.className);
        punishmentImg.alt = 'Punishment';
        const parentElement = tile.parentNode;
        const desiredClassName = tile.className; // Replace with the desired class name

        // Iterate through child elements of the parent
        for (let i = 0; i < parentElement.children.length; i++) {
          const child = parentElement.children[i];
          
          // Check if the child element has the desired class name
          if (child.classList.contains(desiredClassName)) {
            // Insert the punishmentImg before the found element
            parentElement.insertBefore(punishmentImg, child);
            break; // Exit the loop after insertion
          }
        }

        current_maze[clickedRow][clickedCol] = "P";

    } else if(current_maze[clickedRow][clickedCol] == " " && addPunishment == false) {
        const currentImgSrc = tile.src;

        // Toggle the image source between floor and wall
        if (currentImgSrc.endsWith('floor.png')) {
          // Change floor image to wall image
          tile.src = './Images/wall.png';
          current_maze[clickedRow][clickedCol] = "#";
        } 
    }
      

  });
});
}


function sendUDPCommand(command, message) {
	socket.emit(command, message);
}


function replaceAll(str, find, replace) {
	return str.replace(new RegExp(find, 'g'), replace);
}

 // Get a reference to the "Add Punishment" button
    const addPunishmentButton = document.getElementById('Add-Punishment');

    // Add a click event listener to toggle the "active-button" class
    addPunishmentButton.addEventListener('click', function () {
        if(box_checked == false) {
            return;
        }
        if(generatePath || resetMaze) {
          return;
        }
        // Toggle the "active-button" class on button click
        addPunishmentButton.classList.toggle('active-button');
        addPunishment = !addPunishment;
        console.log("Color Changed");
    });

    const generateButton = document.getElementById('generate-button');

    const resetButton = document.getElementById('reset-button');

    const return_button_section = document.getElementById('return-button');
    const return_button_section1 = document.getElementById('return-button1');
    return_button_section1.addEventListener('click', function () {

          sendUDPCommand("kill_python", "kill_python");
          reloadServerAndStaticContent();

    });

    return_button_section.addEventListener('click', function () {

          sendUDPCommand("kill_python", "kill_python");
          reloadServerAndStaticContent();

    });

    generateButton.addEventListener('click', function () {
        if(box_checked == false) {
          return;
        }
        // Toggle the "active-button" class on button click
        if(generatePath || resetMaze) {
          return;
        }
        generatePath = true;
        if(count_generate_path_pressered > 0) {
          showMazeImage(current_maze);
        }
        count_generate_path_pressered++;
        sendUDPCommand("generate_path", "generate_path");
        console.log("send generate_path");

    });

    resetButton.addEventListener('click', function () {
        if(box_checked == false) {
            return;
        }
        // Toggle the "active-button" class on button click
      if(generatePath || resetMaze) {
        return;
      }
      resetMaze = true;
      count_generate_path_pressered = 0;
      sendUDPCommand("reset_maze", "reset_maze");
       
    });

function reloadServerAndStaticContent() {
  fetch('/reload-server', { method: 'POST' })
    .then(function (response) {
      if (response.status === 200) {
        console.log('Server reload initiated...');
        // Execute the batch script to restart the server
        fetch('/reload-static', { method: 'POST' })
          .then(function (response) {
            if (response.status === 200) {
              console.log('Server and static content reloaded successfully.');
              // Reload the entire page after the server and static content restarts
              window.location.reload();
            } else {
              console.error('Failed to reload server and static content.');
            }
          })
          .catch(function (error) {
            console.error('Error:', error);
          });
      } else {
        console.error('Failed to initiate server reload.');
      }
    })
    .catch(function (error) {
      console.error('Error:', error);
    });
}




