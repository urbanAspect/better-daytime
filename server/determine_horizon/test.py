from DEM_operations import demFile
import numpy as np

# array1 = demFile.readFile("../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2")
# # array2 = demFile.readFile("../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2")
# # array3 = demFile.readFile("../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2")
# print(array1)
# print(array1.dtype)

# def createZerosArray(shape):
#             missing_array = np.zeros_like(shape)
#             return missing_array

# z = createZerosArray(array1)
# print(z)
# print(z.dtype)


merged_data = demFile.mergeElevationData("../testdata/Copernicus_DSM_10_N45_00_E015_00_DEM.dt2", "../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2", "../testdata/Copernicus_DSM_10_N45_00_E013_00_DEM.dt2", "../testdata/Copernicus_DSM_10_N46_00_E014_00_DEM.dt2")





