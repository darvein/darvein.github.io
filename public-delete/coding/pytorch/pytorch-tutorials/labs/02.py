import torch
import numpy as np

def create_tensor():
    # From Torch
    data = [[1, 2], [3, 4]]
    x_data = torch.tensor(data)

    # From Numpy
    np_array = np.array(data)
    x_np = torch.from_numpy(np_array)

    print(x_data)
    print(x_np)

##################################################
# Replacing the data without affecting the tensor props
##################################################
def replace_tensor_data():
    x_data = torch.tensor([[1, 2], [3, 4]])

    x_ones = torch.ones_like(x_data) # with 1s
    print(f"Ones Tensor: \n {x_ones} \n")

    x_rand = torch.rand_like(x_data, dtype=torch.float) # with random numbers
    print(f"Random Tensor: \n {x_rand} \n")


##################################################
# 2 Tensors of 3x5 with random, ones and zeros data
##################################################
def create_tensor_random_data():
    shape = (2,3,5)
    rand_tensor = torch.rand(shape)
    ones_tensor = torch.ones(shape)
    zeros_tensor = torch.zeros(shape)

    print(f"Random Tensor: \n {rand_tensor} \n")
    print(f"Ones Tensor: \n {ones_tensor} \n")
    print(f"Zeros Tensor: \n {zeros_tensor}")

def tensor_properties():
    device = "cuda" if torch.cuda.is_available() else "cpu" # GPU or CPU

    tensor = torch.rand(3,4).to(device)
    print(f"Shape of tensor: {tensor.shape}")
    print(f"Datatype of tensor: {tensor.dtype}")
    print(f"Device tensor is stored on: {tensor.device}")

def tensor_slicing():
    tensor = torch.ones(4, 4)

    if torch.cuda.is_available():
        tensor = tensor.to("cuda")

    print(f"First row: {tensor[0]}")
    print(f"First column: {tensor[:, 0]}")
    print(f"Last column: {tensor[..., -1]}")

    tensor[:, 1] = 2
    print(tensor)

    print("Joining tensors: {}".format(torch.cat([tensor, tensor, tensor], dim=1)))

#create_tensor()
#replace_tensor_data()
#create_tensor_random_data()
#tensor_properties()
#tensor_slicing()
