# Course-2 - W1 - MODULE 0 : State Estimation and Localization for Self-Driving Cars

## Overview 
- This module introduces you to the main concepts discussed in the course and presents the layout of the course. 
- The module describes and motivates the problems of state estimation and localization for self-driving cars. 
- An accurate estimate of the vehicle state and its position on the road is required at all times to drive safely.
  
**Course Objectives :**
- Understand the problem of state estimation and its relationship to vehicle localization
- Review the types of sensors introduced througout the course
- Review the main project offered in this course


## Introduction to State Estimation and Localization for Self-driving Cars

### Welcome to the Self-Driving Cars Specialization
- Ok => [course 1 - w1](..\Course1-Introduction-to-Self-Driving-Cars/course1-w1-notes.md)  
### Welcome to the Course

<img src="../Course1-Introduction-to-Self-Driving-Cars/resources/w4/vehicle-frame.png" width="360" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Learn about sensors for state estimation & localization
- `state estimation` is the process of determining the best value of some physical quantity from what are typically **noisy measurements**
- measurements are noisy because sensors are not perfect (random results for the same input signal)
- state estimation is fundamental to any device with sensor  
- Localization is one the most important types of state estimation for self-driving cars
- `Localization:` is the process of determining `where` the car is in world and `how` is moving

**Course overview**

- Understand the method of least squares for parameter and state estimation
- Apply the linear Kalman filter and its nonlinear variants, the extended and unscented Kalman filters, to state estimation problems
- Develop models for typical localization sensors like GPS receivers, inertial sensors, and LIDAR range sensors
- Learn about LIDAR scan matching and the iterate closest point (ICP) algorithm
- Use these tools to fuse data from multiple sensors streams into a single state estimate for self-driving car
- `Final Project:` A full vehicle state estimator for self-driving cars using the CARLA simulator.

### Course Prerequisites: Knowledge, Hardware & Software
- [Course Prerequisites](../Course1-Introduction-to-Self-Driving-Cars/resources/Course-Prerequisites-Knowledge-Hardware-Software.md)
### How to Use Discussion Forums
- OK
### Get to Know Your Classmates
- OK
### How to Use Supplementary Readings in This Course
- OK
## Meet the Self-Driving Car Experts

### Meet the Instructor, Jonathan Kelly 
- OK
### Meet the Instructor, Steven Waslander 
- OK 
### Meet Diana, Firmware Engineer
- Ok
### Meet Winston, Software Engineer 
- OK 
### Meet Andy, Autonomous Systems Architect 
- OK 
### Meet Paul Newman, Founder, Oxbotica & Professor at University of Oxford - OK 
- All already done [course 1 - w1](..\Course1-Introduction-to-Self-Driving-Cars/course1-w1-notes.md)
### The Importance of State Estimation
- Why is state estimation so critical for self-drving cars ? 
  - you need to know where you are
  - all you get as input is sensor data 
  - the state is an answer to where the car is, how it is moving, how fast it is turning
  - state estimation allows to process sensor data at highest level
  - state estimation is a challenging problem to solve because the sensor datas are often foul and noisy 
# Module 1: Least Squares

## Overview 

- The method of least squares, developed by Carl Friedrich Gauss in 1795, is a well known technique for estimating parameter values from data. 
- This module provides a review of least squares, for the cases of unweighted and weighted observations. 
- There is a deep connection between least squares and maximum likelihood estimators (when the observations are considered to be Gaussian random variables) and this  connection is established and explained. 
- Finally, the module develops a technique to transform the traditional 'batch' least squares estimator to a recursive form,  suitable for online, real-time estimation applications.

**Course Objectives:**

- Understand the squared error optimization criterion and its use
- Explain how least squares is employed in parameter estimation problems
- Apply the unweighted and weighted least squares methods to parameter estimation
- Apply a recursive version of least squares to update parameter estimates as new measurements arrive
- Explain how Jacobian matrices are used

### Lesson 1 (Part 1): Squared Error Criterion and the Method of Least Squares

- `Localization:` is the process of determining `where` the car is in world and `how` is moving
- `state estimation` is the process of determining the best value of some physical quantity from what are typically **noisy measurements**

- An accurate localization is a key component of any self-driving car sw stack and state estimation is the way of doing so.
- Any real world measurements will be imprecise
- State estimation is the idea of parameter estimation
  - `state:` physical quantity that changes overtime (ex: position and orientation)
  - `parameter:` is constant over time  (ex: electric resistor)

**Least Squares**

- Develped by Carl F. Gauss (1809)
- Theorem : 

```
The most probable value of the unknown quantities will be that in which the sum of squares of the differences btw the actually observed and the computed values multiplied by numbers that measure the degree of precision is minimum. 
```
**Illustraction examples : Estimating Resistance**
- Measurement model : 
  - $\displaystyle y_{i} = x + \nu_{i}$
