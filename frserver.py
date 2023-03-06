# This python script runs the facial recognition lock server. 
# This server handles communicating with the clients, as well
# as sending SMS push notifications and exporting logging 
# information for unauthorized entry attempts.

from dotenv import load_dotenv  # dotenv (for .env var imports)
from twilio.rest import Client  # twilio libraries
import os                       # to access os vars
import zmq                      # for client/server comms
import signal                   # for SIGINT handling etc
import sys

# *** SCALABILITY ***
# Set this value to the number of clients. Current maximum supported
# is 3, but this can be scaled up by copy/pasting additional port handlers.
# It will always bind at least one client, even if CLIENT_COUNT is set to 0.
CLIENT_COUNT = 1

# ZMQ Setup
## Set up server sockets. Push is 55001, pull is 55002.
## Additional clients require their own sockets.
context = zmq.Context()
pushSocket1 = context.socket(zmq.PUSH)
pushSocket1.bind("tcp://127.0.0.1:55001")
pullSocket1 = context.socket(zmq.PULL)
pullSocket1.bind("tcp://127.0.0.1:55002")
### Additional Clients
if CLIENT_COUNT > 1:
    pushSocket2 = context.socket(zmq.PUSH)
    pushSocket2.bind("tcp://127.0.0.1:55003")
    pullSocket2 = context.socket(zmq.PULL)
    pullSocket2.bind("tcp://127.0.0.1:55004")
if CLIENT_COUNT > 2:
    pushSocket3 = context.socket(zmq.PUSH)
    pushSocket3.bind("tcp://127.0.0.1:55005")
    pullSocket3 = context.socket(zmq.PULL)
    pullSocket3.bind("tcp://127.0.0.1:55006")
### Add more clients as needed, choosing sockets appropriately.

## Handle SIGINT for exiting program and unbinding sockets.
def exitHandler(sig, frame):
    print("Unbinding ports and exiting . . .")
    pushSocket1.unbind("tcp://127.0.0.1:55001")
    pullSocket1.unbind("tcp://127.0.0.1:55002")
    ### Scalable clients, add more if needed.
    if CLIENT_COUNT > 1:
        pushSocket2.unbind("tcp://127.0.0.1:55003")
        pullSocket2.unbind("tcp://127.0.0.1:55004")
    if CLIENT_COUNT > 1:
        pushSocket3.unbind("tcp://127.0.0.1:55005")
        pullSocket3.unbind("tcp://127.0.0.1:55006")
    ### End scalable.
    sys.exit(0)

signal.signal(signal.SIGINT, signal.default_int_handler)
## End SIGINT handler.

# Twilio Setup
## Imports .env variables (SID, authtoken) for Twilio.
load_dotenv()   # imports .env variables
accountSid = os.environ['TWILIO_ACCOUNT_SID']
authToken = os.environ['TWILIO_AUTH_TOKEN']
client = Client(accountSid, authToken)
