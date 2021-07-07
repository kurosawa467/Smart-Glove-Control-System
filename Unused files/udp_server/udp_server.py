import socket
import RPi.GPIO as GPIO

# setup GPIO Pins
pin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

# bind all IP
HOST = '****' 
# Listen on Port 
PORT = 44444 
#Size of receive buffer   
BUFFER_SIZE = 1024    
# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the host and port
s.bind((HOST, PORT))
while True:
    # Receive BUFFER_SIZE bytes data
    # data is a list with 2 elements
    # first is data
    #second is client address
    data = s.recvfrom(BUFFER_SIZE)
    if data:
        #print received data
        print('Client to Server: ' , data)
        message = data[0].decode('utf8')
        if message == "yes":
            print("yes")
            GPIO.output(pin,True)
        else :
            print("no")
            GPIO.output(pin,False)
        
        # Convert to upper case and send back to Client
        s.sendto(data[0].upper(), data[1])
# Close connection
s.close()

GPIO.cleanup()