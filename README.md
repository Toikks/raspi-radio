# raspi-radio
This software is used for testing purposes and is made for Raspberry pi B controlling a radio receiver and Raspberry pi 3 controlling a radio transmitter.

Raspberry pi 3 is used on transmitter side because it has much higher GPIO output switching speed than raspberry pi 1.

# Version with salvaged parts from r/c toy
Rx.py is for receiver, and Tx.py is for transmitter.

Transmitter/Receiver pair uses ASK modulation at 40 Mhz. Maximum speed cannot exceed 1,5 ms per bit due to relays used for interfacing GPIO with external signal. 

# Version with FS1000A/XY-FST
Rx2.py for receiver and Tx2.py for transmitter.
