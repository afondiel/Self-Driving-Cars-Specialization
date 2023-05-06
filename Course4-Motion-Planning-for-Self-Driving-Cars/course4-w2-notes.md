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
- The belief over m_i is equal to the probability that the current cell m_i is occupied given the sensor measurements gathered for that cell location.
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


**Occupancy Grid in Action**

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

- In this video, we will identify the issues with the Bayesian Probability Update step which we saw in the previous lesson.
- We will then present a solution to the issues highlighted using a log odds representation.
- Finally, in this video, we will see the derivation of the Bayesian log odds update step required to update the belief map.

**Bayesian Update of the Occupancy Grid - Summary**

As we have seen in the previous video, we can apply Bayes' theorem to combine the previous belief map with the current measurement information to create a highly accurate occupancy grid at each time step.

<img src="./resources/w2/img/l2-bayesian-update-sum0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This is achieved by the following function in which n represents a normalizing constant, p of yt given mi is the current measurement received, and the belief at time t minus 1 over mi is the previous belief map.
- There is, however, a problem with using this simple Bayesian update.
- To demonstrate the issue, we will look at an example of an update to an unoccupied cell of the occupancy grid with a new unoccupied measurement.

**Issue With Standard Bayesian Update**

Let's suppose we have a cell which previously had a low belief of occupation, 6.38*10 - 4, and the new measurement results in low probability as well, 1.2*10 - 5.
- This means that the resulting belief would be very low, or 8.0 * 10 - 7. As you can see, all of these beliefs are quite close to zero.

<img src="./resources/w2/img/l2-bayesian-update-issue0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Multiplication of floating-point numbers on a computer, however, can lead to significant rounding error when multiplying small numbers, which in turn can lead to instability in the estimate of the probabilities.
- Further, the multiplication of probabilities turns out to be an inefficient way to perform the belief update.
- So our basic application of Bayes' rules to update beliefs over the occupancy cells is `not looking good`.
- There is, however, a solution. Instead of storing the belief map with the values ranging from 0-1, we can convert our beliefs into log odds probabilities using the logit function. We first saw this logit function in course 3.
- This leads to cell values ranging from negative infinity to positive infinity avoiding the issue with numbers close to zero.
- The logit function takes the natural logarithm of the ratio of the probability p and 1-p. So it takes probability values from 0-1 and maps them to the entire real axis.

**Conversion**

It is also possible to transition from the log odds domain back to probabilities.

<img src="./resources/w2/img/l2-conversion0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This is done by taking the ratio of e raised to the logit of p divided by 1 plus e to the logit of p.
- We now have an alternative representation for our cell probabilities.

**Bayesian Log Odds Single Cell Update Derivation**

So let's see how this affects our Bayesian update equation.

<img src="./resources/w2/img/l2-bayesian-log0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- We will start this derivation by the application of Bayes' rule to p of mi given y1 to t, where mi is the current occupancy grid map square at location i and y1 to t are the sensor measurements of that cell from time one to time t.
- Writing out the full Bayesian update for incorporating the latest measurements into our occupancy belief, we get the following equation.
- The first term in the numerator is the probability of getting measurement yt given the cell state at all previous measurements.
- The second term in the numerator is the probability a cell is occupied given all measurements to time t - 1, and the nominator is the probability of getting the measurements yt given all previous measurements up to time t - 1.
- It should be noted that the measurement yt is separated from the rest of the measurements of y1 to t - 1.
- This is done as we would like to update the occupancy grid with only the most recent sensor measurement rather than storing all measurements and applying them again every time.
- Next, we will apply `the Markov assumption` which ensures the current measurement is independent of previous measurements if the map state mi is known.

The next step is to expand the measurement model p of y given mi by the application of Bayes' rule once again.

<img src="./resources/w2/img/l2-bayesian-log1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This results in the probability of map cell mi being the current measurement multiplied by the probability of getting that measurement divided by the probability of grid cell mi is occupied.
- We now substitute the expanded measurement model in blue into the main Bayesian inference equation shown here.
- This leaves us with three terms in the numerator and two terms in the denominator.
- We will now pass this expanded form through the logit function and then start simplifying the resulting expression.
- Let's rearrange the term 1 minus p before we write out the resulting expression.
- The denominator portion of the log odds ratio 1 minus pmi given y1 to t can be constructed by negating the expression for the probability of a cell being occupied, which is of course, the probability that a grid cell is not occupied.
- Next, we form the log odds ratio which is simply the log of the ratio of the probability a cell is occupied to the probability it is not.

<img src="./resources/w2/img/l2-bayesian-log2.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- There are many like terms in this expression which we can now cancel out as follows.
- We arrive at the following simplified expression for the odds ratio with only three terms each in the numerator and denominator.
- We rewrite the expression in the original 1 minus p notation.

