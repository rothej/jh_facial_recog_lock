# Used to test functionality of SMS service using Twilio
from dotenv import load_dotenv  # dotenv (for .env var imports)
from twilio.rest import Client  # twilio libraries
import os                       # to access os vars

# Twilio Setup
## Imports .env variables (SID, authtoken) for Twilio.
load_dotenv()   # imports .env variables
accountSid = os.environ['TWILIO_ACCOUNT_SID']
authToken = os.environ['TWILIO_AUTH_TOKEN']
userPhoneNumber = os.environ['TWILIO_USR_PHONE_NUMBER']
fromPhoneNumber = os.environ['TWILIO_FROM_PHONE_NUMBER']
client = Client(accountSid, authToken)

## Sends a test SMS message to verify functionality
message = client.messages \
                .create(
                     body="This is a test message from sms_test.py",
                     from_=fromPhoneNumber,
                     to=userPhoneNumber
                 )

print(message.sid)
