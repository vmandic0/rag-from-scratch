# Neural Networks

## Structure

A neural network consists of layers of neurons. Each neuron computes a weighted sum of its inputs, adds a bias, and passes the result through an activation function. A network has an input layer, one or more hidden layers and an output layer.

## Activation functions

ReLU returns the input if it is positive and zero otherwise; it is the default choice for hidden layers. Sigmoid squeezes values into the range 0 to 1 and is used for binary output. Softmax turns a vector of scores into probabilities that sum to 1 and is used for multi-class output.

## Training

Training minimizes a loss function. Backpropagation computes the gradient of the loss with respect to every weight, and gradient descent moves the weights in the opposite direction of the gradient. The learning rate controls the size of each step. A learning rate that is too large makes training diverge; one that is too small makes it very slow.

## Epochs and batches

One epoch is one pass through the whole training set. The data are processed in mini-batches, for example 32 examples at a time. After every batch the weights are updated.

## Dropout

Dropout randomly switches off a fraction of neurons during training, for example 20 percent. It reduces overfitting because the network cannot rely on a single neuron.