<img src="./resources/w2/img/l2-bayesian-log3.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- As you may have noticed, this equation is better viewed as three ratios.
- The ratio of the probabilities to 1 minus the same probability.
- The first ratio is the probability of a cell being occupied given a measurement y.
- The second is the probability a cell is not occupied, and the third is the prior belief that a cell is occupied given all measurements up to time t minus 1.
- Finally, we apply the log to our series of probability ratios to arrive at the addition of three logit functions.
- This is our final update equation and has the nice property of simply requiring addition when a new measurement is required.
- The three terms can be written in a convenient shorthand where lt minus 1i is the logit of the belief that cell $i$ is occupied at time $t-1$. Similarly, l0i at time zero and lti at time t. 

**Bayesian log odds Update**

We now arrive at the convenient log odds update rule for Bayesian inference on occupancy grid maps.
- It is made up of the three terms that are combined at each time step based on the latest measurement data.

<img src="./resources/w2/img/l2-bayesian-log4.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The first term the logit of the probability of mi given yt is the logit formed using new measurement information.
- The probability distribution p of mi given yt is known as the inverse measurement model. We'll study how to do this in the next lesson for LIDAR data.
- Lt minus 1i is the previous belief at time t minus 1 for cell i, and l0i is the initial belief at time zero for the same cell.
- The initial belief represents the baseline belief that a grid cell is occupied, which is usually set to 50 percent uniformly as we don't expect to have prior information that improves on this value.
- It shows up in this equation at every time step, which is a bit surprising but is simply a result of the derivation that we studied in this video and adjusts the addition of the first two terms to ensure the updated belief is consistent with the log odds form.
- The Bayesian log odds has two strong advantages over directly updating probabilities.
- The update is numerically stable due to the logit mapping of 01 probabilities to the entire real axis, and computationally, it is also significantly more efficient as it relies exclusively on addition to complete all updates of the occupancy grid.

**Summary**

- We first identified some issues with storing and updating the occupancy grid with a straightforward Bayesian probability update.
- We then saw how this issue could be solved by employing the log odds representation of the probability space.
- Finally, we saw how the Bayesian log odds update is derived from Bayes' rule.


### Lesson 2: Populating Occupancy Grids from LIDAR Scan Data (Part 2)

- In this video, we will define the concept of an inverse measurement model and see how to build a simple inverse measurement model for a lidar sensor.
- We will also describe ray tracing which will significantly reduce computational requirements for the inverse measurement model.
  
**Inverse Measurement Module**

- Recall from the previous video that in order to perform the Bayesian update of our occupancy grid, we need to be able to evaluate the log-odds update rule.

<img src="./resources/w2/img/l21-inv-meas-module0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- To do this we need to compute p of mi given yt which represents the probability of a cell mi in the occupancy grid being occupied, given a certain measurement yt is obtained by the lidar.
- However, so far the measurement models we have seen have taken the form the probability of yt given mi, which is in the mapping case represents the probability of getting a certain lidar measurement, given a cell in the occupancy grid is occupied.
- So for occupancy grid updates, we need to flip this measurement model around.
- That is, we have to construct an inverse measurement model that constructs p of mi given yt for every new measurement received.

**Inverse Measurement Module - To be improved**

As mentioned in the first lesson of this module, for simplicity sake, we will only look at the lidar data as a 2D range data containing two sets of information.

<img src="./resources/w2/img/l21-inv-meas-module1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The bearing at which each beam was fired and the range that the beam traveled.
- This is easily extended to 3D with the addition of an elevation angle.
- The bearing of each beam is represented by a set of angles Phi evenly spaced within a range defined by the minimum and maximum viewing angles of the sensor.
- Typical rotating lidar are able to capture data in all directions around the vehicle, we'll assume the available bearings in this course will cover all 360 degrees.
- The range of each beam corresponds to the distance it has traveled before impacting an object represented by r1 to rJ.
- The range is measured between minimum and maximum ranges r min and r max, and we'll assume r min is zero for simplicity.
- Most lidar today will also return a no echo signal, if a particular beam does not return an echo, indicating the absence of any object within range in that direction.
- As we proceed in this video, we will make an assumption here that the entire lidar scan measurements from a single rotation of the sensor is measured at the same instant in time.
- This is not an accurate model for a vehicle moving at speed with a rotating lidar head, as we must actually correct for the motion of the vehicle, the correction can be done using the state estimates you developed in course two, and interpolating the motion between these state estimates as needed.

