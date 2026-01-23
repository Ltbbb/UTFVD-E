import smbus
import time
import struct


ARDUINO_I2C_ADDRESS1 = 0x08
ARDUINO_I2C_ADDRESS2 = 0x09
NUM_CHANNELS = 8
# Define the struct format for sending and receiving data
# '4B' for 4 uint8_t values followed by '4H' for 4 uint16_t values
# '<' indicates little-endian byte order
STRUCT_FORMAT = '<' + 'B' * NUM_CHANNELS + 'H' * NUM_CHANNELS

# Function to write data to Arduino
def write_data(data,addr):
    try:
        bus = smbus.SMBus(1)
        bus.write_i2c_block_data(addr, 0, list(data))
        time.sleep(0.2)  # Sleep to allow Arduino to process the data
        return True
    except Exception as e:
        print(f"Error writing data to Arduino: {e}")
        return False
    
# Function to read data from Arduino
def read_data(addr):
    try:
        bus = smbus.SMBus(1)
        data = bus.read_i2c_block_data(addr, 0, struct.calcsize(STRUCT_FORMAT))
        return struct.unpack(STRUCT_FORMAT, bytes(data))
    except Exception as e:
        print(f"Error reading data from Arduino: {e}")
        return None
    
#send the pwm values and channels
# Prepare data to send
def send_to_arduino(pwm):
	channels = [i for i in range(NUM_CHANNELS)]  # Example channel values
	pwm_values = [pwm] * NUM_CHANNELS #8 LED configuration, all LEDs on
    
	pwm_bytes=[pwm.to_bytes(2, byteorder='little') for pwm in pwm_values]
	data_to_send = bytes(channels) + b''.join(pwm_bytes)
	#data_to_send=channels+pwm_bytes
	print("data to send: ", list(data_to_send))
	# Write data to Arduino
	try_send(data_to_send, ARDUINO_I2C_ADDRESS1)
	try_send(data_to_send, ARDUINO_I2C_ADDRESS2)
	

def try_send(data_to_send, address):
    if write_data(data_to_send,address):
        print(f"Data sent successfully to {address}.")

		# Read back data from Arduino
        received_data = read_data(address)
        if received_data:
            print("Received data from Arduino pcb:")
            print("Channels:", received_data[:NUM_CHANNELS])
            print("PWM Values:", received_data[NUM_CHANNELS:])
    else:
	    print(f"Failed to send data to {address}.")