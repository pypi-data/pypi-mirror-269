"""
Pymindcore
===
A very user friendly AI library, that has the capacity to be just as powerful as any other *.

Benefits over other libraries:
    1: Pymindcore is much easier to use than Pytorch and Tensorflow. To get started with a checkerboard pattern detection (with inputs as data, and the outputs as expected_outputs), with relu activation and output, and Mean random initialisation.
    >>> import pymindcore as pm #Import the library
    >>> network = pm.Optomised_neural_network(4, [4,4], 2, "relu", "relu", "Mean") #Initialise the network with 4 inputs, 2 layers of 4 middle neurons, 2 outputs, the relu activation for middle and output, and the mean random initialisation
    >>> network.train(data,expected_outputs,20000,0.01,"ADAM") #Train the network with the inputs as data, the outputs as expected_outputs, 20000 epochs at 0.01 learning rate, using the ADAM optomiser.
    >>> network.save_to_file("Trained.npy") #Save the network to Trained.npy file

    2: Pymindcore is quite fast. In speed tests between Pymindcore, Pytorch, and Tensorflow, Pymindcore beats Tensorflow quite easily, and is snapping at the heels of Pytorch. 
        Pytorch uses about 8gb of libraries to speed it up to insane levels. Pymindcore itself is only 81kb, and when including libraries (namely numpy and math), is still only about 85mb. 
    
    3: Dispite its size, Pymindcore is quite powerful (in supported features). By itself, it pales in comparison to Pytorch and Tensorflow
    
"""
from .core import *

print("Pymind package is being imported!")