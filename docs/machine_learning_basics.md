# Machine Learning Basics

## Types of learning

Supervised learning uses labeled examples and covers classification and regression. Unsupervised learning has no labels and finds structure, for example clustering with k-means. Reinforcement learning trains an agent through rewards.

## Data splits

Data are split into a training set, a validation set and a test set. A common split is 70 percent, 15 percent and 15 percent, or 80 percent training and 20 percent test. The test set is used only once, at the end, to estimate performance on new data.

## Overfitting and underfitting

Overfitting means the model memorizes the training data and performs badly on new data: training error is low, validation error is high. Underfitting means the model is too simple and has high error on both sets. Regularization, more data and early stopping reduce overfitting.

## Cross-validation

In k-fold cross-validation the data are split into k parts. The model is trained k times, each time using a different part for validation. The usual value is k = 5 or k = 10.

## Classification metrics

Accuracy is the share of correct predictions. Precision is the share of predicted positives that are truly positive. Recall is the share of true positives that are found. The F1 score is the harmonic mean of precision and recall. On imbalanced data, accuracy can be misleading.
