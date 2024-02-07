# Importing Required Libraries
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin
import os
import numpy as np
import xarray as xr
import pandas as pd
from netCDF4 import Dataset
import rioxarray

# Directory Setup
base_directory = '/Users/jamesquessy/Developer/Projects/Masters/Data/Raster_Data'
shape_file_directory = os.path.join(base_directory, 'Raw_Data')
airport_file_directory = os.path.join(base_directory, 'Raw_Data')

# Ensure that the necessary directories exist
os.makedirs(shape_file_directory, exist_ok=True)
os.makedirs(airport_file_directory, exist_ok=True)

# NSA Mask Creation

# Rasterising the NSA Shapefile
nsa_shapefile_path = os.path.join(shape_file_directory, 'National_Scenic_Areas_-_Scotland.shp')
shapes = gpd.read_file(nsa_shapefile_path)
resolution = 0.1  # Raster resolution in degrees.
left, bottom, right, top = (-44.5, 22.05, 64.9, 72.55)  # Geographic bounds for the raster.
rows = int((top - bottom) / resolution)  # Number of rows in the raster.
cols = int((right - left) / resolution)  # Number of columns in the raster.
transform = from_origin(left, top, resolution, resolution)  # Transformation for the raster.
nsa_raster_output_path = os.path.join(shape_file_directory, 'nsa_raster.tif')  # Output path for the raster file.
out_shape = (rows, cols)  # Shape of the output raster.

# Define metadata for the output raster file.
out_meta = {
    "driver": "GTiff",
    "height": out_shape[0],
    "width": out_shape[1],
    "transform": transform,
    "crs": 'EPSG:4326',
    "dtype": 'uint8',
    "nodata": 0,
    "count": 1
}

# Rasterising the shapefile
with rasterio.open(nsa_raster_output_path, 'w', **out_meta) as out_raster:
    out_raster.write_band(1, rasterize(
        [(geometry, 1) for geometry in shapes.geometry],
        out_shape=out_shape,
        transform=transform,
        fill=0,
        all_touched=True
    ))

# Converting Raster to NetCDF for NSA
with rasterio.open(nsa_raster_output_path) as src:
    raster_data = src.read(1)
    transform = src.transform
    crs = src.crs

    lon = np.arange(transform[2], transform[2] + transform[0] * raster_data.shape[1], transform[0])
    lat = np.arange(transform[5], transform[5] + transform[4] * raster_data.shape[0], transform[4])
    if lat[0] > lat[-1]:
        lat = lat[::-1]
        raster_data = raster_data[::-1, :]

    nsa_raster_da = xr.DataArray(
        data=raster_data,
        dims=('lat', 'lon'),
        coords={'lon': lon, 'lat': lat},
        name='mask'
    )

    nsa_raster_ds = xr.Dataset({'mask': nsa_raster_da})
    nsa_raster_ds.rio.write_crs(crs.to_string(), inplace=True)

    nsa_netcdf_output_path = os.path.join(shape_file_directory, 'nsa_raster_NetCDF.nc')
    nsa_raster_ds.to_netcdf(nsa_netcdf_output_path)
    print(f'NSA raster data has been saved to NetCDF file at: {nsa_netcdf_output_path}')

# Speical Protetion Area Mask Creation

# Rasterising the NSA Shapefile
spa_shapefile_path = os.path.join(shape_file_directory, 'Special_Protection_Areas.shp')
shapes = gpd.read_file(spa_shapefile_path)
resolution = 0.1  # Raster resolution in degrees.
left, bottom, right, top = (-44.5, 22.05, 64.9, 72.55)  # Geographic bounds for the raster.
rows = int((top - bottom) / resolution)  # Number of rows in the raster.
cols = int((right - left) / resolution)  # Number of columns in the raster.
transform = from_origin(left, top, resolution, resolution)  # Transformation for the raster.
spa_raster_output_path = os.path.join(shape_file_directory, 'spa_raster.tif')  # Output path for the raster file.
out_shape = (rows, cols)  # Shape of the output raster.

# Define metadata for the output raster file.
out_meta = {
    "driver": "GTiff",
    "height": out_shape[0],
    "width": out_shape[1],
    "transform": transform,
    "crs": 'EPSG:4326',
    "dtype": 'uint8',
    "nodata": 0,
    "count": 1
}

