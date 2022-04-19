# Weather-station-power-cycle-w-Twilio-SMS-notifications
this is some python 3.8 code that uses twilio and tinytuya to ping my weather station (a SwitchDoc.com Skyweather2 running on a RPi model 3) and notify if its down then power cycle a smart switch on it to bring it back;
read all the comments -- you will need to customize the code to your installation, put your keys and info in the code

It does a 2 out of 3 ping polling test to see if the RPi is running.
If the weather station RPi fails this, the smart power switch on it is cycled.
I run this every 20 minutes using crontab on another RPi on my home network

Please let me know any bugs or improvements you find / make.
Good luck,  
Berne Stober