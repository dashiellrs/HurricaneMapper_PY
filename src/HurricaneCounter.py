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

# Select tool
storm_season = 2025
storm_name = 'CHANTAL'
storm_track_points = "memory\\selected_points"

# Points to Line tool
storm_track_line = "memory\\tracklines"

# County data URL
usa_counties = 'https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Counties_Generalized_Boundaries/FeatureServer/0'

# %%
# Select track points for a single storm
arcpy.analysis.Select(
    in_features = "IBTrACS_NA.shp",
    out_feature_class = storm_track_points,
    where_clause = f"SEASON = {storm_season} And NAME = '{storm_name}'"
)

# %%
arcpy.management.GetCount(storm_track_points)

# %%
# Create storm track using selected points
arcpy.management.PointsToLine(
    Input_Features=storm_track_points,
    Output_Feature_Class=storm_track_line,
    Sort_Field="ISO_TIME"
)

# %%
# Process: select by location
select_result = arcpy.management.SelectLayerByLocation(
    in_layer=usa_counties,
    select_features=storm_track_line,
)

# Save result to a variable
select_output = select_result.getOutput(0)