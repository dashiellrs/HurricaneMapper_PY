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

# Output variable & path
affected_counties = str(processed_folder_path / 'affected_counties.shp')

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

# %%
# Create model output
arcpy.management.CopyFeatures(
    in_features=select_output,
    out_feature_class=affected_counties
)

# %%
# View output

# Import arcgis package
import arcgis

# Create "gis" object
gis = arcgis.GIS()

# Create a map
my_map = gis.map()

# Set the basemap to oceans
my_map.basemap.basemap = "oceans"

# Create feature layers from strom tracks & affected counties
track_lyr = arcgis.GeoAccessor.from_featureclass(storm_track_line)
counties_lyr = arcgis.GeoAccessor.from_featureclass(affected_counties)

# Add layers to the map
my_map.content.add(counties_lyr)
my_map.content.add(track_lyr)

# Show the map
my_map

# %%
# Plot the number of people affected by storm, by state

# Create a plot of people affected by state
the_plot = (
    counties_lyr.
    groupby('STATE_NAME')
    .agg({'POPULATION':'sum'})
    .sort_values(by='POPULATION', ascending=False)
    .plot(
        kind='barh',
        title=f'{storm_name}-{storm_season}',
        xlabel='People affected',
        ylabel=''
    )
)


