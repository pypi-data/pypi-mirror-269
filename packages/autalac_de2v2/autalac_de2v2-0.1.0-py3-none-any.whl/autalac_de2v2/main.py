import numpy as np

def transpose2d(input_matrix: list[list[float]]) -> list:
    """
    Transposes a 2D matrix.
    
    Parameters:
    - input_matrix (list of list of floats): A 2D list containing float elements.
    
    Returns:
    - list: The transposed 2D list.
    
    Raises:
    - ValueError: If the input_matrix is not a 2D list of floats.
    """
    if not all(isinstance(row, list) and all(isinstance(item, float) for item in row) for row in input_matrix):
        raise ValueError("input_matrix must be a 2D list of floats")

    num_rows = len(input_matrix)
    num_cols = len(input_matrix[0])

    transposed_matrix = [[0 for _ in range(num_rows)] for _ in range(num_cols)]

    for row in range(num_rows):
        for col in range(num_cols):
            transposed_matrix[col][row] = input_matrix[row][col]

    return transposed_matrix

def window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> list[list | np.ndarray]:
    """
    Generates sliding windows from a 1D list or numpy.ndarray.
    
    Parameters:
    - input_array (list or np.ndarray): The input 1D list or array.
    - size (int): The size of each window.
    - shift (int): The shift of the window for each step.
    - stride (int): The stride of elements within each window.
    
    Returns:
    - list: A list of windows, each window being a list or numpy.ndarray.
    
    Raises:
    - TypeError: If the input_array is not a list or numpy.ndarray.
    - ValueError: If size, shift, or stride are not positive integers.
    """
    if not isinstance(input_array, (list, np.ndarray)):
        raise TypeError("Input array must be either a list or a numpy.ndarray")
    if not (isinstance(size, int) and size > 0 and isinstance(shift, int) and shift > 0 and isinstance(stride, int) and stride > 0):
        raise ValueError("Size, shift, and stride must be positive integers")
    
    input_is_ndarray = isinstance(input_array, np.ndarray)
    windows = []
    i = 0
    
    while (i + size) <= len(input_array):
        window = input_array[i:i+size:stride]
        
        if input_is_ndarray:
            windows.append(np.array(window))
        else:
            windows.append(list(window))
        
        i += shift
    
    return windows

def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Performs a 2D convolution (actually cross-correlation) operation on a 2D input matrix with a given kernel.
    
    Parameters:
    - input_matrix: A 2D numpy array of real numbers.
    - kernel: A 2D numpy array (the convolution kernel).
    - stride: The stride of the convolution operation.
    
    Returns:
    - A 2D numpy array resulting from the convolution operation.
    
    Raises:
    - TypeError: If input or kernel are not numpy arrays.
    - ValueError: If stride is not a positive integer, or if the kernel's dimensions exceed the input's dimensions.
    """
    if not (isinstance(input_matrix, np.ndarray) and isinstance(kernel, np.ndarray)):
        raise TypeError("Input and kernel must be numpy arrays.")
    if not stride > 0:
        raise ValueError("Stride must be a positive integer.")
    
    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape
    
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1
    output_matrix = np.zeros((output_height, output_width))
    
    for y in range(0, output_height):
        for x in range(0, output_width):   
            current_region = input_matrix[
                y*stride:y*stride+kernel_height, 
                x*stride:x*stride+kernel_width
            ]
            output_matrix[y, x] = np.sum(current_region * kernel)
    
    return output_matrix

if __name__ == "__main__":
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
