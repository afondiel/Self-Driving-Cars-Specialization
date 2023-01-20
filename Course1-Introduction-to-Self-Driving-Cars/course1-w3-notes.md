# Course 1 - W3 - MODULE 3: Safety Assurance for Autonomous Vehicles

## Overview 

- As the self-driving domain matures, the requirement for safety assurance on public roads become more critical to self-driving developers. 
- You will evaluate the challenges and approaches employed to date to tackle the immense challenge of assuring the safe operation of autonomous vehicles in an uncontrolled public road driving environment.

**Learning Objectives**
- Assess the primary contributions to the overall safety system for self-driving cars
- Investigate the main causes of prominent autonomous driving failures recorded to date
- Employ safety assessment methods for analysis of specific scenarios and hazards for self-driving.
- Describe analytical and empirical approaches to safety assessment.


## Safety for Self-driving Cars

### Lesson 1: Safety Assurance for Self-Driving Vehicles
**Examples of Automated Vehicle Crashes** 
-  March 2016 : A Self-Driving Car (now Waymo) ran into side of the bus
    - Causes : lateral distance btw the bus and the self-driving car lane was too narrow (bad estimation/computing by the self(driving sw))
    - Due of that, the self-driving car thought the bus wouldn't pass/overtake
    - By the time the car computes a new measuremnt was too late to react


- In 2017 : Uber self-driving vehicle overreacted during a minor collision caused by the another car and ended up overturning
  - Causes : The dynamic models don't assume disturbance forces from other vehicles acting on the car 
  - Integration of robustness into the control system
  - More exploratory testing that covers as many foreseeable events as possible


- Late 2017 (Law Suit Case) : A GM Cruise Chevy Bolt knocked over a motorcyclist afer it aborted a lane change maneuver
  - Causes : gap in adjacent lane closed rapidly and vehicle aborted the maneuver and knocked over the motorcyclist
  - During the abort the motorcyclist was alrealy forward alongside the vehicle and the vehicle was stuck in a dilemma to colide w/ the motorcyclist or to crash into both cars in the adjacent lane
  - The vehicle didn't anticipate this scenario and knocked over the motorcyclist 
  - Unexpected/Future events still a big decision-making challenge in self-driving cars

- March 2018 : Uber self-driving Taxi fatal accident in Arizona. As consequence of that Uber suspended his self-driving cars testing for a while
  - Causes : the incident occured on a wide multilane divided road at night where a pedestrian was walk her bicycle across the street in an unmarked area
  - Multiple Thing Gones Wrong : 
    - No real time checks on safety drivers (no real-time monitoring system)
    - After the woman was detected on the road (6 sec before the impact)
      - first classified as unkown object
      - the misclassified as a vehicle 
      - then a bicycle
    - Possible assumption : the vehicle aborted the detection because too unreliable
    - 1.3 sec before, Volvo system tried to do emergency braking maneuver
      - The Volvo system wa disable by Uber when in autonomous mode because not possible to have multiple collision avoidance systems operating simultaneouly during the testing
    
    - In Summary :  `Perception system failure` & `planning system` to avoid the detective object even though its class was uncertain & lack of human or emergency braking backup




### Lesson 1 Supplementary Reading: Safety Assurance for Self-Driving Vehicles
### Lesson 2: Industry Methods for Safety Assurance and Testing
### Lesson 2 Supplementary Reading: Industry Methods for Safety Assurance and Testing
### Lesson 3: Safety Frameworks for Self-Driving
### Lesson 3 Supplementary Reading: 
  - Safety Frameworks for Self-Driving
  - How Many Miles of Driving Would It Take to Demonstrate Autonomous Vehicle Reliability?

## Learning from Industry Expert

- OK