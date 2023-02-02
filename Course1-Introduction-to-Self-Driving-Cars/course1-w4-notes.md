# Course 1 - W4 - MODULE 4: Vehicle Dynamic Modeling (VDM)

## Overview 

- The first task for automating an driverless vehicle is to define a model for how the vehicle moves given steering, throttle and brake commands. 
- This module progresses through a sequence of increasing fidelity physics-based models that are used to design vehicle controllers and motion planners that adhere to the limits of vehicle capabilities.

**Learning Objectives**
- Develop a kinematic bicycle model of a car with velocity and steering angle inputs
- Develop a dynamic bicycle models of a car with velocity and steering angle inputs
- Differentiate between models of tire forces
- Develop a model for actuation in a car, from pedal and steering wheel to tire forces

## Dynamic Modeling (DM)
### Lesson 1: Kinematic Modeling in 2D
Generally vehicle motion can be modeled in two ways: 
- dynamic constraint that define its motion 
- considerring all the forces and moments acting on the vehicle

**Kinematic vs Dynamic Model**
- `Kinematic Model` : At low speeds (less significant/low acceleration), it is often sufficient to look only at kinematic models of vehicles
  - Examples : Two wheeled robot, Bicycles model
- `Dynamic Model` : is more involved, but captures vehicle behavior (motion) more precisely over a wide operating range (Also more involved and developed than Kinematic Model)
  - Examples : Dynamic vehicle model

**Coordinate Frames**
- Right handed by convention
- **Inertial frame**
  - Fixed, usually relative to earth
    - ENU (Est: X; North : Y; Z: Up) relative to a reference nearby
    - Or Earth-Centered Earth fixed (ECEFG), used in GNSS systems
- **Body frame**
  - Attached to vehicle, origin at vehicle center of gravity, or center of rotation 
    - Example : the center of gravity of the vehicle or the center point of the rear axle
- **Sensor frame**
  - Attached to sensor, convenient for expressing sensor measurements 

**Why We Need Coordinate Transformation**
- In robotics applications: 
  - Coordinates are attached to the moving system also to represent elements from these frames in the inertial frame
  - To do so, we need to transform variables from one coordinate frame to the other (Body => Inertial frame)

<img src="./resources/w4/robot-frame.png" width="360" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

A two wheeled robot with a single sensor has 3 frames

- Vehicle Frame has multiple sensor frame
  
<img src="./resources/w4/vehicle-frame.png" width="360" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Vectors** 
- Vectors are variables with both magnitude and direction
  
<img src="./resources/w4/vector.png" width="200" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- $v$ is a vector, in a 2D plane, it can be projected both in a body frame and inertial frame
- The vectors {$b1$, $b2$}, {$e1$, $e2$} define two different coordinate frames, $Fb$ and $Fe$ 

**Rotation Matrices in 2D**

frame $e$ and $b$ have the same origin, but $b$ is rotated by angle $\theta$ relative to frame $e$

```
          [cos(theta) sin(theta)]
    Ceb = [-sin(theta) cos(theta)]
```
```
          [cos(theta) -sin(theta)]
    Cbe = [sin(theta) cos(theta)]
```
where : 
- **Ceb** is thansform vectors from **b** to the frame **e** 
- **Cbe** projects the frame **e** onto **b** using the angle $\theta$

**Coordinate Transformation Application example: Two wheeled robot**

<img src="./resources/w4/two-wheeled-robot.png" width="200" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

Problem : 
- Represent the position of the `point P` observed by the robot body frame $b$ w/ respect to the inertial frame $e$
- the **position** of the robot w/ respect to the inertial frame is x and y
- the **orientation** of the robot is $\theta$

Solution : 
- Conversion between Inertial frame and Body cordinates is done with a translation vector and a rotation matrix
  - Location of the point $P$ in Body Frame (B)
  
```
Pb = Ceb(Theta)Pe + Oeb
```
  - Location of the Point(P) in Inertial Frame(E) 
  
```
Pe = Cbe(Theta)Pb + Obe
```
```
where : 
  Oeb/Obe - translation of the axis
  Ceb/Cbe - the rotation of the axis
```

**Homogenous Coordinate Form**

- A 2D vector in homogeneous form

