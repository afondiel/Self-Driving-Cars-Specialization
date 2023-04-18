# Course-2 - W3 - MODULE 3 : GNSS/INS Sensing for Pose Estimation

## Overview 

- To navigate reliably, autonomous vehicles require an estimate of their pose (position and orientation) in the world (and on the road) at all times.
- Much like for modern aircraft, this information can be derived from a combination of GPS measurements and inertial navigation system (INS) data.
- This module introduces sensor models for inertial measurement units and GPS (and, more broadly, GNSS) receivers; performance and noise characteristics are reviewed.
- The module describes ways in which the two sensor systems can be used in combination to provide accurate and robust vehicle pose estimates.

**Course Objectives :**

- Explain the operation of the two most common sensors used for pose estimation in autonomous driving, inertial meaurement units and GNSS receivers.
- Understand the concept of coordinate acceleration and the fundamental equation of inertial navigation.
- Apply gyroscope and accelerometer measurement models in the context of navigation.
- Describe the process of trilateration and justify why four satellites must be visible to obtain a 3D position fix from a GPS (GNSS) receiver.
- Understand why ionospheric delays and multipath effects can degrade the performance of GPS.

## GNSS/INS Sensing for Pose Estimation
### Lesson 1: 3D Geometry and Reference Frames 

**Coordinates Rotations**

- `Vector`: is a geometric object that has a magnitude and a direction.
- Also refered as Vector coordinates/set of numbers that represents the vectors direction and magnitude

<img src="./resources/w3/img/l1-coord-rot0.png" width="480" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Transformation**

- Coordinate points changes when we move to one coordinate frame to another
- For ex. :  we may know the position of a building in some frame, and we want its position in our current vehicle frame 
- To compute this, use vector addition in order to express all of the coordinates in the `same` reference frame
 
<img src="./resources/w3/img/l1-transf.png" width="480" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**How can we reprensent a rotation**
- A critical component of tracking reference frames is tracking their orientation or rotation with respect to some base reference frame.
- Rotations are particularly tricky mathematical objects and they can be the source of major bugs if not dealt with carefully and diligently.

1. Rotation Matrix

<img src="./resources/w3/img/l1-coord-rot1.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The inverse of rotation matrix is its transpose

2. Unit quaternions

- It can be represented as a 4D vector of unit of length ( $\mathbb{R}^4$ )

<img src="./resources/w3/img/l1-coord-rot2.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- We can **convert a quaternion to a rotation matrix** by using the algebra expression below : 

<img src="./resources/w3/img/l1-coord-rot3.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Why use quaternions? 
  - They don't suffer from singularities and need 4 parameters instead of 9.

**Quarterion Multiplication and Rotations**
- Quarternions multiplication is a special operation that is associative but is not commutative in general(just like matrix multiplication)
  
<img src="./resources/w3/img/l1-coord-rot4.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Quaternions is a complex number ( $\mathbb{C}$ )

Sequential rotation operations can also be performed by taking advantage of quaternion multiplication

$$
C( p \bigotimes q) = C(p)C(q)
$$

Where **p** and **q**, are rotation matrices

1. Euler angles

<img src="./resources/w3/img/l1-coord-rot5.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Euler angles are a parsimonious representations requiring only three pa rameters instead of nine for a full rotation matrix.
- The cons of Euler angles is that they are singulaties. Singularites complicate state estimation because they represent particular rotation from which two euler angles are indistinguishable, in opposite of rotation and quaterunions

<img src="./resources/w3/img/l1-coord-rot6.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Which rotation representation should I use?**

<img src="./resources/w3/img/l1-coord-rot7.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- It depends on the use case. Each of representation has pros & cons. 

**Reference Frames - Earth-Centred Inertial Frame (ECIF)**

<img src="./resources/w3/img/l1-coord-rot8.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Reference Frames - Earth-Centred Earth-Fixed Frame (ECEF)**

<img src="./resources/w3/img/l1-coord-rot9.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Where : RHR is the Right Hand Rule

