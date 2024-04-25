def update_graph():
    names = input()
    if(names == 'mlp'):
        print(
            '''
    from math import exp 
from random import seed 
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


# Transfer neuron activation 
def transfer(activation): 
    return 1.0 / (1.0 + exp(-activation)) 


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
dataset = [[2.7810836,2.550537003,0], 
[1.465489372,2.362125076,0], 
[3.396561688,4.400293529,0], 
[1.38807019,1.850220317,0], 
[3.06407232,3.005305973,0], 
[7.627531214,2.759262235,1], 
[5.332441248,2.088626775,1], 
[6.922596716,1.77106367,1], 
[8.675418651,-0.242068655,1], 
[7.673756466,3.508563011,1]] 

n_inputs = len(dataset[0]) - 1 
n_outputs = len(set([row[-1] for row in dataset])) 
network = initialize_network(n_inputs, 2, n_outputs) 
train_network(network, dataset, 0.5, 20, n_outputs) 
for layer in network: 
    print(layer) 

 


'''
        )

    elif(names == 'mlpk'):
        print(
            '''
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# Define the XOR dataset
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])


# Create the model
model = Sequential()
model.add(Dense(2, input_dim=2, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))


# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=1000, batch_size=1)

# Evaluate the model
scores = model.evaluate(X, y)
print((model.metrics_names[1], scores[1]*100))


# Predict the output for the XOR dataset
predictions = model.predict(X)

# Print the predictions
for i in range(len(predictions)):
    print((X[i], predictions[i]))
model.summary()
model.get_config()
from tensorflow.keras.utils import plot_model
plot_model(model, to_file='model.png')



'''
        )

    elif(names == 'mlpc'):
        print(
            '''
import numpy as np
from sklearn.neural_network import MLPClassifier

# Define the XOR dataset
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 1, 1, 0])

# Create the MLP classifier
mlp = MLPClassifier(hidden_layer_sizes=(2,), activation='logistic', solver='adam', max_iter=1000)

# Train the model
mlp.fit(X, y)

# Evaluate the model
accuracy = mlp.score(X, y)
print((accuracy * 100))

# Predict the output for the XOR dataset
predictions = mlp.predict(X)

# Print the predictions
for i in range(len(predictions)):
    print((X[i], predictions[i]))


'''
        )

    elif(names == 'bam'):
        print(
            '''
import numpy as np

# Define memory vectors
mem_vectors_x = np.array([[0, 1, 0, 1, 0], [1, 1, 0, 0, 0]])  # Fx vectors
mem_vectors_y = np.array([[1, 0, 0, 1], [0, 1, 0, 1]])  # Fy vectors

# Compute weight matrix
wt_matrix = np.dot(mem_vectors_x.T, mem_vectors_y)

# Set up probe and initial signals
probe = np.array([0, 1, 0, 1, 1])
signal_x = 2 * probe - 1
signal_y = np.random.choice([-1, 1], mem_vectors_y.shape[1])

# Store patterns
pattern_x = [signal_x]
pattern_y = [signal_y]

# Iterate until bidirectional equilibrium is reached
while True:
    signal_y = np.sign(np.dot(signal_x, wt_matrix))
    pattern_y.append(signal_y)

    signal_x = np.sign(np.dot(signal_y, wt_matrix.T))
    pattern_x.append(signal_x)

    if np.array_equal(signal_x, pattern_x[-2]) and np.array_equal(signal_y, pattern_y[-2]):
        break

# Print updated traces
print("Updated traces on Fx:")
print(pattern_x)
print("Updated traces on Fy:")
print(pattern_y)


'''
        )

    elif(names == 'cam'):
        print(
           '''
import numpy as np

# Define memory vectors
mem_vectors = np.array([
    [1, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 1]
])

# Compute weight matrix
zd_wt_mat = np.dot(mem_vectors.T, mem_vectors) - mem_vectors.shape[0] * np.eye(mem_vectors.shape[1])

# Define probe vector
probe = np.array([1, 0, 0, 1, 0, 0, 0, 1])

# Recall using CAM
signal_vector = np.dot(zd_wt_mat, probe)

# Threshold the signal vector to obtain the recalled vector
recalled_vector = np.where(signal_vector >= 0, 1, 0)

print("The recalled vector is:", recalled_vector)


'''
        )
    elif(names == 'rdf'):
        print(
            '''
import numpy as np 
import pandas as pd 
from sklearn.preprocessing import LabelEncoder, StandardScaler 
from sklearn.metrics import accuracy_score 
from sklearn.model_selection import train_test_split 
from sklearn.cluster import KMeans 

# Load dataset
data = pd.read_csv('diabetes.csv') 

# Encode categorical variables
encoder = LabelEncoder()
encoded_data = data.apply(encoder.fit_transform)

# Separate features and target variable
X = encoded_data.drop(columns=['Outcome'])
y = encoded_data['Outcome']

# Split dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=4)

# Scale features
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# Determine cluster centers using KMeans
k_cent = 8
km = KMeans(n_clusters=k_cent, max_iter=100)
km.fit(x_train_scaled)
cent = km.cluster_centers_

# Determine sigma
d = np.max(np.linalg.norm(cent[:, None] - cent[None, :], axis=-1))
sigma = d / np.sqrt(2 * k_cent)

print(d)
print(sigma)

# Compute G matrix for training set
G_train = np.exp(-np.linalg.norm(x_train_scaled[:, None] - cent[None, :], axis=-1) ** 2 / (2 * sigma ** 2))

print(G_train)

# Compute weights matrix W
W = np.linalg.lstsq(G_train, y_train, rcond=None)[0]

# Compute G matrix for testing set
G_test = np.exp(-np.linalg.norm(x_test_scaled[:, None] - cent[None, :], axis=-1) ** 2 / (2 * sigma ** 2))

# Make predictions
predictions = 0.5 * (np.sign(np.dot(G_test, W) - 0.5) + 1)

# Calculate accuracy
accuracy = accuracy_score(predictions, y_test)
print('Accuracy:', accuracy * 100)


'''
        )
    elif(names == 'kfold'):
        print(
            '''
from random import seed
from random import randrange
from random import random
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

# Transfer neuron activation
def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))

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
    return predictions

# Test Backprop on Seeds dataset
seed(1)
# load and prepare data
filename = 'diabetes.csv'
dataset = load_csv(filename)
for i in range(len(dataset[0])-1):
    str_column_to_float(dataset, i)
# convert class column to integers
str_column_to_int(dataset, len(dataset[0])-1)
# normalize input variables
minmax = dataset_minmax(dataset)
normalize_dataset(dataset, minmax)
# evaluate algorithm
n_folds = 5
l_rate = 0.3
n_epoch = 500
n_hidden = 5
scores = evaluate_algorithm(dataset, back_propagation, n_folds, l_rate, n_epoch, n_hidden)
print('Scores: %s' % scores)
print('Mean Accuracy: %.3f%%' % (sum(scores)/float(len(scores))))

'''
        )
    elif(names == 'fuzzy'):
        print('''
x_temp = float(input("Enter the value of Temperature:"))
x_press = float(input("Enter the value of Pressure:"))

print("RULE 1")
print("If Temperature is below average ")

L = 15
R = 45
C = (R + L) / 2
if  x_temp > L and x_temp <= C:
    z_rule1_temp = (x_temp - L) / (C - L)
elif x_temp > C and x_temp <= R:
    z_rule1_temp = (R - x_temp) / (R - C)
else:
    z_rule1_temp = 0
print("Temperature Membership for Rule 1:", z_rule1_temp)

print("Pressure is below average ")
R = 2.75
L = 1.25
C = (R + L) / 2
if x_press > L and x_press <= C:
    z_rule1_press = (x_press - L) / (C - L)
elif x_press > C and x_press <= R:
    z_rule1_press = (R - x_press) / (R - C)
else:
    z_rule1_press = 0
print("Pressure Membership for Rule 1:", z_rule1_press)

print("RULE 2")
print("If Temperature is low ")
R = 25
C = 10
D = C - L
L = C + D
if x_temp > L and x_temp <= C:
    z_rule2_temp = (x_temp - L) / (C - L)
elif x_temp > C and x_temp <= R:
    z_rule2_temp = (R - x_temp) / (R - C)
else:
    z_rule2_temp = 0
print("Temperature Membership for Rule 2:", z_rule2_temp)

print("Pressure is low")
R = 1.75
C = 1
D = C - L
L = C + D
if x_press > L and x_press <= C:
    z_rule2_press = (x_press - L) / (C - L)
elif x_press > C and x_press <= R:
    z_rule2_press = (R - x_press) / (R - C)
else:
    z_rule2_press = 0
print("Pressure Membership for Rule 2:", z_rule2_press)

min_memb_Z1 = min(z_rule1_temp,z_rule1_press)
print(min_memb_Z1)

min_memb_Z2 = min(z_rule2_temp,z_rule2_press)
print(min_memb_Z2)
#for HP
print("HP rule 1")

L_Hp_R1= 3.25
R_Hp_R1 =4.75
C_Hp_R1 = (L_Hp_R1+R_Hp_R1)/2
Area_1=(1/2)(R_Hp_R1 - L_Hp_R1)(1)
print(Area_1)

print("Hp rule 2")
L_Hp_R2= 4.25
C_Hp_R2 = 5
D_Hp_R2 = C_Hp_R2-L_Hp_R2
R_Hp_R2 = C_Hp_R2 + D_Hp_R2

Area_2 = (1/2)(R_Hp_R2 - L_Hp_R2)(1)

print(Area_2)


print(min_memb_Z1)
print(Area_1)
print(C_Hp_R1)
print(min_memb_Z2)
print(Area_2)
print(C_Hp_R2)
Center_Hp= ((min_memb_Z1)(Area_1)(C_Hp_R1)+ (min_memb_Z2)(Area_2)(C_Hp_R2)) / ((min_memb_Z1)(Area_1)+(min_memb_Z2)(Area_2))
print(Center_Hp)

#For VO
print("VO rule 1")

L_Vo_R1= 1.25
R_Vo_R1 =2.75
C_Vo_R1 = (L_Vo_R1+R_Vo_R1)/2
Area_vo1=(1/2)(R_Vo_R1 - L_Vo_R1)(1)
print(Area_vo1)

print("Vo rule 2")
R_Vo_R2= 1.75
C_Vo_R2 = 1
D_Vo_R2 = C_Vo_R2-R_Vo_R2
L_Vo_R2 = C_Vo_R2 + D_Vo_R2

Area_vo2 = (1/2)(R_Vo_R2 - L_Vo_R2)(1)

print(Area_vo2)

Center_Vo= ((min_memb_Z1)(Area_vo1)(C_Vo_R1)+ (min_memb_Z2)(Area_vo2)(C_Vo_R2)) / ((min_memb_Z1)(Area_vo1)+(min_memb_Z2)(Area_vo2))
print(Center_Vo)
        
''')
    elif(names == 'sl'):
        print('''
def predict(row, weights): 
    activation = weights[0] 
    for i in range(len(row)-1): 
        activation = activation + weights[i+1] * row[i] 
    return 1.0 if activation >= 0.0 else 0.0 

# Training Weights Function  
def train_weights(train, l_rate, n_epoch): 
    weights = [0.0 for i in range(len(train[0]))] 
    for epoch in range(n_epoch): 
        sum_error = 0.0 
        for row in train: 
            predication = predict(row, weights) 
            error = row[-1] - predication 
            sum_error = sum_error + error**2  
            weights[0] = weights[0] + l_rate * error 
            for i in range(len(row)-1): 
                weights[i+1] = weights[i+1] + l_rate * error * row[i] 
        print("Epoch =  {} , lrate = {} , ERROR {}".format(round(epoch,3) , round(l_rate,3) , round(sum_error , 3))) 
    return weights 

dataset = [[2.7810836,2.550537003,0], 
           [1.465489372,2.362125076,0], 
           [3.396561688,4.400293529,0], 
           [1.38807019,1.850220317,0], 
           [3.06407232,3.005305973,0], 
           [7.627531214,2.759262235,1], 
           [5.332441248,2.088626775,1], 
           [6.922596716,1.77106367,1], 
           [8.675418651,-0.242068655,1], 
           [7.673756466,3.508563011,1]] 

l_rate = 0.1 
n_epoch = 5 
weights = train_weights(dataset, l_rate, n_epoch) 
print(weights)
       
        
        ''')
    
    elif(names == 'sland'):
        print('''
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

# Use the predict function to make predictions on the dataset
for row in dataset: 
    prediction = predict(row, weights) 
    print("Expected=%d, Predicted=%d" % (row[-1], prediction))

        
        ''')
    elif(names == 'slor'):
        print('''
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

# Use the predict function to make predictions on the dataset
for row in dataset: 
    prediction = predict(row, weights) 
    print("Expected=%d, Predicted=%d" % (row[-1], prediction))

        ''')
    
    elif(names == 'rdfo'):
        print(
            '''
# Importing Packages  

import math 
import pandas as pd 
from sklearn.preprocessing import LabelEncoder 
from sklearn.metrics import accuracy_score 
from sklearn.model_selection import train_test_split 
from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler 
import numpy as numpy  

 
# Importing Data set using Pandas 

Data = pd.read_csv('/content/bank-full.csv') 
print(Data) 

cols= Data[["age","balance","day","duration","campaign","pdays","previous"]] 
 
# Converting Characteristic Values into Numeric using Label Encoding 
 
encoding = Data[['job','marital','education','housing','loan','contact','month','poutcome','Target']] 
print(encoding) 
encoder = encoding.apply(LabelEncoder().fit_transform) 
print(encoder) 
Data = pd.concat([cols , encoder] , axis = 1) 
print(Data) 
# Splitting Data into features (x) and target Variable (y) 
X=Data[['age','balance','day','duration','campaign','pdays','previous','job','marital','education','housing','loan','contact','month','poutcome']] 
y = Data[['Target']] 
print(X) 
print(y) 

 

# Splittng Data into training and Testing set 
x_train ,x_test, y_train , y_test = train_test_split(X,y , test_size = 0.33 , random_state=4) 
print(x_train)
print(x_test) 
 
# Applying standarScaler() from sklearn to scales the different features 
scaler = StandardScaler() 
scaler.fit(x_train) 
x_train = scaler.transform(x_train) 
x_test = scaler.transform(x_test) 
print(x_train) 
print(x_test) 

# Splitting Data into features (x) and target Variable (y) 
X=Data[['age','balance','day','duration','campaign','pdays','previous','job','marital','education','housing','loan','contact','month','poutcome']] 
y = Data[['Target']] 
print(X) 
print(y) 

 

# Splitting Data into training and Testing set 
x_train ,x_test, y_train , y_test = train_test_split(X,y , test_size = 0.33 , random_state=4) 
print(x_train) 
print(x_test) 

# Applying standarScaler() from sklearn to scales the different features 
scaler = StandardScaler() 
scaler.fit(x_train) 
x_train = scaler.transform(x_train) 
x_test = scaler.transform(x_test) 

print(x_train) 
print(x_test) 
# Determine Centers of Neuron Using kMeans 
k_cent = 8 
km = KMeans(n_clusters = k_cent , max_iter = 100) 
km.fit(x_train) 
cent = km.cluster_centers_ 
print(cent) 
 

# Determine the value of sigma 
max = 0  
for i in range(k_cent): 
    for j in range(k_cent): 
        d = numpy.linalg.norm(cent[i] - cent[j]) 
        if(d > max): 
            max = d 
d = max 
sigma = d/math.sqrt(2*k_cent) 
print(d) 
print(sigma) 

 
# Set up Matrix G 
shape= x_train.shape 
row= shape[0] 
column= k_cent 
G= numpy.empty((row,column), dtype= float) 
for i in range(row): 
     for j in range(column): 
            dist= numpy.linalg.norm(x_train[i]-cent[j]) 
            G[i][j]= math.exp(-math.pow(dist,2)/math.pow(2*sigma,2)) 
print(shape) 
print(G) 
# Finding weights Matrix W to train Network 
GTG= numpy.dot(G.T,G) 
GTG_inv= numpy.linalg.inv(GTG) 
fac= numpy.dot(GTG_inv,G.T) 
W= numpy.dot(fac,y_train) 
print(GTG) 
print(GTG_inv) 
print(fac) 
print(W) 

 

# Setup the metrix G for Test Set 
row= x_test.shape[0] 
column= k_cent 
G_test= numpy.empty((row,column), dtype= float) 
for i in range(row): 
    for j in range(column): 
        dist= numpy.linalg.norm(x_test[i]-cent[j]) 
        G_test[i][j]= math.exp(-math.pow(dist,2)/math.pow(2*sigma,2)) 
print(G_test) 

# Analyzing Accuracy and Predication 
prediction= numpy.dot(G_test,W) 
prediction= 0.5*(numpy.sign(prediction-0.5)+1) 
score= accuracy_score(prediction,y_test) 
print(score.mean()) 
print('Accuracy :- ' , score*100)         
            '''
        )
    

    else:
        print(
            '''
Multilayer Perceptron :- mlp
Multilayer Perceptron :- mlpk
Multilayer Perceptron :- mlpc
BAM :- bam
CAM :- cam
RDF :- rdf
RDF Original : rdfo
KFOLD :- kfold
FUZZY :- fuzzy
Single Layer : sl
Single Layer AND : sland
Single Layer OR : slor

'''
        )
