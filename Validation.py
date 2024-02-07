import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from geopy.distance import geodesic

def process_and_plot_model_output(model_output_filename, existing_farms_gdf, compiled_data):
    # Load the model output
    model_output_df = pd.read_excel(model_output_filename)

    # Convert DataFrame to GeoDataFrame
    gdf_model_output = gpd.GeoDataFrame(model_output_df, geometry=gpd.points_from_xy(model_output_df['Best_Lon'], model_output_df['Best_Lat']))

    # Initialize columns with appropriate data types
    gdf_model_output['Closest_Existing_Wind_Farm'] = pd.Series(dtype=object)
    gdf_model_output['Distance_km'] = pd.Series(dtype=float)

    # Calculate the distance to the closest existing wind farm using geodesic distances
    closest_farms_per_year = {}

    for index, predicted_location in gdf_model_output.iterrows():
        predicted_point = (predicted_location['Best_Lat'], predicted_location['Best_Lon'])
        min_distance = float('inf')
        closest_farm_name = None

        for _, farm in existing_farms_gdf.iterrows():
            farm_point = (farm['Latitude'], farm['Longitude'])
            distance = geodesic(predicted_point, farm_point).kilometers

            if distance < min_distance:
                min_distance = distance
                closest_farm_name = farm['Site Name']

        gdf_model_output.at[index, 'Closest_Existing_Wind_Farm'] = closest_farm_name
        gdf_model_output.at[index, 'Distance_km'] = min_distance

        year = predicted_location['Year']
        if year not in closest_farms_per_year or min_distance < closest_farms_per_year[year][1]:
            closest_farms_per_year[year] = (closest_farm_name, min_distance)

    # Group by 'Year' to get the average nearest distance per year
    yearly_distances = gdf_model_output.groupby('Year')['Distance_km'].mean().reset_index()
    
    # Print the closest wind farm for each year to the terminal
    for year, (farm_name, distance) in closest_farms_per_year.items():
        print(f"Year {year}: Closest Wind Farm is '{farm_name}' at {distance:.2f} km")
        
    # Add data to the compiled DataFrame
    for year, (farm_name, distance) in closest_farms_per_year.items():
        compiled_data.append({'Model': model_output_filename, 'Year': year, 'Closest_Wind_Farm': farm_name, 'Average_Distance_km': distance})

    # Set up the figure for the plot
    plt.figure(figsize=(10, 6), dpi=300)  # High resolution for publication

    # Create bars for each year
    bars = plt.bar(yearly_distances['Year'].astype(str), yearly_distances['Distance_km'], color='skyblue', edgecolor='grey', width=0.6)

    # Add labels and title
    plt.xlabel('Year', fontweight='bold', fontsize=12)
    plt.ylabel('Average Distance (km)', fontweight='bold', fontsize=12)
    plot_title = f'Average Distance to Nearest Wind Farm by Year ({model_output_filename.split("/")[-1].replace(".xlsx", "")})'
    plt.title(plot_title, fontsize=14)

    # Annotate each bar with the closest wind farm name
    for bar, year in zip(bars, yearly_distances['Year']):
        closest_farm, _ = closest_farms_per_year[year]
        annotation = f"{closest_farm}\n{bar.get_height():.2f} km"
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), annotation, ha='center', va='bottom', rotation=0, fontsize=8, color='black')

    # Improve layout and aesthetics
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save the plot to a file
    output_filename = model_output_filename.replace('.xlsx', '.png')
    plt.savefig(output_filename)
    plt.close()

# Load existing wind farm data - common for all models
existing_farms_df = pd.read_excel('Validation/Scottish_wind_farms_with_lat_lon.xlsx')
gdf_existing_farms = gpd.GeoDataFrame(existing_farms_df, geometry=gpd.points_from_xy(existing_farms_df['Longitude'], existing_farms_df['Latitude']))

# Initialize an empty list to compile data
compiled_data = []

# Process and plot each model output file
model_output_files = ['Validation/model_output_2.6.xlsx', 'Validation/model_output_4.5.xlsx', 'Validation/model_output_8.5.xlsx']
for filename in model_output_files:
    process_and_plot_model_output(filename, gdf_existing_farms, compiled_data)

# Convert the compiled data to a DataFrame and save to Excel
compiled_df = pd.DataFrame(compiled_data)
compiled_df.to_excel('Validation/compiled_wind_farm_validation.xlsx', index=False)