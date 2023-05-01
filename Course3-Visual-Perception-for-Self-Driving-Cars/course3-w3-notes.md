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

**Machine Leaning Algorithm Design Process**

Generally, supervised machine learning models including neural networks have two modes of operation : 
- **inference** 
- **training**. 

Recall are basic neural network formulation. 
- Given a set of parameters data, the input $x$ is passed through the model $f(x:theta)$ to get an output $y$. 

<img src="./resources/w3/img/l2-ml-design0-0.png" width="300" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- This mode of operation is called `inference`, and is usually the one we usually `deploy` the machine learning algorithms in the real world. 
- The network and its parameters are fixed and we use it to extract perception information from new input data. 
- However, we still need to define how to obtain the parameter set data. 

Here we need a second mode of operation involving optimization over the network parameters. 

This mode is called `training` and has the sole purpose of generating a satisfactory parameter set for the task at hand. 

<img src="./resources/w3/img/l2-ml-design0-1.png" width="400" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- We start with the same workflow as inference. However, during training we have training data. As such we know what $f^{*}(x)$ is, the expected output of the model.
- For self-driving, this training data often takes the form of human annotated images which take a long time to produce. 
- We compare our inference to a predicted output $y$ , to the true output $f^{*}(x)$ , through a loss or a cost function. 
- The loss function takes as an input the predicted output y from the network, and the true output $f^{*}(x)$ , and provides a measure of the difference between the two. 
- We usually try to minimize this measure by modifying the parameters data so that the output $y$ from the network is as similar as possible to the $f^{*}(x)$. 
- We do this modification to data via an optimization procedure. 
- This optimization procedure takes in the output of the loss function and provides a new set of parameters data that provide a lower value for that loss function. 


**Artificial Neural Networks**

By extending the design process to neural networks. 

<img src="./resources/w3/img/l2-ml-design1.png" width="480" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- We discussed in the last lesson a feed-forward neural network which takes an input $x$ , passes it through a sequence of hidden layers, then passes the output of the hidden layers through an output layer. 
- This is the end of the inference stage of the neural network. 
- For `training`, we pass the predicted output through the loss function, then use an optimization procedure to produce a new set of parameters data that provide a lower value for the loss function. 

```The major difference between the design of traditional machine learning algorithms in the design of artificial neural networks, is that the neural network only interacts with the loss function via the output layer```. 

- Therefore, it is quite reasonable that the output layer and the loss function are designed together depending on the task at hand. 

**Tasks: Classification and Regression**

Let's dig deeper into the major perception tasks we usually encounter in autonomous driving. 

- The first important task that we use for autonomous driving perception is `classification`. 

<img src="./resources/w3/img/l2-ml-class0.png" width="520" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- **Classification** can be described as taking an input x and mapping it to one of k classes or categories. 
- Examples include : 
  - **image classification**, where we just want to map an image to a particular category, to say whether or not it contains cats or dogs for example
  - **semantic segmentation**, where we want to map every pixel in the image to a category.
 
<img src="./resources/w3/img/l2-ml-class-img-seg0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The second task that we usually use for autonomous driving perception is a `regression`. 

- In regression, we want to map inputs to a set of real numbers. 
- Examples of regression include, 
  - depth estimation, where we want to estimate a real depth value for every pixel in an image. 

<img src="./resources/w3/img/l2-ml-reg0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- We can also mix the two tasks together. 
  - For example : 
    - **object detection**is usually comprised of a regression task where we estimate the bounding box that contains an object 
    - **classification** task where we identify which type of object is in the bounding box.

<img src="./resources/w3/img/l2-ml-class-reg0.png" width="520" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

**Classification: Softmax Output  Layers**

We will now describe the output layer loss function pairs associated with each of these basic perception tasks. 

Let's start with the classification task first.Usually, for a $k$ class classification tasks, we use the `softmax output layer`. 

<img src="./resources/w3/img/l2-class-softmax0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- **Softmax output layers** are capable of representing a probability distribution over $k$ classes. 
- The softmax output layer takes as input $h$, the output of the last hidden layer of the neural network. 

- It then passes it through an affine transformation resulting in a transformed output vector $z$. 
- Next, the vector $z$ is transformed into a discrete probability distribution using the softmax element-wise function. 
- For each element $z_{i}$, this function computes the ratio of the exponential of element $z_{i}$ over the sum of the exponentials of all of the elements of $z$.
- The result is a value between zero and one and the sum of all of these elements is one, making it a proper probability distribution. 

