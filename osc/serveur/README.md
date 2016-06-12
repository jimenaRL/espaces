This code opens a Web Socket in a web page that communicates with a Node.js server.
The server is responsible for relaying OSC messages bidirectionally between the web page and Pure Data.

## Installation

From the command line:
1. In the <code>serveur</code> folder, run <code>npm install</code>
2. In the <code>web</code> folder, run <code>bower install</code>

## Running

1. In the <code>serveur</code> folder, start the Node.js server: <code>node .</code>
2. In <code>web</code> folder, open index.html in a web browser; a log message will be printed to the terminal when you have connected.
3. To send an OSC message via UDP to the browser, click on images.