<img src="./resources/w3/img/l1-coord-rot-cef-ecif.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- ECEF is fixed to the earth, while the ECIF is fixed with respect to the distance stars.  
- Useful for satelites and inertial sensing onboard aircraft

**Reference Frames - Navigation**

- For pratical vehicle application we use a frame that is fixed with respect to the ground
- For ex. : the navigation frame or local tangent frame

<img src="./resources/w3/img/l1-nav0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- A very common navigation frame is one that is attached to some known starting point and aligns the `x-axis pointing north`, the `y-axis pointing east`, and the `z-axis pointing down`. This is called the NED frame (North, East, Down). 
- A closely related frame is the ENU frame which aligns the `x-axis pointing east`, the `y-axis pointing north`, and the `z-axis pointing up`, where ENU (Easting Northing Up). 

<img src="./resources/w3/img/l1-nav1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Reference Frames - Sensor & Vehicle**

<img src="./resources/w3/img/l1-sensor-vehicle.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">
 
- A sensor frame that is rigidly attached to a sensor like a **LIDAR, a GPS receiver or an Inertial Measurement Unit**. 
- This frame will typically be distinct from the general vehicle frame which can be placed anywhere on the vehicle that is convenient, at the center of mass, for example. 
- For localization, we will often ignore the distinction between the vehicle and sensor frame and assume that if we can track the sensor, we should be able to track any point on the vehicle, given proper calibration

**Summary - 3D geometry and Reference Frames**

- Vector quantities can be expressed in different reference frames
- Rotations can be parametrized by rotation matrices, quaternions or Euler angles
- ECEF, ECIF and Navigation frames are important in localization

### Lesson 1 Supplementary Reading: 3D Geometry and Reference Frames

For more information on 3D geometry and reference frames, check out the resources below:

- Read Chapter 6, Sections 1 to 3 of [Timothy D. Barfoot, State Estimation for Robotics (2017)](http://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser17.pdf) (available for free).

- Make use of this online [interactive quaternion calculator](https://quaternions.online/) and a handy online [3D rotation converter](https://www.andre-gaschler.com/rotationconverter/).

- Read the [Wikipedia article](https://en.wikipedia.org/wiki/Rotation_matrix) on rotation matrices.

### Lesson 2: The Inertial Measurement Unit (IMU)
### Lesson 2 Supplementary Reading: The Inertial Measurement Unit (IMU)
### Lesson 3: The Global Navigation Satellite Systems (GNSS)
### Lesson 3 Supplementary Reading: The Global Navigation Satellite (GNSS)
## Learning from Industry Expert
### Why Sensor Fusion?
## Weekly Assignement
### Module 3: Graded Quiz



# References

- [Course 1 - W4 - MODULE 4: Vehicle Dynamic Modeling (VDM) -  Lesson 1: Kinematic Modeling in 2D](https://github.com/afondiel/Self-Driving-Cars-Specialization-Coursera/blob/main/Course1-Introduction-to-Self-Driving-Cars/course1-w4-notes.md)


# Appendices
- [3D Space](https://en.wikipedia.org/wiki/Three-dimensional_space)
- [3D pose estimation](https://en.wikipedia.org/wiki/3D_pose_estimation)
- [Rotation Matrix](https://en.wikipedia.org/wiki/Rotation_matrix)
- [Coordinate System](https://en.wikipedia.org/wiki/Coordinate_system)
- [Spherical Coordinate System - Earth coordinates](https://en.wikipedia.org/wiki/Spherical_coordinate_system)
- [Horizontal Coordinate System](https://en.wikipedia.org/wiki/Horizontal_coordinate_system)
- [Pose (computer vision)](https://en.wikipedia.org/wiki/Pose_(computer_vision))
- [Computer Vision](https://en.wikipedia.org/wiki/Computer_vision)
- [Camera Resectioning](https://en.wikipedia.org/wiki/Camera_resectioning)
- [Optics](https://en.wikipedia.org/wiki/Optics)
- [Geometrical Optics](https://en.wikipedia.org/wiki/Geometrical_optics)
- 