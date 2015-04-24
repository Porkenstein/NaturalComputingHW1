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


class phase_ann:
    #Takes two lists of weights and randomly chooses between the two weight to pick
    def combine_weights( weights1, weights2 ):
        for i in range(self.num_layers):
            for j in self.size[i]:
                for k in self.size[i]+1:
                    tmp = random.random()
                    if( tmp < 0.5 ):
                        self.weight[i][j][k] = weights1[i][j][k]
                    elif( tmp < .80):
                        self.weight[i][j][k] = weights2[i][j][k]

    def mutate_weights( num_weights ):
        for i in range( num_weights ):
            j = random.randint(0, self.num_layers-1)
            k = random.randint(0, self.size[i] )
            l = random.randint(0, self.size[i] + 1)

            self.weights[j][k][l] = random.random()
            



#/* define the activation (transfer) function and its derivative */

    def xferfunc( x, theta)
        return 1.0 / (1.0 + exp(-(theta*x)));

    def xferfuncprime( xprime, theta)
        return theta * (xprime * (1.0 - xprime));

#/* Methods for scaling the input and output data                */
    def scale( x ):
        return ((x - xfermin) / (xfermax - xfermin) * (outmax-outmin)) + outmin;

    def unscale( x ):
        return ((x / (outmax - outmin)) * (xfermax - xfermin)); 

    #/* Allocate storage for the bpnet                               */
    def new_all():
        #/* allocate storage for the layers */
        self.activation = [0 * self.numlayers] #new
        self.dotprod = [0 * self.numlayers]         #new double*[numlayers];
        self.weights = [0 * self.numlayers-1]       #new double**[numlayers-1];
        self.sigma =   [0 * self.numlayers]         #new double*[numlayers];
        self.delta =   [0 * self.numlayers]         #new double**[numlayers-1];     

        for i in range( self.numlayers ):
            self.activation[i] = [0 * ( self.size[i] ) ]  #new double[size[i]];
            self.dotprod[i] = [0 * ( self.size[i] ) ]     #new double[size[i]];

            self.sigma[i] = [0 * ( self.size[i] ) ]   #new double[size[i]];

            if(i < (numlayers - 1)):
                self.weights[i] = [0 * ( self.size[i+1] ) ]  #new double*[size[i+1]];
                self.delta[i] =   [0 * ( self.size[i+1] ) ]  #new double*[size[i+1]];

            for j in range( size[i+1] ):   #(j = 0 ; j < size[i+1] ; j++)
                #// add one for the bias input
                self.weights[i][j] = [ 0 * ( self.size[i] + 1 ) ] #new double[size[i]+1];
                self.delta[i][j] =   [ 0 * ( self.size[i] + 1 ) ] #new double[size[i]+1];  

#/****************************************************************/
#/* Constructor for the backpropagation networks                 */
#/* arguments:                                                   */
#/*    number of layers,                                         */
#/*    size of input layer,                                      */
#/*    size of first hidden layer,                               */
#/*    ...                                                       */
#/*    size of output layer                                      */
    def __init__(self, layers, *args)
        self.set_defaults() 
        self.numlayers = layers;  
        self.size = [ 0 * numlayers ]
  
        for i in range( len( args ))
            self.size[i] = args[i];
         self.new_all();
  
  #/* randomize the weights and set deltas to zero */
        for i in range( numlayers-1 ):  #(i = 0 ; i < (numlayers - 1) ; i++)
            for j in range( size[i+1] ):     #(j = 0 ; j < size[i+1] ; j++)
                for k in range( size[i]+1 ):   #(k = 0 ; k < size[i]+1 ; k++)  // +1 for the bias input 
                    self.weights[i][j][k] = random.random()
                    self.delta[i][j][k] = 0.0;


    def set_defaults():
        self.THETA = 1.0;
        self.STEP = 0.01;
        self.MOMENTUM = 0.0;
        self.outmax = 1.0; 
        self.outmin = -1.0; 
        self.activation_function_type = Sigmoid;
        self.xfermin = 0;
        self.xfermax = 1;
        self.LINEAR_OUTPUT = 0;

#/* evaluate the network from inputs to outputs                  */
    def evaluate(double *input_vector,double *output_vector)
  #/* Don't copy input vector.  Just set the pointer  */
        self.activation[0] = self.input_vector;
  
        for i in range ( self.numlayers - 1):       #(i = 0 ; i < numlayers - 1 ; i++)      // i = layer number
            for j in range( self.size[i+1] ):       #(j = 0 ; j < self.size[i+1] ; j++)    #// j = to node
                dotprod[i+1][j] = 0.0;
                for k in range( size[i] ):          #(k = 0 ; k < size[i] ; k++)      #// k = from node
                    self.dotprod[i+1][j] += (self.weights[i][j][k] * self.activation[i][k]);
                self.dotprod[i+1][j] += self.weights[i][j][size[i]] * 1.0;                  #// bias input 
                if((i < self.numlayers-2) || (!LINEAR_OUTPUT))
                    self.activation[i+1][j] = self.xferfunc(dotprod[i+1][j],self.THETA);
                else
                    self.activation[i+1][j] = self.dotprod[i+1][j] * self.THETA;         
  
        for i in range( size[numlayers - 1] ):   #(i = 0 ; i < size[numlayers-1] ; i++)
            output_vector[i] = self.scale( self.activation[numlayers-1][i] );
