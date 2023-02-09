class Robot {
    /**
    *@param {float} diameter Diameter of the Wheel in mm(millimeter).
    *@param {float} rpm RPM of the motors.
    *@param {float} trackWidth Trackwidht of robot in mm(millimeter).
    *@param {float} cof Coefficient of friction between wheels and surface.
    *@returns
    */
    constructor(diameter , rpm , trackWidth , cof){
        this.diameter = diameter/1000;
        this.rpm = rpm;
        this.trackWidth = trackWidth/1000;
        this.cof = cof;
        this.perimeter = 3.142*(this.diameter);
        this.speed = (this.perimeter*rpm)/60;
    }

    /**
     * 
     * @param {float} Dist Distance to be travelled straight in Meters  
     * @returns 
     */
    DistanceToTime(Dist){
        return Dist / this.speed;        
    }

    /**
     * 
     * @param {int} rot Clockwise Rotation in Degrees.
     * @returns 
     */
    RotationToTime(rot){
        return ((((this.trackWidth/2)*((3.142*parseFloat(rot))/180)) / this.speed)) / (1 - this.cof)
    }
}


bot =  new Robot(70,100,238,0.8)

class ScanVicinity {
    /**
     * 
     * @param {int} numberOfStops Number for stops in scanning.
     * @param {float} StepLength Distance between each stop in meter.
     * @param {int} NumberOfCameraPositions Number of Camera Positions to be scanned in 180 deg.
     * @param {int} stepTimeForCamera Time between switching camera position in seconds.
     */
    
    constructor(numberOfStops,StepLength,NumberOfCameraPositions,stepTimeForCamera){
        if(numberOfStops < 0 || StepLength < 0 || NumberOfCameraPositions < 0 || stepTimeForCamera < 0){
            throw '[ERROR] : Values cannot be negative'
        }else if ( NumberOfCameraPositions < 1 ){
            throw '[ERROR] : Number of camera positions should be greater than 0'
        }
        this.numberOfStops = parseInt(numberOfStops);
        this.StepLength = parseFloat(StepLength);
        this.NumberOfCameraPositions = parseInt(NumberOfCameraPositions);
        this.stepTimeForCamera = parseInt(stepTimeForCamera);
        this.scnnedSteps = 0;
        this.isScanAborted = false;
        this.CurrentServoAngle = 0;
    };

    StartScan(){
        console.log(`
        this.numberOfStops = ${this.numberOfStops};
        this.StepLength = ${this.StepLength};
        this.NumberOfCameraPositions = ${this.NumberOfCameraPositions};
        this.stepTimeForCamera = ${this.stepTimeForCamera};
        this.scnnedSteps = ${this.scnnedSteps}
        `)
        console.log('[SCAN] Time for step (cal.) : ',bot.DistanceToTime(this.StepLength))
        this.Scan()
        
    }
  
    /**
     * 
     * @param {int} angle Angle at which servo motor needs to be directed. 
     */
    cameraposition(angle){
        //skt.emit('servocontrol',angle);
        console.log('[EMIT] Servo Angle' , angle)
    };

    Scan(){
        var minimumAngle = 180/this.NumberOfCameraPositions;
        var angles = [];
        for(var i=1;i<this.NumberOfCameraPositions+1;i++){
            angles.push(minimumAngle*i);
            //console.log(`Cal. Camera step ${i} = ${minimumAngle*i} deg`);
        };
        var currentCameraPosition = 0;
        console.log('Cal, angles : ' + angles)
        console.log(angles)
        this.cameraposition(0);
        var loop = setInterval(()=>{
            if(this.isScanAborted == false){
                if(currentCameraPosition < this.NumberOfCameraPositions){
                    
                    this.cameraposition(angles[currentCameraPosition]);
                    this.CurrentServoAngle = angles[currentCameraPosition]
                    console.log('[SCAN] Camera Position : ',currentCameraPosition,' at angle :',angles[currentCameraPosition])
                    currentCameraPosition++;
                }
                else{
                    clearInterval(loop)
                    console.log('[SCAN] moving Ahead ')
                    this.movestepahead()
                }
            }
            if(this.isScanAborted == true){
                clearInterval(loop)
            }
        },this.stepTimeForCamera*1000)
    };

    movestepahead(){
        console.log('[SCAN] Scanned positions : ',this.scnnedSteps)
        if(this.isScanAborted == false){
            if(this.scnnedSteps < this.numberOfStops){
                this.scnnedSteps++;
                console.log('[EMIT] Forward')
                //skt.emit('keypress','w')
                setTimeout(() => {
                    //skt.emit('keyup');
                    console.log('[EMIT] Stop')
                    this.Scan()
                }, bot.DistanceToTime(this.StepLength)*1000);
            }else{
                console.log('SCANNING DONE')
            }
        }
    }

    /**
     * 
     * @returns Last recorded position of servo motor.
     */
    AbortScan(){
        this.isScanAborted = true;
        //skt.emit('keyup');
        this.cameraposition(90)
        console.log('[SCAN] ---Canceled by user--- ')
        return this.CurrentServoAngle
    }

}

scan1 = new ScanVicinity(2,1,10,1)
scan1.NumberOfCameraPositions = 20
console.log(scan1.NumberOfCameraPositions)

scan1.StartScan()

/* setTimeout(() => {
    scan1.AbortScan()
}, 4000); */