- where :
  - $y$ : measurements  
  - $i$ : the number of experiments/ independent measurements
  - $x$ : Actual resistance (constant)
  - $\nu$ : Measurement noise 
  
- after 4 measurements : 

<img src="./resources/w1/resistor-estimation.png" width="360" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Minimizing the Squared Error Criterion (SEC)**

$$
\displaystyle \hat{x}_{LS} = 
argmin_{x}(e_{1}^2 + e_{2}^2 +e_{3}^2 +e_{4}^2) = 
J_{LS}(x)
$$

- To minimize the SEC, we rewrite the errors in matrix notation 
- Useful when dealing with thousands/larges numbers of measurements 

<img src="./resources/w1/matrix-error.png" width="360" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

where : 
- $e$ : is the error vector
- $y$ : the measurements/function of observations
- $H$ : the Jacobian matrix 
  - $dim(H) = m x n$ , $m$ : numbers of measurements, $n$ : nb of unkown/parameters to be estimated
- $x$ : the resistance (a single scalar but can also be a vector) 

We can now express our criterion as follows

$$
\displaystyle J_{LS}(x) =
e^Te = (y - Hx)^T(y - Hx) = y^Ty - x^TH^Ty - y^THx + x^TH^THx
$$

- To minimize this, we can compute `the partial derivative` with respect to our parameter, set to `zero`, and solve for extremum:


<img src="./resources/w1/error-criterion.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

> We will only be able to solve for $\hat{x}$ if $(H^TH)^-1$ exits, i.e : $H$ has an inverse

<img src="./resources/w1/transpose-theorems.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

<img src="./resources/w1/problem-solution.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Assumptions**

- Our measurement model, $y = x + \nu$ , is linear
- Measurements are **equally weighted** (we do not suspect that some have more noise than others)


### Lesson 1 (Part 2): Squared Error Criterion and the Method of Least Squares

**Method of Weighted Least Squares**

- One of the reason we may want to trust certain measurments more than others is that they may come from a better sensor
- Ex: In the resistance estimation we could use a much better and expensive device in order to get a better measurement accurancy

<img src="./resources/w1/measurement-device.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- From now on, we also drop the assumption that we're only estimation one parameter and derive the more general normal equations.
- This allows to estimate multiple parameters at one time

<img src="./resources/w1/weighted-ls.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

If we instead assume that each noise term has a different variance : 

<img src="./resources/w1/weighted-ls2.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Re-deriving Regular Least Square**

- What happen if all of our variances are the same ? 
  
<img src="./resources/w1/weighted-ls3.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Minimizing the Weighted Least Square Criterion**

<img src="./resources/w1/weighted-ls4.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Where the derivative is a `Gradient` 
- Solving this derivative we then solve for our best or optimal parameter vector $\hat{x}$ .

**How Method of Weighted Least Square works ?**

- From the weighted normal equations : 

$$
\displaystyle \hat{x} = 
(H^TR^-1H)^-1*H^TR^-1y
$$

Assuming that the last two measurements were actually taken with a multimeter that had a much smaller noise variance

<img src="./resources/w1/weighted-ls5.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

We can see (below) that the final resistance value we get is much closer to what the more accurate multimeter measured as expected

<img src="./resources/w1/weighted-ls6.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Ordinary  vs Weighted Least Squares**

<img src="./resources/w1/weighted-ls7.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">


### Lesson 1 Supplementary Reading: The Squared Error Criterion and the Method of Least Squares

To learn more about the squared error criterion and least squares, check out some of the resources below: 

- [Here's an interactive least squares fitting simulator provided by the PhET Interactive Simulations project at the University of Colorado](https://phet.colorado.edu/sims/html/least-squares-regression/latest/least-squares-regression_en.html)

- [You can find an overview of the Method of Least Squares in the Georgia Tech online textbook](https://textbooks.math.gatech.edu/ila/least-squares.html)

- [Read more about least squares on Wikipedia](https://en.wikipedia.org/wiki/Least_squares)

- [Read Chapter 3, Sections 1 and 2 of Dan Simon, Optimal State Estimation (2006)](https://onlinelibrary.wiley.com/doi/book/10.1002/0470045345)

### Lesson 1: Practice Quiz
### Lesson 1 Practice Notebook: Least Squares

## Recursive Squares 

### Lesson 2: Recursive Least Squares
### Lesson 2 Practice Notebook: Recursive Least Squares
### Lesson 2 Supplementary Reading: Recursive Least Squares
### Lesson 3: Least Squares and the Method of Maximum Likelihood
### Lesson 2: Practice Quiz
### Lesson 3 Supplementary Reading: Least Squares and the Method of Maximum Likelihood
### Module 1: Graded Quiz



# References

[Least square for estimate theta - line 3321](https://github.com/afondiel/research-notes/blob/master/datascience-notes/courses/certificates/coursera/ibm/ds-ibm-notes.txt)

# Appendices