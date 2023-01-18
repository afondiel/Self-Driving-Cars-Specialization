# Course 1 - W2 : Self-Driving Hardware and Software Architectures

## Overview 
- System architectures for self-driving vehicles are extremely diverse, as no standardized solution has yet emerged. 
- This module describes both the hardware and software architectures commonly used and some of the tradeoffs in terms of **cost**, **reliability**, **performance** and **complexity** that constrain autonomous vehicle design.
**Course Objectives :**
- Design an omni-directional multi-sensor system for an autonomous vehicle
- Describe the basic architecture of a typical self-driving software system
- Break down the mapping requirements for self-driving cars based on their intended uses.

## MODULE 2: Self-Driving Hardware and Software Architectures

### Lesson 1: Sensors and Computing Hardware
**Sensors** : device that measures or detects a property of the environment, or changes to a/another property overtime.

![self-driving-cars-sensors](./resources/w2/self-driving-cars-sensors.png)

- categorization : 
  - **exteroceptive** : extero=surroundings => they record the property of the environment
  - **proprioceptive** : proprio=internal => they record the property of the `ego-vehicule`

Sensors for perception : 
- `Exteroceptive`
  - **Cameras** : essential for correctly perceiving.
    - *Passive* & light-collecting sensors that are used for capturing rich detailed infromation about a scene
    - Comparison metrics:
      - `Resolution` (quality of the image) : number of pixels that create the image (l x w)
      - `Field of view (FOV)` : the horizontal and vertical angular extent that is *visible* to the camera (depending lens selection and zoom)
      - `Dynamic Range` : the difference btw the **darkest** and **lightest** tones in an image
        - High Dynamic range (HDR) is essential for self-driving vehicles to navigate in variable lighting conditions, particularly at night.
    - Trade-off btw resolution and FOV ?
      - Wilder `field of view` allows a larger viewing region in the environment but fewer pixels that absorb light from one particular object
      - FOV increases, the resolution needs to be increases as well, to still be able to perceive with the same quality
      - other properties that affect perception : 
        - focal length, depth of field and frame rate
        - further explanation **on course 3 : visual perception**
    - Cameras types :
      - Exteroceptive STEREO Camera: the combination of two cameras with overlapping FOVs and aligned image planes.
      - enables depth estimation from image data (synchronized image pairs)
      - Pixel values from image can be matched to the other image producing a disparity map of the scene then be used to estimate depth at each pixel
  - **LiDAR (Light Detection And Ranging)** : involves shooting light beams into the environment and measuring the reflet return
    - by measuring the amount of returned light and time of flight (TOF) of the beam based on intensity and range to the reflecting object can be estimated
    - LIDAR : includes a spinning element with multiple stacked light sources and outputs a detailed 3D scene geometry from LIDAR point cloud
    - Active sensor w/ it's own light sources therefore not affected by the environments lighting
    - different behavior than camera when operating in poor or variable lighting conditions
    - Comparison metrics:
      - **Number of beams** (of sources) : most common sizes 8, 26, 32, 64 
      - **Points per second** : the faster the point collection, the more detailed the 3D point cloud can be.
      - **Rotation Rate** : The higher this rate, the faster the 3D point clouds are updated 
      - **Detection Range** : dictated by the power output of the light source
      - **FOV**
    - Upcoming : Solid state LIDAR ! 
      - High-Resolution Solid-state LIDAR : without a rotational component from typical LIDAR
        - Extremely low-cost and reliable
  - **RADAR (Radio Detection And Ranging)** : old than Lidars and robustly detects **large** objects in the environment
    - They are particularly useful in adverse weather(fog and rain) as they are mostly unaffected by precipitation (poor visibility)
    - Comparison metrics:
      - **Detection Range** 
      - **FOV** 
      - **Position and speed accuracy**
    - Configurations : 
      - Short range : Wide FOV 
      - Long range : Narrow FOV 
  - **ULTRASONIC/SONARS(Sound Navigation and Ranging)** : measures range using sound waves
    - Short-range all weather distance measurement  
    - applications : 
      - good for low-cost parking scenarios, where ego-vehicle needs to make movement very close to other cars
    -  Unaffected by lighting, precipitation
    - Comparison metrics:
      - Range : The maximum Range they can measure
      - FOV :
      - Cost
  
- `Proprioceptive` : 
  - **GNSS (Global Navigation Satellite Systems)** : 
    - GPS (Global Positioning System) with variable Range  : 5 to 10m
    - Galileo : more accurated than GPS
    - GNSS receivers are used to measure ego vehicle position, velocity and heading
      - varying accuracies: RTK, PPP, DGPS
      - the accuracy depends a lot on the actual positioning methods and the corrections used
  
  - **IMU (Inertial Measurement Units)** :   
    - angular rotation rate
    - acceleration 
    - heading (IMU, GPS) : the most important of vehicle control
    - combined measurements can be used to estimate the 3D orientation of the vehicle
  
  - **WHEEL ODOMETRY** : 
    - Tracks wheel velocities and orientation
    - Uses these to calculate overall speed and orientation of car
      - Speed accuracy
      - position drift (heading rate)
      - tracks the mileage on the vehicle

**Computing Hardware** : the most crucial part is the **computing brain** and the main decision making unit of the car
- Takes in all sensor data
- computes actions
- Already existing advanced systems that do self driving car processing
  - Eg : NVIDIA Drive Px/AGX, Intel & Mobileye EyeQ
- computer brain needs both serial and parallel compute modules 
  - Image LiDAR processing: to do segmentation, Object detection, Mapping
    - GPUs : Graphic Processing Unit 
    - FPGAs : Field Programmable Gate Array
    - ASICs: Application Specific Integrated Chip
