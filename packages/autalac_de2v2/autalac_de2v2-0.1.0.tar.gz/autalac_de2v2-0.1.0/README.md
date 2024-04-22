# Python Matrix and Array Manipulations Library

This Python library, developed as a proof of concept (POC) at a large software company, provides essential data transformation functionalities for data scientists. The library includes operations for matrix transposition, time series windowing, and 2D convolution, all crucial for preparing data used in machine learning models.
## Overview

You are working as a data engineer tasked with building this library to aid in data transformation tasks commonly encountered in data science workflows. This document details the initial sprint of the library, which involves the development of three key functions.
## Features
1. Matrix Transposition
    - Function: transpose2d(input_matrix)
    - Description: This function transposes a 2D matrix (2d tensor), an essentialoperation in data science for reorienting data.
    - Usage: Transpose the axes of a matrix to rearrange data, making it suitablefor various algorithms that require specific data orientations.
    - Learn More: numpy.transpose

2. Time Series Windowing
    - Function: window1d(input_array, size, shift=1, stride=1)
    - Description: Generates sliding windows from a 1D list or numpy.ndarray, - valuable for time series analysis and modeling.
    - Usage: Extract features or patterns from time series data by analyzing - segments of the dataset.
    - Learn More: tf.data.Dataset.window

3. 2D Convolution (Cross-Correlation)
    - Function: convolution2d(input_matrix, kernel, stride=1)
    - Description: Performs a 2D convolution operation (technically - cross-correlation), a cornerstone in neural network architectures like CNNs.
    - Usage: Apply filters to images or other two-dimensional data to extract - features or apply effects.
    - Learn More: torch.nn.functional.conv2d

## Installation

To use this library, install it via pip:

```bash
pip install autalac-de2v2-1-5
```
## Usage

Here are some examples of how to use the functions in this library:

```python
import numpy as np
from autalac-de2v2-1-5 import transpose2d, window1d, convolution2d

# Transposes a 2D matrix.
input_matrix_t2d = [
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0]
]

transposed = transpose2d(input_matrix_t2d)
print("\nOriginal matrix:")
for row in input_matrix_t2d:
    print(row)
print("Transposed matrix:")
for row in transposed:
    print(row)

# Generates sliding windows from a 1D list or numpy.ndarray.
input_list_w1d = [11, 52, 63, 42, 5, 64, 79, 8, 29, 10]
print("\nList input example:")
for window in window1d(input_list_w1d, size=3, shift=3, stride=1):
    print(window)

input_array_w1d = np.arange(1, 15)
print("Numpy array input example:")
for window in window1d(input_array_w1d, size=4, shift=4, stride=1):
    print(window)


#     Performs a 2D convolution (actually cross-correlation) operation on a 2D input matrix with a given kernel.
input_matrix_2d_con = np.array([
    [1, 6, 2],
    [5, 3, 1],
    [7, 0, 4]
])

kernel_2d_con = np.array([
    [1, 2],
    [-1, 0]
])
print("\nFunction convolution2d input_matrix")
for row3 in input_matrix_2d_con:
    print(row3)
print("Function convolution2d kernel")
for row4 in kernel_2d_con:
    print(row4)
output_matrix = convolution2d(input_matrix_2d_con, kernel_2d_con, stride=1)
print("Function convolution2d example")
for row5 in output_matrix:
    print(row5)
```