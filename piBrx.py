# This software is the first test of for Raspberry pi B controlling a radio receiver from rc helicopter
# Byte of data is received and translated to integer
# Pin 9 is connected to the receiver


def rx_status():                        # Check input pin
    if GPIO.input(pin) == 1:
        return 0
    if GPIO.input(pin) == 0:
        return 1


                                        # Return lenght of the signal
def signal_lenght(start_time = 0, end_time = 0):
    while True:
	start_time = time.time()
	if rx_status() == 1:
	    break
    while True:
        end_time = time.time()
	if rx_status() == 0:
	    break
    holder = int((end_time - start_time) * 100)
    print([end_time, start_time, holder])
    if holder > 0:
        return holder
    else:
	return 0


def wait_rx():			        # Wait until action on receiver
    while rx_status() == 0:
        time.sleep(0.0001)
    return True


def listen_rx(synctime):		# Record a byte
    synctime += 0.5
    message = []
    holder = 0
    while time.time() < synctime:
	time.sleep(0.001)
    time.sleep(0.1)
    while len(message) < 8:
        holder = rx_status()
        message.append(holder)
        time.sleep(0.2)
        print(message)
    return message


def get_num(num, total = 0):            # Turn byte sequence into integer in range 0-255
    for i in range(0, len(num)):
	if num[i] == 1:
	    total += 2**i
    print(total)

if __name__ == '__main__':
    import RPi.GPIO as GPIO
    import time

    pin = 9
    lis = []
    synctime = time.time()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    if wait_rx() == True:
	synctime = time.time()
	get_num(listen_rx(synctime))

    GPIO.cleanup()
