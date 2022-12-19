# Course-1 : INTRODUCTION TO SELF-DRIVING CARS

## Overview 
This course will introduce you to the terminology, design considerations and safety assessment of self-driving cars

  **Course Objectives :**
- Understand commonly used hardware used for self-driving cars
- Identify the main components of the self-driving software stack
- Program vehicle modelling and control  
- Analyze the safety frameworks and current industry practices for vehicle development

`W1 : Welcome to the Self-Driving Cars Specialization!`

## MODULE-0 : Welcome to Self-Driving Specialization

  This module will introduce you to the main concepts and advances in safety and performance metrics in the field of autonomous vehicles over the past two decades. It will highlight the major players and their contributions to the field.
      
  **Module Objectives :**
  - Review the layout of the courses in the Specialization
  - Review the main projects offered in this course
  - Examine the state of the self-driving industry


### Introduction to Self-Driving Cars
---
- **Welcome to the Self-Driving Cars Specialization**


Instructors : `Steve Waslander` and `Jonathan Kelly` both Associate professor in Aerospace studies at [University of Toronto](https://www.utoronto.ca/).

`Self-driving cars` is a sleeping geant which can change everything
  - road safety
  - mobility for everyone
  - reduce the cost of driving 
  - Steve and Jonathan built a self-driving car for research porpose :
    `Autonomoose`
Global overview and requirements for each of four courses which are already described in the introduction section of each course.

Autonomous driving is a constantly and changing field : 
- Self-driving
- Robotics
- AI and ML
---

- **Welcome to the Course**

By the end of this course : 
- Learn about the elements of drving : perception, prediction, decision making
- Understand how to design the software(sw) and hardware(hw) stack to do autonomous driving 
- Understand common safety pratices for autonomous driving
- Learn the basics of vehicle modeling and control, and controllers to do speed regulation, path following(finding)
- State of the art of the model predictive trajectory controllers for precisely executing challenging maneuvers
- Use these concepts to help navigate a self driving car in CARLA(test the limits of the vehicles performances...)
---
- **Course Prerequisites: Knowledge, Hardware & Software**

  - [Prerequisites notes](https://github.com/afondiel/Self-Driving-Cars-Specialization-Coursera/blob/main/Course1-Introduction-to-Self-Driving-Cars/resources/Course-Prerequisites-Knowledge-Hardware-Software.md)

---
- **The Story of Autonomous Vehicles**
  
- More than **94%** of road accidents are caused by some kind of human error
- The Ambition/dream/motivation behind the self-driving cars technology is to minimize or reduce human errors and driving deaths `out of the picture` through the **automation**. 
- Other advantages : 
  - replace the driving tasks/controls and focus on the eat, relax. Make the morning more productive : send emails for instance.
  
- `1925` : Francis Udina(A Mechanic Engineer) demostrated a remote control car `The American Wonder` drove in the street of Manhattan with an empty drivers seat
- `1956` : GM promoted a campaign of self-driving car to be arrived by 1976
- `1980s` in Europe : pionniers have been working on self-driving for 40 years. Early vehicles were partially autonomous and operating in a low speed
- `1986`: Ernst Dickens(Germany) : created a robotic van that could drive fully autonomously without traffic
- `1987` : Dickens van drove it speeds up to 60km/h
- `1990s` : Dickens's team worked on the Eurka Prometheus project, and develop an autonomous Daimler Benz using psychotic computer vision that focusing on points of interest in the environment. 
  - They used over 50 transporters
  - The latest microprocessors of the day
  - same probabilistic approach used in robotics and some sensors 
  - React road situation in the real time
  - Diamond Bends drove 1600Km in traffic from Munich to Copenhagen : 
    - mean distance : btw human intervension of 9km
- `1986` In US : Carnegie University Navlab team created the **Navlab1**, their first autonomous vehicle
  - Managed to drive 30km/h on the road using mutliple sun 
- `1990s` : Navlab2 was born, a modified Humvee which could perform autonomously both off than on-road. With speed of 110 km/h on the road
- `1996` :  Navlab2 drove 4800 km route across the America with no hands, with **98.2%** to autonomous driving.
- UC Berkerley developped a path project of autonomous platoons of vehicles operating on dedicated HOV lanes on the I5
  - `1992`: four of their vehicles drove a convoy at highway speed relying on magnetic markers for precise relative positioning saving on fuels costs and reduces wing drag ? 
  - `1997`: the project continues with alot of sucessful tests with use of new technologies like : RADAR station and V2V communication
    - Leading to advances such as : Adaptive cruise control and emergency braking systems
- `2002` : DARPA (The Defene Advanced Research Projects Agency) created the DARPA challenge for self-driving cars for universities
- `2004`: The event was a competition to build an autonomous vehicle capable to navigate 142miles(228,527Km) through the Mojave Desert(Stanford win the next year followed by Carnegie Mellon)
- `2007`: DARPA Urban Challenge took place on busy roads. The vehicles were much more equiped with GPS and other adavanced sensors. 
  - This was a jumping point in the tech industry that a new market was openning and race was on 
  - google reacted and hired the tech lead from both Carnigie Mellon and Stanford (Chris Thomposon and Mike Monte-Carlo) to push their design in public roads
- `2010`: Google cars had logged over thousand miles in california. Thus, they believed they could cut the number of road death by half (in US)
- `2018` :  Google logged over 10 million miles  
- Around the same time `Viz Lab` started an autonomous testing campaign with tow orange van and competed the international autonomous challenge driving th entire road from the University of Parma Italy to Shanghai China about 15000km w/ almost no driver intervention 

- `2019` : Volvo launched the Road Train concept which one vehicle could control several other vehicles behind it, by reducing road congestion and improving driver comfort
- `2012`: The Nevada Department of Motor Vehicles issued Google the first ever autonomous vehicle testing license (Google now test their self-driving cars in public roads) and California was next
- `2013`: Mercedes Benz demostrated their self-driving capabilities after 125 year since their first self-driving Betha Bens covering the entir 106 km autonomously.
- CES in Nevada (Las Vegas) become the annual show case for the greatest self-driving tech and automobile industries
- `2014` : Google demoed, firefly 'concept' car
  - Specs : 40km/h speeds, no steering wheels and pedals
- `2015` : Tesla introduced the `autopilot`
- `2016` : Autopilot could self park and be summoned by a button
- The research carried on, Autonomous taxi startups wecame popular like zoox and nuTonomy(first operational in Singapure) leading the way.
  
- Even though we have logged million miles of datas there is still alot of challenges and setbacks:
- `2016` :  Tesla Model S first fatal accident in Florida(due to a camera and radar sensor failure)
- `2018` : Uber self-driving Taxi fatal accident in Arizona. As consequence of that Uber suspended his self-driving cars testing for a while
- We should see more and more outcome services in year 2020s like : Robotaxi and driveless delivery.
-  The cost of self-driving car still high but prices will fall quicly as economies of scale takeover.
- There still so much to be done and as the Industry will to continue to grow, Outstanding Engineers will be needed to **produce innovative solution for driving**.

---
- **How to Use Discussion Forums**
  - OK

---
- **Get to Know Your Classmates**
  - OK

---
- **Glossary of Terms**
  - [here](./resources/glossary.md) ! 
---
- **How to Use Supplementary Readings in This Course**
  - OK 
---

### Meeting the Self-Driving Car Experts

---
- **Meet the Instructor, Steven Waslander**
  - OK
---

- **Meet the Instructor, Jonathan Kelly**
  - OK
---
- **Meet Diana, Firmware Engineer**
  - OK
---
- **Meet Winston, Software Engineer**
  - OK
---
- **Meet Andy, Autonomous Systems Architect**
  - OK
---
- **Meet Paul Newman, Founder, Oxbotica & Professor at University of Oxford**
  - OK 
---
- **Why Should You Take This Course?**
  - OK
---

- Quiz
- Assignment


## MODULE-1 : The requirements for Autonomy 

Self-driving cars present an extremely rich and inter-disciplinary problem. This module introduces the language and structure of the problem definition, defining the most salient elements of the driving task and the driving environment.

> Learning Objectives : 
> - Identify perception, prediction and planning requirements for driving
> - Define the environmental elements that influence driving
> - Breakdown the task of driving into elemental decisions and actions
> - Assess the effects of driving conditions on the driving task
---
### Driving Taxonomy, Perception and Driving Decisions

- Lesson 1: Taxonomy of Driving
- Lesson 1 Supplementary Reading: Taxonomy of Driving
- Lesson 1: Practice Quiz
- Practice Quiz•5 questions
- Lesson 2: Requirements for Perception
- Lesson 2 Supplementary Reading: Requirements for Perception
- Lesson 2: Practice Quiz
- Practice Quiz•5 questions
- Lesson 3: Driving Decisions and Actions
- Lesson 3 Supplementary Reading: Driving Decisions and Actions

### Learn from Industry Expert 

- Advice for Breaking into the Self-Driving Cars Industry

### Weekly Assignment

Module 1: Graded Quiz
Quiz
Grade


