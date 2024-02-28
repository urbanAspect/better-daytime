import numpy as np
from pathlib import Path
from dted import Tile

def readDemFile(path):
    tile = Tile(path)
    assert isinstance(tile.data, np.ndarray)
    print("Reading dt2 file successful")
    return tile.data

print(readDemFile("../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2").__class__)

def mergeElevationData(file1, file2):
    if isinstance(file1, Tile) and isinstance(file2, Tile):
        coordF1 = file1.dsi.south_west_corner
        coordF2 = file2.dsi.south_west_corner

        if coordF1.longitude == coordF2.longitude:
            if coordF1.latitude > coordF2.latitude:
                merged_array = np.concatenate((coordF1, coordF2), axis=0)
                print("Vertical merging successful")
                return merged_array
            elif coordF1.latitude < coordF1.latitude:
                merged_array = np.concatenate((coordF2, coordF1), axis=0)
                print("Vertical merging successful")
                return merged_array
            else:
                print("Can not merge 2 files of the same area. Files have the same latitude and longitude of the SW corner.")
                return 0
        elif coordF1.latitude == coordF2.latitude:
            if coordF1.longitude < coordF2.longitude:
                merged_array = np.concatenate((coordF1, coordF2), axis=1)
                print("Horizontal merging successful")
                return merged_array
            elif coordF1.latitude > coordF1.latitude:
                merged_array = np.concatenate((coordF2, coordF1), axis=1)
                print("Vertical merging successful")
                return merged_array
            else:
                print("Can not merge 2 files of the same area. Files have the same latitude and longitude of the SW corner.")
                return 0
    else:
        print("Can not merge data. Provided files are not class Tile. Check back to readDemFile.")
        return 0


print
print(mergeElevationData(readDemFile("../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2"), readDemFile("../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2")))