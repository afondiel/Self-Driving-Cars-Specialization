# Course-2 - W4 - MODULE 4 : LIDAR Sensing 

## Overview 

- LIDAR (light detection and ranging) sensing is an enabling technology for self-driving vehicles. LIDAR sensors can ‘see’ farther than cameras and are able to provide accurate range information. 
- This module develops a basic LIDAR sensor model and explores how LIDAR data can be used to produce point clouds (collections of 3D points in a specific reference frame). 
- Learners will examine ways in which two LIDAR point clouds can be registered, or aligned, in order to determine how the pose of the vehicle has changed with time (i.e., the transformation between two local reference frames).

**Learning  Objectives**

- Explain how LIDAR sensors are able to generate range data from time-of-flight measurements
- Understand inverse and forward sensor models for a basic scanning LIDAR
- Apply standard transfomations (translation, rotation, and scaling) to LIDAR point cloud data
- Summarize how the problem of motion distortion can affect LIDAR scans acquired from a moving vehicle
- Utilize the iterative closest point (ICP) algorithm to align point clouds from consecutive LIDAR scans

## LIDAR Sensing 

- LIDAR has been an enabling technology for self-driving cars because it can see in all directions and is able to provide very accurate range information. 

- In fact, with few exceptions, most self-driving cars on the road today are equipped with some type of LIDAR sensor.

### Lesson 1: Light Detection and Ranging Sensors (LIDAR)

- Some self-driving cars equiped with LiDAR
  
<img src="./resources/w4/img/l1-lidar-waymo.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

Waymo

<img src="./resources/w4/img/l1-lidar-uber.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

Uber 

- LiDAR job is to provide detailed 3D scans (mapping) of the environment around the vehicle.
- Other applications : Rototics

They can be found in many different shapes and sizes as well as for different applications: from measuring the distance to a single point, a 2D slice of the world or perform a full 3D scan

Some of the most popular models/brand used today : 
- **Velodyne** (in California, USA)  
<img src="./resources/w4/img/l1-lidar-velodyne.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- **Hokuyo** in Japan and **SICK** in Germany 
  
<img src="./resources/w4/img/l1-lidar-hokuyo-sick.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

For the purpose of this course we will using the Velodyne LiDAR but the basic techniques applied to other types of LiDARs too

**Measuring Earth, Sea and Sky**

- LiDAR was originated in the 1960s shortly after the invention of the laser
  
<img src="./resources/w4/img/l1-lidar-meteo.png" width="280" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- First used by meteorologists to clouds, but these ground-based celiometers are still in use today not only to measure water cloud but also to detect volcanic ash and air polution

- Airborne LiDAR sensors are commonly used today to survey and map the earth's surface for agriculture, geology, military, and other uses

<img src="./resources/w4/img/l1-lidar-mapping.png" width="300" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The first application that brought LiDAR into public consciousness was Apollo 15
- the fourth manned mission to land on the moon, and the first to use a laser altimeter to map the surface of the moon.

<img src="./resources/w4/img/l1-lidar-apollo15.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Measuring Distance with Time-of-Flight**

- LiDAR can be used to measure distances and create a certain type of map, but how it works in context of self-driving cars ? 
- To build a basic LIDAR in 1D, 3 components are needed : 
1. A laser
2. A photodetector
3. A very precise stop watch

<img src="./resources/w4/img/l1-lidar-dist-measurement0.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The laser first emits a short pulse of light usually in the near infrared frequency band along some known ray direction
- At the same time the stopwatch starting counting
- The laser pulse travels outwards from the sensor at the speed of light and hits a distant target (It maybe another vehicle in front of us on the road or a stationary object like a stop sign or a building.)

<img src="./resources/w4/img/l1-lidar-dist-measurement1.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- As long as the surface of the target isn't too polished or shiny, the laser pulse will scatter off the surface in all directions, and some of that reflected light will travel back along the original ray direction. 


<img src="./resources/w4/img/l1-lidar-dist-measurement2.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The photodetector catches that return pulse and the stopwatch tells you how much time has passed between when the pulse first went out and when it came back. 

