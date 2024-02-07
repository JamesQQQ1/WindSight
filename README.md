# Masters-Research

## Complete Model for Master's Research

### Overview
This repository contains the complete model developed as part of my Master's research. It is designed to run comprehensive analyses once all data manipulation processes have been completed.

### File Descriptions

- `Prophet.py`: This script utilizes the Prophet forecasting model to generate predictions based on time series data.
- `Raster_Layer.py`: This script handles the conversion of ArcGIS raster files to the NetCDF format, facilitating the integration of additional datasets into the model.
- `extrapo_population.py`: This script extrapolates population data to estimate population distribution across geographical regions.
- `final_2.6.py`: This script represents one of the final versions of the model, tailored for scenario 2.6.
- `final_4.5.py`: This script represents one of the final versions of the model, tailored for scenario 4.5.
- `final_8.5.py`: This script represents one of the final versions of the model, tailored for scenario 8.5.
- `land_use_change.py`: This script analyzes changes in land use patterns over time, providing crucial input for the model's environmental impact assessments.
- `land_use_slice.py`: This script slices and processes land use data to generate inputs for the model, ensuring accurate representation of land use factors in the analysis.
- `last_year_avg.py`: This script calculates the average values of relevant variables from the last year of data, serving as a baseline for comparison in scenario analysis.

### Data Preparation

The model expects input files in NetCDF format. Ensure that all your data files conform to this format or modify the script to accommodate different file formats as needed.

#### Pre-processing Scripts

Apart from the main model script, this repository includes several Python scripts used for data preparation:

- **Land Use Files**: These scripts should be executed first to prepare the datasets required by the model. They process information related to land use patterns and changes.
  
- **Raster File Conversion**: This script converts ArcGIS files to the NetCDF format. It's essential for incorporating datasets not originally in NetCDF format.
  
- **Population Files**: These scripts analyze population centers and should be run to accurately gauge population distribution.

### Running the Model

To run the model for various scenarios, follow these steps:

1. Ensure all your datasets are in the correct format (NetCDF) or have been converted using the provided scripts.
2. Execute the land use preparation scripts.
3. Run the raster file conversion script for any additional datasets.
4. Execute the population files script to prepare population data.
5. Run the `Final.py` script to perform the analysis for each scenario.

### Raw Data Files and Flexibility

#### Included Data Files

This repository includes raw data files that were specifically used in my research. These files serve as examples or starting points for users who wish to understand the data format and structure required by the model. They are only for the RCP 4.5 scinario.

#### Model Flexibility

The model is designed with flexibility in mind, allowing for the analysis of different geographical regions and climate data. Users are encouraged to use their datasets, provided they meet the format requirements specified (NetCDF). This adaptability ensures that the model can be applied to various research contexts and objectives, extending its utility beyond the initial case study.

#### Customization for Different Datasets

- **Geographical Regions**: Users can input data pertaining to any geographical location. The model's applicability is not restricted to the regions covered in the included datasets. This feature is particularly useful for comparative studies across different locations.
  
- **Climate Data**: The model supports a broad range of climate data types. Whether your research focuses on temperature, precipitation, wind patterns, or other climatic variables, the model can be adjusted to incorporate these datasets into the analysis.

### Tips for Using Different Datasets

1. **Ensure Compatibility**: Before running the model with new datasets, verify that they are in the NetCDF format or use the provided conversion scripts as needed.
2. **Data Preparation**: Follow the data preparation steps outlined above to ensure your datasets are correctly formatted and structured for the model.
3. **Customization**: Depending on your specific research needs, you may need to slightly modify the scripts to accommodate the peculiarities of your data, such as different variable names or spatial resolutions.

By adhering to these guidelines, users can effectively leverage the model for a wide array of research questions, making the most of its capabilities to analyze and interpret wind energy potential, land use impacts, or other environmental and geographical phenomena.

For any queries or further assistance, feel free to open an issue in this repository.
