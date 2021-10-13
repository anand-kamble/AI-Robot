<div align="center">
  <h1>AI Robot</h1>
  <h3>This project is in devolopment.</h3>
</div>

## v2.0  
This version of the project can be deployed on Internet. It includes Server files in the folder named [Server](/v2.0/server/) which are deployed on Heroku and Client files in the [Client folder](/v2.0/Client/). The Clients file are to be run on RaspberryPi, before running make sure RaspberryPi has an active internet connection. Run the following command to start the program on RaspberryPi.
```
python3 client.py
```
RaspberryPi will connect to the server and the server will broadcast to every user connected that the robot has connected along with it's name on a web page can be accessed by going to the server Url.   
  
### Connecting to the Robot 
Go to the [server Url](https://airobotserver.herokuapp.com/) using a browser like Chrome, Safari, Edge. If Any robots are online you will be able to see it's Display name on screen.
In order to connect to the robot user must enter the password for that robot. Then click on Connect Button next to it.  
  
![](https://raw.githubusercontent.com/anand-kamble/AI-Robot/master/v2.0/docs/Screenshot%20(146).png)
  
Once Connected, You can see the live Feed from Robots Camera in the center. You can also monitor the latency between the robot and your machine in the left column below the name of the robot.  
Here you can control the movement of the Robot by using the controls specified on the page.  
  
![](https://raw.githubusercontent.com/anand-kamble/AI-Robot/master/v2.0/docs/Screenshot%20(147).png)
  
### Requirements for v2.0  
python - 3.9.7^  
opencv-python - 4.5.3.56^  
python-socketio - 5.4.0^  
<hr />  

## v1.0  
This is the first version of code devoloped for robot. Used mostly for testing purpose, running on a RaspberryPi it creates a Web Server on Local Area Network. Users connected to this network can connet to RaspberryPi with it's LocalIP entered as URL in browsers like Chrome, Safai, Microsoft Edge. Users are able to watch the live feed from the robots camera and can also control the movement of the robot. 
![](https://raw.githubusercontent.com/anand-kamble/AI-Robot/6e9f8718679a5712326926747d3a9c631b79bbc3/v1.0/docs/Screenshot%20(145).png)  
  
### Requirements for v1.0  
python - 3.9.7^  
opencv-python - 4.5.3.56^  
Flask - 2.0.1^  
