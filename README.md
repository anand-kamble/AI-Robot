<div align="center">
  <h1>AI Robot</h1>
</div>

## Tutorial

### On RaspberryPi

Copy the Raspberry.py file in RaspberryPi
and run it by using command

```
python Raspberry.py
```

Simultaneously, we need to start the server.  
for running the server,

### On Linux

Run the start.sh file by

```
./start.sh
```

### On Windows

Run the start.bat file by

```
start.bat
```

After successful execution of the program, it will automatically open the UI in the default browser of the system.

In case the connection of the robot to server fails, please check the serverUrl in the Raspberry.py matches the url server actually running on, which is displayed when localServer.py file is executed.

---

## Publications

Materials Today: Proceedings - Elsevier  
[Object following robot based on AI/ML](https://www.sciencedirect.com/science/article/pii/S2214785322064185)

---

## Changelog

### v6.0

Added support for PiCamera improving performance of image processing.

### v5.0

Improved stability and optimizations over version 4.0

### v4.0

Introducing Scanning feature in this version which scans the vicinity around the robot and if it detects the desired object or human it will store the direction in which it has seen it. And after we command it to follow, it will turn the robot in that direction and start following the object. This version also includes improvements and bug fixes in Client User Interface.

> File named Raspberry.py should be executed on the RaspberryPi.

### Requirements for v4.0

python - 3.9.7^  
opencv-python - 4.5.3.56^  
python-socketio - 5.4.0^

### v3.0

The robot can now follow a bottle in its sight by tracking the position of the bottle in image and deciding the direction to move in. This version has also added safety features to prevent collision using Ultrasonic sensor.

### v2.0

This version of the project can be deployed on Internet. It includes Server files in the folder named [Server](archives/v2.0/server/) which are deployed on Heroku and Client files in the [Client folder](archives/v2.0/Client/). The Clients file are to be run on RaspberryPi, before running make sure RaspberryPi has an active internet connection. Run the following command to start the program on RaspberryPi.

```
python3 client.py
```

RaspberryPi will connect to the server and the server will broadcast to every user connected that the robot has connected along with it's name on a web page can be accessed by going to the server Url.

### Connecting to the Robot

Go to the [server Url](https://airobotserver.herokuapp.com/) using a browser like Chrome, Safari, Edge. If Any robots are online you will be able to see it's Display name on screen.
In order to connect to the robot user must enter the password for that robot. Then click on Connect Button next to it.

![](<archives/v2.0/docs/Screenshot%20(146).png>)

Once Connected, You can see the live Feed from Robots Camera in the center. You can also monitor the latency between the robot and your machine in the left column below the name of the robot.  
Here you can control the movement of the Robot by using the controls specified on the page.

![](<archives/v2.0/docs/Screenshot%20(147).png>)

### Requirements for v2.0

python - 3.9.7^  
opencv-python - 4.5.3.56^  
python-socketio - 5.4.0^

<hr />

## v1.0

This is the first version of code devoloped for robot. Used mostly for testing purpose, running on a RaspberryPi it creates a Web Server on Local Area Network. Users connected to this network can connet to RaspberryPi with it's LocalIP entered as URL in browsers like Chrome, Safai, Microsoft Edge. Users are able to watch the live feed from the robots camera and can also control the movement of the robot.
![](<https://raw.githubusercontent.com/anand-kamble/AI-Robot/6e9f8718679a5712326926747d3a9c631b79bbc3/v1.0/docs/Screenshot%20(145).png>)

### Requirements for v1.0

python - 3.9.7^  
opencv-python - 4.5.3.56^

### Contributors

[Anand Kamble](https://anand-kamble.github.io/)  
[Aniket Tathe](https://www.linkedin.com/in/aniket-tathe-458793200/)
