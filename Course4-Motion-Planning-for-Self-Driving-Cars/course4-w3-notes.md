# Course-4 - W3 - MODULE 3: Mission Planning in Driving Environments

## Overview

- This module develops the concepts of shortest path search on graphs in order to find a sequence of road segments in a driving map that will navigate a vehicle from a current location to a destination. 
- The modules covers the definition of a roadmap graph with road segments, intersections and travel times, and presents `Dijkstra’s` and `A*` search for identification of the shortest path across the road network.

**Learning Objectives**

- Recall the mathematical concept of a graph.
- Understand how graphs can be used to represent road networks.
- Apply Breadth First Search (BFS) to an unweighted graph to find the shortest path to a destination.
- Apply Dijkstra's Search to a weighted graph for finding the shortest path in a more realistic road network.
- Apply heuristics through A* Search to improve shortest path search speed.


### Lesson 1: Creating a Road Network Graph

**Learning Objectives**

- In this module, we'll be discussing the mission planning problem in autonomous driving and how to solve it.
- If you recall from Module 1, the autonomous driving mission is the highest level portion of our motion planning task and it's crucial for navigating the autonomous car to its destination.
- In this video, we'll introduce the mathematical concept of a graph and how it can be used in our mission planner.
- In addition, we will discuss how a graph can be used to represent the road network that we are required to navigate through.
- Finally, we'll discuss the Breadth-First Search algorithm and how it can be applied to mission planning.

**Recall: Mission Planning.**

The objective of the autonomous driving mission is to find the optimal path for the eagle vehicle from its current position to a given destination by navigating the road network while abstracting away the lower-level details like the rules of the road and other agents present in the driving scenario.

<img src="./resources/w3/img/l1-motion-planning0.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- ```In this module, we will think of `optimality` in terms of the amount of time or distance it takes for the car to reach its destination.```

- For autonomous driving, mission planning is considered the highest level planning problem.
- This is because the spatial planning scale of the mission planner is on the order of kilometers and the mission planner doesn't focus on low-level planning constraints such as obstacles or dynamics.
- Instead, the mission planner will focus on aspects of the road network when planning, such as *speed limits* and *road lengths*, traffic flow rates and road closures.
- Based on these constraints posed to us by the map, the mission planner needs to find the optimal path to our required destination.

One thing to note about the road network is that it is highly structured which is something we can exploit in our planning process to simplify the problem.

<img src="./resources/w3/img/l1-motion-planning1.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- By exploiting the structure, we can efficiently find the optimal path to our destination based on the map given to us.
- To do this, we will need to use a mathematical structure known as a `graph`, which we've overlaid onto our road network here.

**Graph**

- A graph is a discrete structure composed of a set of vertices denoted as $V$ and a set of edges denoted as $E$ .

<img src="./resources/w3/img/l1-graph0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- For the mission planner, each vertex in V will correspond to a given point on the road network, and each edge E will correspond to the road segment that connects any two points in the road network.
- In this sense, a sequence of contiguous edges in the graph corresponds to a path through the road network from one point to another.
- For now, we will assume each road segment is of equal length, so the edges of this graph are all unweighted.
- However, in future lessons, we will relax this restriction.
- To generate a graph such as this, the road network needs to be `discreetly sampled`, which will give us the vertices of our graph.
- The edges will then be defined by the segments of the road that connect each sample point according to the rules of the road.
- Note that in general, just because point $A$ is adjacent to point $B$ using a road segment, it does not mean that point A can be reached from point $B$ from that same road segment.
- This is because in many cases there is only one direction that a road segment can be legally traversed.
- In this sense, the edges of our graph are `directed` in that the edge is only traversable in one direction. We've denoted this by using arrows for our edges in the graph to display their directionality.


*Now that we have are directed graph, how do we find an optimal path to our destination?* 

- First, we locate the vertices in the graph that correspond to our current eagle vehicle position which we will denote as $S$ and our desired destination which we will denote as $t$ .
- These two vertices are shown on the graph here.
- Once we have these two vertices, we can use an efficient graph search algorithm to find the optimal or shortest path to our destination.
- Since our graph formulation is currently unweighted, a good candidate algorithm is the Breadth-First Search (BFS).

**Breadth-First Search (BFS)**

