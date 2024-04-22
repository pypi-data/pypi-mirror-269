The Data Transformation Libraries package contains three modules:<br>
transpose<br>
time_series_windowing<br>
cross_correlation<br>

### transpose
The transpose module includes the "transpose2d" function, which switches the axes of a 2D tensor.<br>
Transpose function has signature: **transpose2d(input_matrix: list[list[float]]) -> list**<br>
### time_series_windowing
The time_series_windowing module includes the "window1d" function for time series windowing.<br>
Time series windowing function has signature: **window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> list[list | np.ndarray]**<br>
### cross_correlation
The cross_correlation module includes the "convolution2d" function for cross-correlation.<br>
Cross correlation function has signature: **convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride : int = 1) -> np.ndarray**<br>