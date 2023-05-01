# Course-3-W3-MODULE 3: Feedforward Neural Networks

## Overview

- Deep learning is a core enabling technology for self-driving perception. 
- This module briefly introduces the core concepts employed in modern convolutional neural networks, with an emphasis on methods that have been proven to be effective for tasks such as object detection and semantic segmentation. 
- Basic network architectures, common components and helpful tools for constructing and training networks are described.

## Learning Objectives
- Perform linear regression to estimate the driving road plane from image data
- Build a basic deep neural network for classification
- Define common loss functions for deep convolutional neural networks
- Use backpropagation to compute the gradient of a loss function with respect to network weights for training
- Train a deep convolutional neural network for an autonomous driving classification task

## Neural Networks
### Lesson 1: Feed Forward Neural Networks

**Feedforward Neural Network**

A feedforward neural network defines a `mapping` from an input $x$ to an output $y$ through a function $f$ of $x$ and $\theta$ . 

<img src="./resources/w3/img/l1-fnn0-1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

For example, we use neural networks to produce outputs such as **the location of all cars in a camera image**. 

- The function $f$ takes an input $x$, and uses a set of learned parameters $\theta$ , to interact with $x$ , resulting in the output $y$ . 
- The concept of learned parameters is important here, as we do not start with the correct form of the function $f$ , which maps our inputs to our outputs directly. 
- Instead, we must construct an approximation to the true function using a generic neural network. This means that neural networks can be thought of as `function approximators`. 

Usually we describe a feedforward neural network as a function composition :  

<img src="./resources/w3/img/l1-fnn0-1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- In a sense, each function $f$ of $i$ is a layer on top of the previous function, $f$ of $i- 1$. 
- Usually we have $N$ functions in our compositions where $N$ is a large number, stacking layer upon layer for improved representation. 
- This layering led to the name `deep learning` for the field describing these sequences of functions. 

**Feedforward Neural Network - Example**

Now let us describe this function composition visually. Here you can see a `4-layer feedforward neural network`. 
- This neural network has an `input layer` which describes the data input $x$ to the function approximator.

<img src="./resources/w3/img/l1-fnn1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- Here $x$ can be a **scalar**, a **vector**, a **matrix** or even a `n-dimensional tensor` such as **images**.
- The input gets processed by the first layer of the neural network, the function $f1$ of $x$. 
- We call this layer the first hidden layer. Similarly, the second hidden layer processes the output of the first hidden layer through the function $f2$ of $x$. 
- We can add as many hidden layers as we'd like, but each layer adds additional parameters to be learned, and more computations to be performed at run time. 
- We will discuss how the number of hidden layers affects the performance of our system later on in the course. 
  
- The final layer of the neural network is called the `output layer`.

<img src="./resources/w3/img/l1-fnn2.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- It takes the output of the last hidden layer and transforms it to a desired output $Y$.

*Now, we should have the intuition on why these networks are called feedforward*.

`This is because information flows from the input $x$ through some intermediate steps, all the way to the output $Y$ without any feedback connections`

The terms are used in the same way as we use them in Course 1, when describing control for our self-driving car. 

**FNN**

Now let us go back to the network definition and check out how our visual representation matches our function composition. 

<img src="./resources/w3/img/l1-fnn3.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- In this expression we see $x$ , which is called the input layer. We see the outer most function $f_{N}$ , which is the output layer. And we see each of the functions $f1$ to $f_{N-1}$ in between, which are the hidden layers. 

Now before we delve deeper into these fascinating function approximators, let's look at a few examples of how we can use them for autonomous driving.   

`Remember, this course is on visual perception, so we'll restrict our input x to always be an **image**.` 

**FNN - Classification & Detection Example**

- The most basic perception task is that of `classification`. Here we require the neural network to tell us what is in the image via a label. 
- We can make this task more complicated by trying to estimate a location as well as a label for objects in the scene.This is called `object detection`

<img src="./resources/w3/img/l1-fnn4.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**FNN - Depth Estimation Example**

- Another set of tasks we might be interested in are pixel-wise tasks. As an example we might want to estimate a depth value for every pixel in the image. This will help us determine where objects are. 

<img src="./resources/w3/img/l1-fnn5.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**FNN - Semantic Segmentation Example**

- Or, we might want to determine which class each pixel belongs to. This task is called `semantic segmentation`. 

<img src="./resources/w3/img/l1-fnn6.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- In each case, we can use a neural network to learn the complex mapping between the raw pixel values from the image to the perception outputs we're trying to generate, without having to explicitly model how that mapping works. 

- This flexibility to represent hard-to-model processes is what makes neural networks so popular. 

**Mode Of Action Of Neural Networks**

Now let's take a look at how to learn the parameters needed to create robust perception models.