- At a high level, BFS can be thought of as iterating through all of the vertices in the graph but doing so in a manner such that all adjacent vertices are evaluated first before proceeding deeper into the graph.
- In this sense, the graph search proceeds like a moving wavefront through the graph or breadth-first.
- We construct 3 data structures to aid in our search and `open queue of vertices` still to be assessed, a `closed set of vertices` that have been assessed by the search algorithm and a `dictionary` of predecessors which store the results of the search.
  - **A queue** is a first-in-first-out (FIFO) data structure, such that the first vertex pushed or added to the queue is the first one popped off or returned from the queue.
  - **A dictionary** is an unordered set of `key-value pairs` and for each node in the closed set, stores a predecessor vertex that will identify momentarily.

<img src="./resources/w3/img/l1-bfs0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

```
- The algorithm starts by adding our start vertex to the open queue.
- Then, while the open queue contains vertices, we take the first element from the open queue and check if it is the goal location.
- If so, we found our shortest path. If not, we then add all adjacent vertices not already in the open queue or closed set to the open queue.
- This prevents us from getting stuck in cycles during the graph search.
- Note that by adjacent, we mean all vertices that can be reached from the current vertex.
- Because we use a queue to store open vertices, we ensure that all adjacent vertices at the current depth in the search are processed before proceeding deeper into the graph.
- So all vertices that are one step away from the start vertex will be processed before moving on to vertices that are two steps away.
- As a vertex is added to the open queue, we store its preceding vertex in the predecessor dictionary.
- This will help us reconstruct the optimal path once the goal is found.
- Finally, we add the currently active vertex to the closed set and return to the next element of the open queue to process.
```
- Because of the breadth-first nature of the BFS algorithm, by the time we reach the goal vertex, we have processed all possible predecessor vertices of the golden vertex that are closer to the start vertex then the goal vertex.
- This means that when we reach the goal vertex, we have found `the shortest path` to the goal vertex and we can terminate the algorithm.

- To solidify our understanding of this algorithm, let's work through a concrete example.

**Example - First Wavefront**

Suppose our mission planner needs to find the optimal path from point $s$ to our destination $t$ through the set of vertices in our graph which are now labeled. 

<img src="./resources/w3/img/l1-1-wavefront.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The first step would be to process the origin $s$ and add all adjacent vertices to our queue and set their predecessors to $s$ .
- The outgoing edges that lead to the adjacent vertices are highlighted in blue.
- Once we've added these to our queue, we then add $s$ to our closed list.
- Next, we pop off vertex $a$ .

**Example - Second Wavefront**

<img src="./resources/w3/img/l1-20-wavefront.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The outgoing edges of a lead to $d$ and $b$, but $b$ is already in our queue, thus, we only add $d$ to the queue and mark $a$ as its predecessor.
- We've highlighted this duplicate path to be in red to show that we do not add b to the queue twice.
- We've now processed all adjacent edges from a and move it to the closed set.
- We repeat the same process for $b$ which adds $E$ to the queue with $b$ as its predecessor and $c$ which has no new adjacent vertices so does not add vertices to the open queue.
- Next, we process $d$ from the queue, which only adds $t$ to the queue with $d$ as its predecessor since $e$ has already been added.

<img src="./resources/w3/img/l1-3-wavefront.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- When $e$ is popped off, it doesn't add $c$ or $d$ to the queue because both of these vertices have already been processed and are present in the closed set.

- Finally, we pop off $t$ from the queue. This is our goal vertex.

<img src="./resources/w3/img/l1-optimal-path0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- So we now reconstruct the path from $s$ to $t$ by following the chain of predecessors from $t$ back to $s$.
- Once this is done, we've found the optimal path to our destination, which is highlighted in green.
- The sequence of edges corresponding to our optimal path in the graph can be turned into a root over the road network using our map, which can then be used to govern more detailed motion planning in the subsequent layers of our planning hierarchy.
- Before we wrap up this lesson, we should note that there is also the highly related `Depth-First Search algorithm` among many others.
- **Depth-First Search** (DFS) uses a last-in, first-out (LIFO) stack instead of a queue for the open set.
- This change means that the most recently added vertex is evaluated instead of the oldest.
- The result is a search that quickly moves deeper in the graph and then eventually backtracks to vertices added much earlier.

**Summary**

- From this video, you should have an understanding of the mission planning problem and how we construct and use graphs as a map level representation of our planning domain.
- In addition, you should now be comfortable with using Breadth-First Search to navigate an unweighted graph to find the shortest path to a given destination.


### Lesson 2: Dijkstra's Shortest Path Search

