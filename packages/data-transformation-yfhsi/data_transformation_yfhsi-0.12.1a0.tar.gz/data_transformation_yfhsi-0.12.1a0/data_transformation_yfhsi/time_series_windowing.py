import numpy as np
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def window1d(
    input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1
) -> list[list | np.ndarray]:
    """
    The time series windowing function for 1D matrix or numpy array.

    Parameters:
        input_array (list | np.ndarray): The input 1D array or numpy array.
        size (int): The size of the sliding window.
        shift (int): The amount to shift the window by for each step.
        Default is 1.
        stride (int): The stride of the window.
        Default is 1.

    Returns:
        list[list | np.ndarray]: A list of windows,
        each containing elements from the input array.
    """
    try:
        if np.array(input_array).ndim == 1:
            if isinstance(input_array, list) or isinstance(input_array,
                                                           np.ndarray):
                if not all(
                    isinstance(item, (float, int, np.int32, np.float64))
                    for item in input_array
                ):
                    raise ValueError("All matrix items must be real numbers.")
            else:
                raise ValueError("Submitted matrix is not list or np.ndarray.")
        else:
            raise ValueError("Submitted matrix is not 1D.")

        def variables_verification(variable):
            """
            The function verifies if variables are positive numbers.
            """
            if isinstance(variable, int):
                if not variable > 0:
                    raise ValueError(
                        "Variables size, shift and stride"
                        + " must be positive numbers."
                    )
            else:
                raise ValueError(
                    "Variables size, shift and stride must be integer numbers."
                )

        variables_verification(size)
        variables_verification(shift)
        variables_verification(stride)

        windows = []
        for index in range(0, len(input_array), shift):
            window = input_array[index:index + size * stride:stride]
            if len(window) == size:
                windows.append(window)

        return windows

    except Exception as error:
        logging.error(error)
