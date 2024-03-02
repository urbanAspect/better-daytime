import numpy as np
from dted import Tile
import itertools

# Requires modified tile.py file from dted modulem
# Replacement file provided inside ./modified_files/tile.py



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

    def upscaleDem(array, Xtimes=1):
        array = array.repeat(3*Xtimes, axis=0).repeat(3*Xtimes, axis=1)
        print("Upscaling DEM file successful")
        return array

    def getPointElevation(latitude, longitude, path: str) -> float:
        tile = Tile(path, in_memory=False)
        return tile.get_elevation(latitude, longitude)

    # print(getPointElevation(46.474854, 15.672934, "../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2"))

    def mergeElevationData(*files) -> np.ndarray:
        class DEF:
            def __init__(self, file=None, elevationArray=None, latitude:int=None, longitude:int=None) -> None:
                if elevationArray is None:
                    self.elevationArray = demFile.readFile(file)
                    tile = Tile(file)
                    self.latitude = int(tile.dsi.south_west_corner.latitude)
                    self.longitude = int(tile.dsi.south_west_corner.longitude)
                elif file == None:
                    self.elevationArray = elevationArray
                    self.latitude = int(latitude)
                    self.longitude = int(longitude)
            
            def __eq__(self, other):
                if isinstance(other, DEF):
                    return (self.latitude, self.longitude) == (other.latitude, other.longitude)
                return False

            def __ne__(self, other):
                if isinstance(other, DEF):
                    return (self.latitude, self.longitude) != (other.latitude, other.longitude)
                return NotImplemented
            
            def __lt__(self, other):
                if isinstance(other, DEF):
                    if self.latitude == other.latitude:
                        return self.longitude < other.longitude
                    else:
                        return self.latitude < other.latitude
                return NotImplemented

            def __gt__(self, other):
                if isinstance(other, DEF):
                    if self.latitude == other.latitude:
                        return self.longitude > other.longitude
                    else:
                        return self.latitude > other.latitude
                return NotImplemented
            
            def __hash__(self):
                return hash((self.latitude, self.longitude))

        def createZerosArray(shape):
            missing_array = np.zeros_like(shape)
            return missing_array


        tiles = []

        # Convert files to arrays and extract SW coordinates
        # store DEF object in tiles array
        for file in files:
            if not isinstance(file, str):
                raise TypeError("All arguments must be of type 'str', provide valid path to .dt2 file")
            else:
                tiles.append(DEF(file=file))
            
        # Remove duplicate dem files
        unique_tiles = list(set(tiles))
        # Group files with the same latitude
        grouped_tiles = {}
        for tile in unique_tiles:
            if tile.latitude not in grouped_tiles:
                grouped_tiles[tile.latitude] = []
            grouped_tiles[tile.latitude].append(tile)

        # convert dictionary to array of touples
        grouped_tiles = list(grouped_tiles.items())

        # sort by latitude for easier access
        grouped_tiles.sort(key=lambda group: group[0])

        # Keep track of longitudes 
        observed_longitudes = {}

        for latitude, tiles_in_group in grouped_tiles:
            sorted_tiles = sorted(tiles_in_group, key=lambda x: x.longitude)
            print("Sorting latitude", latitude, "by longitude successful")
            
            observed_longitudes[latitude] = [tile.longitude for tile in sorted_tiles]
            print("Observed longitudes", observed_longitudes)

            prev_longitude = None
            for tile in sorted_tiles:
                print("latitude: ", tile.latitude, "   longitude: ", tile.longitude)
                if prev_longitude is not None and tile.longitude - prev_longitude > 1:
                    missing_longitude = prev_longitude + 1
                    print("Created missing longitude: ", missing_longitude)

                    # create array the same size as array in tile
                    missing_array = createZerosArray(tile.elevationArray)                    

                    new_tile = DEF(elevationArray=missing_array, latitude=latitude, longitude=missing_longitude)
                    print("New tile: ", new_tile)
                    tiles.append(new_tile)
                prev_longitude = tile.longitude

        # Iterate over observed longitudes to ensure consistency across all latitude groups
        for latitude, observed_longitude_list in observed_longitudes.items():
            min_observed_longitude = min(observed_longitude_list)
            max_observed_longitude = max(observed_longitude_list)
            for longitude in range(min_observed_longitude, max_observed_longitude):
                print("Longitude", longitude, "in latitude", latitude)
                if longitude not in observed_longitude_list:
                    print("Missing longitude 2nd try:", longitude - 1)
                    # Insert missing longitude into the group
                    tile_with_same_latitude = next(tile for tile in grouped_tiles if tile[0] == latitude)
                    shape_array = tile_with_same_latitude[1][0].elevationArray
                    missing_array = createZerosArray(shape_array)

                    missing_tile = DEF(elevationArray=missing_array, latitude=latitude, longitude=longitude)
                    tiles.append(missing_tile)



        # Sort tiles array and concatenate first inside groups, then groups themselves

        print("Tiles ", tiles)
        for tile in tiles:
            print(tile. latitude, tile.longitude)
        grouped_tiles = {}
        for tile in tiles:
            if tile.latitude not in grouped_tiles:
                grouped_tiles[tile.latitude] = []
            grouped_tiles[tile.latitude].append(tile)

        # convert dictionary to array of touples
        # grouped_tiles = list(grouped_tiles.items())

        # sort by latitude for easier access
        # grouped_tiles.sort(key=lambda group: group[0])

        print("Grouped Tiles ", grouped_tiles)
        for latitude in grouped_tiles:
            for tile in grouped_tiles[latitude]:
                print(tile.latitude, tile.longitude)
        
        return tiles

    # print(mergeElevationData("../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2", "../testdata/Copernicus_DSM_10_N46_00_E015_00_DEM.dt2"))

    def cropElevationData(data):
        return
