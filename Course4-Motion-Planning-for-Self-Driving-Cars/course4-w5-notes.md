# Course-4 - W5 - MODULE 5: Principles of Behaviour Planning

## Overview

- This module develops a basic rule-based behaviour planning system, which performs high level decision making of driving behaviours such as lane changes, passing of parked cars and progress through intersections. 
- The module defines a consistent set of rules that are evaluated to select preferred vehicle behaviours that restrict the set of possible paths and speed profiles to be explored in lower level planning.

**Learning Objectives**

- Recall the role of the Behaviour Planner, as well as its inputs and outputs.
- Use state machines to perform behaviour planning, and recognize their advantages and disadvantages.
- Recognize which behaviours are required to handle certain scenarios.
- Understand the advantages and disadvantages of rule engines in behaviour planning.
- Understand the advantages and disadvantages of reinforcement learning in behaviour planning.


### Lesson 1: Behaviour Planning

Welcome to the fifth week of the motion planning course.
- In this module, we will be discussing a very important part of our motion planning architecture, behavior planning.
- We will start this module off by introducing the concept of behavior planning, and how to construct the behavior plan or using a state machine.
- Then, throughout the rest of the module, we will go through the process of creating a state machine-based behavior planner, able to handle multiple scenarios.
- Finally, we will finish off this module by looking at alternative approaches to the behavior planning problem, to understand their relative strengths and weaknesses.
- In this lesson, we will, define the requirements for a behavior planning system, explore the typical inputs and outputs to a behavior planning module, and finally, introduce the concept of finite state machines, and how they can be used to create a behavior planning system.


**Behavior Planning**

`A behavior planning system` plans the set of high level driving actions, or maneuvers to safely achieve the driving mission under various driving situations.

<img src="./resources/w5/img/l1-behav-planning0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The set of maneuvers which are planned should take into account, the rules of the road, and the interactions with all static and dynamic objects in the environment.
- The set of high level decisions made by the planner must ensure vehicle safety and efficient motion through the environment.
- We discussed many of these concepts already in course one of this specialization, and it is the behavior planner that needs to make the right decisions to keep us moving safely towards our goal.
- As an example of the role of the behavior planner, let's suppose the autonomous vehicle arrives at a busy intersection.
- The behavior planner must plan when and where to stop, how long to stay stopped for, and when to proceed through the intersection.
- The behavior planner has to perform this type of decision-making in a computationally efficient manner, so that it can react quickly to changes in the environment, and be deployed on an autonomous vehicle hardware.
- The behavior planners should also be able to deal with inputs that are both inaccurate, corrupted by measurement noise, and incorrect, affected by perception errors such as false positive detections and false negative detections.


**Driving Maneuvers**

- Now that we have the definition for the role of the behavior planner, let's build a list of basic behaviors that we'll work with for the rest of this module.
- We've described most of these in an earlier video in this course, and we'll use this list as a representation of the set of likely maneuvers or driving behaviors encountered throughout regular driving that an autonomous vehicle may need to execute.
- In all, we'll consider 5 behaviors.

  - The first is `track speed`.

<img src="./resources/w5/img/l1-drv-maneuvers0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This behavior amounts to unconstrained driving on open road, meaning that the only restriction on forward progress is that the speed limit should be respected.
- Next, is `follow lead vehicle`.
- The speed of the vehicle in front of the ego vehicle should be matched and a safe following distance should be maintained.
- The third is `decelerate to stop`.

<img src="./resources/w5/img/l1-drv-maneuvers1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- A stop point exists in the ego vehicle's lane within the planning horizon, and the vehicle should decelerate to a standstill at that stop point.
- Every regulatory element that requires a complete stop triggers this behavior.


- Next, we have `stay stopped`.

<img src="./resources/w5/img/l1-drv-maneuvers2.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The vehicle should continue to stay stationary for a fixed amount of time.
- As an example, when the vehicle stops at a stop sign, it should stay stopped for at least `3 seconds`.

- Finally, we have the `merge behavior`.

<img src="./resources/w5/img/l1-drv-maneuvers3.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The vehicle should either merge into the left or right lane at this time.
- This basic list of maneuvers will serve us well in developing the principles of behavior planning.
- However, many more behaviors should be considered in practice, and the overall complexity of the behavior planner will grow as a result.

**Output of Behavior Planner**

The primary output of the behavior planner is a driving maneuver to be performed in the current environment.

<img src="./resources/w5/img/l1-behav-planner-output.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Along with the driving maneuver, the behavior planner also outputs a set of constraints, which constrain the local planning problem.
- The constraints which we will use and populate throughout this module include, the default path from the current location of the vehicle to the goal destination, for many behaviors, this is the center line of the ego vehicle's current lane.
- The speed limit along the default path.
- The lane boundaries of the current lane that should be maintained under nominal driving conditions.
- Any future stop locations which the vehicle needs to arrive at, and this constraint is only populated if the relevant maneuver is selected.
- Finally, the set of dynamic objects of high interest which the local planner should attend to.
- These dynamic objects may be important due to proximity or estimated future path.

**Input requirements**

