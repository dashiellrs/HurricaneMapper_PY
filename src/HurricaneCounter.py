# %%
# # Hurricane Tracker
# By:     Dashiell Ridolfi-Starr\
# Date:   Oct. 28, 2026\
# \
# This script allows users to plot the paths of past hurricanes and identify the counties affected.

# %%
# Import packages
import arcpy
from pathlib import Path

# %%
# Create relative folder paths

# Raw data
raw_folder_path = Path.cwd().parent / 'data' / 'raw'

# Processed data
processed_folder_path = Path.cwd().parent / 'data' / 'processed'

# %%
# Allow ArcPy to overwrite output
arcpy.env.overwriteOutput = True

# Set default & scratch workspaces
arcpy.env.workspace = str(raw_folder_path)

# %%
# Define model variables

# Raw data
ibtracs = str(raw_folder_path / 'IBTrACS_NA.shp')

# Select tool
storm_season = 2024
storm_name = 'HELENE'
storm_track_points = "memory\\selected_points"

# Points to Line tool
storm_track_line = "memory\\tracklines"

# County data URL
usa_counties = 'https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Counties_Generalized_Boundaries/FeatureServer/0'

# %%
# Make a list of storm names per season

# Create empty list
storm_list = []

# Open search cursor
storms = arcpy.da.SearchCursor(
    in_table = ibtracs,
    field_names = ['NAME'],
    where_clause = "SEASON = 2020"
)

# Iterate through storm data
for row in storms:
    name = row[0]
    if name not in storm_list and name != "UNNAMED":
        storm_list.append(name)
    else:
        continue

# Delete cursor
del storms

# %%
# Select track points for a single storm
arcpy.analysis.Select(
    in_features = ibtracs,
    out_feature_class = storm_track_points,
    where_clause = f"SEASON = {storm_season} And NAME = '{storm_name}'"
)

# %%
arcpy.management.GetCount(storm_track_points)

# %%
# Create storm track using selected points
arcpy.management.PointsToLine(
    Input_Features = storm_track_points,
    Output_Feature_Class = torm_track_line,
    Sort_Field = "ISO_TIME"
)

# %%
# Process: select by location
select_result = arcpy.management.SelectLayerByLocation(
    in_layer = usa_counties,
    select_features = storm_track_line,
)

# Save result to a variable
select_output = select_result.getOutput(0)

# %%
# Count the affected counties
select_count = arcpy.management.GetCount(select_output)
county_total = int(select_count.getOutput(0))
