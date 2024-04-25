def single_layer_perceptron(condition):
    if condition == "SXOR":
        print("""
#XOR
# Make a prediction with weights
def predict(row, weights):
    activation = weights[0]
    for i in range(len(row)-1):
        activation += weights[i + 1] * row[i]
    return 1.0 if activation >= 0.0 else 0.0

# Estimate Perceptron weights using stochastic gradient descent
def train_weights(train, l_rate, n_epoch):
    weights = [0.0 for i in range(len(train[0]))]
    for epoch in range(n_epoch):
        sum_error = 0.0
        for row in train:
            prediction = predict(row, weights)
            error = row[-1] - prediction
            sum_error += error**2
            weights[0] = weights[0] + l_rate * error
            for i in range(len(row)-1):
                weights[i + 1] = weights[i + 1] + l_rate * error * row[i]
        print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))
    return weights

# Calculate weights
dataset=[[0 ,0 ,0],
[0 ,1, 1],
[1 ,0, 1],
[1 ,1, 0]
]

l_rate = 0.1
n_epoch = 5
weights = train_weights(dataset, l_rate, n_epoch)
print(weights)

for row in dataset:
    prediction = predict(row, weights)
    print("Expected=%d, Predicted=%d" % (row[-1], prediction))
""")
    elif condition == "SAND":
        print("""
#AND
# Make a prediction with weights
def predict(row, weights):
    activation = weights[0]
    for i in range(len(row)-1):
        activation += weights[i + 1] * row[i]
    return 1.0 if activation >= 0.0 else 0.0

# Estimate Perceptron weights using stochastic gradient descent
def train_weights(train, l_rate, n_epoch):
    weights = [0.0 for i in range(len(train[0]))]
    for epoch in range(n_epoch):
        sum_error = 0.0
        for row in train:
            prediction = predict(row, weights)
            error = row[-1] - prediction
            sum_error += error**2
            weights[0] = weights[0] + l_rate * error
            for i in range(len(row)-1):
                weights[i + 1] = weights[i + 1] + l_rate * error * row[i]
        print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))
    return weights

# Calculate weights
dataset=[[0 ,0 ,0],
[0 ,1, 0],
[1 ,0, 0],
[1 ,1, 1]
]

l_rate = 0.1
n_epoch = 5
weights = train_weights(dataset, l_rate, n_epoch)
print(weights)

for row in dataset:
    prediction = predict(row, weights)
    print("Expected=%d, Predicted=%d" % (row[-1], prediction))
""")
    elif condition == "SOR":
        print("""
#OR
# Make a prediction with weights
def predict(row, weights):
    activation = weights[0]
    for i in range(len(row)-1):
        activation += weights[i + 1] * row[i]
    return 1.0 if activation >= 0.0 else 0.0

# Estimate Perceptron weights using stochastic gradient descent
def train_weights(train, l_rate, n_epoch):
    weights = [0.0 for i in range(len(train[0]))]
    for epoch in range(n_epoch):
        sum_error = 0.0
        for row in train:
            prediction = predict(row, weights)
            error = row[-1] - prediction
            sum_error += error**2
            weights[0] = weights[0] + l_rate * error
            for i in range(len(row)-1):
                weights[i + 1] = weights[i + 1] + l_rate * error * row[i]
        print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))
    return weights

# Calculate weights
dataset=[[0 ,0 ,0],
[0 ,1, 1],
[1 ,0, 1],
[1 ,1, 1]
]

l_rate = 0.1
n_epoch = 5
weights = train_weights(dataset, l_rate, n_epoch)
print(weights)

for row in dataset:
    prediction = predict(row, weights)
    print("Expected=%d, Predicted=%d" % (row[-1], prediction))
""")
    elif condition == "MXOR":
        print("""
from math import exp
from random import seed
import numpy as np
from random import random

# Initialize a network
def initialize_network(n_inputs, n_hidden, n_outputs):
    network = list()
    hidden_layer = [{'weights':[random() for i in range(n_inputs + 1)]} for i in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights':[random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
    network.append(output_layer)
    return network

# Calculate neuron activation for an input
def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights)-1):
        activation += weights[i] * inputs[i]
    return activation

# Transfer neuron activation Sigmoid
def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))
              
# Transfer neuron activation relu
def relu(activation):
    return max(0, activation)
              
# Transfer neuron activation tanh
def tanh(activation):
    return math.tanh(activation)
              
# Transfer neuron activation softmax
def softmax(activation):
    exp_values = np.exp(activation - np.max(activation, axis=-1, keepdims=True))
    return exp_values / np.sum(exp_values, axis=-1, keepdims=True)

# Forward propagate input to a network output
def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

# Calculate the derivative of an neuron output
def transfer_derivative(output):
    return output * (1.0 - output)

# Backpropagate error and store in neurons
def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network)-1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(neuron['output'] - expected[j])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

# Update network weights with error
def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j]
            neuron['weights'][-1] -= l_rate * neuron['delta']

# Train a network for a fixed number of epochs
def train_network(network, train, l_rate, n_epoch, n_outputs):
    for epoch in range(n_epoch):
        sum_error = 0
        for row in train:
            outputs = forward_propagate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
            backward_propagate_error(network, expected)
            update_weights(network, row, l_rate)
        print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))

# Test training backprop algorithm
seed(1)
dataset=[[0 ,0 ,0],
[0 ,1, 1],
[1 ,0, 1],
[1 ,1, 0]
]
n_inputs = len(dataset[0]) - 1
n_outputs = len(set([row[-1] for row in dataset]))
network = initialize_network(n_inputs, 2, n_outputs)
train_network(network, dataset, 0.7, 2000, n_outputs)
for layer in network:
    print(layer)

# Make a prediction with a network
def predict(network, row):
    outputs = forward_propagate(network, row)
    return outputs.index(max(outputs))

# Test making predictions with the network
# Calculate weights
dataset=[[0 ,0 ,0],
[0 ,1, 1],
[1 ,0, 1],
[1 ,1, 0]
]
network = [[{'weights': [-7.11633529326649, -7.1581068047308865, 2.8371570815867537]}, {'weights': [-4.678619410470838, -4.675030707099385, 6.896387527026277]}],
[{'weights': [7.09659482524775, -6.874292052797358, 3.1886537350444337]}, {'weights': [-7.1851092830671766, 6.9544476386375385, -3.224973160770339]}]]
for row in dataset:
    prediction = predict(network, row)
    print('Expected=%d, Got=%d' % (row[-1], prediction))""")
    
    elif condition == "MCSV":
        print("# Backprop on the Seeds Dataset")
        print("""
from random import seed
from random import randrange
from random import random
import numpy as np
from csv import reader
from math import exp

# Load a CSV file
def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset

# Convert string column to float
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

# Convert string column to integer
def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup

# Find the min and max values for each column
def dataset_minmax(dataset):
    minmax = list()
    stats = [[min(column), max(column)] for column in zip(*dataset)]
    return stats

# Rescale dataset columns to the range 0-1
def normalize_dataset(dataset, minmax):
    for row in dataset:
        for i in range(len(row)-1):
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])

# Split a dataset into k folds
def cross_validation_split(dataset, n_folds):
    dataset_split = list()
    dataset_copy = list(dataset)
    fold_size = int(len(dataset) / n_folds)
    for i in range(n_folds):
        fold = list()
        while len(fold) < fold_size:
            index = randrange(len(dataset_copy))
            fold.append(dataset_copy.pop(index))
        dataset_split.append(fold)
    return dataset_split

# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0

# Evaluate an algorithm using a cross validation split
def evaluate_algorithm(dataset, algorithm, n_folds, *args):
    folds = cross_validation_split(dataset, n_folds)
    scores = list()
    for fold in folds:
        train_set = list(folds)
        train_set.remove(fold)
        train_set = sum(train_set, [])
        test_set = list()
        for row in fold:
            row_copy = list(row)
            test_set.append(row_copy)
            row_copy[-1] = None
        predicted = algorithm(train_set, test_set, *args)
        actual = [row[-1] for row in fold]
        accuracy = accuracy_metric(actual, predicted)
        scores.append(accuracy)
    return scores

# Calculate neuron activation for an input
def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights)-1):
        activation += weights[i] * inputs[i]
    return activation

# Transfer neuron activation sigmoid
def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))

# Transfer neuron activation relu
def relu(activation):
    return max(0, activation)
              
# Transfer neuron activation tanh
def tanh(activation):
    return math.tanh(activation)
              
# Transfer neuron activation softmax
def softmax(activation):
    exp_values = np.exp(activation - np.max(activation, axis=-1, keepdims=True))
    return exp_values / np.sum(exp_values, axis=-1, keepdims=True)

# Forward propagate input to a network output
def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

# Calculate the derivative of an neuron output
def transfer_derivative(output):
    return output * (1.0 - output)

# Backpropagate error and store in neurons
def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network)-1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(neuron['output'] - expected[j])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

# Update network weights with error
def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j]
            neuron['weights'][-1] -= l_rate * neuron['delta']

# Train a network for a fixed number of epochs
def train_network(network, train, l_rate, n_epoch, n_outputs):
    for epoch in range(n_epoch):
        for row in train:
            outputs = forward_propagate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            backward_propagate_error(network, expected)
            update_weights(network, row, l_rate)

# Initialize a network
def initialize_network(n_inputs, n_hidden, n_outputs):
    network = list()
    hidden_layer = [{'weights':[random() for i in range(n_inputs + 1)]} for i in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights':[random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
    network.append(output_layer)
    return network

# Make a prediction with a network
def predict(network, row):
    outputs = forward_propagate(network, row)
    return outputs.index(max(outputs))

# Backpropagation Algorithm With Stochastic Gradient Descent
def back_propagation(train, test, l_rate, n_epoch, n_hidden):
    n_inputs = len(train[0]) - 1
    n_outputs = len(set([row[-1] for row in train]))
    network = initialize_network(n_inputs, n_hidden, n_outputs)
    train_network(network, train, l_rate, n_epoch, n_outputs)
    predictions = list()
    for row in test:
        prediction = predict(network, row)
        predictions.append(prediction)
    return(predictions)

# Test Backprop on Seeds dataset
seed(1)
# load and prepare data
filename = '/content/wheat-seeds.csv'
dataset = load_csv(filename)
for i in range(len(dataset[0])-1):
    str_column_to_float(dataset, i)
# convert class column to integers
str_column_to_int(dataset, len(dataset[0])-1)
# normalize input variables
minmax = dataset_minmax(dataset)
normalize_dataset(dataset, minmax)
# evaluate algorithm
n_folds = 6
l_rate = 0.01
n_epoch = 10000
n_hidden = 5
scores = evaluate_algorithm(dataset, back_propagation, n_folds, l_rate, n_epoch, n_hidden)
print('Scores: %s' % scores)
print('Mean Accuracy: %.3f%%' % (sum(scores)/float(len(scores))))""")
    
    elif condition == "FUZZY":
        print("""
# if left, x = x - L / C - L
# if right, x = R - x / R - C
# otherwise zero

x = float(input("Enter the value of Temperature: "))
y = float(input("Enter the value of Pressure: "))


print("FOR RULE ONE")
# For Temperature ++++++++++++++++++++++++++++++++++++++++++++
print("Temperature is Below Average")
R=45
L=15
C=(R+L)/2
if x > C and x <= R:
    z1 = (R - x) /( R - C)
elif x <= C and x >= L:
    z1 = (x - L) / (C - L)
else:
    z1 = 0
print("Z value for temperature:", z1)

# For Pressure ++++++++++++++++++++++++++++++++++++++++++++
print("Pressure is Below Average")
R=2.75
L=1.25
C=(R+L)/2
if y > C and y <= R:
    z = (R - y) /( R - C)
elif y <= C and y >= L:
    z = (y - L) / (C - L)
else:
    z = 0
print("Z value for temperature:", z)

##########################################################################
##########################################################################

print("FOR RULE TWO")
# For Temperature ++++++++++++++++++++++++++++++++++++++++++++
print("Temperature is Low")
R=25
C=10
D=C-L
L=C+D
if x > C and x <= R:
    zp = (R - x) /( R - C)
elif x <= C and x >= L:
    zp = (x - L) / (C - L)
else:
    zp = 0
print("Z value for temperature:", zp)

# For Pressure ++++++++++++++++++++++++++++++++++++++++++++
print("Pressure is Low")
R=1.75
C=1
D=C-L
L=C+D
if y > C and y <= R:
    zp1 = (R - y) /( R - C)
elif y <= C and y >= L:
    zp1 = (y - L) / (C - L)
else:
    zp1 = 0
print("Z value for temperature:", zp1)

min_membership_of_r1 = min(z1,z)
rounded_min_membership_of_r1 = "{:.2f}".format(min_membership_of_r1)
print("Minimum membership value for Rule 2:", rounded_min_membership_of_r1)

min_membership_of_r2 = min(zp, zp1)
rounded_min_membership_of_r2 = "{:.2f}".format(min_membership_of_r2)
print("Minimum membership value for Rule 1:", rounded_min_membership_of_r2)


#For HP
print("For Rule on 1")
LHPr1=3.25
RHPr1=4.75
CHPr1=(LHPr1+RHPr1)/2
arear1=(1/2)*(RHPr1-LHPr1)*(1)
print(arear1)

print("For Rule on 2")
LHPr2=4.25
CHPr2=5
dhp=CHPr2-LHPr2
RHPr2=CHPr2+dhp
arear2=(1/2)*(RHPr2-LHPr2)*(1)
print(arear2)

CenterHP= ((min_membership_of_r1)*(arear1)*(CHPr1) + (min_membership_of_r2)*(arear2)*(CHPr2))/ ((min_membership_of_r1)*(arear1)+(min_membership_of_r2)*(arear2))
print("Crisp value of Heating Power:", CenterHP)

#For VO
print("For Rule on 1")
LVOr1=1.25
RVOr1=2.75
CVOr1=(LVOr1+RVOr1)/2
arearv1=(1/2)*(RVOr1-LVOr1)*(1)
print(arearv1)

print("For Rule on 2")
RVOr2=1.75
CVOr2=1
dvo=CVOr2-RVOr2
LVOr2=CVOr2+dvo
arearv2=(1/2)*(RVOr2-LVOr2)*(1)
print(arearv2)

CenterVO= ((min_membership_of_r1)*(arearv1)*(CVOr1) + (min_membership_of_r2)*(arearv2)*(CVOr2))/ ((min_membership_of_r1)*(arearv2)+(min_membership_of_r2)*(arear2))
print("Crisp value of valve opening: ",CenterVO)""")
        
    elif condition == "CAM":
        print("""
import numpy as np

mem_vectors = np.array([
    [1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 0]
])

q = mem_vectors.shape[0] # number of vectors
n = mem_vectors.shape[1] # dimension of the vectors

bip_mem_vectors = 2 * mem_vectors - 1 # Convert to bipolar

# Initialize and compute the weight matrix
zd_wt_mat = np.zeros((n, n))
for i in range(q):
    zd_wt_mat += np.outer(bip_mem_vectors[i], bip_mem_vectors[i])

zd_wt_mat -= q * np.eye(n) # Zero diagonal

probe = input('Enter the probe vector: ')
probe = np.array(list(map(int, probe.split())))

signal_vector = 2 * probe - 1
flag = 0 # Initialize flag

while flag != n:
    permindex = np.random.permutation(n) # Randomize order
    old_signal_vector = signal_vector.copy()

    for j in range(n): # update all neurons once per epoch
        act_vec = signal_vector.dot(zd_wt_mat)
        if act_vec[permindex[j]] > 0:
            signal_vector[permindex[j]] = 1
        elif act_vec[permindex[j]] < 0:
            signal_vector[permindex[j]] = -1

    flag = np.dot(signal_vector, old_signal_vector)

print('The recalled vector is:', 0.5 * (signal_vector + 1))""")
        
    elif condition == "BAM":
        print("""
import numpy as np

# Parameters
n = 5  # Dimension of Fx
p = 4  # Dimension of Fy
q = 2  # Number of associations

# Memory vectors initialization
mem_vectors_x = np.array([[0, 1, 0, 1, 0], [1, 1, 0, 0, 0]])
mem_vectors_y = np.array([[1, 0, 0, 1], [0, 1, 0, 1]])

# Conversion to bipolar form
bip_mem_vectors_x = 2 * mem_vectors_x - 1
bip_mem_vectors_y = 2 * mem_vectors_y - 1

# Initialize weight matrix
wt_matrix = np.zeros((n, p))

# Compute weight matrix
for i in range(q):
    wt_matrix += np.outer(bip_mem_vectors_x[i], bip_mem_vectors_y[i])

# Set up probe vector for input and randomize initial signal vector for output
probe = np.array([0, 1, 0, 1, 1])
signal_x = 2 * probe - 1
signal_y = np.random.choice([-1, 1], p)

# Iteration loop
pattern_x = [signal_x]
pattern_y = [signal_y]
k = 1
flag = 0

while flag != 1:
    act_y = np.dot(signal_x, wt_matrix)
    signal_y = np.sign(act_y)

    if k > 1:
        compare_y = np.array_equal(signal_y, pattern_y[k - 1])
    else:
        compare_y = False

    pattern_y.append(signal_y)

    act_x = np.dot(signal_y, wt_matrix.T)
    signal_x = np.sign(act_x)
    pattern_x.append(signal_x)

    k += 1

    if k > 1:
        compare_x = np.array_equal(signal_x, pattern_x[k - 1])
    else:
        compare_x = False

    flag = compare_x * compare_y

# Display updated traces
print("Pattern traces for Fx:")
for pattern in pattern_x:
    print(pattern)

print("Pattern traces for Fy:")
for pattern in pattern_y:
    print(pattern)""")
        
    elif condition == "RXOR":
        print("""
import random
import math

# Define the activation function (sigmoid)
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# Define the derivative of the activation function (sigmoid)
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Define the gaussian_rbf function
def gaussian_rbf(x, center, sigma):
    return math.exp(-sum((a - b) ** 2 for a, b in zip(x, center)) / (2 * sigma**2))

# Define the RBF transformation
def rbf_transform(X, rbf_centers, rbf_width):
    return [[gaussian_rbf(x, center, rbf_width) for center in rbf_centers] for x in X]

# Define the perceptron training function
def train_perceptron(X, y, learning_rate, epochs):
    input_size = len(X[0])
    weights = [random.uniform(-1, 1) for _ in range(input_size)]
    bias = random.uniform(-1, 1)

    for _ in range(epochs):
        for i in range(len(X)):
            prediction = sum(X[i][j] * weights[j] for j in range(input_size)) + bias
            prediction = sigmoid(prediction)
            error = y[i] - prediction
            for j in range(input_size):
                weights[j] += learning_rate * error * X[i][j]
            bias += learning_rate * error

    return weights, bias

# Define the perceptron prediction function
def predict_perceptron(X, weights, bias):
    predictions = []
    for i in range(len(X)):
        prediction = sum(X[i][j] * weights[j] for j in range(len(X[i]))) + bias
        prediction = sigmoid(prediction)
        predictions.append(prediction)
    return predictions

# Define the XOR truth table
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [0, 1, 1, 0]

# Define the RBF centers and width for transformation
rbf_centers = [[0, 0], [1, 1]]
rbf_width = 1.0

# Transform the input using RBF
X_transformed = rbf_transform(X, rbf_centers, rbf_width)

# Train the perceptron
learning_rate = 0.1
epochs = 10000
weights, bias = train_perceptron(X_transformed, y, learning_rate, epochs)

# Make predictions
predictions = predict_perceptron(X_transformed, weights, bias)

# Print expected and predicted outputs
print("Expected  Predicted")
for expected, predicted in zip(y, predictions):
    print(f"   {expected}         {round(predicted)}")

# Calculate accuracy
accuracy = sum(int(round(pred)) == true for pred, true in zip(predictions, y)) / len(y) * 100
print(f"Accuracy: {accuracy:.2f}%")""")
    
    elif condition == "RBF":
        print("""
import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder


# Read data from CSV
data = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/heart.csv")

# Preprocess the data: Encoding categorical variables using OneHotEncoder
categorical_columns = ['column1', 'column2', ...]  # Replace column names with actual categorical columns
encoder = OneHotEncoder()
encoded_categorical_data = encoder.fit_transform(data[categorical_columns])
encoded_categorical_df = pd.DataFrame(encoded_categorical_data.toarray(), columns=encoder.get_feature_names_out(categorical_columns))

# Concatenate the encoded categorical data with numerical features
processed_data = pd.concat([data.drop(columns=categorical_columns), encoded_categorical_df], axis=1)

# Split data into input features (X) and target variable (Y)
X = processed_data.drop("output", axis=1)
Y = processed_data["output"]

#Without encoding
X = data.drop("output", axis=1)
Y = data["output"]

# Standardize input features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform K-Means clustering
K_cent = 8
km = KMeans(n_clusters=K_cent, max_iter=100)
km.fit(X_scaled)
cent = km.cluster_centers_

# Calculate sigma
max_dist = 0
for i in range(K_cent):
    for j in range(K_cent):
        dist = np.linalg.norm(cent[i] - cent[j])
        if dist > max_dist:
            max_dist = dist
sigma = max_dist / math.sqrt(2 * K_cent)

# Compute RBF transformation matrix for training data
row, column = X_scaled.shape
G = np.empty((row, K_cent), dtype=float)
for i in range(row):
    for j in range(K_cent):
        dist = np.linalg.norm(X_scaled[i] - cent[j])
        G[i][j] = math.exp(-math.pow(dist, 2) / math.pow(2 * sigma, 2))

# Compute weights
GTG = np.dot(G.T, G)
GTG_inv = np.linalg.inv(GTG)
fac = np.dot(GTG_inv, G.T)
W = np.dot(fac, Y)

# Split data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.33, random_state=42)

# Compute RBF transformation matrix for testing data
row_test, _ = X_test.shape
G_test = np.empty((row_test, K_cent), dtype=float)
for i in range(row_test):
    for j in range(K_cent):
        dist = np.linalg.norm(X_test[i] - cent[j])
        G_test[i][j] = math.exp(-math.pow(dist, 2) / math.pow(2 * sigma, 2))

# Predict output
prediction = np.dot(G_test, W)
prediction = 0.5 * (np.sign(prediction - 0.5) + 1)

# Evaluate model
score = accuracy_score(prediction, Y_test)
print("Accuracy:", score)""")
        
    elif condition == "MPC":
        print("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve
import tensorflow as tf
              
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/banana_quality.csv')
df.isnull().sum()

df.dtypes  

df['Quality'].unique()

#encoding
label_encoder = preprocessing.LabelEncoder()

# Encode labels in column 'species'.
df['Quality']= label_encoder.fit_transform(df['Quality'])

df['Quality'].unique()   

# Extract features and target variable
X = df[['Size', 'Weight', 'Sweetness', 'Softness', 'HarvestTime', 'Ripeness', 'Acidity', ]]
y = df['Quality']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#SKLEARN 
param_grid = {
    'hidden_layer_sizes': [(8, 4, 2)],
    'activation': ['logistic', 'tanh', 'relu', 'relu', 'elu'],
    'solver': ['sgd', 'adam', 'rmsprop', 'lbfgs'],
    'learning_rate_init': [0.1],
    'max_iter': [500],
    'alpha': [0.1, 0.01]  
}

# Create the MLPClassifier
mlp_model = MLPClassifier(random_state=42)

# Initialize GridSearchCV
grid_search = GridSearchCV(mlp_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)

# Fit the model with the data
grid_search.fit(X_train_scaled, y_train)

# Print the best parameters found by GridSearchCV
print("Best Parameters:", grid_search.best_params_)

# Predict on the test set using the best model
best_mlp_model = grid_search.best_estimator_

# Predictions on the test set
y_test_pred =  best_mlp_model.predict(X_test_scaled)
y_train_pred =  best_mlp_model.predict(X_train_scaled)

# Evaluate the model
accuracy_test = accuracy_score(y_test, y_test_pred)
accuracy_train = accuracy_score(y_train, y_train_pred)
conf_matrix = confusion_matrix(y_test, y_test_pred)
class_report_test = classification_report(y_test, y_test_pred)
class_report_train = classification_report(y_train, y_train_pred)

print("Accuracy for test:", accuracy_test)
print("Accuracy for train:", accuracy_train)
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report for testing:\n", class_report_test)
print("Classification Report for training:\n", class_report_train)

#TENSOR FLOW 
# Define the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model and capture the training history
history = model.fit(X_train_scaled, y_train, epochs=100, validation_data=(X_test_scaled, y_test), verbose=0)

# Evaluate the model on the test set
y_pred_prob = model.predict(X_test_scaled)
y_pred = (y_pred_prob > 0.5).astype(int)

# Generate the classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Plot the loss vs. epoch curve
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Plot the accuracy vs. epoch curve
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()
""")
        
    else:
        print("""
              SAND: single_layer_per AND
              SXOR: single_layer_per XOR
              SOR:  single_layer_per OR
              MXOR: multi_layer_per XOR
              MPC: multi_layer_per with Package
              MCSV: multi_layer_per K-fold for CSV
              FUZZY: FUZZY (May need to change the rule)
              RBF: Radial Base Function for CSV
              RXOR: Radial Base Function XOR
              CAM: ++
              BAM: ++
              """)

# Call the function with the condition
