import numpy as np
import h5py
import os

arr = np.random.randn(1000)
print(arr)

# with h5py.File("data_processing/test.hdf5", "w") as file:
#     dset = file.create_dataset("default", data = arr)


        