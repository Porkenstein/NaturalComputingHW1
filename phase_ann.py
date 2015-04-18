import numpy as np
from numpy import *
import random

#input and out layers are separted from the hidden layers to allow for variable 
#number of inputs and outputs compared to the hidden layer nodes. 
#However the hidden layer must be a square matrix

class phase_ann: 
    def __init__( self, i_nodes, h_layers,h_nodes, o_nodes ):
        #number of hidden layers and nodes
        self.n_hidden = h_layers
        self.h_nodes = h_nodes + 1 #add one for bias input
        
        #number of input nodes and output nodes
        self.in_nodes = i_nodes
        self.out_nodes = o_nodes
        
        #input weights to first hidden layer
        self.in_weights = np.empty( ( self.in_nodes, self.h_nodes ) )
        #last hidden layer weights to output layer
        self.out_weights = np.empty( ( self.h_nodes, self.out_nodes ) )
                
        #hidden layer weights
        self.weights = np.empty( (self.n_hidden, self.n_nodes, self.n_nodes) )
        self.init_weights()
        
        #activation function
        self.activation = np.empty( ( self.n_hidden, self.n_nodes))

        #dotprod
        self.dotprod = np.empty( ( self.n_hidden, self.n_nodes ))
        
        self.THETA = 1.0
    
    def init_weights():
        for i in range( self.n_hidden ):
            for j in range( self.n_nodes ):
                for k in range( self.n_nodes ):
                    self.weights[i][j][k] = random.random()

    def evaluate( in_vector, out_vector ):
        #Store the input vecor as the first row in the activation 
        x = 0
        for i in range( self.in_nodes )
            activation[0][x] = in_vector[i]
            x += 1


        #evaluate input layer to first hidden layer
        for i in range(self.in_nodes):
            for j in range( self.h_nodes ):
                
        #evaluate through hidden layers
        for i in range(self.n_hidden):        #i = layer number
            
            for j in range(self.n_nodes):       #j = to node
                dotprod[i+1][j] = 0.0;
            
                for k in range( self.n_nodes):      #k = from node
                    dotprod[i+1][j] += (weights[i][j][k] * activation[i][k]);
            
            dotprod[i+1][j] += weights[i][j][size[i]] * 1.0; # bias input 
            
            if((i < numlayers-2) || (!LINEAR_OUTPUT))
                activation[i+1][j] = activation_function(dotprod[i+1][j],THETA);
            else
                activation[i+1][j] = dotprod[i+1][j] * THETA;
        #evaluate from last hidden layer to output layer
        for i in range( self.out_nodes - 1 ):
            output_vector[i] = scale( activation[n_hidden-1][i] )

    def adjust_weights( num_to_adjust)
    def activation_function(double x,double theta):
        return 1.0 / (1.0 + exp(-(theta*x)))
    def double activation_prime(double xprime,double theta):
        return theta * (xprime * (1.0 - xprime));