<img src="./resources/w4/img/l1-lidar-dist-measurement3.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">


- That time is called the **round-trip time**. 
- Now, we know the speed of light, which is a bit less than 3x$10^8 m/s$.
- So, we can multiply the speed of light by the round-trip time to determine the total round trip distance traveled by the laser pulse

<img src="./resources/w4/img/l1-lidar-dist-measurement31.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Since light travels much faster than cars, it's a good approximation to think of the LIDAR and the target as being effectively stationary during the few **nanoseconds** that it takes for all of this to happen. 
- That means that the distance from the LIDAR to the target is simply half of the round-trip distance we just calculated
- This technique is called **time-of-flight ranging**. Although it's not the only way to build a LIDAR, it's a very common method that also gets used with other types of ranging sensors like **radar** and **sonar**
- It's worth mentioning that the photodetector also tells you the intensity of the return pulse relative to the intensity of the pulse that was emitted
- This intensity information is less commonly used for self-driving, but it provides some extra information about the geometry of the environment and the material the beam is reflecting off of
- intensity data is useful, bacause it's possible to create 2D images from LIDAR intensity data that you can then use the same computer vision algorithms 
- Since LIDAR is its own light source, it actually provides a way for self-driving cars to see in the dark
- So, now we know how to measure a single distance to a single point using a laser, a photodetector, a stopwatch, and the time-of-flight equation, but obviously it's not enough to stay laser focused on a single point ahead

- So, how do we use this technique to measure a whole bunch of distances in 2D or in 3D?

**Measuring Distance with Time-of-Flight** 

- The trick is to build a rotating mirror into the LIDAR that directs the emitted pulses along different directions. 

<img src="./resources/w4/img/l1-lidar-dist-measurement4.png" width="190" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- As the mirror rotates, you can measure distances at points in a 2D slice around the sensor
- If you then add an up and down nodding motion to the mirror along with the rotation, you can use the same principle to create a scan in 3D


<img src="./resources/w4/img/l1-lidar-dist-measurement5.png" width="180" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- For Velodyne type LIDARs, where the mirror rotates along the entire sensor body, it's much harder to use a knotting motion to make a 3D scan. 
- Instead, these sensors will actually create multiple 2D scan lines from a series of individual lasers spaced at fixed angular intervals, which effectively lets you paint the world with horizontal stripes of laser light

<img src="./resources/w4/img/l1-lidar-dist-measurement6.png" width="200" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

Here's an example of a typical raw LIDAR stream from a Velodyne sensor attached to the roof of a car

<img src="./resources/w4/img/l1-lidar-dist-measurement7.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The black hole in the middle is a blind spot where the sensor itself is located, and the concentric circles spreading outward from there are the individual scan lines produced by the rotating Velodyne sensor. 
- Each point in the scan is colored by the intensity of the return signal. 
- The entire collection of points in the 3D scan is called a `point cloud`

**Measurement Models for 3D LIDAR Sensors**

- 3D LiDAR sensors report *range*, *azimuth* angle and *elevetion angle*( + return intensity)

Before propagation of light 

<img src="./resources/w4/img/l1-lidar-dist-measurement8.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

After propagation of light 

<img src="./resources/w4/img/l1-lidar-dist-measurement10.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- LIDARs measure the position of points in 3D using spherical coordinates : 
  - **range or radial distance** from the center origin to the 3D point ( $P(x,y,z)$ ), 
  - **elevation angle** measured up from the sensors XY plane
  - **azimuth angle** measured counterclockwise from the sensors x-axis.


<img src="./resources/w4/img/l1-lidar-dist-measurement11.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The azimuth and elevation angles tell you the direction of the laser pulse, and the range tells you how far in that direction the target point is located

-  The azimuth and elevation angles are measured using encoders that tell you the orientation of the mirror, and the range is measured using the time of flight as we've seen before

- For Velodyne type LIDARs, the elevation angle is fixed for a given scan line

<img src="./resources/w4/img/l1-lidar-dist-measurement111.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Now, suppose we want to determine the cartesian XYZ coordinates of our scanned point in the sensor frame, which is something we often want to do when we're combining multiple LIDAR scans into a map