<img src="./resources/w3/img/l1-fnn7.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- During a process referred to as Neural Network Training, we drive the neural network function $f(x)$ and theta to match a true function $f*(x)$ by modifying the parameters theta that describe the network. 
- The modification of theta is done by providing the network pairs of input x and its corresponding true out output $f*(x)$ . 
- We can then compare the true output to the output produced by the network and optimize the network parameters to reduce the output error. 
- Since only the output of the neural network is specified for each example, the training data does not specify what the network should do with its hidden layers. 
The network itself must decide how to modify these layers to best implement an approximation of $f*(x)$ . As a matter of fact, hidden units are what make neural networks unique when compared to other machine learning models. 

**Hidden Units**

So let us define more clearly the hidden layer structure. 

- The hidden layer is comprised of an affine transformation followed by an element wise non-linear function $g$ . 

<img src="./resources/w3/img/l1-fnn8.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This non-linear function is called the activation function. The input to the nth hidden layer is $h_{n-1}$ , the output from the previous hidden layer. 
- In the case where the layer is the first hidden layer, its input is simply the input image $x$. The affine transformation is comprised of a multiplicative weight matrix W, and an additive bias Matrix $B$ . 
- These weights and biases are the learn parameters theta in the definition of the neural network. 
- Finally, the transformed input is passed through the activation function $g$. Most of the time, $g$ does not contain parameters to be learned by the network. 

**The Rectified Linear Unit - ReLU**

As an example, let us take a look at the rectified linear unit (ReLU), **the default choice** of activation functions in most neural networks nowadays. 

<img src="./resources/w3/img/l1-fnn9.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- **ReLUs** use the maximum between 0 and the output of the affine transformation as their element-wise non-linear function. 
- Since they are very similar to linear units, they're quite easy to optimize. 

**Example: Hidden Layer With RELU Activation Function**

Let us go through an example of a ReLU hidden-layer computation. 
- We are given the output of the previous hidden layer $h_{n-1}$ , the weight matrix $W$ , and the `bias matrix` $b$ . 

<img src="./resources/w3/img/l1-fnn10.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- We first need to evaluate the `affine transformation`. Remember, the weight matrix is transposed in the computation. 
- Let's take a look at the dimensions of each of the matrices in this expression. $h_{n-1}$ is a 2x3 matrix in this case. 
- $W$ is a 2x5 matrix. The final result of our affine transformation is a 5x3 matrix. 

Now, let us pass this matrix through the ReLU non-lineary. 
- We can see that the ReLU prevents any negative outputs from the affine transformation from passing through to the next layer. 

**Other activation functions in research field**

- There are many additional activation functions that can be used as element wise non-linearities in hidden layers for neural networks. 
- In fact, the design of hidden units is another extremely active area of research in the field and does not yet have many guiding theoretical principles. 
- As an example, certain neural network architectures use the sigmoid non-linearity, the hyperbolic tangent non-linearity, and the generalization of ReLU, the maxout non-linearity as their hidden layer activation functions. 

<img src="./resources/w3/img/l1-fnn11.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- If you're interested in learning more about neural network architectures, I strongly encourage you to check out some of the deep learning courses offered on Coursera. They're amazing. 

**Summary**

- In this lesson, you learned the main building blocks of feedfoward neural networks including the hidden layers that comprise the core of the machine learning models we use. 
- You also learned different types of activation functions with ReLUs being the default choice for many practitioners in the field. 

### Supplementary Reading: Feed-Forward Neural Networks

- Goodfellow, I., Bengio, Y., Courville, A., & Bengio, Y. (2016). Deep Learning (Vol. 1). Cambridge: MIT press. Read sections 6.1, 6.3. https://www.deeplearningbook.org/.

### Lesson 2: Output Layers and Loss Functions
### Supplementary Reading: Output Layers and Loss Functions
### Lesson 3: Neural Network Training with Gradient Descent
### Supplementary Reading: Neural Network Training with Gradient Descent

## Neural Networks Continued
### Lesson 4: Data Splits and Neural Network Performance Evaluation
### Supplementary Reading: Data Splits and Neural Network Performance Evaluation
### Lesson 5: Neural Network Regularization
### Supplementary Reading: Neural Network Regularization
### Lesson 6: Convolutional Neural Networks
### Supplementary Reading: Convolutional Neural Networks
### Grade : Feed-Forward Neural Networks

# References
- [Machine Learning Resources - Personal Research Notes](https://github.com/afondiel/research-notes/tree/master/ai/ml-notes)
- [Deep Learning Resources - Personal Research Notes](https://github.com/afondiel/research-notes/tree/master/ai/ml-notes/deep-learning-notes)
- [Neural Network (NN) Architecture - Notes](https://github.com/afondiel/research-notes/blob/master/ai/ml-notes/deep-learning-notes/neural-nets-architecture-notes.md)

# Appendices


