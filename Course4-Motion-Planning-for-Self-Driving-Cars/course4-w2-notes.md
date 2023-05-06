# Course-4 - W2 - MODULE 2: Mapping for Planning

## Overview

- The occupancy grid is a discretization of space into fixed-sized cells, each of which contains a probability that it is occupied. 
- It is a basic data structure used throughout robotics and an alternative to storing full point clouds. 
- This module introduces the occupancy grid and reviews the space and computation requirements of the data structure. 
- In many cases, a 2D occupancy grid is sufficient; learners will examine ways to efficiently compress and filter 3D LIDAR scans to form 2D maps.

**Learning Objectives**

- Create an occupancy grid map to identify static obstacles in the environment.
- Apply the log odds update to efficiently update occupancy beliefs.
- Apply filtering and compression to map 3D lidar scans to 2D occupancy grids.
- Understand the impact of dynamic obstacles on occupancy grids.

### Lesson 1: Occupancy Grids

**Learning Objectives**

- In this module, we will discuss the creation of two environmental maps :  
  - the occupancy grid map 
  - the high-definition road map.
- Both of the maps we will discuss play a critical role in the task of motion planning, as we will see throughout this course.
- We will start by defining the occupancy grid map in detail, and understand how it can be created on an autonomous vehicle.
- We will then try to understand the noise inherent in measurement data used for the creation of an occupancy grid map.
- Finally, you will see how to handle this noise in the measurement data, by learning about Bayesian updates of occupancy grid beliefs.


**Occupancy grid**

An `occupancy grid` is a discretized grid which surrounds the current ego vehicle position.

<img src="./resources/w2/img/l1-occup-grid0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This discretization can be done in two or three dimensions. The methods we discussed can be applied to both 2D and 3D problems.
- However, to simplify both the explanations as well as the computational requirements in this module, we will only be *focusing on the 2D version*.
- Each grid square of the occupancy grid indicates if a static or stationary object is present in that grid location. If so, that grid location is classified as `occupied`.

An example of static objects that would be classified as occupying a grid cell can include *trees, buildings, road signs, and light poles*.
- In the domain of autonomous vehicles, other objects which you might not think of as obstacles, should also be classified as occupying space, including all non drivable surfaces such as *lawns or sidewalks*.
- Each square of the occupancy grid noted by m_i, maps to a binary value in which one indicates that the square is occupied by a static object, and zero indicates that it is not.
- In the above map, we can see that the squares with trees and grass cover are labeled as $1$, whereas the road is labeled $0$ .

The resulting map looks like this : 

<img src="./resources/w2/img/l1-occup-grid1.png" width="520" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- All the occupied squares of the grid are purple, and the rest of the map corresponding to the drivable surfaces is left transparent.

**Assumption of Occupancy Grid**

We will now look at the set of assumptions that are made in order to create an accurate occupancy grid.

<img src="./resources/w2/img/l1-occup-grid2.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- First, the environment that is currently measured to create this occupancy grid only corresponds with static objects.
- Meaning, all dynamic objects or moving objects must be removed from the sensor data before it is used for occupancy grid mapping.
- Second, each grid cell is independent of all others. This assumption is made to simplify the update functions needed to create the occupancy grid.
- Finally, the current vehicle state is exactly known in relation to the occupancy map at every time step.

- In the domain of self-driving cars to observe distance between the car and the current state of the world, `the LIDAR sensor` is used most frequently.

<img src="./resources/w2/img/l1-occup-grid3.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- ```As a quick reminder, the LIDAR sensor uses pulses of light to measure the distance to all objects surrounding the car, and returns a point cloud of measurements throughout its field of view.``` 

**LIDAR Data Filtering**

- In this video, we can see the output of the LIDAR sensor.

<img src="./resources/w2/img/l1-data-filtering0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Several components of the LIDAR data need to be filtered out before this data can be used to construct an occupancy grid.
- The first step is to filter all LIDAR points which comprise the ground plane.
- In this case, `the ground plane` is the road surface which the autonomous car can safely drive on.
- Next, all points which appear above the highest point of the vehicle are also filtered out.

<img src="./resources/w2/img/l1-data-filtering1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This set of LIDAR points can be ignored as they will not impede the progression of the autonomous vehicle.

<img src="./resources/w2/img/l1-data-filtering2.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Finally, all non-static objects which had been captured by the LIDAR need to be removed.

- This includes all vehicles, pedestrians, bicycles, and animals.
- Once all filtering of the LIDAR data is complete, the 3D LIDAR data will need to be projected down to a 2D plane to be used to construct our occupancy grid.

<img src="./resources/w2/img/l1-data-filtering3.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The filtering and compression of the LIDAR data to create accurate occupancy grids for autonomous cars, will be covered in a later video in this module.

