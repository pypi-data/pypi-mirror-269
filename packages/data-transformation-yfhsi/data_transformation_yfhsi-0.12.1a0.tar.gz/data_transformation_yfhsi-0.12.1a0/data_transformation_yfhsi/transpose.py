import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def transpose2d(input_matrix: list[list[float]]) -> list:
    """
    The transpose function for a 2D matrix.

    Parameters:
        input_matrix (list[list[float]]): The input 2D matrix to be transposed.

    Returns:
        list: The transposed 2D matrix.
    """
    try:
        if all(isinstance(row, list) for row in input_matrix):
            for row in range(len(input_matrix)):
                if len(input_matrix[0]) != len(input_matrix[row]):
                    raise ValueError("The matrix has an inhomogeneous shape.")
            for row in input_matrix:
                if not all(isinstance(item, float) for item in row):
                    raise ValueError(
                        "All matrix items must be floating-point numbers."
                    )
        else:
            raise ValueError("Submitted matrix is not 2D.")

        transposed_matrix = []
        for column_index in range(len(input_matrix[0])):
            column = [row[column_index] for row in input_matrix]
            transposed_matrix.append(column)

        return transposed_matrix

    except Exception as error:
        logging.error(error)