# Rasterising the shapefile
with rasterio.open(nsa_raster_output_path, 'w', **out_meta) as out_raster:
    out_raster.write_band(1, rasterize(
        [(geometry, 1) for geometry in shapes.geometry],
        out_shape=out_shape,
        transform=transform,
        fill=0,
        all_touched=True
    ))

# Converting Raster to NetCDF for NSA
with rasterio.open(nsa_raster_output_path) as src:
    raster_data = src.read(1)
    transform = src.transform
    crs = src.crs

    lon = np.arange(transform[2], transform[2] + transform[0] * raster_data.shape[1], transform[0])
    lat = np.arange(transform[5], transform[5] + transform[4] * raster_data.shape[0], transform[4])
    if lat[0] > lat[-1]:
        lat = lat[::-1]
        raster_data = raster_data[::-1, :]

    spa_raster_da = xr.DataArray(
        data=raster_data,
        dims=('lat', 'lon'),
        coords={'lon': lon, 'lat': lat},
        name='mask'
    )

    spa_raster_ds = xr.Dataset({'mask': spa_raster_da})
    spa_raster_ds.rio.write_crs(crs.to_string(), inplace=True)

    spa_netcdf_output_path = os.path.join(shape_file_directory, 'spa_raster_NetCDF.nc')
    spa_raster_ds.to_netcdf(spa_netcdf_output_path)
    print(f'SPA raster data has been saved to NetCDF file at: {nsa_netcdf_output_path}')

# Airport Mask Creation

# Adjusting Latitudes and Longitudes to Grid Points
def round_to_grid(value, grid_start, increment):
    increments_from_start = (value - grid_start) / increment
    rounded_increments = round(increments_from_start)
    return grid_start + (rounded_increments * increment)

def adjust_to_grid(csv_filepath):
    df = pd.read_csv(csv_filepath)
    df['Latitude'] = df['latitude_deg'].apply(lambda x: round_to_grid(x, 22.05, 0.1))
    df['Longitude'] = df['longitude_deg'].apply(lambda x: round_to_grid(x, -44.5, 0.1))
    df.drop(['latitude_deg', 'longitude_deg'], axis=1, inplace=True)
    return df[['ident', 'name', 'Latitude', 'Longitude']]

# Processing CSV file and creating airport mask
csv_filepath = os.path.join(airport_file_directory, 'scotland_airports.csv')
adjusted_df = adjust_to_grid(csv_filepath)
airports_directory = os.path.join(airport_file_directory)
adjusted_df.to_excel(os.path.join(airports_directory, 'scotland_airports_grid.xlsx'), index=False)

excel_file = os.path.join(airports_directory, 'scotland_airports_grid.xlsx')
airports_df = pd.read_excel(excel_file)

# Define the grid boundaries and step size for the airport mask
min_lat, max_lat, step_lat = 22.05, 72.55, 0.1
min_lon, max_lon, step_lon = -44.5, 64.9, 0.1

# Calculate the size of the grid
lat_size = int((max_lat - min_lat) / step_lat) + 1
lon_size = int((max_lon - min_lon) / step_lon) + 1

# Now you can create the airport_array with the defined size
airport_array = np.zeros((lat_size, lon_size))


# Creating the airport mask in a new NetCDF file
airport_array = np.zeros((lat_size, lon_size))

for _, row in airports_df.iterrows():
    lat, lon = row['Latitude'], row['Longitude']
    lat_idx = int((lat - min_lat) / step_lat)
    lon_idx = int((lon - min_lon) / step_lon)

    if 0 <= lat_idx < lat_size and 0 <= lon_idx < lon_size:
        airport_array[lat_idx, lon_idx] = 1

new_netcdf_file = os.path.join(airport_file_directory, "airport_mask.nc")

with Dataset(new_netcdf_file, 'w') as new_nc:
    new_nc.createDimension('lat', lat_size)
    new_nc.createDimension('lon', lon_size)

    latitudes = new_nc.createVariable('latitude', np.float32, ('lat',))
    longitudes = new_nc.createVariable('longitude', np.float32, ('lon',))
    latitudes[:] = np.linspace(min_lat, max_lat, lat_size)
    longitudes[:] = np.linspace(min_lon, max_lon, lon_size)

    airport_var = new_nc.createVariable('airport', airport_array.dtype, ('lat', 'lon'))
    airport_var[:] = airport_array
    airport_var.units = '1 if airport exists else 0'
    airport_var.long_name = 'Airport grid presence'

print("Rasterization and conversion to NetCDF for NSA, SPA, and airport mask completed.")