```             [X]
P = [x] => P'=  [Y]
    [y]         [1]
```
- Transforming a point from body to inertial coordinates with homogeneous coordinates

```
P'e = [Ceb(theta) | Oeb]P'b
```

**2D Kinematic Modeling**

<img src="./resources/w4/two-wheeled-robot-k-modeling.png" width="200" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The Kinematic constraint is nonholonomic
  - A constraint on rate of change of degrees of freedom
  - Vehicle velocity always tangent to current path

> ## $\frac{dy}{dx} = tan \theta = \frac {sin \theta}{cos \theta}$

- Nonholonomic constraint
   
> ## $\dot{y} cos \theta - \dot{x} sin \theta$

- Velocity components
> ## $\dot{y} = vcos \theta$ 
> ## $\dot{x} = vsin \theta$

**Simple Robot Motion Kinematics**

```mermaid
  graph LR
    A[Inputs]-->B[Simple Model]
    B-->C[Outputs / States]
```
> ## $\dot{y} = vcos \theta$ 
> ## $\dot{x} = vsin \theta$
> ## $\dot{\theta} = \omega$

```
where :
- Inputs : [v, w] , the velocity and rotation rate
- Output : [theta, x, y], theta, x and y, the orientation, position of the robot and its heading 
``` 

> **State** is a set of variables often arranged in the form of vectors that fully describe the system at the current time

**Two-Wheeled Robot Kinematic Model**
- Assume control inputs are wheel speeds : 

<img src="./resources/w4/two-wheeled-robot-k-modeling-2D.png" width="200" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

```
where : 
  - p : center of the robot
  - l : wheel to center
  - r : wheel radius
  - w1, w2 : wheel rotation rates
```
- Kinematic constraint 

<img src="./resources/w4/robot-wheel.png" width="300" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

> ## $vi = rwi$

assuming no slip btw the wheel and the surface

<img src="./resources/w4/robot-icr.png" width="300" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

> ## $v = \frac{v1 + v2}{2} = \frac{rw1 + rw2}{2}$

The robot moves in a curved path about some Instantaneous Center of Rotation (ICR)
- ICR == robot kinematic model 

<img src="./resources/w4/robot-icr-w.png" width="300" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Use the instantaneous center of rotation (ICR)
- Equivalent triangle give the angular rate of rotation

> ## $w = \frac{-v2}{\rho} = \frac{-(v2 -v1)}{2l} = \frac{(rw1-rw2)}{2l}$


**Kinematic Model of a Simple 2D Robot**

- **Continuous time model** : 

> ## $\dot{x} = [(\frac{rw1 + rw2}{2})cos \theta]$ 
   
> ## $\dot{y} = [(\frac{rw1 + rw2}{2})sin \theta]$

> ## $\dot{\theta} = (\frac{rw1 - rw2}{2*l})$

- **Discrete time model** : enable to convert the model from differentiel to finite difference form (FDF) for control design & simulation

> ## $x_{k+1}= x_{k} + [(\frac{rw_{1,k} + rw_{2,k}}{2})cos \theta] \Delta t$

> ##  $y_{k+1} = y_{k} + [(\frac{rw_{1,k} + rw_{2,k}}{2})sin \theta] \Delta t$

> ## $\theta_{k+1} = \theta_{k} + (\frac{rw_{1,k} - rw_{2,k}}{2*l}) \Delta t$

```
where : 
  - k :  value of the variable in the current time step
  - k + 1 : value of the variable in the next time step
```


### Supplementary Readings for Module 4

Read more about **2D plan motion and coordinate frames** in the PDF below:
 
