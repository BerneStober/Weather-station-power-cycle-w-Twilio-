import os
import sys
import time
from datetime import datetime
import tinytuya
from twilio.rest import Client

Debug_file = 'debugPowerCycle.txt'
sys.stdout = open(Debug_file, "a")
now = datetime.now()
print("Debug file for Power cycle and SMS code ", now)   

# replace blow with the correct ip on your network
hostname = "the ip address for your weather station" #example
# following is a test for negative response
#hostname = "some nonexistant ip address" #example
response = os.system("ping -c 1 " + hostname)

TWILIO_ACCOUNT_SID = '' # replace with your Account SID
TWILIO_AUTH_TOKEN = '' # replace with your Auth Token
TWILIO_PHONE_SENDER = "" # replace with the phone number you registered in twilio
TWILIO_PHONE_RECIPIENT = "" # replace with your smartphone number

msg_from 	= 'Study RPi'								# Custom sender ID (leave blank to accept replies).
msg_body_ping_good 	= 'Weather Station ping is good'					# The message to be sent.
msg_bad_ping = 'Weather station down, am cycling power'

def send_text_alert(alert_str,text):
    """Sends an SMS text alert."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=TWILIO_PHONE_RECIPIENT,
        from_=TWILIO_PHONE_SENDER,
        body = text)
    print(message.sid)
    
"""    OUTLET Device    """

# put the proper information in the following line
#d = tinytuya.OutletDevice('device id', 'ip address', 'local key')

d.set_version(3.3)
data = d.status()  

# Show status and state of first controlled switch on device
#print('Dictionary %r' % data)
#Status = 'State %r' % data['dps']['1']
print(data)  

# test if switch is currently off
# not sure on this code; needs testing
# may be that controlling switch thru app results in different data response
if ('Error' in data) or not(data['dps']['1']):
    print ('Switch is off, toggle')
    # turn switch on
    switch_state = True
    data = d.set_status(switch_state) 
    print('set_status() result %r' % data)
    print('Weather station should be back on')
    txt = 'Weather station was found off and attempted to power cycle switch. If power is down this will not work until it comes back.' 
    send_text_alert("?",txt)
    # now exit this run because makes no sense to immediately ping test
    quit()
else:    
    print ('Switch is on proceed to ping')

# ping three times, with 30 seconds sleep between
rest = 30

if response == 0:
    print (hostname, 'is up!')
    Good1 = True
    time.sleep(rest)
else:
    Good1 = False
    time.sleep(rest)
    
if response == 0:
    print (hostname, 'is up!')
    Good2 = True
    time.sleep(rest)
else:
    Good2 = False
    time.sleep(rest)

if response == 0:
    print (hostname, 'is up!')
    Good3 = True
    time.sleep(rest)
else:
    Good3 = False
    time.sleep(rest)

# two out of three polling logic:
Good = (int(Good1) + int(Good2) + int(Good3)) >= 2

if Good:
    print (hostname, 'is up! Good = ',Good, Good1, Good2, Good3)
    #uncomment here if you are testing, but you'll want to comment this out in production
    #text = msg_body_ping_good + " from " + msg_from
    #send_text_alert("?",text)
 
else:
    print (hostname, 'is down! Good = ',Good, Good1, Good2, Good3)
    txt = msg_bad_ping + " from " + msg_from
    send_text_alert("?",txt)
    #power cycle
    d.set_version(3.3)
    data = d.status()  
    # Show status and state of first controlled switch on device
    #print('Dictionary %r' % data)
    print('State (bool, true is ON) %r' % data['dps']['1'])
    
    switch_state = data['dps']['1']
    data = d.set_status(not switch_state)  # This requires a valid key
    if data:
        print('set_status() result %r' % data)
        print('Weather station should be off')  
    time.sleep(10)
    #time.sleep(360)

    switch_state = data['dps']['1']
    data = d.set_status(not switch_state)  # This requires a valid key
    if data:
        print('set_status() result %r' % data)
        print('Weather station should be back on')
        txt = 'Weather station has been power cycled' 
        send_text_alert("?",txt)
      