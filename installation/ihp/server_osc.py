import os
from OSC import OSCServer, OSCMessage
from espaces import EspaceClient
espace_client = EspaceClient()


HOST = "localhost"
PORT = 9001

server = OSCServer((HOST,PORT))
server.timeout = 0
run = True
print "listen to %s on %s" % (HOST,PORT) 

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)

def set_ir_params(args):
    ir_params = {  'duration'      : float(args[3]),
                   'nu'            : float(args[4]),
                   'sampling_rate' : float(args[5]),
                   'ev_params'     : {'space': str(args[0]), 'c':float(args[1]), 'j_max':int(args[2]),'F':list(args[6:])},
                }
    return ir_params

def espaces_callback(path, tags, args, source):

    print "received"
    print "\tpath   : %s" % path
    print "\ttags   : %s" % tags
    print "\targs   : %s" % args
    print "\tsource :%s" % str(source)


    ir_params = set_ir_params(args)

    command = espace_client.handle_request(ir_params)

    # send a reply to the client.
    msg = OSCMessage("/pd")
    msg.append(command['saved_audio_path'])
    # msg.append(['/Users/JRLetelier/perso/espaces/dev/installation/ihp/ir_exemple_h2e1.wav'])
    address = (source[0],9002)
    server.client.sendto(msg, address,timeout=1)
    print address
    print msg



def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False


server.addMsgHandler( "/espaces", espaces_callback )
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