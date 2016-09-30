==================
    TO REWRITE
==================

This code opens a Web Socket in a web page that communicates with a Node.js server.
The server is responsible for relaying OSC messages bidirectionally between the web page and Pure Data.


## Installation

From the command line:
1. Run <code>npm install</code>
2. In the <code>web</code> folder, run <code>bower install</code>
3. Use [pip](https://pypi.python.org/pypi/pip) to install pyosc: <code>sudo pip install pyosc --pre</code>
** On Mac OS X, pip can be easily installed using the command <code>sudo easy_install pip</code>.
** On Windows, install pip via Anaconda with python 2.7 (https://www.continuum.io/downloads#_windows)


## Running

1. In the <code>server</code> folder, start the Node.js server: <code>node .</code>
2. In <code>web</code> folder, open index.html in a web browser; a log message will be printed to the terminal when you have connected.
3. To send an OSC message via UDP to the browser, click on images.