In order for the behavior planner to be able to produce the required output, it needs a large amount of information from many other software systems in our autonomy stack.

<img src="./resources/w5/img/l1-input-reqs.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- First, the behavior planner relies on full knowledge of the road network near the vehicle.
- This knowledge comes from the high definition road map.
- Next, the behavior planner must know which roadways to follow to get to a goal location.
- This comes in the form of a mission path over the road network graph.
- Further, the location of the vehicle is also vital to be able to correctly position HD roadmap elements in the local environment around the vehicle.
- Accurate localization information is also needed from the localization system as a result.
- Finally, the behavior planner requires all relevant perception information, in order to fully understand the actions that need to be taken, to safely activate the mission.
- This information includes, all observed dynamic objects in the environment, such as cars, pedestrians, or bicycles.
- For each dynamic object, its current state, predicted paths, collision points, and time to collision, are all required.
- It also includes, all observed static objects in their respective states, such as parked vehicles, construction cones, and traffic lights, with an indication of their state.
- Finally, it includes a local occupancy grid map defining the safe areas to execute maneuvers.
- With all the necessary information available to it, the behavior planner must select the appropriate behavior, and define the necessary accompanying constraints to keep the vehicle safe and moving efficiently.
- To do so, we will construct a set of rules either explicitly or implicitly that consider all of the rules of the road and all of the interactions with other dynamic objects.

**Finite State Machines**

One approach traditionally used to represent the set of rules required to solve behavior selection is a finite state machine.

<img src="./resources/w5/img/l1-FSM0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Throughout this module, we will go through a step-by-step process of constructing a finite state machine-based behavior planner.
- We'll discuss some of the limitations of this approach.
- To better understand the finite state machine approach, let's walk through a simple example of a finite-state machine for a single scenario, handling a stop sign intersection with no traffic.
- The first set of components of a finite state machine, is the set of states.
- For behavior planning system, the states will represent each of the possible driving maneuvers, which can be encountered.
- In our example, we will only need two possible maneuvers or states, track speed and decelerate to stop.
- The maneuver decision defined by the behavior planner is set by the state of the finite state machine.
- Each state has associated with it an entry action, which is the action that is to be taken when a state is first entered.
- For our behavior planner, these entry actions involve setting the necessary constraint outputs to accompany the behavior decision.
- For instance, as soon as we enter the decelerate to stop state, we must also define the stopping point along the path.
- Similarly, the entry condition for the track speed state, sets the speed limit to track.
- The second set of components of the finite state machine, are the transitions, which define the movement from one state to another.
- In our two-state example, we can transition from track speed to decelerate to stop, and from decelerate to stop back to track speed.
- Note that there can also be transitions which return us to the current state, triggering the entry action to repeat for that state.
- Each transition is accompanied with a set of transition conditions that need to be met before changing to the next state.
- These transition conditions are monitored while in a state to determine when a transition should occur.
- For our simple example, the transition conditions going from track speed to decelerate to stop involved checking if a stop point is within a threshold distance in our current lane.
- Similarly, if we have reached zero velocity at the stop point, we can transition from decelerate to stop back to track speed.
- These two-state example highlights the most important aspects of the finite state machine-based behavior planner.
- As the number of scenarios and behaviors increases, the finite state machine that is needed becomes significantly more complex, with many more states and conditions for transition.
- Finite state machines can be a very simple and effective tool for behavior planning.

**Advantages Of Finite State Machines in Behaviour Planning**

We can think of them as a direct implementation of the definition of behavior planning, which requires us to define maneuvers or states, and local planning constraints or entry actions that satisfy the rules of the road and check safe interaction with other dynamic and static objects in the environment or transition conditions.

<img src="./resources/w5/img/l1-FSM2.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- By keeping track of the current maneuver and state of the driving environment, only relevant transitions out of the current state need to be considered, greatly reducing the number of conditions to check at each iteration.
- As a result of the decomposition of behavior planning into a set of states with transitions between them, the individual rules required remain relatively simple.
- This leads to straightforward implementations with clear divisions between separate behaviors.
- However, as the number of states increases, the complexity of defining all possible transitions and their conditions explodes.
- There is also no explicit way to handle uncertainty and errors in the input data.
- These challenges mean that the finite-state machine approach tends to run into difficulties, as we approach full level five autonomy.
- But it is an excellent starting point for systems with restricted operational design domains, permitting a manageable number of states.
- We'll look into these limitations and alternative approaches to behavior planning in the final video in this module.

**Summary**

- In this video, we formulated a clear definition of the behavior planning problem and its role within the overall motion planning system.
- We discussed the standard inputs and outputs of the behavior planning module.
- We introduced the finite state machine and its components, and applied it to a two-state behavior planning problem.
- From here, we'll start to add more capabilities to our finite-state machine behavior planner.



### Lesson 2: Handling an Intersection Scenario Without Dynamic Objects
### Lesson 3: Handling an Intersection Scenario with Dynamic Objects
### Lesson 4: Handling Multiple Scenarios
### Lesson 5: Advanced Methods for Behaviour Planning
### Module 5 Supplementary Reading

### Grade : Quiz

# References

# Appendices