**Inverse Measurement Module (cont'd)**

So the inverse measurement model will take the following form.

<img src="./resources/w2/img/l21-inv-meas-module2.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Suppose this is the vehicle with a lidar sensor collecting range measurements at different bearings in the following environment.
- We construct a temporary occupancy grid that encompasses the maximum range of the beams in all directions.

<img src="./resources/w2/img/l21-inv-meas-module3.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The coordinate frame for this measurement grid uses the occupancy grid map frame and so we define a position x1 t and x2 t and an orientation x3 t of the sensor in the occupancy grid frame.
- In practice, this occupancy grid frame is set to the vehicle frame and the map is transformed at each step based on our state estimates.
- We're now ready to populate the temporary measurement grid with occupancy probabilities.
- Based on the current lidar data, we can define 3 distinct areas of the measurement grid.

<img src="./resources/w2/img/l21-inv-meas-module4.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- First, there is an area of no information which none of the lidar beams had been able to reach.
- The current lidar scan provides no new information about the environment in this area.
- Then there is an area with low probability of an object, as all the beams have passed through this area without encountering anything.
- Finally, there is an area with high probability of an object, in which the lidar has come into contact with an object and has returned a non maximum range value.

**Inverse Measurement Module - To be fixed**

To translate these areas onto the measurement grid, each grid square will be assigned a range in bearing relative to the vehicles current location.

<img src="./resources/w2/img/l21-inv-meas-module5.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The relative range of each cell is simply the Euclidean distance from the sensor to the cell, defined as follows, where ri is the range to grid cell i and mxi and myi are the x and y coordinates of the center of the grid cell.
- Finally, x1 t and x2 t are the sensor location at the current time t.
- The relative bearing to each cell is computed using the tan inverse function.
- Here Phi identifies the bearing to the given cell in reference to the sensor's coordinate frame.
- For each cell, we associate the most relevant lidar beam by finding the measurement with the minimum error between its beam angle and the cell bearing.

We then define two parameters Alpha and Beta, which define a sector around each beam in which cell occupancy should be determined based on the beam range.

<img src="./resources/w2/img/l21-inv-meas-module6.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This essentially creates a region around each beam which will get assigned the measurement information of that particular beam.
- $\alpha$ controls the range cells at the range of the beam which will be tagged as high probability.
- $\beta$ controls the angle of the beam for which cells will be marked as either low or high probability.

**Inverse Measurement Module - Algorithm**

- We are now ready to assign a probability that any cell is occupied given the lidar measurements received based on these 3 types of cells.

<img src="./resources/w2/img/l21-inv-meas-module7.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The no information zone corresponds to all cells with a greater range, than the measured range or outside the angle Beta sized cone for the measurements associated with it.
- We assign a probability of an obstacle equal to the prior probability of a cell being occupied which is usually 0.5.
- The high information zone defines cells that fall within Alpha over two of the range measurement and within Beta over two of the angle of the measurement associated with it.
- We assign an occupied probability of greater than 0.5. to these cells.
- Finally, the low information zone is defined by cells that have a range less than the measured range minus Alpha over two and lie within the Beta sized cone about the measurement.
- We assign an occupied probability of less than 0.5 to these cells.

For example, let's say a lidar scan returns a range to an object at the location marked by a red X.

<img src="./resources/w2/img/l21-inv-meas-module8.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The affected area which will be tagged as high probability is given in red.
- Increasing the value of Alpha will increase the range of the affected region and increasing the value of Beta affects the angle of the affected region.
- We can now construct the full inverse measurement model to be used in our log-odds update.

**Inverse Measurement Module - With Ray Tracing**

However, this simple inverse measurement model can be computationally expensive.

<img src="./resources/w2/img/l21-inv-meas-module9.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- It requires a full update of every cell in the measurement map, and relies on multiple floating-point operations to identify which measurements correspond to which cells.
- An alternative, is to use a ray tracing algorithm, such as the computer science classic, the Bresenham's line algorithm.
- `Bresenham's line algorithm` was originally designed in the early 1960's to efficiently solve the line plotting problem for displays and printing on the available hardware of the day.
- By ray tracing along the beams of the lidar scan, we reduce the number of cells that need to be processed and identify them more quickly relying on integer addition subtraction and bit shifting to move through the grid along the lidar beams.
- Interestingly, many beams go through the same cells near the car greatly increasing the confidence in measurements nearby.
- This concludes our discussion of the inverse measurement model for log odds occupancy grid mapping.

**Summary**

- In this video, we constructed a simple inverse measurement model for lidar data needed in the log-odds update step.
- We also briefly covered a potential improvement by using ray tracing to speed computations.


### Lesson 3: Occupancy Grid Updates for Self-Driving Cars
### Lesson 4: High Definition Road Maps
### Module 2 Supplementary Reading


### Lab : Occupancy Grid Generation
### Grade : Occupancy Grid Generation

# References

# Appendices
