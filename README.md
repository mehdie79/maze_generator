# Maze Generator and Path Finder

This project allows you to generate a random maze with a specified width and height using a web interface. It also provides the ability to find the shortest path from the start to the end square within the generated maze using different path-finding algorithms.

## Prerequisites

Before you can run the application, make sure you have the following prerequisites installed on your system:

- [Node.js](https://nodejs.org/) - A JavaScript runtime.
- [Python](https://www.python.org/) - A high-level programming language.

## Dependencies

The project has the following dependencies, which you need to install using npm (Node Package Manager):

```bash
npm install express@4.18.2 mime@2.5.2 socket.io@4.0.1
```

## Running the Application

To run the application, follow these steps:

1. Open your terminal/command prompt.

2. Navigate to the project's root directory.

3. Change the working directory to the server folder:

   ```bash
   cd server
   ```

4. Start the Node.js server:

   ```bash
   node main_server.js
   ```

5. After running the Node.js server, you can access the web interface by opening a web browser and going to the following URL:

   [http://127.0.0.1:8088/](http://127.0.0.1:8088/)

## How to Use

1. On the web interface, you can input the width and height for the maze generation. Ensure that both values are between 5 and 30.

2. Select a path-finding algorithm from the available options.

3. Click the "Submit" button to generate the maze and find the shortest path.

4. The generated maze will be displayed on the web interface along with the shortest path highlighted.
