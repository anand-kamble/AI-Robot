import socket

skt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

PORT = 5000

robotIP = socket.gethostbyname('raspberrypi')

skt.bind(('',PORT))

print('Binded')

skt.listen(5)

while True:
     
# Establish connection with client.
  c, addr = skt.accept()    
  print ('Got connection from', addr )
 
  # send a thank you message to the client. encoding to send byte type.
  c.send('Thank you for connecting'.encode())
 
  # Close the connection with the client
  c.close()
   
  # Breaking once connection closed
  break