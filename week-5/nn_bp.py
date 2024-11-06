import numpy as np
from random import random

class Full_NN(object):

    def __init__(self, X=2, HL=[2,2], Y=2): 
        self.X=X # inputs
        self.HL=HL # hidden layers
        self.Y=Y # outputs

        # total number of layers
        L=[X]+HL+[Y] 

        # array for weights
        W=[] 

        # repetition for filling up random values into layers
        for i in range(len(L)-1): 
            w=np.random.rand(L[i], L[i+1]) 
            W.append(w) 

        # assigned weights
        self.W=W 

        # derivative array
        Der = []

        # assign zeros to the derivatives
        for i in range(len(L)-1):
            d=np.zeros((L[i], L[i+1]))
            Der.append(d)
            self.Der=Der

        # output list
        out=[] 

        # assign zeros to the outputs
        for i in range(len(L)):
            o=np.zeros(L[i])
            out.append(o)
            self.out=out
    
    # Runs the network forwards
    def FF(self,x):
        # input layer's output is just the input
        out=x   

        # link outputs to the class variable for back propagation
        self.out[0]=x

        # iterate the network layers via weight variables
        for i, w in enumerate(self.W):
            # calculate product with weights and outputs
            Xnext=np.dot(out, w)
            # activation function
            out=self.sigmoid(Xnext)
            # pass result to the class variable to preserve for later
            self.out[i+1]=out
        # return outputs of the layers    
        return out
    
    # Back propagation function
    def BP(self, Er):

        #iterating backwards
        for i in reversed (range(len(self.Der))):
            # get layer output from previous layer
            out=self.out[i+1]
            # applying the derivative of the activation function
            D=Er*self.sigmoid_Der(out) 
            # turn Delta into an array of appropritate size
            D_fixed=D.reshape(D.shape[0], -1).T
            # current layer output
            this_out=self.out[i]
            # reshape as before to get column array suitable for the multiplication
            this_out=this_out.reshape(this_out.shape[0],-1)
            # matrix multiplication
            self.Der[i]=np.dot(this_out, D_fixed)
            # back propagate the error
            Er=np.dot(D, self.W[i].T)

    # training of the network
    def train_nn(self, x, target, epochs, lr): 
        # training loop for as many epochs we need
        for i in range (epochs):
            # variable to carry the error
            S_errors=0
            # iterate through the training data and inputs
            for j, input in enumerate (x):
                t=target[j]
                # use the network calculations for forward calculations
                output=self.FF(input)
                # obtain overall network output error
                e=t-output
                # use the erro to do the back propagation
                self.BP(e)
                # gradient descent
                self.GD(lr)
                # update the overall error
                S_errors+=self.msqe(t,output)

    # Gradient descent
    def GD(self, lr=0.05):
        # go through the weights
        for i in range(len(self.W)):
            W=self.W[i]
            Der=self.Der[i]
            # update the weights by applying the learning rate
            W+= Der*lr     

    # Sigmoid activation function
    def sigmoid(self,x): 
        y=1.0/(1+np.exp(-x))
        return y 
    
    # Sigmoid function n derivative
    def sigmoid_Der(self, x): 
        sig_der=x*(1.0-x)
        return sig_der 

    # mean square error
    def msqe(self, t, output): 
        msq=np.average((t-output)**2)
        return msq 

if __name__ == "__main__": 
    # create training set of inputs
    training_inputs = np.array([[random()/2 for _ in range(2)] for _ in range(1000)]) 
    # create training set of outputs
    targets = np.array([[i[0] * i[1]] for i in training_inputs])
    # creates a NN with 2 inputs, 2 hidden layers and 1 output
    nn=Full_NN(2, [5, 5], 1) 
    # trains the network with 0.1 learning rate for 10 epochs
    nn.train_nn(training_inputs, targets, 10, 0.1) 
    # testing data to identify if Network trained well
    input = np.array([0.3, 0.2]) 
    target = np.array([0.06]) 
    NN_output = nn.FF(input)
    
    print("=============== Testing the Network Screen Output===============")
    print ("Test input is ", input)
    print()
    print("Target output is ",target)
    print()
    print("Neural Network actual output is ",NN_output, "there is an error (not MSQE) of ",target-NN_output)
    print("=================================================================") 
