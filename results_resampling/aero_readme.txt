Minimum revisit frequency data contained in file "aero_min_revisit_rates.csv"

File is comma-delimited, with 4 columns:
Latitude, Longitude, Surface Runoff (qsurf), and Soil Moisture (sm1)

All frequencies are given in units of hours. The lat/lon points reflect a 1-degree grid, and they are centered in the middle of each grid cell.

The hydrologic states in columns 3 and 4 refer to the minimum revisit frequency required to achieve a certain level of model performance in each grid cell. Generally, surface runoff requires more frequent monitoring than does soil moisture.

NOTE: Only the lat/lon points with available data are given in this file. Points not contained in this file may fall into one of two categories: 
(1) No observation data available to calculate model performance (e.g. over the oceans, in remote areas, etc.)
(2) No model runs were able to reproduce observed data at an acceptable level