# Raspberry pi B


def rx_status():                                        # Check input pin
    if GPIO.input(pin):
        return True
    else:
        return False


def wait_msg(rx_start=None):                            # Sleep until next broadcast

    if rx_start is not None:                            # No argument results in no delay
        while time.time() < rx_start:
            pass

    while True:
        msg = []
        while True:                                     # Record 8 bits to continue
            while not rx_status():
                pass
            msg.append(pulse_length())
            if len(msg) >= 8:
                if len(msg) > 8:
                    break
                return msg


def pulse_length():                                     # Returns length of a pulse
    while True:
        while True:
            start_time = time.time()
            if rx_status():
                break

        while True:
            end_time = time.time()
            if not rx_status():
                break

        pulse_time = end_time - start_time

        if pulse_time > noise_threshold:                 # Filter out noise
            return pulse_time


def starting_time(until_start):                         # Returns starting time from wanted delay
    return time.time() + compensation + until_start     # Second argument empty for no time compensation


def get_num(msg):                                       # Turn sequence received into integer in range 0-255
    for i in range(0, len(msg)):                        # Length of the pulse is compared to threshold and interpreted
        if msg[i] > value_threshold:
            msg[i] = True
        else:
            msg[i] = False

    num = 0
    for i in range(0, len(msg)):
        if msg[i]:
            num += 2**i
    return num                                          # Return integer


def get_char(number):                                   # Turn integer into letter
    if type(number) == list:                            # List of numbers is returned as list of characters
        for i in range(0, len(number)):
            number[i] = chr(number[i])
        return number
    else:
        return chr(number)


if __name__ == '__main__':
    import RPi.GPIO as GPIO
    import time

    # Settings
    pin = 9                                             # Input pin
    compensation = 0.0                                  # Difference in clocks
    pulse = 0.03                                        # Base length for pulses in seconds
    transmission_density = 10                           # Time to wait between bytes
    noise_threshold = 0.015                             # Minimum length for valid signal
    value_threshold = 1.2 * pulse                       # Threshold to choose boolean values from signals
    GPIO.setmode(GPIO.BCM)                              # GPIO configuration
    GPIO.setup(pin, GPIO.IN)

    # Testing program
    word = []
    while True:
        message = wait_msg()
        message = get_num(message)
        message = get_char(message)
        word.append(message)
        if word[-1] == '.':
            print(''.join(word))
            word = []