[Chapter 2 - "Models of Mobile Robots in the Plane" B.A. Francis and M. Maggiore, Flocking and Rendezvous in Distributed Robotics, SpringerBriefs in Control, Automation and Robotics (2016)](https://edisciplinas.usp.br/pluginfile.php/5679996/mod_resource/content/5/Models-of-Mobile-Robots-in-the-Plane.pdf)


### Lesson 2: The Kinematic Bicycle Model

**Bicycle Kinematic Model** : has been used as suitable `control-oriented model` for representing vehicles.
- 2D bicycle model (simplified car model)
- Nonholonomic constraints of a car
- Front wheel steering model (similar to cars in 2D plane inertial frame (FI))

<img src="./resources/w4/front-wheel-steering-model.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Rear Wheel Reference Point**

<img src="./resources/w4/rear-wheel-ref.png" width="250" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Apply Instantaneous Center of Rotation (ICR)
  
  $\displaystyle \dot{\theta} = \omega = \frac{v}{R}$

- Similar triangles
  
  $\displaystyle \tan \delta = \frac{L}{R}$
  
- Rotation rate equation

  $\displaystyle \dot{\theta} = \omega = \frac{v.tan \delta}{L}$

where : 

- $\displaystyle v$ : the velocity
- $\displaystyle R$ : the radius
- $\displaystyle \theta$ : the heading of bicycle
- $\displaystyle \delta$ : the steering angle  
- $\displaystyle \omega$  : the angular/rotation rate of the bicycle
- $\displaystyle L$ : the gap/length between the two wheels
- $\displaystyle x, y$ : the front/rear axle reference point

**Rear Axle bicycle Model**

- If the desired point is at the center of the rear axle : 

<img src="./resources/w4/RearAxleBicycleModel.png" width="250" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

$\displaystyle \dot{x}_{r} = v cos \theta$ 
   
$\displaystyle \dot{y}_{r}  = vsin \theta$

$\displaystyle \dot{\theta} = \frac{v.tan \delta}{L}$

**Front Axle bicycle Model**

- If the desired point is at the center of the front axle : 

<img src="./resources/w4/FrontAxleBicycleModel.png" width="250" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

$\displaystyle \dot{x}_{f} = v cos(\theta + \delta)$ 
   
$\displaystyle \dot{y}_{f}  = vsin(\theta + \delta)$

$\displaystyle \dot{\theta} = \frac{v.sin \delta}{L}$

**Center of the Gravity (CG) Model**

- If the desired point is at the center of the front axle : 

<img src="./resources/w4/cg-BicycleModel.png" width="250" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

---
$\displaystyle \dot{x}_{c} = v cos(\theta + \beta)$ 
   
$\displaystyle \dot{y}_{c}  = vsin(\theta + \beta)$

$\displaystyle \dot{\theta} = \frac{v.cos \beta .tan \delta}{L}$

$\displaystyle \beta = tan^-1 (\frac{v.cos \beta .tan \delta}{L})$

---

where :  

$\displaystyle \beta$ - is the side slip angle

$\displaystyle lr$ - the distance from rear wheel to the cg

**State - Space Representation**

It is 'hard' to instantaneously change the steering angle ( $\delta$ ) of the vehicle from one extreme of its range to another but it's possible with our kinematic model. If we assume we can only control the `rate of change` of the new steering angle ( $\phi$ )
- Modify CG kinematic bicycle model to use steering rate input
  - Inputs : $[v, \phi]^T$ (steering rate phi as our modified input)
  - State: $[x, y, \theta, \delta]^T$ (extended version with delta as a state)
---
$\displaystyle \dot{x}_{c} = v cos(\theta + \beta)$ 
   
$\displaystyle \dot{y}_{c}  = vsin(\theta + \beta)$

$\displaystyle \dot{\theta} = \frac{v.cos \beta .tan \delta}{L}$


$\displaystyle \dot{\delta} = \phi$

---
where : $\phi$ - is the modified Input: **rate of change** of steering angle

### Lesson 2 Supplementary Reading: The Kinematic Bicycle Model

Read more about **the Kinematic Bicycle Model (pages 15-26)** in the PDF below: 

[Chapter 2 - "Models of Mobile Robots in the Plane" B.A. Francis and M. Maggiore, Flocking and Rendezvous in Distributed Robotics, SpringerBriefs in Control, Automation and Robotics (2016)](https://edisciplinas.usp.br/pluginfile.php/5679996/mod_resource/content/5/Models-of-Mobile-Robots-in-the-Plane.pdf)

### Lesson 3: Dynamic Modeling in 2D

**Dynamic Modeling**

- Why Dynamic Modeling is important ?
  - At higher speed and slippery roads, vehicles do not satisfy no slip condition
  - Forces such as drag, road friction govern required throttle inputs
- Steps to build a typical dynamic model  : 
```
1. Coordinate frames
2. Lumped dynamic elements
3. Free Body Diagram
4. Dynamic Equations
```
**Dynamic Modeling - Translation Systems**
- Deals with forces and torques
- Roughly, need to equate all forces
- Governed by **Newton's Second Law** ( $\displaystyle \Sigma \overrightarrow{F} {i} = M\overrightarrow{a}$ )

<img src="./resources/w4/translation-system.png" width="250" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Example: Vehicle Shock Absorver (Suspension)
**Dynamic Modeling - Translation Systems**

**Dynamic Modeling - Rotation Systems**
- Very common in the automobile : 
  - Ex : Internal combustion engine chap, gear boxes, converters and tires etc
  
<img src="./resources/w4/rotational-system.png" width="200" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

```
- Inertia, J
- Torsion force, T
- Forces resisting that torsionanl force
  - Spring force
  - Damping force
  - Inertia force
```

**Full Vehicle Modeling**

- All components, forces and moments in 3D
  - Pitch, roll, normal forces
  - Suspension, drivetrain, components models

<img src="./resources/w4/project-chrono.png" width="200" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

Dynamic models of vehicles are useful for multiple applications : 
  - Improvement of state estimation methods in **sensor fusion** to track motion
  - trajectory path tracking
  - help define the limits of vehicle performance : unsafe trajectories that car cannot track

- A Full 3D vehicle modeling is very complex due to all components, forces and moments ... 
- One of the 'easiest' way is to split the model into two 2D models : 
  - steering control
  - Throttle and brake control problem

**2D Dynamics - Vehicle Longitudinal Motion**

<img src="./resources/w4/2D-longitudinal-motion.png" width="300" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**2D Dynamics - Vehicle Lateral Motion**

<img src="./resources/w4/2D-lateral-motion.png" width="300" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- In both model There are several forces acting in the vehicles

### Lesson 3 Supplementary Reading: Dynamic Modeling in 3D

**General Dynamics**:

- Ardema, Mark D. Newton-Euler Dynamics, Springer: Santa Clara University, Santa Clara (2005).

- [Tong,  David. Classical Dynamics University of Cambridge Course Notes (2004)](http://www.damtp.cam.ac.uk/user/tong/dynamics/clas.pdf)  

**Vehicle Modeling**:

- Rajamani, Rajesh. Vehicle dynamics and control, Springer Science & Business Media (2011).

- [Jacobson, Bengt, et al. Vehicle Dynamics, Vehicle Dynamics Group, Division of Vehicle and Autonomous Systems, Department of Applied Mechanics, Chalmers University of Technology (2016)](https://publications.lib.chalmers.se/records/fulltext/244369/244369.pdf)


### Lesson 4: Longitudinal Vehicle Modeling
Based on the dynamic of the vehicle that generated **forward motion**

<img src="./resources/w4/longitudinal-modeling.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

Where : 

```
- Faero : Aerodynamic drag force
- Fxf, Fxr : Front and rear tire forces
- Rxf, Rxr : Rolling 
- mgsin(alpha) : force of gravity where alpha is the local road slope
```
Based on `Newton 2nd Law` :

---
$\displaystyle m\ddot{x} = F_{xf} + F_{xr} - F_{aero} - R_{xf} - R_{xr} -mg \sin \alpha$

---
The imbalance btw these forces defines the acceleration of the vehicle in the longitudinal direction ( $\ddot{x}$ )

**The Simplified Longitudinal Dynamics**

- The full eq. : 
  - $\displaystyle m\ddot{x} = F_{xf} + F_{xr} - F_{aero} - R_{xf} - R_{xr} -mg \sin \alpha$

- Let $F_{x}$ - total longitudinal force : $F_{x} = F_{xf} + F_{xr}$
- Let $R_{x}$ - total `rolling force` : $R_{x} = R_{xf} + R_{xr}$
- Assume $\alpha$ is a small angle (small road inclinations): $\sin \alpha = \alpha$
- Then the simplified longitudinal dynamics become

  - $\displaystyle m\ddot{x} = F_{x} - F_{aero} - R_{x} - mg \alpha$

- where then  : 
  
```
  - x : inertial term for longitudinal acceleration
  - Fx : the traction Force generated by the powertrain
  - (Faero - Rx - mgalpha) : the Total Resistance Forces (Fload)
```
> `Each force` in the equation has a separated model associated to it.

**Simple Resistance Force Models**

- Total **resistance load** : 
  - $\displaystyle F_{load} = F_{aero} + R_{x} + mg \alpha$
      - We already built a model for the effects on gravity in the previsous lesson above
- The **aerodynamic force** can depend on air density, frontal area, on the speed of the vehicle
  - $\displaystyle F_{aero} = 1/2 C_{\alpha} \rho A \dot{x}^2$
  - Given a fixed vehicle shaped and standard atmospheric pressure : 
    - $\displaystyle F_{aero} = C_{\alpha}\dot{x}^2$
  - where : 

```
- C_alpha : lumped Coefficient
- Rho : Air density
- A : front area of the vehicle/vehicle coef of friction?
- x (.) = current speed of the vehicle 
```
- The **Rolling resistance** can depend on the tire normal force (N), tire pressures and vehicle speed
  - $\displaystyle R_{x} = N (\hat{C}_{r,0} + \hat{C}_{r,1} |\dot{x}| + \hat{C}_{r,2} \dot{x}^2)$
  - If we assume nominal operating conditions, and dropping the 2nd-order terms for simplicity we get a `linear rolling model`: 
  - $\displaystyle R_{x} \approx {C}_{r,1} |\dot{x}|$

where  : 
```
- Cr1 : linear rolling coef resistance
```
Notice this an approximative model. In pratice the accuracy required of the controller or the **simulation environment**.

**Powertrain Modeling**

<img src="./resources/w4/powertrain.png" width="500" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The force generated to conquered the resistance forces comes from the power train, 
- They can be modeled as being generated by series of components 
- the power provided by `combustion in gasoline/diesel engines`, `electrochemical reactions in batteries for electric/hybrid vehicles` flow to the `driveline` providing a torque to the wheels

- The **driveline** refers to the sequences of components btw the engine and the wheels : 
  - the torque converter/clutch
  - the transmission/gearbox
  - differentials

- The connection btw wheel and engine when in gear it is possible to model the relationship wheel speed - engine speed as a `kinematic constraint` 

  - Rotational Coupling : 
    - $\displaystyle \omega_{w} = GR \omega_{t} = GR \omega_{e}$

where  : 
```
- Ww : wheel angular speed (provided by the differential axle)
- Wt : turbine angular speed
- We : engine angular speed
- GR : Combined gear ratios (changes depending on the powertrain components state)
```
- The vehicle forward velocity is proportional to the wheel angle speed times the effective tire radius
  - Longitudinal velocity : 
    - $\displaystyle \dot{x} = r_{eff} \omega{w}$
 
where  : 
```
- Ww : wheel angular speed (provided by the differential axle)
- reff : effective tire radius
```
  - Longitudinal acceleration
    - $\displaystyle \ddot{x} = r_{eff} GR \dot{\omega}_{e}$

**Power flow in the PowerTrain**

<img src="./resources/w4/powerflow.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Wheel
  - $\displaystyle \ddot{x} = r_{eff} GR \dot{\omega}_{e} + r_{eff} F_{x} + T_{wheel} - r_{eff} F_{x}$

### Lesson 4 Supplementary Reading: Longitudinal Vehicle Modeling

To learn more about longitudinal dynamics and vehicle drivetrain, read **Chapter 4**  in the textbook below:

- [Rajamani R. (2012) "Longitudinal Vehicle Dynamics." In: Vehicle Dynamics and Control. Mechanical Engineering Series. Springer, Boston, MA.](http://link.springer.com/content/pdf/10.1007%2F978-1-4614-1433-9_4.pdf)
### Lesson 5: Lateral Dynamics of Bicycle Model
### Lesson 5 Supplementary Reading: Lateral Dynamics of Bicycle Model
### Lesson 6: Vehicle Actuation
### Lesson 6 Supplementary Reading: Vehicle Actuation
### Lesson 7: Tire Slip and Modeling
### Lesson 7 Supplementary Reading: Tire Slip and Modeling

## Learn from Industry Expert
### Challenges for the Industry
## Weekly assignment
- OK 
## References