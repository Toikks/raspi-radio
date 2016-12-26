# Raspberry pi 3


def tx(mode):                      	                    # Turn on transmitter
    if mode:
        GPIO.output(pin, GPIO.HIGH)
        return
    elif not mode:                                      # Turn off transmitter
        GPIO.output(pin, GPIO.LOW)
        return


def get_number(num=None):                               # Make a list of broadcast sequence

    if num is None:
        num = int(input('Enter a number: '))

    if num in range(0, 256):
        seq = list(bin(num))
        seq.remove('b')
        while len(seq) < 8:
            seq.insert(0, 0)
        seq = [int(x) for x in seq]
        seq.reverse()
        if len(seq) > 8:
            del seq[-1]
        return seq

    else:
        sys.exit('invalid number')


def get_word(word=None):                                # Make a list with alphabetically numbered letters
    if word is None:
        word = list(str(raw_input('Enter a word: ')))
    return [(ord(x)) for x in word]


def starting_time(until_start):                         # Returns starting time from wanted delay
    return time.time() + compensation + until_start     # Second argument blank for no time compensation


def send_sequence(seq, tx_start=None):                  # Sends a byte long sequence
    if tx_start is not None:
        while time.time() < tx_start:
            pass

    for i in range(0, 8):
        if seq[i] == 1:
            tx(True)
            time.sleep(2 * pulse)
            tx(False)

        elif seq[i] == 0:
            tx(True)
            time.sleep(1 * pulse)
            tx(False)

        time.sleep(0.5 * pulse)
    return


if __name__ == '__main__':
    import RPi.GPIO as GPIO
    import time
    import sys

    # Settings
    pin = 23                                                # GPIO pin number
    compensation = 0                                        # Difference in clocks
    pulse = 0.03                                            # Base length for pulses in seconds
    transmission_density = 10                               # time to wait between bytes
    GPIO.setmode(GPIO.BCM)                                  # GPIO configuration
    GPIO.setup(pin, GPIO.OUT)

    # Testing program
    while True:
        message = get_word()
        for i in range(0,len(message)):
            message[i] = get_number(message[i])
        for i in message:
            send_sequence(i)