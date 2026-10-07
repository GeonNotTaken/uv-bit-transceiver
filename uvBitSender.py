import time
import array
import board
import digitalio

# Define the transmitter and receiver idle states during a period with no communication.
TX_IDLE_VALUE = False
RX_IDLE_VALUE = True

# Define the duration of a single bit in seconds.
BIT_DURATION = 0.005
HALF_BIT_DURATION = BIT_DURATION / 2

# Define the length of a message in bits.
MSG_BITS = 8

# Minimum number of idle bits before a start bit.
MIN_IDLE_BITS = MSG_BITS + 1

# Configure the receive digital input.
RX = digitalio.DigitalInOut(board.GP20)
RX.direction = digitalio.Direction.INPUT
RX.pull = digitalio.Pull.UP if RX_IDLE_VALUE else digitalio.Pull.DOWN # Idle when disconnected

# Configure the transmit digital output.
TX = digitalio.DigitalInOut(board.GP22)
TX.direction = digitalio.Direction.OUTPUT

# Configure the transmit indicator LED.
LED = digitalio.DigitalInOut(board.GP21)
LED.direction = digitalio.Direction.OUTPUT

def transmit(msg):
    assert len(msg) == MSG_BITS
    # Add the minimum number of idle bits then a start bit.
    prologue = [TX_IDLE_VALUE] * MIN_IDLE_BITS + [not TX_IDLE_VALUE]
    data = [TX_IDLE_VALUE if not bit else not TX_IDLE_VALUE for bit in msg]
    # Allocate and fill an efficient array of the bits to transmit.
    bits_array = array.array('B', prologue + data)
    #print('Start message')
    for k, bit in enumerate(bits_array):
        TX.value = LED.value = bit
        #print(f'bit[{k}] = {bit}')
        time.sleep(BIT_DURATION)
    # Leave the bus in the idle state.
    TX.value = TX_IDLE_VALUE
    
def receive():
    # Allocate an efficient array of the received bits.
    bits_array = array.array('B', [0] * MSG_BITS)
    # Loop until we find a valid start bit.
    while True:
        # Wait for the bus level to be RX_IDLE_VALUE (if it isn't already)
#         while TX.value != RX_IDLE_VALUE:
#             print(TX.value)
#         print('idle start')
        # Keep checking for RX_IDLE_VALUE for the minimum idle period.
        wait_until = time.monotonic() + MIN_IDLE_BITS * BIT_DURATION
        while wait_until > time.monotonic():
            pass        
#         print('min idle completed')
        while RX.value == RX_IDLE_VALUE:
                pass
#         print('got start bit')
        break
    # Delay for half a bit.
    time.sleep(HALF_BIT_DURATION)
    # Sample each bit at its nominal center time.
    for i in range(MSG_BITS):
        time.sleep(BIT_DURATION)
        LED.value = bits_array[i] = (RX.value != RX_IDLE_VALUE)
        print(bits_array[i])
    return bits_array


def char_to_bits(char, nbits=8):
    """Encode a single character as a sequence of nbit binary values
    representing its numeric code, starting with the least-significant bit.
    """
    value = ord(char)
    binary = bin(value)
#     print(value)
    binary = ''
    for i in range(nbits):
        binary += str((value >> i) & 1)
    return binary

def bits_to_char(bits, nbits=8):
    """Decode a sequence of nbit binary values back to a character.
    """
    value = 0
    for i, bit in enumerate(bits):
        value |= int(bit) << i  # Reconstruct value bit by bit
    return chr(value)


def send_text(text):
    """Send each character of the text then 8 zeros.
    """
    for char in text:
        transmit([int(b) for b in char_to_bits(char)])  # Convert string to list of ints
    # Transmit 8 zeros to signal that we are done.
    transmit([0] * 8)
    
def get_text():
    """Get characters until we see 8 zeros.
    """
    text = ''
    while len(text) < 128:
        bits = receive()
        if any(bits):
            text += bits_to_char(bits)
        else:
            # Got 8 zeros so we are done.
            return text
        
msg = 'Hello World'

while True:
    # Uncomment the first line in the untethered Pico or the second in the Pico connected via USB.
#     send_text(get_text().upper())
    #print('>>', msg); send_text(msg); print('<<', get_text()); time.sleep(0.5)
    send_text(msg)
#     print(get_text())







