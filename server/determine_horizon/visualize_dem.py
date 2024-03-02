from DEM_operations import demFile
import numpy as np
import matplotlib.pyplot as plt


def adjustGrayscale(array: np.ndarray):
    print("Passed min: ", min, " Passed max: ", max)
    # find min and max in array and reduce max for value of min
    nullifiedMax =  np.max(array) - np.min(array)
    # set lowest value in array as 0 and remap standard deviation on scale [0, 255]
    grayvalueArray = int(((array - min) * 255) / nullifiedMax)
    return grayvalueArray


array = demFile.readFile("../testdata/Copernicus_DSM_10_N00_00_E020_00_DEM.dt2")
merged_data = demFile.mergeElevationData("../testdata/Copernicus_DSM_10_N45_00_E015_00_DEM.dt2", "../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2", "../testdata/Copernicus_DSM_10_N45_00_E013_00_DEM.dt2", "../testdata/Copernicus_DSM_10_N46_00_E014_00_DEM.dt2")
# 

plt.imshow(np.rot90(merged_data, axes=(0, 1)), cmap='gray_r', interpolation='nearest')
plt.colorbar()
plt.show()