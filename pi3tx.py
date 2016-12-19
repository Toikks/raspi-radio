# This software is the first test for Raspberry pi 3 controlling a radio transmitter from rc helicopter
# Integer is translated to byte of booleans and sent to ransmitter
# Pin 23 is used as output for controlling transmission


def tx_on():                      	        # Turn on transmitter
    GPIO.output(pin, GPIO.LOW)
    return


def tx_off():                        	        # Turn off transmitter
    GPIO.output(pin, GPIO.HIGH)
    return


def get_number(num = 0, lis = []):              # Get integer input from user and translate it to fit for transmitter
    num = int(input('Enter a number in range of 0-255: '))
    lis = list(bin(num))
    lis.remove('b')
    while len(lis) < 8:
	lis.insert(0, 0)    
    lis = lis[::-1]
    lis = [int(x) for x in lis]
    return lis

def sync(synctime):				#set common reference time
    synctime += 1
    while time.time() < synctime:
	time.sleep(0.001)
    tx_on()
    synctime += 0.1
    while time.time() < synctime:
	time.sleep(0.001)
    tx_off()


def handshake(synctime):                    	# Confirm the right signal
    synctime += 0.5
    print(synctime)
    while time.time() < synctime:    
	time.sleep(0.001)
    tx_on()
    synctime += 0.1
    while time.time() < synctime:
	time.sleep(0.001)
    tx_off()
    synctime += 0.1
    while time.time() < synctime:
	time.sleep(0.001)
    tx_on()
    synctime += 0.3
    while time.time() < synctime:
	time.sleep(0.001)
    tx_off()


def send_byte(byte, synctime):			# Send a byte of data from list

    synctime += 0.5
    while time.time() < synctime:
	time.sleep(0.001)
    for i in range(0, 8):
	if byte[i] == 0:
	    tx_off()
	    state = 0
	if byte[i] == 1:
	    tx_on()
	    state = 1
	time.sleep(0.2)
    tx_off()

if __name__ == '__main__':
    import RPi.GPIO as GPIO
    import time

    pin = 23
    byte = []
    synctime = time.time()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    tx_off()
    byte = get_number()
    synctime = time.time()
    sync(synctime)
    synctime += 1.0
    send_byte(byte, synctime)
    GPIO.cleanup()
