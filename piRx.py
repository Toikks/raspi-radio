# Testing software for Raspberry pi B controlling a radio receiver salvaged from R/C helicopter toy
# ASK modulation at 27,095 Mhz
# Maximum speed cannot exceed 1,5 ms per bit due to relays used for interfacing GPIO with external signal.


def rx_status():                                            # Check input pin
    if GPIO.input(pin) == 0:
        return True
    if GPIO.input(pin) == 1:
        return False


def wait_rx(sleep, pulse):                                  # Sleep until next broadcast
    while not rx_status():
        time.sleep(sleep)
    time.sleep(pulse)
    return


def pulse_lenght():                                         # Returns lenght of a pulse
    while True:
        start_time = time.time()
        if rx_status():
            break
    while True:
        end_time = time.time()
        if not rx_status():
            break
    pulse_lenght = end_time - start_time
    #print([end_time, start_time, pulse_lenght])            # For testing purposes
    if pulse_lenght > 0:
        return pulse_lenght
    else:
        return False


def time_until(goal_time):                                  # Returns starting time for action
    return time.time() + goal_time


def listen_seq(pulse, sleep, rx_start):                     # Record sequence
    seq = []
    while time.time() < rx_start:
        time.sleep(sleep)
    time.sleep(0.5 * pulse)                                 # Move to the center of the pulse
    while len(seq) < 8:
        seq.append(rx_status())
        time.sleep(pulse)
    return seq


def get_num(seq, total = 0):                                # Turn sequence into integer in range 0-255
    for i in range(0, len(seq)):
        if seq[i]:
            total += 2**i
    return total


def get_word(num):                                          # Turn integers to letters
    return chr(num + 96)


if __name__ == '__main__':
    import RPi.GPIO as GPIO
    import time

    # Settings
    pin = 9
    compensation = 0.0                                      # Difference in clocks
    sleep = 0.0001                                          # Waiting cycle
    pulse = 0.2                                             # Lenght of sync pulse in seconds
    transmission_density = 10                               # time to wait between bytes
    GPIO.setmode(GPIO.BCM)                                  # GPIO configuration
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # Testing program
    message = []
    while True:
        wait_rx(sleep, pulse) # Wait for transmission start
        rx_start = time_until(0.2) # Get starting time
        message.append(get_word(get_num(listen_seq(pulse, sleep, rx_start)))) # List received letters
        print(''.join(message)) # Join and print letters
    GPIO.cleanup() # Reset GPIO
