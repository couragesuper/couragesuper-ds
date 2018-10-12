# visualize
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show

# numpy
import numpy as np

# torch
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.init as init

if True :
    def mscatter(p, x, y, size=5, fill_color="orange", alpha=0.5, marker="circle"):
        p.scatter(x, y, marker=marker, size=size,
                  fill_color=fill_color, alpha=alpha)
    def scatter(x, y, title='', size=5, color='orange', height=600, width=600):
        p = figure(title=title)
        p.width = width
        p.height = height
        mscatter(p, x, y, size, color)
        return p

def show_tensor_image(img, cmap='gray'):
    if len(img.shape) >= 3: img = torch.squeeze(img)
    img = img.numpy()
    show_image(img, cmap)

def show_image(img_2d, cmap='gray'):
    plt.imshow(img_2d, cmap=cmap)
    plt.show()

print('PyTorch version = {}'.format(torch.__version__))

# 1.data generation

# option : 정규화
std = 5
num_data = 1000

# noise
noise = init.normal( torch.FloatTensor(num_data,1),  std = std  )  #
print( "noise tensor = {}".format( noise ))

# x
x     = init.uniform( torch.Tensor(num_data,1),  a = -10,  b = 10 )
print( "value of x ={}".format( x ) )

# y
if True :
    y = -x ** 2 + noise
    y = y + noise
else :
    y = noise

print( type(x) )
print( x.size() )

p = scatter( x.numpy().reshape(-1), y.numpy().reshape(-1) )

# model construction
model = nn.Linear(1,1)

# loss function & optimizer
# Mean Squared Error loss
loss_func = nn.MSELoss()

# Stochastic Gradient Descent optimizer
optimizer = optim.SGD(model.parameters(),lr=0.01)

# define train function
def train(x, y, model, loss_func, optimizer, num_epoch):
    # output as Variable
    label = y
    # for given epochs
    for i in range(1, num_epoch + 1):
        # prediction
        output = model(x)
        # clears the gradients of all optimized
        optimizer.zero_grad()
        # compute loss
        loss = loss_func(output, label)
        # back-propagation
        loss.backward()
        # update model parameter
        optimizer.step()
        if i % 100  == 0: print('\r iter = {}, loss = {}'.format(i, loss.data.numpy()), end='')
        if i % 1000 == 0: print()
    return model, output

model, output = train( x, y, model, loss_func, optimizer, num_epoch=1000 )

print( type(output) )
print( type(output.data) )
print( output.data.size() )

# convert torch.Tensor to numpy.ndarray
output_numpy = output.data.numpy()
type(output_numpy)

output_numpy.shape
y_pred = output.data

p = scatter( x.numpy().reshape(-1), y_pred.numpy().reshape(-1) )
mscatter( p, x.numpy().reshape(-1), y.numpy().reshape(-1), fill_color='red' )

# model construction
# 그래프와 같은 것인 듯하다.
model = nn.Sequential(
    # 1st hidden layer
    nn.Linear(1,20),
    # 1st activation function
    nn.ReLU(),
    # 2nd hidden layer
    nn.Linear(20,5),
    # 2st activation function
    nn.ReLU(),
    # last hidden layer
    # output is 1-dim for prediction
    nn.Linear(5,1),
)



# loss function & optimizer
# L1 loss
loss_func = nn.L1Loss()

# Adam optimizer
optimizer = optim.Adam(model.parameters(),lr=0.001)

model, output = train(x, y, model, loss_func, optimizer, num_epoch=10000)
y_pred = output.data

p = scatter( x.numpy().reshape(-1), y_pred.numpy().reshape(-1))
mscatter( p, x.numpy().reshape(-1), y.numpy().reshape(-1), fill_color='red')
show(p)