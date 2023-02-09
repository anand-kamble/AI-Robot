import socket

hostname = socket.gethostname()
print('My HostNmae : %s' %hostname)
local_ip = socket.gethostbyname('raspberrypi.local')
print('my IP : %s' %local_ip)