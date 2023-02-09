from time import process_time
import socket

from numpy import array

class Robot:
    def __init__(self , diameter , rpm , trackWidth , cof):
        """"
        :param diameter: Wheel diameter in mm
        :param rpm: RPM of the motor
        :param trackWidth: Track width in mm
        :param cof: Coefficient of friction between wheels and surface
        """
        self.diameter = diameter/1000 #m
        self.rpm = rpm 
        self.perimeter = 3.142*(self.diameter) #m
        self.DistancePerMinute = (self.perimeter*rpm) #meter per minute
        self.speed = (self.perimeter*rpm)/60  #m/s
        self.trackWidth = trackWidth/1000 #m
        self.coeffOfFriction = cof 
    def TimeforDistance (self,distance):
        ''' 
        :param distance: distance in m
        '''
        timeInSeconds = ( distance / self.speed) #sec
        return timeInSeconds
    def TimeForRotation (self,degrees):
        radian = (3.142*degrees)/180
        distanceRequired = ((self.trackWidth/2)*radian) # m
        timeInSeconds = ( distanceRequired / self.speed)
        finalTime = timeInSeconds / (1 - self.coeffOfFriction)
        return finalTime

WheelDiameter = 70
TrackWidth = 238
COF = 0.8 # Coefficient of Friction between rubber and concrete
botRotate = Robot(WheelDiameter,100,TrackWidth,COF)

timeReq = botRotate.TimeForRotation(360)
print('\nParameter                   : ',botRotate.perimeter,'m')
print('speed                       : ',botRotate.speed,'m/s')
print('Time for 1 meter [sec]      : ',botRotate.TimeforDistance(1),'sec')
#print('dist for 360 deg. [meter]   : ',botRotate.TimeForRotation(360),'m')
print('time for 360 rotation [sec] : ',timeReq,'sec\n')

""" degreee = int(input('Enter Degree [0 < deg < 180] : '))
if degreee >= 0 and degreee <= 180:
    percentage = (degreee / 180) * 100
    print('Percentage Revolution :',percentage)
    duty = (percentage/10) + 2
    print('Duty Cycle will be',duty) """
hostname = 'LAPTOP-OD010PRQ'
print(socket.gethostbyname('LAPTOP-OD010PRQ'))

