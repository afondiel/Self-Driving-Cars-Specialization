# Course 1 - W7 - MODULE 7: Putting it all together

## Overview 

- For the last week of the course, now you will get hands on with a simulation of an autonomous vehicle that requires longitudinal and lateral vehicle control design to track a predefined path along a racetrack with a given speed profile. - You are encouraged to modify the speed profile and/or path to improve their lap time, without any requirement to do so. Work and play!

**Learning Objectives**
- Integrate vehicle modeling and controller design into a complete vehicle control system
- Develop a working simulation with a python-based vehicle autonomy agent
- **Tune** a control system for tracking performance on a complex path

## Final Project: Self-Driving Vehicle Control

### Lesson 1: Carla Overview - Self-Driving Car Simulation

- test & simulation? 
- realistic self-driving car environment for testing self-driving cars
- allows to make sure our vehicle operates safely before step to it
- in simulator we can test all our modules together or independently: 
  - perception
  - planning
  - control
- we can run sophisticated scenarios involving many AI controller vehicles and pedestrians, in multiples variations to ensure the vehice consitently make the correct decision.
- Most importanly, we can test our car in a situation that would be too `dangerous` for us to test on actual roads.

**CARLA**
- Opensource Simulator developed at the Autonomous University of Barcelona by the Computer Vison Center, Intel and Toyota Research Institute and built using the **Unreal Game Engine (UGE)**

- Features : 
  -  detailed virtual worlds with roadways, buildings, weather, and vehicle and pedestrian agents.
  -  Images of these environments can be captured in various formats  : 
    - depts maps and segmented images which 
- The entire simulation can be controlled with an **external client** which can be used to send cmds to the vehicle, record data and automatically execute scenarios for evaluating the performance of the car.

- A modified version of CARLA is used for the purpose of this Specialization.
  - Carla can be customized to create a specific scenario or environment

### Lesson 1 Supplementary Reading: Carla Overview - Self-Driving Car Simulation

You can read more about CARLA and its original paper, listed in the PDF below:

- You can also find the original source code at this link: 
  - https://github.com/carla-simulator/carla/

- If you're interested in learning about the Unreal Engine, check out this link: 
  - https://www.unrealengine.com/en-US/features


### CARLA Installation Guide

You can access instructions to install CARLA in the PDF document attached below, along with the necessary files.

Please note that the CARLA binaries used here are a modified version of the original CARLA with additional maps included, so please use these binaries when working on the assignments.

**Linux (Ubuntu 16.04 or later)**
Download both the CARLA Setup Gude (Ubuntu).pdf and CarlaUE4Ubuntu.tar.gz files. 

Read the PDF guide to setup and test the CARLA binaries and example clients for Linux.

**Windows 7 (64-bit) or later**
Download both the **CARLA Setup Gude (Windows x64).pdf** and **CarlaUE4Windows.zip** files. 

Read th e PDF guide to setup and test the CARLA binaries and example clients for **Windows**.

**MacOS**
At this time macOS is not natively supported by CARLA and therefore the CARLA binaries that we provide also do not support macOS. It is recommended to create a dual-boot to either Linux or Windows in order to setup CARLA for the course.

Resources: 

**Install Windows on your Mac with Boot Camp** - https://support.apple.com/en-ca/HT201468

**Dual-Boot between Ubuntu and MacOS** - https://help.ubuntu.com/community/MactelSupportTeam/AppleIntelInstallation

There are other online resources that can assist you with creating a dual boot for Windows or Ubuntu. Feel free to search for these sites on your prefered web browser.

**Virtual Machines**

Virtual Machines are discouraged as they generally do not have the necessary hardware virtualization to run the Unreal Engine (which CARLA is based on). It is recommended to install Linux or Windows directly as a dual boot in order to setup CARLA for the course.


### Lesson 2: Final Project Overview

- `input` :
  - the track is a loop circuit
    - sorted list of waypoints equally spaced on the track
      - contain both position and speed 
      - waypoint become the `reference signal` for the controller and navigating to all waypoints to complete the full track
  -  => implementation of `Longitudinal` and `Lateral control` is needed to control the vehicle
  
- `output` :
  - throttle
  - brake
  - steering angle 

- for final grade provide : 
  - trajectory.txt file


### Final Project: Self-Driving Vehicle Control
### Final Project Solution

Congratulations ! 

## References
- CARLA Documentation : 
  - https://carla.readthedocs.io/en/stable/
## Appendices
- CARLA simulator keyboard shortcut : 
  - https://carla.readthedocs.io/en/stable/simulator_keyboard_input/  

- Building a race track in the CARLA simulator : 
  - https://www.youtube.com/watch?v=MM4IrPoBtXs
