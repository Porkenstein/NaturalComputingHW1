#/**********************************************************************/
#/*                                                                    */
#/*  Copyright (c) 1994                                                */
#/*  Larry D. Pyeatt                                                   */
#/*  Computer Science Department                                       */
#/*  Colorado State University                                         */
#/*                                                                    */
#/*  Permission is hereby granted to copy all or any part of           */
#/*  this program for free distribution.   The author's name           */
#/*  and this copyright notice must be included in any copy.           */
#/*                                                                    */
#/*  Contact the author for commercial licensing.                      */

import random
from math import exp

class phase_ann:
    #Takes two lists of weights and randomly chooses between the two weight to pick
    def combine_weights( self, weights1, weights2 ):
        for i in range(self.numlayers):
            for j in self.size[i]:
                for k in self.size[i]+1:
                    tmp = random.random()
                    if( tmp < 0.5 ):
                        self.weight[i][j][k] = weights1[i][j][k]
                    else:
                        self.weight[i][j][k] = weights2[i][j][k]

    def mutate_weights( self, num_weights ):
        for i in range( num_weights ):
            j = random.randint(0, self.numlayers-2)
            k = random.randint(0, self.size[j+1]-1 )
            l = random.randint(0, self.size[j])
            self.weights[j][k][l] = random.random()
            



#/* define the activation (transfer) function and its derivative */

    def xferfunc(self, x, theta):
        return 1.0 / (1.0 + exp(-(theta*x)));

    def xferfuncprime( self, xprime, theta):
        return theta * (xprime * (1.0 - xprime));

#/* Methods for scaling the input and output data                */
    def scale( self, x ):
        return ((x - self.xfermin) / (self.xfermax - self.xfermin) * (self.outmax-self.outmin)) + self.outmin;

    def unscale( self, x ):
        return ((x / (self.outmax - self.outmin)) * (self.xfermax - self.xfermin)); 

    #/* Allocate storage for the bpnet                               */
    def new_all(self):
        #/* allocate storage for the layers */
        self.activation = [0 for i in range(self.numlayers)] #new
        self.dotprod = [0 for i in range(self.numlayers)]         #new double*[numlayers];
        self.weights = [0 for i in range(self.numlayers-1)]       #new double**[numlayers-1];
        self.sigma =   [0 for i in range(self.numlayers)]         #new double*[numlayers];
        self.delta =   [0 for i in range(self.numlayers-1)]         #new double**[numlayers-1];     
        for i in range( self.numlayers ):
            self.activation[i] = [0 for k in range( self.size[i] ) ]  #new double[size[i]];
            self.dotprod[i] = [0 for k in range( self.size[i] ) ]     #new double[size[i]];

            self.sigma[i] = [0 for k in range( self.size[i] ) ]   #new double[size[i]];

            if( i < ( self.numlayers - 1 ) ):
                self.weights[i] = [0 for k in range( self.size[i+1] ) ]  #new double*[size[i+1]];
                self.delta[i] =   [0 for k in range( self.size[i+1] ) ]  #new double*[size[i+1]];
                for j in range( self.size[i+1] ):   #(j = 0 ; j < size[i+1] ; j++)
                    #// add one for the bias input
                    self.weights[i][j] = [ 0 for k in range( self.size[i] + 1 ) ] #new double[size[i]+1];
                    self.delta[i][j] =   [ 0 for k in range( self.size[i] + 1 ) ] #new double[size[i]+1];  

#/****************************************************************/
#/* Constructor for the backpropagation networks                 */
#/* arguments:                                                   */
#/*    number of layers,                                         */
#/*    size of input layer,                                      */
#/*    size of first hidden layer,                               */
#/*    ...                                                       */
#/*    size of output layer                                      */
    def __init__(self, layers, *args):
        self.set_defaults();
        self.numlayers = layers;  
        self.weights = []
        self.size = [ 0.0 for i in range(self.numlayers) ]
        j = 0
        for i in args:
            self.size[j] = i;
            j = j + 1
        self.new_all();
  #/* randomize the weights and set deltas to zero */
        for i in range( 0, self.numlayers-1 ):  #(i = 0 ; i < (numlayers - 1) ; i++)
            for j in range( 0, self.size[i+1] ):     #(j = 0 ; j < size[i+1] ; j++)
                for k in range( 0, self.size[i]+1 ):   #(k = 0 ; k < size[i]+1 ; k++)  // +1 for the bias input 
                    self.weights[i][j][k] = random.random()
                    self.delta[i][j][k] = 0.0;


    def set_defaults(self):
        self.fitness = -1;
        self.THETA = 1.0;
        self.STEP = 0.01;
        self.MOMENTUM = 0.0;
        self.outmax = 1.0; 
        self.outmin = -1.0; 
        self.xfermin = 0;
        self.xfermax = 1;
        self.LINEAR_OUTPUT = 0;

#/* evaluate the network from inputs to outputs                  */
    def evaluate( self, input_vector, output_vector):
  #/* Don't copy input vector.  Just set the pointer  */
        self.activation[0] = input_vector;
  
        for i in range ( self.numlayers - 1):       #(i = 0 ; i < numlayers - 1 ; i++)      // i = layer number
            for j in range( self.size[i+1] ):       #(j = 0 ; j < self.size[i+1] ; j++)    #// j = to node
                self.dotprod[i+1][j] = 0.0;
                for k in range( self.size[i] ):          #(k = 0 ; k < size[i] ; k++)      #// k = from node
                    self.dotprod[i+1][j] += (self.weights[i][j][k] * self.activation[i][k]);
                self.dotprod[i+1][j] += self.weights[i][j][self.size[i]] * 1.0;                  #// bias input 
                if( ( i < self.numlayers-2 ) or ( not self.LINEAR_OUTPUT )):
                    self.activation[i+1][j] = self.xferfunc(self.dotprod[i+1][j],self.THETA);
                else:
                    self.activation[i+1][j] = self.dotprod[i+1][j] * self.THETA;         
  
        for i in range( self.size[self.numlayers - 1] ):   #(i = 0 ; i < size[numlayers-1] ; i++)
            output_vector[i] = self.scale( self.activation[self.numlayers-1][i] );


def main():
    layers = 4
    layer1 = 4
    layer2 = 4
    layer3 = 4
    layer4 = 15
    input_vector = [0,0,0,1]
    output_vector = [0 for i in range(15)]
    while( output_vector[1] < i for i in output_vector ):
        test = phase_ann(layers, layer1, layer2, layer3, layer4 )
        test.evaluate(input_vector, output_vector)
        test.mutate_weights(1)
    print(output_vector)

if __name__ == "__main__":
    main()
