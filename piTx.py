def tx_on():                      	                    # Turn on transmitter
    GPIO.output(pin, GPIO.LOW)
    return


def tx_off():                        	                # Turn off transmitter
    GPIO.output(pin, GPIO.HIGH)
    return


def sync_pulse(pulse):                                  # Give a common reference time
    tx_on()
    time.sleep(pulse)
    tx_off()
    return


def get_number(num):                                    # Make a list of broadcast sequence
    seq = list(bin(num))
    seq.remove('b')
    while len(seq) < 8:
        seq.insert(0, 0)
    seq = [int(x) for x in seq]
    seq.reverse()
    return seq


def get_word():                                         # Make a list with alphabetically numbered letters
    word = str(raw_input('Enter a word: '))
    word = list(word)
    word = [(ord(x)-96) for x in word]
    return word


def time_start(compensation):                           # Set starting time and add compensation
    return time.time() + compensation


def time_running(stime):                                # Returns time since sync
    return time.time() - stime


def time_until(goal_time, compensation):                # Returns starting time
    return time.time() + compensation + goal_time


def send_sequence(seq, pulse, sleep, tx_start):         # Sends a byte long sequence
    while time.time() < tx_start:
        time.sleep(sleep)
    for i in range(0, 8):
        if seq[i] == 1:
            tx_on()
        elif seq[i] == 0:
            tx_off()
        time.sleep(pulse)
    time.sleep(0.5 * pulse)
    return


if __name__ == '__main__':
    import RPi.GPIO as GPIO
    import time

    # Necessary variables
    seq = []                                            # Container for broadcast sequence
    stime = 0.0                                         # Synced time
    tx_start = 0.0                                      # Transmission starting time

    # Settings
    pin = 23                                            # GPIO pin number
    compensation = 0.04                                 # Difference in clocks
    sleep = 0.0001                                      # Waiting cycle
    pulse = 0.2                                         # Lenght of sync pulse in seconds
    transmission_density = 10                           # time to wait between bytes
    GPIO.setmode(GPIO.BCM)                              # GPIO configuration
    GPIO.setup(pin, GPIO.OUT)

    # Testing program
    while True:
        tx_off()
        seq = get_word() # Get input
        for i in range(0, len(seq)):
            sync_pulse(pulse) # Wake up receiver
            tx_start = time_until(0.2, compensation)
            send_sequence(get_number(seq[i]), pulse, sleep, tx_start) # Send byte
    #GPIO.cleanup() # Reset GPIO