**Range Sensor**

The LIDAR data which is now filtered and compressed, resembles data from a high definition 2D range sensor, which accurately measures distance to all static objects around the vehicle in the plane.

<img src="./resources/w2/img/l1-range-sensor0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- However, there is still a problem. After all the filtering has been completed, there are still major map uncertainties due to the filtering methods used on the data, the complexity of the data at hand, and most of all, environmental and sensor noise.

<img src="./resources/w2/img/l1-data-noise1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Probabilistic Occcupancy Grid**

In order to handle this noise, the occupancy grid will be modified to be probabilistic.
  
<img src="./resources/w2/img/l1-proba-occup-grid0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Instead of cell i storing a binary value for occupied, now each cell i will store a probability between zero and one, corresponding to the certainty that the given square is occupied.
- The higher the value stored, the higher the probability that the given square is occupied.
- To use this set of probabilities, the occupancy grid can now be represented as a belief map denoted by the term $bel_{t}$ .
- To keep notations simple, m_i represents a single square of the occupancy grid, where $i$ can be constructed from measurements $Y$, and the vehicle location $X$ .
- The belief over Mi is equal to the probability that the current cell Mi is occupied given the sensor measurements gathered for that cell location.
- To convert back to a binary map, a threshold value can be established at which a given belief is confident enough to be classified as occupied.
- Any value below the set threshold will be set to free.

As an example, the occupied square in the figure to the left has a probability of 0.94, which classifies the square is occupied.
  
- On the other hand, the square found on the street only has a probability of 0.12 of being occupied, and thus will be classified as a free location.


**Bayesian Update of the Occupancy Grid**

- Multiple sets of measurements can be combined from time one to time t to achieve far more accurate belief of occupancy.

<img src="./resources/w2/img/l1-bayesian-update0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- In fact, we can update beliefs in a recursive manner so that at each time step t, we use all prior information from time one onwards to define our belief.
- The belief at time t over the map cell m_i is defined as the probability that m_i is occupied given all measurements and the vehicle position from time one to t.
- To combine multiple measurements into a single belief map, Bayes theorem can be applied.
- In the case of the occupancy grid, we get a Bayesian update step that takes the following form.
- The distribution p of y_t given m_i, is the probability of getting a particular measurement given a cell m_i is occupied.
- This is known as the measurement model, which you studied in detail in course two.
- The belief at time $t-1$ over m_i corresponds to the prior belief stored in our occupancy grid from the previous time step.
- We rely on `the Markov assumption`, that all necessary information for estimating cell occupancy is captured in the belief map at each time step.
- So no earlier history needs to be considered in the cell update equations.
- Finally, eta in this case corresponds to a normalizing constant applied to the belief map.
- This is needed to scale the results to make sure it remains a probability distribution.


**Cccupancy Grid in Action**

Lets see an occupancy grid in action.

- In this video, we will follow the autonomous vehicle as it drives out of the driveway and down a road, while the occupancy grid is updating in real time.

<img src="./resources/w2/img/l1-occup-grid-action0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The lighter grid cells represent free squares, whereas the black grid cells represent occupied squares.
- We can also see the raw LIDAR data in red, and the filtered outputs in orange.
- Notice how the map tracks the vehicle motion which is estimated using the same techniques as we've presented in [course 2](https://github.com/afondiel/Self-Driving-Cars-Specialization-Coursera/blob/main/Course2-State-Estimation-and-Localization-for-Self-Driving-Cars/course2-w1-notes.md).

<img src="./resources/w2/img/l1-occup-grid-action1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">
  
- In this video, the threshold of belief needed for an object to be classified as obstructing is set to very high, thus only large static objects are getting identified as occupied.
- Lowering this threshold value will result in more cells to be tagged as occupied, but will lead to noisier maps as well.

**Summary**

- you learned the basic definition of the Occupancy grid map, and saw how the LIDAR sensor data can be filtered and compressed to create an occupancy grid.
- You then learned how to represent the occupancy grid as a belief map, and applied Bayesian updates to incorporate new measurements in the occupancy grid.
- In the next video, we will discuss some of the numerical problems with our belief space map representation, and introduce the logit function as a solution to this problem.
- We will also look at an inverse measurement model which is needed to create the occupancy map grid from 2D LIDAR data using the logit function.


### Lesson 2: Populating Occupancy Grids from LIDAR Scan Data (Part 1)
### Lesson 2: Populating Occupancy Grids from LIDAR Scan Data (Part 2)
### Lesson 3: Occupancy Grid Updates for Self-Driving Cars
### Lesson 4: High Definition Road Maps
### Module 2 Supplementary Reading
### Lab : Occupancy Grid Generation
### Grade : Occupancy Grid Generation

# References

# Appendices
