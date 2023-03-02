# Course 1 - W6 - MODULE 6: Vehicle Lateral Control

## Overview 

- This week, you will learn about how lateral vehicle control ensures that a fixed path through the environment is tracked accurately.
- You will see how to define geometry of the path following control problem and develop both a simple geometric control and a dynamic model predictive control approach.

**Learning Objectives**
- Define the geometry of the lateral control problem, including heading and cross track errors
- Design a geometric steering controller to track a straight line segment
- Identify the limits of geometric controllers as wheel slip increases
- Explore options for dynamic control, including model predictive control

## Lateral Control
- learning objectives : 
  - Explore lateral vehicle control definitions
  - Design two geometric path following controllers
  - Discuss model predictive control for autonomous driving
### Lesson 1: Introduction to Lateral Vehicle Control (LVC)
- Problem : 
  - ensuring the vehicle can precisely follow a predefined path, execution the motion plan devised in the higher level planning module
- Solution:
  - Lateral Vehicle Control
    - select the **steering angle** required to correct any errors that accumulates and track changes in the path direction as they appear

**Lateral Control Design**

- Lateral control for an automotive
  - Define error relative to desired path
  - Select a control law that drives errors to zero and satisfies input contraints (max lateral acceleration and min jerk)
  - Add dynamic considerations to manage forces and moments acting on vehicle

**The Reference Path**
- Track
  - Straight line segment
  
  <img src="./resources/w6/ref-path-track1.png" width="250" style="border:0px solid #FFFFFF; padding:1px; margin:1px">
    
      - very compact and easy to construct
      - points are very well space in the environment allows for mostly straight line motion (Manhattan grid of roadways)
      - this path has heading discontinuities which make precise tracking a challegence with a steered vehicle
  
  - Waypoints
  
  <img src="./resources/w6/ref-path-track2.png" width="250" style="border:0px solid #FFFFFF; padding:1px; margin:1px">
    
      - a refinement of the line segment approach is to provide a series of tightly spaced waypoints
      - spacing usually fixed in terms of distance or travel time
      - the relative position of the waypoints can be restrictedd to satisfy an approximate curvature constraint
      - very common, easy to work with and can be directly constructed from state estimate or GPS waypoints collected in earlier runs of a particular route
  
  - Parameterized curves

  <img src="./resources/w6/ref-path-track3.png" width="250" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

      - a sequence of continuous parameterized curves, 
      - drawn from a fixed set of motions primitives or can be identified through optimization during planning
      - the curves provides the benefit of continuously carying motion
      - can be constructed to have smooth derivatives to aid in consistency of error and error rate calcultations.
  
> - In all cases of path following the controller tries to eliminate the offset of the vehicle to desired path and to align the vehicle heading with the path heading
> - for each of those paths definitions the direction of travel along the path is also provided, wich can encoded with the point ordering or cureve ordering

- Main goals: 
  - Heading path alignment
  - Elimination of offset to path

**Two Types of Control Design**
- Geometric Controllers : geometry of the desired path + kinematic models of the vehicle
  - Pure pursuit (carrot following)
  - Stanley

- Dynamic Controllers
  - Model Predictive controller (MPC) control : performs a finite horizon optimization to identify the control command to apply
    - the most advanced controller
    - able to handle a wide variety of constrainsts and identify optimized solution that consider more than just the current errors
  - Other control systems
    - Sliding mode, feedback linearization
  
**Plant Model**
- Vehicle (bicycle) model & parameters
  - All states variables and inputs defined relative to the centre of front axle
   
<img src="./resources/w6/bicycle-model.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Driving Controller**
- Controller error terms
  - Heading error
    - Component of velocity perpendicular to trajectory divided by the ICR radius
    - Desired heading is zero (because the ref heading is not time-varying for a straight line) 

<img src="./resources/w6/driving-controller.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- where : 
  - $\psi(t)$ is the rate of heading and allows to understand how the heading error evolves overtime 

- Crosstrack error (e) : 
   - Distance from center of front axle to the closest point on path

- Rate of change of crosstrack error ( $\dot{e}$ ) : 
  - $\displaystyle \dot{e}(t) =  v_{f}(t) \sin( \psi(t) - \delta(t))$

<img src="./resources/w6/crosstrack-error.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

> - Both errors must converge to `zero` for vehicle to properly tracking the desired path
> - both errors are hard to deal with in the curved path and add some additional complexities, as it's not immediately clear where the ref point should lie


### Lesson 1 Supplementary Reading: Introduction to Lateral Vehicle Control

To learn more about the lateral control of autonomous vehicles, read the article below: 

- [J. Jiang and A. Astolfi, "Lateral Control of an Autonomous Vehicle," in IEEE Transactions on Intelligent Vehicles, vol. 3, no. 2, pp. 228-237, June 2018.](http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8286943&isnumber=8363076)

To compute the minimum distance to a curved path defined by a spline: 

- [Wang, H., Kearney, J., & Atkinson, K. (2002, June). Robust and efficient computation of the closest point on a spline curve. In Proceedings of the 5th International Conference on Curves and Surfaces (pp. 397-406).](http://homepage.divms.uiowa.edu/~kearney/pubs/CurvesAndSurfaces_ClosestPoint.pdf) 

### Lesson 2: Geometric Lateral Control - Pure Pursuit
### Lesson 2 Supplementary Reading: Geometric Lateral Control - Pure Pursuit
### Lesson 3: Geometric Lateral Control - Stanley
### Lesson 3 Supplementary Reading: Geometric Lateral Control - Stanley
### Lesson 4: Advanced Steering Control - MPC
### Lesson 4 Supplementary Reading: Advanced Steering Control - MPC


## References
## Appendices

