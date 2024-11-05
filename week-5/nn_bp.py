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
    
    def FF(self,x):
        out=x

        self.out[0]=x

        for i, w in enumerate(self.W):
            Xnext=np.dot(out, w)
            out=self.sigmoid(Xnext)
            self.out[i+1]=out
        return out
    
    def BP(self, Er):
        for i in reversed (range(len(self.Der))):
            out=self.out[i+1]
            
            D=Er*self.sigmoid_Der(out) 
            D_fixed=D.reshape(D.shape[0], -1).T

            this_out=self.out[i]
            this_out=this_out.reshape(this_out.shape[0],-1)

            self.Der[i]=np.dot(this_out, D_fixed)
            Er=np.dot(D, self.W[i].T)

    def train_nn(self, x, target, epochs, lr): 
        for i in range (epochs):
            S_errors=0

            for j, input in enumerate (x):
                t=target[j]

                output=self.FF(input)
                e=t-output

                self.BP(e)
                self.GD(lr)

                S_errors+=self.msqe(t,output)

    def GD(self, lr=0.05):
        for i in range(len(self.W)):
            W=self.W[i]
            Der=self.Der[i]
            W+= Der*lr     

    def sigmoid(self,x): 
        y=1.0/(1+np.exp(-x))
        return y 
    
    def sigmoid_Der(self, x): 
        sig_der=x*(1.0-x)
        return sig_der 

    def msqe(self, t, output): 
        msq=np.average((t-output)**2)
        return msq 

if __name__ == "__main__": 
    training_inputs = np.array([[random()/2 for _ in range(2)] for _ in range(1000)]) 
    targets = np.array([[i[0] * i[1]] for i in training_inputs])

    nn=Full_NN(2, [5, 5], 1) 
    nn.train_nn(training_inputs, targets, 10, 0.1) 
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
