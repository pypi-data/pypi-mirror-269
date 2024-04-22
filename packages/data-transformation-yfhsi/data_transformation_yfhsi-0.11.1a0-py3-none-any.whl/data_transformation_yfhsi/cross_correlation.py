import numpy as np
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def convolution2d(
    input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1
) -> np.ndarray:
    """
    The cross correlation function between a 2D input matrix and a 2D kernel.

    Parameters:
        input_matrix (np.ndarray): The input 2D matrix.
        kernel (np.ndarray): The 2D convolution kernel.
        stride (int): The stride of the convolution operation. Default is 1.

    Returns:
        np.ndarray: The result of the 2D convolution operation.
    """
    try:

        def matrix_verification(matrix):
            if np.array(matrix).ndim == 2:
                if isinstance(matrix, np.ndarray):
                    for row in matrix:
                        if not all(
                            isinstance(
                                item, (np.int32, np.float64)) for item in row
                        ):
                            raise ValueError(
                                f"All '{matrix}' matrix "
                                + "items must be real numbers."
                            )
                else:
                    raise ValueError(
                        f"Submitted '{matrix}' matrix is not np.ndarray."
                        )
            else:
                raise ValueError(f"Submitted '{matrix}' matrix is not 2D.")

        matrix_verification(input_matrix)
        matrix_verification(kernel)

        if isinstance(stride, int):
            """
            The function verifies if variables are positive integer numbers.
            """
            if not stride > 0:
                raise ValueError("Variable stride must be positive number.")
        else:
            raise ValueError("Variable stride must be integer number.")

        matrix_rows, matrix_columns = len(input_matrix), len(input_matrix[0])
        kernel_rows, kernel_columns = len(kernel), len(kernel[0])
        width, height = (
            ((matrix_rows - kernel_rows) // stride) + 1,
            ((matrix_columns - kernel_columns) // stride) + 1,
        )

        output_matrix = np.zeros((width, height))
        for column in range(0, height):
            for row in range(0, width):
                window = input_matrix[
                    row:row + kernel_rows, column:column + kernel_columns
                ]
                value = np.sum(window * kernel)
                output_matrix[row, column] = value

        return output_matrix

    except Exception as error:
        logging.error(error)
