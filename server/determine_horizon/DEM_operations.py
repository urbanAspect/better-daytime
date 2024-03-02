import numpy as np
from dted import Tile
import itertools

# Requires modified tile.py file in dted module
# Replacement file provided here: ./modified_files/tile.py



class demMetadata:
    def __init__(self, path) -> None:
        self.compilationDate = Tile(path).dsi.compilation_date
        self.latResolution = Tile(path).dsi.latitude_interval
        self.longResolution = Tile(path).dsi.longitude_interval


class demFile:
    def readFile(path) -> np.ndarray:
        tile = Tile(path)
        assert isinstance(tile.data, np.ndarray)
        print("Reading %s at coordinates"%(path.rpartition("/")[2]), int(tile.dsi.south_west_corner.latitude), int(tile.dsi.south_west_corner.longitude), "successful")
        return tile.data

    def upscaleDem(array, Xtimes=3):
        array = array.repeat(Xtimes, axis=0).repeat(Xtimes, axis=1)
        print("Upscaling DEM file successful")
        return array

    def getPointElevation(latitude, longitude, path: str) -> float:
        tile = Tile(path, in_memory=False)
        return tile.get_elevation(latitude, longitude)

    # print(getPointElevation(46.474854, 15.672934, "../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2"))

    def mergeElevationData(*files) -> np.ndarray:
        class DEF:
            def __init__(self, file=None, elevationArray=None, latitude:int=None, longitude:int=None) -> None:
                if elevationArray is None and latitude is None and longitude is None:
                    # correctly oriented array from dem file
                    self.elevationArray = np.rot90(demFile.readFile(file), axes=(0, 1))
                    tile = Tile(file)
                    self.latitude = int(tile.dsi.south_west_corner.latitude)
                    self.longitude = int(tile.dsi.south_west_corner.longitude)
                if file != None and elevationArray == None and latitude != None and longitude != None:
                    self.elevationArray = demFile.readFile(file)
                    self.latitude = int(latitude)
                    self.longitude = int(longitude)
                elif file == None:
                    self.elevationArray = elevationArray
                    self.latitude = int(latitude)
                    self.longitude = int(longitude)
            
            def __hash__(self):
                return hash((self.latitude, self.longitude))

        def createZerosArray(shape):
            missing_array = np.zeros_like(shape)
            return missing_array

        def groupByLatitude(array) -> dict:
            grouped_tiles = {}
            for tile in array:
                if tile.latitude not in grouped_tiles:
                    grouped_tiles[tile.latitude] = []
                grouped_tiles[tile.latitude].append(tile)
            return grouped_tiles

        def sortByLongitude(arrayGroupedByLatitude) -> list:
            for latitude in arrayGroupedByLatitude:
                arrayGroupedByLatitude[latitude] = sorted(arrayGroupedByLatitude[latitude], key=lambda tile: tile.longitude)
            return arrayGroupedByLatitude # return list of sorted arrays

        def findUniqueLongitudes(arrayGroupedByLatitude) -> list:
            observed_longitudes = []
            for latitude, tiles_on_latitude in arrayGroupedByLatitude:
                # sorted_tiles = sorted(tiles_in_group, key=lambda x: x.longitude)
                print("Sorting latitude", latitude, "by longitude successful")
                for tile in tiles_on_latitude:
                    observed_longitudes.append(tile.longitude)
            unique_longitudes = list(set(observed_longitudes))
            print("unique longitudes:", unique_longitudes)
            return unique_longitudes
        
        def generateMissingArrays(holedArray):
            unique_longitudes = findUniqueLongitudes(holedArray)
            for latitude, tiles_in_group in holedArray:
                for longitude in unique_longitudes:
                    if not any(tile.longitude == longitude for tile in tiles_in_group):
                        print("        Missing longitude:", longitude, "in latitude", latitude)
                        # Insert missing longitude into the group
                        tile_with_same_latitude = next(tile for tile in holedArray if tile[0] == latitude)
                        shape_array = tile_with_same_latitude[1][0].elevationArray
                        missing_tile = DEF(elevationArray=createZerosArray(shape_array), latitude=latitude, longitude=longitude)
                        TILES.append(missing_tile)

        def concatenateTiles(array) -> np.ndarray:
            array = [v for k, v in array.items()]
            mergedArray = []
            for row in array:
                mergedArray.append(np.concatenate(([tile.elevationArray for tile in row]), axis=1))
            mergedArray.reverse()
            mergedArray = np.concatenate((mergedArray), axis=0)
            return mergedArray

        TILES = []

        # Convert files to arrays and extract SW coordinates
        # store DEF object in TILES array
        for file in files:
            if not isinstance(file, str):
                raise TypeError("All arguments must be of type 'str', provide valid path to .dt2 file")
            else:
                TILES.append(DEF(file=file))
                
            
        # Remove duplicate dem files
        unique_tiles = list(set(TILES))
        grouped_tiles = groupByLatitude(unique_tiles)

        # convert dictionary to array of touples
        grouped_tiles = list(grouped_tiles.items())

        # sort by latitude
        grouped_tiles.sort(key=lambda group: group[0])

        # Ensure there is the same number of DEM file arrays in every row of the matrix
        # to ensure np.concatenate can merge arrays successfully
        generateMissingArrays(grouped_tiles)

        # Sort TILES array
        grouped_tiles = sortByLongitude(groupByLatitude(TILES))

        # concatenate horizontally (inside groups), then vertically (groups themselves)
        return concatenateTiles(grouped_tiles)

    # print(mergeElevationData("../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2", "../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2"))

    def cropElevationData(data):
        return
