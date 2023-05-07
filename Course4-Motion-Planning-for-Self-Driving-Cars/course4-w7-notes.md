# Course-4 - W7 - MODULE 7: Putting it all together - Smooth Local Planning

## Overview

- Parameterized curves are widely used to define paths through the environment for self-driving.
- This module introduces continuous curve path optimization as a two point boundary value problem which minimized deviation from a desired path while satisfying curvature constraints.

**Learning Objectives**

- Recall the definition of parametric curves, motion planning constraints, and motion planning boundary conditions.
- Understand the differences between spirals and splines, and the tradeoffs of using either.
- Design optimization objectives suited to particular motion planning tasks.
- Use Python libraries to solve optimization problems.
- Implement a conformal lattice planner based on polynomial spiral optimization.
- Compute a velocity profile constrained by curvature, speed limits, and dynamic obstacles.

## Smooth Local Planning

### Lesson 1: Parametric Curves

**Learning Objectives**

- In this module, we'll discuss the lowest level of our hierarchical motion planner, which is the local planner.
- As a reminder, the local planner is the portion of the hierarchical planner that executes the maneuver requested by the behavior planner in a collision-free, efficient, and comfortable manner.
- This results in either a trajectory, which is a sequence of points in space at given times or a path and velocity profile, which is a sequence of points in space with the required velocities at each point.
- This plan can then be given as the reference input to the controllers that you developed in course one.
- In this module, we'll build upon the introductory reactive planner we developed back in module four, such that it is able to handle some of the nuances presence in the autonomous driving motion planning problem.
- In particular, we'll move from the discrete time to continuous time in order to produce smooth parameterized paths that are easy to track with our controllers.
- In this video, we'll introduce the path planning problem and its associated constraints and boundary conditions.
- As well, we'll discuss parametric curves and how they are useful for representing paths for this problem.
- In particular, you should understand the difference between splines and spirals in the context of motion planning, and the advantages and drawbacks of each.


**Boundary Conditions**

- The first step in understanding the path planning problem is to first understand its most fundamental requirements.

<img src="./resources/w7/img/l1-params-curv0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- For the path planning problem, this is given a starting position, heading, and curvature, find a path to an ending position heading and curvature that satisfies our kinematic constraints.
- In the context of an optimization, the starting and end values can be formulated as the boundary conditions of the problem, and the kinematic motion of the vehicle can be formulated as continuous time constraints on the optimization variables.
- In this context, the boundary conditions are the conditions that must hold on either end point of the path for a given optimization solution to be considered feasible.
- If these boundary conditions are violated, no matter how great the path is, we haven't achieved our core objective of actually getting to the point we want to get to.
- So the path is not useful to us.
- These boundary conditions will influence how we decide to set up the underlying structure of the optimization problem.

**Kinematic constraints** 

- For our path planner, our only kinematic constraint is going to be restricting the maximum curvature along the path.

<img src="./resources/w7/img/l1-params-curv1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- In general, this is not easy to satisfy since there are infinitely many points along a continuous path.
- Instead, we will often take samples of the curvature at different points along the path, and constrain the curvature of each of these points.
- Assuming the path is relatively well-behaved, this will likely correspond to the curvature of the entire path satisfying the constraint.

**Parametric Curves**

- To simplify the representation of our optimization problem, we're going to define a path as a parametric curve.

<img src="./resources/w7/img/l1-params-curv2.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- **A parametric curve** is a curve that can be described as a set of equations with specific parameters.
- These parameters often denote path traversal, whether it will be through arc length or just varying from zero to one.
- For example, here we have a cubic spline set of parametric equations for the x and y positions of a path.
- The parameter of the equations u varies from zero to one, as we traveled from the start of the path to the end of the path.
- The vector valued function r contains the x and y position at each point corresponding to a given u value.

**Path Optimization**

- For autonomous driving, we often but not always require the path to be a `parametric curve`.

<img src="./resources/w7/img/l1-params-curv3.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- We often focus on planning methods that optimize a given path according to boundary conditions shown here by Beta naught and Beta f, kinematic constraints shown here by Alpha, and an objective functional shown here by f.
- Having a parametric representation of the path make setting up the optimization problem simpler, as we have a function we can directly give to our objective functional f.
- Note that the term functional refers to mappings that takes a function as their argument and return a real value, so it can be used to define a cost over a space of functions or parametrized curves.

**Non-Parametric Path**

- We can contrast this parametric curve approach with the reactive planner in module four, where we represented the trajectory and the path with a sequence of points in space.

<img src="./resources/w7/img/l1-params-curv4.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This is known as a non-parametric path since the curve we followed did not have a parametric representation.

**Path Parameterization Examples**

- In the field of autonomous driving, there are two common types of path parameterizations.

