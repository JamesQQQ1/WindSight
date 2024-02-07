import pandas as pd
from pyproj import Proj, transform

# Load the Excel file
excel_path = '/Users/jamesquessy/Desktop/wind_farm.xlsx'  # Replace with the path to your Excel file
df = pd.read_excel(excel_path)

# Filter the data to only include rows where 'Technology Type' is not 'Wind Onshore'
# and 'Country' is 'Scotland'
filtered_df = df[(df['Technology Type'] == 'Wind Onshore') & (df['Country'] == 'Scotland') & (df['Development Status'] == 'Operational') & (df['Development Status (short)'] == 'Operational')]

# Save the filtered data to a new Excel file
output_path = '/Users/jamesquessy/Desktop/Scottish_wind_farms.xlsx'  # Replace with the path where you want to save the new file
filtered_df.to_excel(output_path, index=False)

def bng_to_latlon(easting, northing):
    # British National Grid Projection
    bng_proj = Proj('epsg:27700')
    
    # WGS84 Projection
    wgs84_proj = Proj('epsg:4326')
    
    # Convert the BNG coordinates to WGS84
    lon, lat = transform(bng_proj, wgs84_proj, easting, northing)
    return lat, lon

# Load the Excel file
excel_path = '/Users/jamesquessy/Desktop/Scottish_wind_farms.xlsx'  # Update with the path to your Excel file
df = pd.read_excel(excel_path, engine='openpyxl')

# Apply the conversion function to each row and create new columns for Latitude and Longitude
df['Latitude'], df['Longitude'] = zip(*df.apply(lambda x: bng_to_latlon(x['X-coordinate'], x['Y-coordinate']), axis=1))

# Save the DataFrame with the new columns to a new Excel file
output_path = '/Users/jamesquessy/Desktop/Scottish_wind_farms_with_lat_lon.xlsx'  # Update with your desired output file path
df.to_excel(output_path, index=False, engine='openpyxl')
