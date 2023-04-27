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
pushSocket1.bind("tcp://*:55001")
pullSocket1 = context.socket(zmq.PULL)
pullSocket1.connect("tcp://192.168.1.6:55002")
### Additional Clients
if CLIENT_COUNT > 1:
    pushSocket2 = context.socket(zmq.PUSH)
    pushSocket2.bind("tcp://*:55003")
    pullSocket2 = context.socket(zmq.PULL)
    pullSocket2.connect("tcp://*:55004")
if CLIENT_COUNT > 2:
    pushSocket3 = context.socket(zmq.PUSH)
    pushSocket3.bind("tcp://*:55005")
    pullSocket3 = context.socket(zmq.PULL)
    pullSocket3.connect("tcp://*:55006")
### Add more clients as needed, choosing sockets appropriately.
print("Socket setup complete.")

## Handle SIGINT for exiting program and unbinding sockets.
def exitHandler(sig, frame):
    print("Unbinding ports and exiting . . .")
    pushSocket1.unbind("tcp://*:55001") # change this depending on IP of target
    pullSocket1.unbind("tcp://*:55002")
    ### Scalable clients, add more if needed.
    if CLIENT_COUNT > 1:
        pushSocket2.unbind("tcp://*:55003")
        pullSocket2.unbind("tcp://*:55004")
    if CLIENT_COUNT > 1:
        pushSocket3.unbind("tcp://*:55005")
        pullSocket3.unbind("tcp://*:55006")
    ### End scalable.
    sys.exit(0)

signal.signal(signal.SIGINT, signal.default_int_handler)
## End SIGINT handler.

# Twilio Setup
## Imports .env variables (SID, authtoken) for Twilio. These are stored locally in the top
## level folder for the repository. It is added to .gitignore and thus must be set up
## manually, view the README.md for more details.
load_dotenv()   # imports .env variables
accountSid = os.environ['TWILIO_ACCOUNT_SID']
print(accountSid)
authToken = os.environ['TWILIO_AUTH_TOKEN']
print(authToken)
userPhoneNumber = os.environ['TWILIO_USR_PHONE_NUMBER']
print(userPhoneNumber)
fromPhoneNumber = os.environ['TWILIO_FROM_PHONE_NUMBER']
print(fromPhoneNumber)
client = Client(accountSid, authToken)
print("Twilio setup complete, running...")

## Handles message reception, SMS alerts and log creation
while True:
    work1 = pullSocket1.recv_string()   # Will need to add multiple threads for scaled clients
    print(work1)
    message = client.messages \
                .create(
                     body=work1,
                     from_=fromPhoneNumber,
                     to=userPhoneNumber
                 )
    print(message.sid)  # prints return msg to server terminal
    with open("access_log.txt", "a") as text_file:      # append mode
        print(f"Client 1: {work1}\n", file=text_file)   # Will need to be Client 2, 3 etc. for scalable, polling sockets