- In this lesson we'll modify our unweighted graph, from the previous lesson to contain edge weights.
- To give a more applicable representation for our mission planning problem.
- We'll then discuss how it impacts our algorithm, and how we can overcome this challenge while still planning efficiently.
- In particular by the end of this video, you should be able to understand the difference between weighted and unweighted graphs, and why weighted graphs are more useful for mission planning.
- You should have a firm grasp of the Dijkstra's algorithm.
- A graph search algorithm that is useful for weighted graphs.

**Unweighted Graph**

As a refresher, recall that for our mission planning problem, the goal is to find the optimal path in our road network from the ego vehicles current position, to the required final destination.

<img src="./resources/w3/img/l2-unweighted-graph.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- In the last video we presented the breadth-first search algorithm to solve this problem.
- However, in the process we assume that all road segments have equal length, which is an overly simplistic assumption.
- Depending on factors such as road lengths, traffic, speed limits, and weather, different road segments can vary wildly in their traversal costs.
- For simplicity, we will initially focus purely on distance in our search graph.
- To reflect this, we will add edge weights to each edge in the graph, that correspond to the length of the corresponding road segment.

**Weighted Graph**

This is shown here, after updating our unweighted graph with appropriate edge weights.

<img src="./resources/w3/img/l2-weighted-graph.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The units of the weights are arbitrary, as long as they are common to all edges.
- For this instance, suppose the edge weights are the number of kilometers it takes to travel across that road segment.
- As before, the goal is to find the optimal path from the vertex of the ego vehicles current position S to the final destination vertex T.
- Unfortunately, our BFS algorithm doesn't take edge weights into consideration.
- So it isn't guaranteed to find the optimal path in this situation.
- We instead need to use a different more powerful algorithm. This is where `Dijkstra's algorithm` comes in.

**Dijkstra's algorithm**

- `Edsger Dijkstra`, a Dutch computer scientist, first conceived of this algorithm in 1956.
- In an interview in 2001, he explains that he was shopping with his fiance at the time, and got tired and they sat down for a coffee.
- He had been puzzling with the shortest path problem in his head, and within 20 minutes he worked out his algorithm without pen or paper.
- It took him three more years to write a paper on this topic, but he credits the simplicity and elegance of the idea with being forced to work through the solution entirely in his head.

The overall flow of Dijkstra's algorithm is quite similar to BFS.
- The main difference is in the order we process the vertices. We've highlighted the differences from the BFS algorithm in `blue`.
  
<img src="./resources/w3/img/l2-dijkstra-algo0.png" width="520" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- As before, we keep track of the vertices we have already processed in the closed set, and the vertices we've discovered but not yet processed in the open set.
- The key difference is that instead of using a `queue` for the open set, we'll be using a `min heap`.
- ```A min heap is a data structure that stores keys and values, and sorts the keys in terms of their associated values from smallest to largest```.
- In our case, the values of each key vertex in the graph will correspond to the distance it takes to reach that vertex, along the shortest path to that vertex we've found so far.
- In this sense, Dijkstra's algorithm processes vertices with a lower accumulated cost before other ones.
- Thus unlike BFS, a vertex that was added later in the search can be processed before when that was added earlier, so long as it's accumulated cost is lower.
- Other than that, Dijkstra's algorithm is largely the same as BFS.
- Progressing through the vertices, while adding and popping them off of the min heap until the goal vertex is processed.
- One interesting case however, is if we find a new path to a vertex that is already in the open heap but has not been processed yet.
- In this case, we have to check if the newly found path to this vertex is cheaper than the old path.
- If it is, we need to update its cost in the min-heap otherwise, no action is required.
- Once we process the goal vertex we must have necessarily processed all possible predecessor vertices of the goal node.
- Since a predecessor must have accumulated distance less than or equal to the goal vertex.
- Since all predecessor vertices have been processed, we will have found the shortest path to the goal vertex.
- Once the goal vertex has been processed, so the algorithm can terminate.
- To solidify our understanding, let's step through the application of Dijkstra's algorithm to our new weighted graph.

**Example - Processing S**

- For our graph as with BFS, the first vertex to process is $S$ , which then adds $A$ , $B$ and $C$ , to the min heap.

<img src="./resources/w3/img/l2-dijkstra-algo1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- By default, the accumulated cost of the origin $S$ is $0$ . So the cost to reach $A$, $B$ and $C$, is $5$, $7$ and $2$ respectively.
- Since we are using a min-heap instead of a queue for Dijkstra's algorithm, the order of the open vertices is now $CAB$ sorted from lowest cost to highest cost in the heap.
- We store each of these vertices predecessors as $S$, and then add $S$ to the closed set.

