import pandas as pd
from pyproj import Transformer

# Read CSV
df = pd.read_csv('validation.csv', encoding='ISO-8859-1')

# Set up the transformer
transformer = Transformer.from_crs("EPSG:27700", "EPSG:4326")

# Function to apply the transformation
def transform_coordinates(row):
    lat, lon = transformer.transform(row['X-coordinate'], row['Y-coordinate'])
    return pd.Series([lat, lon], index=['lat', 'lon'])

# Apply the transformation to the DataFrame
df[['lat', 'lon']] = df.apply(transform_coordinates, axis=1)

# Save to a new CSV file
df.to_csv('updated_validation.csv', index=False, float_format='%g')