<img src="./resources/w7/img/l1-params-curv5.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The first are quintic splines which are fifth order polynomial functions of the x and y position of the car.
- The second type is the polynomial spiral, given by a polynomial curvature function with respect to arc length.
- Pictured here is a third order polynomial spiral, a cubic spiral, both of these parameterized curves give us the means to satisfy the boundary conditions we just discussed, and also offer us parameters to use in objective functions to craft the paths according to our requirements.
- Selecting either of these has associated tradeoffs.
  

**Quintic Splines**

- First, let's discuss the quintic spline.

<img src="./resources/w7/img/l1-params-curv6.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The quintic spline is given by two equations, one for the progression of x along the spline and one for y.
- Here we can see that the quintic spline has 12 parameters, six for the x equation and six for the y equation.
- These parameters correspond to the polynomial coefficients that form the shape of the curve.
- The traversal parameter u is fairly arbitrary here.
- For simplicity, we take it to be in the range of zero to one.
- What this means is that u equals zero corresponds to the start of the path, and u equals one corresponds to the end.
- A nice property of the quintic spline is that for given position heading and curvature boundary conditions, there is an immediate closed form solution for the spline coefficients that satisfy them.
- The solution is quite long so we won't listed here, but it is still cheaper to evaluate than generating a path using an iterative optimization method.
- See the supplemental materials for a full listing.
- There are also additional degrees of freedom which can be further optimize depending on this application.
- This is desirable because it allows us to generate a feasible solution to the boundary conditions immediately, which can be further refined in anytime fashion.

**Quintic Splines Curvature**

- The downside with quintic splines is that it is often hard to constrain curvature within a certain set of bounds as is often required in autonomous driving.

<img src="./resources/w7/img/l1-params-curv7.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- If we look at the curvature equation for a parametric curve, we can see that for our quintic splines, the curvature as a function of arc length will not in general be a polynomial.
- This has the potential to introduce cusps or even discontinuities of the curvature in the spline, which makes it difficult to approximately satisfy curvature constraints across the entire domain of the spline.
- We will discuss these curvature constraints in more detail in our next lesson, where we set up the optimization problem for path planning.

**Polynomial Spirals**

- As an alternative approach, we can also employ polynomial spirals to represent our path.

<img src="./resources/w7/img/l1-params-curv8.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- These curves offer a closed form equation for the curvature of the curve along each point of its arc length.
- For autonomous driving, it is common to select a cubic polynomial as our curvature function of arc length.
- However, higher-order functions are also acceptable.
- The main positive of using polynomial spirals is that their structure is highly conducive to satisfying the approximate curvature constraints that are often required by the path planning problem.
- Since a spiral is a polynomial function of curvature, the curvature value will not change extremely quickly like it can in the case of quintic splines.
- This means we can constrain the curvature of only a few points in the spiral and the spiral will very likely satisfy the curvature constraints across the entire curve.
- This is highly useful when performing path optimization, as the number of constraints greatly increases the computational effort of each optimization step.

**Polynomial Spiral Position**

- The downside of using polynomial spirals is that there is no closed form solution of the position and heading of the spiral, unlike the case in the quintic spline.

<img src="./resources/w7/img/l1-params-curv9.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Therefore, we must perform an iterative optimization in order to generate a spiral that satisfies our boundary conditions.
- As can be seen here, the position equations results in Fresnel integrals, which have no closed form solution.
- We therefore need to use numerical approximation techniques to compute the final end points of the spiral.
- In this module, we will approximate these Fresnel integrals using Simpson's rule shown here on the third line.
- Simpson's rule is more accurate with fewer points than other approximation methods, which will be useful when we setup our optimization problem.
- When it comes to the strengths and weaknesses of the spiral, we almost have a duality when compared to the spline, each has a weak point where the other is strong.
- The spline provides closed form solutions based on start and end points alone, whereas the spiral does not.
- The spiral ensures smooth curvature variation along the path, while the spline does not.
- You will therefore need to determine which method is appropriate depending on your specific application.
- As a brief shorthand, the spline leads to computational efficiency, while the spiral leads to easier implementation of curvature constraints.
- For this module, we will focus on the polynomial spirals as we develop our path planner, as we have a strong interest in ensuring the paths generated by our local planner can be executed smoothly and safely by the vehicle.
- However, many of the techniques described going forward can also be applied to quintic splines.

**Summary**

- We gave you an overview of the boundary conditions and parametric curves used in autonomous driving path planning, and we introduced splines and spirals as alternative path representations, and discuss their differences in the path planning context.
- In our next lesson, we'll be discussing how to set up the path planning optimization problem using the cubic spiral parametrization we discussed in this lesson, as well as the constraints and objective functions we defined earlier in this course.

### Lesson 2: Path Planning Optimization
### Lesson 3: Optimization in Python
### Lesson 4: Conformal Lattice Planning
### Lesson 5: Velocity Profile Generation
### Module 7 Supplementary Reading
## Final Project 



# References

# Appendices