**Example - Processing C**

Next, we pop $C$ from the heap. Since it is the lowest cost vertex so far.

<img src="./resources/w3/img/l2-dijkstra-algo2.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- $C$ is only connected to $E$ , which has not yet been discovered.
- So we add it to the min heap with a cost of $2$ plus $8$ is ten, along with C as its predecessor.
- Our new heap ordering is $A$ , $B$ and $E$ . We then add $C$ to the closed set.

**Example - Processing A**

The next vertex to pop off the heap is $A$ , which connects to both $D$ and $B$ .

<img src="./resources/w3/img/l2-dijkstra-algo3.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- $D$ is not yet been explored, so we add it to the heap with a cost of $5$ plus 2 for $7$, and $b$ however has been explored as it currently has an accumulated cost of $7$.
- The edge $AB$ has weight one, so the new cost of going through $A$ is $5$ plus one for $6$ .
- Since this is lower than the current cost of $B$ which was $7$, we update the cost of $B$ in the heap to $6$ , and change its predecessor from $S$ to $A$ .
- To show that the cost of $B$ was updated, we have marked the new edge to be as purple.
- We then close vertex $A$ . Our vertex ordering in the min heap is now $B$ , $D$ and $E$ .

**Example - Processing B**

- We now pop $B$ off of the heap, which only connects to $E$. 
  
<img src="./resources/w3/img/l2-dijkstra-algo4.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The cost so far to reach $B$ is $6$ , which gives us a cost of nine to reach $E$ .
- $E$ was already stored in the min heap with a cost of ten.
- So, we need to update the cost of $E$ to nine, as well as change its predecessor from $C$ to $B$ .
- Finally, we close vertex $B$ . Our new vertex ordering in the min-heap is $D$ then $E$ .

**Example - Processing D**

Next, we pop $D$ off of the heap which connects both $E$ and $T$ .

<img src="./resources/w3/img/l2-dijkstra-algo5.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- $E$ is already in the heap with cost nine, and the new path from $D$ to $E$ has a cost of 14.
- Since this is higher than E's current cost, we can ignore this new path.
- To show that we've ignored it, we mark the new edge to $E$ as red instead of purple.
- We then add $T$ to the heap of a cost of $7$ plus one is $8$, setting D as its predecessor.
- Finally, we close vertex $D$ . Our new heap ordering is $T$ and then $E$ .

**Example - Optimal Path**

The final vertex that we pop off is T, which is our goal vertex.

<img src="./resources/w3/img/l2-dijkstra-algo6.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This completes the planning process, and we now have an optimal path formed by chaining together the predecessors of T all the way back to the origin, as highlighted on this graph here.

**Search on a Map**

Next, let's take a look at how this mission planning problem looks on a real map.

<img src="./resources/w3/img/l2-dijkstra-map.png" width="480" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Here we have a map of Berkeley, California. Where the vertices of the graph correspond to intersections, and the edges correspond to road segments as we discussed earlier.
- The two red dots, correspond to the start and end points of our required plan.
- We have to remember that certain roads are one-way roads. As such, the graph is directed.
- After running Dijkstra's algorithm, the shortest path between the two nodes is given by the red path.
- Dijkstra's algorithm is quite efficient, which allows it to scale really well to real-world problems such as the ones shown here.
- In fact, it even works with a much larger scale problems such as navigating over New York City. Whose road network graph is shown below.
- While Dijkstra's is an efficient algorithm, we can leverage certain heuristics to make it even faster in practice, which we'll discuss in our next lesson.

**Summary**

- We first introduced the concept of a weighted graph, and discussed that having the ability to make certain edges have higher weights than others, better reflects the autonomous driving mission.
- As different roads are longer than others.
- As a consequence of this, our breadth-first search algorithm no longer works.
- So we introduced Dijkstra's algorithm, to handle this added complexity.
- In our next lesson, we'll be discussing how to solve these problems more efficiently using search heuristics. We'll introduce the A-star algorithm.


### Lesson 3: A* Shortest Path Search
### Module 3 Supplementary Reading
### Practice Assignment: Road Network Shortest Path Search


### Lab : Road Network Shortest Path Search
### Grade : Quiz

# References

- [Motion planning - Wikipedia](https://en.wikipedia.org/wiki/Motion_planning)

# Appendices


