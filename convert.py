import pandas as pd
from pyproj import Transformer
from geopy.distance import geodesic

# Function to convert BNG (British National Grid) coordinates to WGS84 (lat/lon)
def bng_to_latlon(easting, northing):
    transformer = Transformer.from_crs("epsg:27700", "epsg:4326", always_xy=True)
    lon, lat = transformer.transform(easting, northing)
    return lat, lon

# Function to calculate distance between two lat/lon coordinates
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

# Replace with the actual path to your Excel file containing wind farm data
wind_farm_path = '/Users/jamesquessy/Desktop/Uni Work/Masters/Reasearch Project/Code/RCP_4.5/Validation/Scottish_wind_farms_with_lat_lon.xlsx'
# Replace with the actual path to your Excel file containing model output data
model_output_path = '/Users/jamesquessy/Desktop/Uni Work/Masters/Reasearch Project/Code/RCP_4.5/Validation/model_output.xlsx'


# Load your data
wind_farm_data = pd.read_excel(wind_farm_path, engine='openpyxl')
model_output_data = pd.read_excel(model_output_path, engine='openpyxl')

# Check if Latitude and Longitude columns are missing in wind_farm_data
if 'Latitude' not in wind_farm_data or 'Longitude' not in wind_farm_data:
    wind_farm_data['Latitude'], wind_farm_data['Longitude'] = zip(*wind_farm_data.apply(
        lambda x: bng_to_latlon(x['X-coordinate'], x['Y-coordinate']), axis=1))

# Find the closest wind farm for each entry in the model output data
closest_wind_farms = []
distances_to_closest = []

# Assuming 'Best_Lat', 'Best_Lon' columns are present in your model output data
for index, model_row in model_output_data.iterrows():
    # Calculate all distances from the model point to each wind farm
    distances = wind_farm_data.apply(
        lambda x: calculate_distance(x['Latitude'], x['Longitude'], model_row['Best_Lat'], model_row['Best_Lon']),
        axis=1
    )
    # Find the minimum distance and the corresponding wind farm
    min_distance = distances.min()
    closest_wind_farm = wind_farm_data.loc[distances.idxmin(), 'Site Name']
    
    # Append the results to the lists
    closest_wind_farms.append(closest_wind_farm)
    distances_to_closest.append(min_distance)

# Add the results to the model output DataFrame
model_output_data['Closest Wind Farm'] = closest_wind_farms
model_output_data['Distance to Closest Wind Farm (km)'] = distances_to_closest

# Save the updated model output data to a new Excel file
output_path = '/Users/jamesquessy/Desktop/Uni Work/Masters/Reasearch Project/Code/RCP_4.5/Validation/val_output.csv'
model_output_data.to_excel(output_path, index=False, engine='openpyxl')
