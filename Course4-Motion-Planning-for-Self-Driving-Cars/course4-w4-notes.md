# Course-4 - W4 - MODULE 4: Dynamic Object Interactions

## Overview

- This module introduces dynamic obstacles into the behaviour planning problem, and presents learners with the tools to assess the time to collision of vehicles and pedestrians in the environment.

**Learning Objectives**

- Recall the different types of motion prediction assumptions, and the differences between them.
- Understand how map knowledge can be used for prediction.
- Understand how multi-hypothesis prediction can be used to predict multiple behaviours.
- Compute Time-to-Collision (TTC) through estimation and simulation methods.

### Lesson 1: Motion Prediction

- This week, we will discuss methods used within the motion planner, to handle interactions between dynamic objects and the ego vehicle.
- We will start this week, by looking at the prediction of dynamic object motion.
- We will then go on to understanding how we are able to use the dynamic object predictions, in order to calculate the time to collision between the ego vehicle and other dynamic objects.
- In this lesson, we will define motion prediction for dynamic objects and identify the importance of such predictions in the greater path planning problem.
- We'll describe the requirements to accurately and safely predict the motion of dynamic objects, and explore the challenges inherent in motion prediction.
- Finally, we'll perform our first predictions with the constant velocity prediction model.

**Motion prediction - Definition**

**Motion prediction** attempts to estimate the future positions, headings, and velocities of all dynamic objects in the environment over some finite horizon.

<img src="./resources/w4/img/l1-motion-pred0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This is crucially important for the motion planning problem, as it allows us to plan future actions and maneuvers for the autonomous vehicle, based on the expected motions of other objects.
- The predicted paths also allow us to make sure that the path which the ego vehicle plans to execute, will not collide with any future objects at a future time.


**Requirements for Motion Prediction Models**

In order to be able to predict the motion of moving objects, we must have access to some information about the environment around us.

<img src="./resources/w4/img/l1-motion-pred-reqs.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Especially as it relates to dynamic objects.
- For all dynamic objects, we must first know the class of the object.
- This information is vitally important as most prediction models have different algorithmic approaches to vehicles as opposed to pedestrians.
- Next, we need to have information regarding the dynamic objects current state, its position, and velocity in the environment.
- Represented here by a red vector with the vector origin equal to the vehicle position, the vector magnitude equal to its speed, and the vector's direction equal to its current heading or direction of travel.
- Without this minimal information, no predictions can be made about the dynamic objects future states.
- Finally, there are many other pieces of information which although not required to make a prediction, can greatly improve the accuracy of the predictions.
- While this list that we'll present is not exhaustive, it does demonstrate some of the major sources of additional information to improve predictions.
- First is the history of the dynamic vehicle state or the vehicle track as it moves through the environment. This can be extremely useful.
- You've learned how to generate vehicle tracks from object detections in course three.
- We can use this information to get a better idea of how the object is maneuvering through the environment.
- As we can see in our example, we can see the vehicle state history shown as black arrow, with the position heading and speed represented as before.
- A high definition roadmap can also be used as an additional information source, to determine future behavior of dynamic objects.
- As will be discussed further in this module, vehicles tend to follow their respective lanes while driving down the road.
- This can provide strong cues to improve prediction accuracy.
- An image of the dynamic object in its current state can also be a useful source of information that can improve predictions.
- This is true for both vehicles and pedestrians.
- For vehicles, the image can provide information concerning the current indicator light or brake lights states, for example.
- Similarly, images of pedestrians can serve to show the current orientation of the person, which can help predict a future direction of travel, even if the pedestrian is currently stationary.

**Simplification of Motion Prediction - Cars**

Although the complexities of the task of motion prediction are quite large, there are several assumptions we can use to simplify the problem.

<img src="./resources/w4/img/l1-motion-pred-cars.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- We will start by looking at simplifications for vehicles and then move on to pedestrians.
- These are the two main categories we'll discuss, but you can imagine similar approaches needed for cyclists and animals such as dear, rodents, or even kangaroos.
- The `first class` of assumptions we rely on, is that vehicles must follow a set of physical constraints governing their movement.
  - As we saw in course one when we were discussing Vehicle Kinematics and Dynamics.
  - These very same vehicle dynamics can be applied to other vehicles in the environment to predict their motion.
  - We refer to this type of prediction as a `physics-based prediction`.
- The `second class` of assumptions that can be used are that almost all motions by a vehicle on the road, are made up of a finite set of maneuvers in a restricted domain in the environment.
  - In this case, we assume that vehicles which are on the road will stay on the road and follow the driving rules.
  - For example, they will most likely stay in their lane unless indicating otherwise and stop at regulatory elements requiring stops.
  - They are unlikely to drive over sidewalks or lawns or through obstacles.
  - We refer to this type of assumption as maneuver-based.
- Finally, the `third class` makes the same assumptions as `the maneuver-based assumptions`.
  