Let's take a look at a numerical example to better explain the softmax output layer. 

In this example, we'd like to classify images containing a cat, a dog or a fox. 

<img src="./resources/w3/img/l2-class-softmax1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- First we define the first element of our output vector to correspond to the probability that the image is a cat according to our network. 
- The ordering of classes is arbitrary and has no impact on network performance. 
- Taking the output of the affine transformation, we compute the probability by dividing the exponential of each elements of the output by the sum of the exponentials of all of the elements. 
- Given values of 13 minus seven and 11 as the outputs of the linear transformation layer, we achieve a probability of 88% that this image is a cat, 11.9% that this image is a fox and a very low probability that this image is a dog. 

**Classification: Cross-Entropy Loss Function**

Now, let's see how to design a loss function that uses the output of the softmax output layer to show us how accurate our estimate is. 

<img src="./resources/w3/img/l2-class-entropy0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The standard loss function to be used with the softmax output layer is the `Cross-Entropy Loss`, which is formed by taking the negative log of the softmax function. 
- The Cross-Entropy Loss has two terms to control how close the output of the network is to the true probability. 
- $Z_{i}$ is the output of the hidden layer corresponding to the true class before being passed through the softmax function.

- This is usually called the class logit which comes from the field of logistic regression.
- When minimizing this loss function, the negative of the class logit $z_{i}$ encourages the network to output a large value for the probability of the correct class.   
- The second term on the other hand, encourages the output of the affine transformation to be small. 

<img src="./resources/w3/img/l2-class-entropy1.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The two terms together encourages the network to minimize the difference between the predicted class probabilities and the true class probability. 
- To understand this loss better. Let's take a look at a numerical example on how the Cross-Entropy Loss is computed from the output of a classification neural network. 

**Classification: Softmax Output Layers**

Revisiting our previous example, we first need to choose what our $z_{i}$ is. 

<img src="./resources/w3/img/l2-class-softmax2.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- $Z_{i}$ is the linear transformation output corresponding to the true class of inputs. 
- In this case, $z_{i}$ is the element of the output of the linear transformation corresponding to the cat class. 
- Once we determine $z_{i}$ , we use the Cross-Entropy to compute the final loss value. 
- In this case, the network correctly predicts that the input is a cat and sees a loss function value of **0.12**. 
- Let us now do the computation again but with an erroneous network output. The input to the network is still a cat image. 
- The network still assigns the value of **13** to the cat entry of the output of the linear transformation. But this time the fox entry will get a value of **14**. 
- Computing the Cross-Entropy Loss, we find that it evaluates to **1.31** more than ten times the value of the previous slide. 
- Note how the loss function heavily penalizes erroneous predictions even when the difference in output is only one. 

```This difference accelerates the learning process and rapidly steers network outputs to the true values during training.```

**Regression: Linear Output Layers**

Let's now go through the most common output layer for the regression task. 

The linear output layer is mostly used for regression tasks to model statistics of common probability distributions. 

<img src="./resources/w3/img/l2-ml-reg-output0.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- The linear output layer is simply comprised of a single affine transformation without any non-linearity. 
- The statistics to be modeled with the linear output layer depends on the loss function we choose to go with it. 

For example, to model the mean of a probability distribution, we use `the mean squared error` as our loss function. 
- The linear and softmax output units described above are the most common output layers used in neural networks today and can be coupled with a variety of tasks specific loss functions to perform a variety of useful perception tasks for autonomous driving. 

- Many other output layers and loss functions exist and this remains an active area of research in deep learning. 

**Summary**

<img src="./resources/w3/img/l2-ml-summary.png" width="600" style="border:0px solid #FFFFFF; padding:1px; margin:1px">

- In this lesson, you learned that to build a machine learning model you need to define a **network model**, a **loss function** and an **optimization procedure** to learn the network parameters. 
- You also learn what loss function to choose based on the task that needs to be done by the neural network model. 

### Supplementary Reading: Output Layers and Loss Functions

- Goodfellow, I., Bengio, Y., Courville, A., & Bengio, Y. (2016). Deep Learning (Vol. 1). Cambridge: MIT press. Read sections 6.2, 6.4. https://www.deeplearningbook.org/


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


