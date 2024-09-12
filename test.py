#%%
import openeo

connection = openeo.connect("openeo.dataspace.copernicus.eu")

#%%
# List collections available on the openEO back-end
connection.list_collection_ids()

# Get detailed metadata of a certain collection
connection.describe_collection("SENTINEL2_L2A")
# %%
connection.authenticate_oidc()
# %%
datacube = connection.load_collection(
    "SENTINEL2_L2A",
    spatial_extent={"west": 5.14, "south": 51.17, "east": 5.17, "north": 51.19},
    temporal_extent = ["2021-02-01", "2021-04-30"],
    bands=["B02", "B04", "B08"],
    max_cloud_cover=85,
)
# %%
datacube = datacube.max_time()
# %%


# First, we connect to the back-end and authenticate. 
con = openeo.connect("openeo.dataspace.copernicus.eu")
con.authenticate_oidc()

# Now that we are connected, we can initialize our datacube object with the area of interest 
# and the time range of interest using Sentinel 1 data.
sentinel2_cube = connection.load_collection(
    "SENTINEL2_L2A",
    spatial_extent={"west": 5.14, "south": 51.17, "east": 5.17, "north": 51.19},
    temporal_extent = ["2021-02-01", "2021-04-30"],
    bands=["B02", "B08", "B04"],  # B02: Blue, B03: Green, B04: Red
    max_cloud_cover=85,
)


#%%

# By filtering as early as possible (directly in load_collection() in this case), 
# we make sure the back-end only loads the data we are interested in and avoid incurring unneeded costs.


#From this data cube, we can now select the individual bands with the DataCube.band() method and rescale the digital number values to physical reflectances:
blue = sentinel2_cube.band("B02") * 0.0001
red = sentinel2_cube.band("B04") * 0.0001
nir = sentinel2_cube.band("B08") * 0.0001


# We now want to compute the enhanced vegetation index and can do that directly with these band variables:
evi_cube = 2.5 * (nir - red) / (nir + 6.0 * red - 7.5 * blue + 1.0)


#%%
# Because GeoTIFF does not support a temporal dimension, we first eliminate it by taking the temporal maximum value for each pixel:
evi_composite = evi_cube.max_time()


# Now we can download this to a local file:
evi_composite.download("evi-composite.tiff")
# %%