- However, instead of only evaluating each vehicle independently, we can also incorporate the assumption that the dynamic objects will react and interact with each other.
- An example of this type of prediction, is during a merge by a vehicle into an adjacent lane.
- Often, the vehicle in the destination lane will slow down to make more room for the incoming vehicle to maintain a safe following distance.
- These types of assumptions are referred to as interaction-aware assumptions.

**Complexities of Motion Prediction - Pedestrians**

For pedestrians, the same three categories can be used to summarize the assumptions we can make.

<img src="./resources/w4/img/l1-motion-pred-pedestrians.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- In terms of physics-based assumptions, pedestrians tend to have a low top speed but can change their direction of motion and speed very quickly.
- This makes pedestrians quite challenging to predict reliably using purely physics-based assumptions, but the range of positions a pedestrian can reach in a short time frame is limited.
- For maneuver based assumptions, pedestrians tend not to interact directly with vehicles.
- As they primarily use sidewalks or other pedestrian exclusive zones when traveling.
- When entering the drivable areas of the environment such that they might come into contact with vehicles, they primarily use pedestrian crossings.
- Although restricting pedestrian motion to these regions is a reasonable assumption, it is not a hard constraint and the unpredictability of pedestrians requires maintaining multiple possible hypotheses about their future actions.
- Finally, pedestrians ultimately have the right of way and it is the self-driving cars duty to stop when necessary.
- Inattentive pedestrians may wander into a roadway without warning, but will often stop when threatened by an oncoming vehicle.
- These types of interactive assumptions can also be incorporated into motion prediction for pedestrians.

**Constant Velocity Prediction Model**

Now that we have a better understanding of motion prediction, let's have a look at a simple computationally efficient algorithm, that can be equally applied to both pedestrians and vehicles.

<img src="./resources/w4/img/l1-motion-pred-velocity-model.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This algorithm makes only one extreme assumption regarding the motion of the dynamic object.
- All dynamic objects will maintain their current velocity both in terms of magnitude as well as heading.
- Understanding this, let's now look at the algorithmic implementation of this simple constant velocity model.

**Constant Velocity Prediction Model - Algorithm**

- The algorithm takes three basic inputs t, the prediction horizon or the amount of time to predict the object's location into the future, dt, the update rate or path simulation frequency, that is the amount of time between state predictions, and x object, the current object's state which includes the position and velocity of the dynamic object.

<img src="./resources/w4/img/l1-motion-pred-velocity-model-algo.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This algorithm iterates from the current time zero until the end of the horizon t in increments of dt.
- As we saw in the trajectory rollout algorithm in the previous videos, updating the path with constant velocity model.
- The output of this algorithm is a list of predicted objects states, positions, and velocities for every time step in the prediction horizon.

**Constant Velocity Prediction Model - Example**

To see how well these predictions perform, let's look at a quick example.

<img src="./resources/w4/img/l1-motion-pred-velocity-model-ex.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- We'll use a three second horizon with a one second update step and the current vehicles state as indicated by the red arrow in this figure.
- As expected, the predicted locations of the vehicle move in a constant direction with a fixed step size which corresponds very nicely with this straight line segment, with a constant speed limit.
- Simply put, this is because the constant velocity assumption is valid for this segment of roadway.

**Constant Velocity Prediction Model - Issues**

Where the constant velocity estimate fails, however, is everywhere else.

<img src="./resources/w4/img/l1-motion-pred-velocity-model-issues.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- While this algorithm weakly falls into the category of physics-based assumptions, it fails to capture the full complexity of vehicle dynamics models, or even the ability of a vehicle to accelerate or decelerate or apply a steering command other than zero.
- Another large flaw of the constant velocity assumption, is that it fails to account for vehicles tendency to follow changes in the road shape.
- At every point in this curved roadway example, the constant velocity model predicts the path will continue into the oncoming lane.
- These predictions are wholly unsuited to behavior planning.
- Similarly, the constant velocity prediction fails to account for road signs to make velocity adjustments.
- Vehicles approaching stop signs tend to slow down and vehicles leaving a stop line tend to accelerate.
- The assumption which this algorithm makes is quite strong and does not apply for most cases that dynamic objects may be observed in.
- The key challenge to motion prediction is really to select the most likely inputs, to a vehicle or pedestrian model given what information is available.
- Nonetheless, the constant velocity model is an excellent starting point and helps define the concept of motion prediction clearly.
- It relies on a minimum of information about the dynamic object, to form its predictions and can be used wherever additional cues are completely unavailable.


**Summary**

- In this lesson, we learned about the task of motion prediction for dynamic objects and its importance to autonomous driving.
- We then defined minimal and optional information requirements to create effective motion prediction algorithms for both vehicles and pedestrians.
- We then looked at a simple constant velocity algorithm for predicting the future location of objects and identified many of its limitations.


### Lesson 2: Map-Aware Motion Prediction
### Lesson 3: Time to Collision
### Module 4 Supplementary Reading

### Grade: Quiz

# References

# Appendices