- HW synchronization : 
  - To synchronize different modules and provide **common clock**
  - sensor measurements must be timestamped with consitent times for `Sensor Fusion` to function correctly
  - GPS relies on extremely accurate timing and act as an appropriate reference clock when available

### Lesson 1 Supplementary Reading: Sensors and Computing Hardware

[The ME597 - Autonomous Mobile Robotics Course at the University of Waterloo](http://wavelab.uwaterloo.ca/sharedata/ME597/ME597_Lecture_Slides/ME597-4-Measurement.pdf)

### Lesson 2: Hardware Configuration Design

    - Sensor coverage requirement for different scenarios : 
      - Highway driving
      - Urban driving
    - Overall coverage, blind spots
**Assumptions** : we define the deceleration driving which will drive the detection ranges need for the sensors

- Aggressive deceleration  = 5 m/s^2 
  - when breaking hard in case of emergency
- Comfortable deceleration = 2 m/s^2
  - This is the norm, unless otherwise stated 
>-  ## Stopping distance: **$\frac{v^2 }{2a}$**

    where : d - the distance
            v - the vehicle velocity
            a - the rate of of deceleration

**Where to place sensors ?**
- Need sensors to support maneuvers within ODD 
  - ODD our system can produce decision for
  - We shall be able to provide all of the decision with suffient input
- Broadly, we have two driving environments
  - Highway driving
  - Urban driving

|--| Highway | Urban/Residential|
|--|--|--|
|Traffic Speed |High|Low - Medium|
|Traffic Volume |High|Medium - High|
|# of lanes|More |2-4 typically|
|Other features|Fewer, gradual curves; merges|Many turns and intersections|

`Highway Analysis` : 
- Broadly, 3 kinds of maneuvers : 
  1. Emergency Stop : 
  - Longitudinal Coverage : If there is a blockage ahead, we want to stop in time 
   - Applying the stopping distance eq : `v  = 120 kmph => d = 110 m` (aggressive deceleration)
   - Most self-driving cars aim for a stopping distance btw `150 - 200m`in front of vehicle as result
  - Lateral Coverage : To avoid collision, either we stop or change lanes
    - At least adjacent lanes (3.7 meterss wide in North America), since we may change lanes to avoid a **hard stop**
  
  2. Maintain Speed : relative speeds are typically less than 30kmph
  - Longitudinal Coverage :
    - `2s`is the reaction time in Nominal conditions for human drivers: 2s (it can be accessible in aggressive deceleration of vehicle in front and the our ego-vehicle behind)
    - At 120kph ==> 165m are needed to have at least 100m in front
    - Both vehicles are moving, so don't need to look as far as emergency-stop case

  - Lateral Coverage : Maintain speed with merge 
    - Usually current lane (ego-vehicle)
    - Adjacent lanes would be preferred for merging vehicle detection 
    - A wide 160 to 180 degree FOV is required to track adjacent lanes and a range of 40 to 60m is needed to find space btw vehicles
    - 
  3. Lane Change
   - We want to move safely to an adjacent lane (left or rigth)
   - Logitudinal coverage : Need to look forward to maintain a safe distance from the leading vehicle
     - But also needs to look behind to look what others vehicles are doing
     - We need to look not just in the adjacent lanes, but probably further
   - Lateral Coverage : Need wider sensing 
     - What if ? Other vehicle attemps to maneuver lane at the same time as we do?
       -  We'll need to coordinate our lane changes room maneuvers so we don't crash
    -  The requirements are equivalent to those in the maintain speed scenario : front, behind and side of ego-vehicle
- Overall Coverage highway

![sensor overall coverage](./resources/w2/overallcoverage-sensors.png)

`Urban Aanalysis`
- Broadly, 6 kinds of maneuveres: 
  1. Emergency Stop
  2. Maintain Speed
  3. Lane Change
    - same as the highway, but since we're not moving as quickly we don't need the same extent for our long-range sensing

  4. Overtaking 
    - Longitudinal converage : 
      - If overtaking a parked or moving the vehicle (wide short-range), need to detect oncoming traffic (narrow long-range) beyond point of return to own lane
    - Lateral coverage : 
      - Always need to observe adjacent lanes
        - Need to observe additianl lanes if other vehicles can move into adjacent lanes


  5. Turning, crossing at intersections
     - Intersections : 
       - Observe behoyond intersection for approaching vehicles, pedestrian crossings, clear exit lanes
       - Requires near omnidirectional sensing for arbitrary intersection angles

  6. Passing roundabouts(rondpoints)
    - Longitudinal coverage :
      -  Due to the shape of the roundabout, need a wider FOV
    - Lateral coverage : 
      - Vehicles are slower than usual, limited range requirement 

- Overall Coverage urban
  
![overallcoverage-sensors-urban](resources/w2/overallcoverage-sensors-urban.png)

Cost and blind spots : 
The final choice of configuration also depends on : 
- requiremnt of operating conditions
- sensor redundacy due to failure and budgets

### Lesson 2 Supplementary Reading: Hardware Configuration Design

- [K.J. Bussemaker's master's thesis: Sensing requirements for an automated vehicle for highway and rural environments](https://repository.tudelft.nl/islandora/object/uuid:2ae44ea2-e5e9-455c-8481-8284f8494e4e)


### Lesson 3: Software Architecture
### Lesson 3 Supplementary Reading: Software Architecture



### Lesson 4: Environment Representation
### Lesson 4 Supplementary Reading: Environment Representation


### The Future of Autonomous Vehicles