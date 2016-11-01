import os, sys
import types

from espaces import EspaceClient
espace_client = EspaceClient()

from OSC import OSCServer, OSCMessage, getUrlStr

def handle_timeout(self):
    """ this method of reporting timeouts only works by convention
        that before calling handle_request() field .timed_out is
        set to False
    """
    self.timed_out = True

def espaces_callback(path, tags, args, source):

    msg_string = ""
    msg_string += "\n\tpath   : %s" % path
    msg_string += "\n\ttags   : %s" % tags
    msg_string += "\n\targs   : %s" % args
    msg_string += "\n\tsource :%s" % str(source)
    print "OSCServer received: %s\nfrom %s.\n" % (msg_string, getUrlStr(source))

    ir_params = {  'duration'      : float(args[4]),
                   'nu'            : float(args[5]),
                   'sampling_rate' : float(args[6]),
                   'ev_params'     : {'space': str(args[1]), 'c':float(args[2]), 'j_max':int(args[3]),'F':list(args[7:])},
                }

    command = espace_client.handle_request(ir_params)

    # send reply to the client
    reply_port = int(args[0])
    reply_addresse = (source[0], reply_port)
    msg = OSCMessage("/pd")
    msg.append(command['saved_audio_path'])
    server.client.sendto(msg,reply_addresse,timeout=1)
    print "OSCServer send:\n\t%s\nto %s.\n" %(msg,reply_addresse)

    return OSCMessage("/")


def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

# create server
HOST = "localhost"
PORT = 9001
server = OSCServer((HOST,PORT))
server.timeout = 0
run = True
print "Running | ip addresse : %s | port : %s" % (HOST,PORT)


# add handle_timeout method to the server
server.handle_timeout = types.MethodType(handle_timeout, server)

# add callback methods to the server
server.addMsgHandler( "/espaces", espaces_callback)
server.addMsgHandler( "/quit", quit_callback )


# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()

while run:
    each_frame()

server.close()