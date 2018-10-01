import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.init as init

#tensor
tensor = torch.Tensor( 10,10 )
print( tensor )
print( tensor.numpy()) # 값은 아주 지멋대로 들어있음.

#tensor create randomly
# uniform
tensor = torch.rand( 10,10,10 )
print( tensor )

# normal
tensor = torch.randn(7,7)
print( tensor )

#






zeros = torch.zeros( 10 )
print( zeros )