- This gives us an inverse sensor model. We say this is the inverse model because our actual measurements are given in spherical coordinates, and we're trying to reconstruct the Cartesian coordinates at the points that gave rise to them
 
- To go the other way from Cartesian coordinates to spherical coordinates, we can work out the inverse transformation given here. 
- This is our forward sensor model for a 3D LIDAR, which given a set of Cartesian coordinates defines what the sensor would actually report.
 
**Measurement Models for 2D LIDAR Sensors**

- most of the time the self-driving cars we're working with use 3D LIDAR sensors like the Velodyne, but sometimes you might want to use a 2D LIDAR on its own, whether for detecting obstacles or for state estimation in more structured environments such as parking garages.


<img src="./resources/w4/img/l1-lidar-dist-measurement112.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- For 2D LIDARs, we use exactly the same forward and inverse sensor models. But the elevation angle enhance the z component of the 3D point in the sensor frame are both zero. 
  
- In other words, all of our measurements are confined to the XY plane of the sensor, and our spherical coordinates collapsed to the familiar 2D polar coordinates. 

**Sources of Measurement Noise**

- First, there is uncertainty in the exact time of arrival of the reflected signal, which comes from the fact that the stopwatch we use to compute the time of flight necessarily has a limited resolution.
- Similarly, there is uncertainty in the exact orientation of the mirror in 2D and 3D LIDARs since the encoder is used to measure this also have limited resolution. 
- Interaction with the target (surface absorption, specular reflection, etc)
- Variation of propagation speed (e.g., throug materials)

<img src="./resources/w4/img/l1-lidar-dist-measurement113.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- These factors are commonly accounted for by assuming additive **zero-mean Gaussian noise** on the spherical coordinates with an empirically determined or manually tuned covariance. 
- The Gaussian noise model is particularly convenient for state estimation even if it's not perfectly accurate in most cases.


**Motion Distortion** 

- Another very important source of error that can't be accounted for so easily is motion distortion, which arises because the vehicle the LIDAR is attached to is usually moving relative to the environment it's scanning. 

- Now, although the car is unlikely to be moving at an appreciable fraction of the speed of light, it is often going to be moving at an appreciable fraction of the rotation speed of the sensor itself, which is typically around 5-20 hertz when scanning objects at distances of 10 to a 100 meters. 

- This means that every single point in a LIDAR sweep is taken from a slightly different position and a slightly different orientation, and this can cause artifacts such as duplicate objects to appear in the LIDAR scans. 

- This makes it much harder for a self-driving car to understand its environment, and correcting this motion distortion usually requires an accurate motion model for the vehicle provided by GPS and INS for example

**Summary**

- LIDAR sensors measure distances by emitting pulse laser light and measuring the time of flight of the pulse. 
- 2D or 3D LIDAR is extend this principle by using a mirror to sweep the laser across the environment and measure distances in many directions.

### Lesson 1 Supplementary Reading: Light Detection and Ranging Sensors

For more information on LIDAR sensors, check out the resources below:

- Read Chapter 6, Section 4.3 of [Timothy D. Barfoot, State Estimation for Robotics (2017)](http://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser17.pdf) (available for free).

- Read the Wikipedia article on [LIDAR](https://en.wikipedia.org/wiki/Lidar) sensors.

- Read Chapter 4, Section 1.9 of [Roland Siegwart, Illah R. Nourbakhsh, Davide Scaramuzza, Introduction to Autonomous Mobile Robots (2nd ed., 2011)](https://mitpress.mit.edu/books/introduction-autonomous-mobile-robots-second-edition).


### Lesson 2: LIDAR Sensor Models and Point Clouds
### Lesson 2 Supplementary Reading: LIDAR Sensor Models and Point Clouds
### Lesson 3: Pose Estimation from LIDAR Data
### Lesson 3 Supplementary Reading: Pose Estimation from LIDAR Data
## Learn from Insdustry Experts
### Optimizing State Estimation
## Weekly Assignment
### Module 4: Graded Quiz

# References

# Appendices
