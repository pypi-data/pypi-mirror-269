from cartopy.io import shapereader
from geopandas import read_file, GeoDataFrame

def ne_countries(scale: int = 10) -> GeoDataFrame:
    """Return a GeoDataFrame of the world countries.
    
    Download the world countries shapefile from Natural Earth and
    return a GeoDataFrame of the countries.

    Parameters
    ----------
    scale : int, optional
        The scale of the shapefile, by default 10. The allowed values are
        10, 50 and 110.

    Returns
    -------
    GeoDataFrame
        A table of the world countries.
    """
    # Check if scale is one of the allowed values (10, 50, 110)
    if scale not in [10, 50, 110]:
        raise ValueError('Scale must be one of 10, 50, 110')

    # Setup rnaturalearth parameter
    resolution = str(scale) + 'm'
    category = 'cultural'
    name = 'admin_0_countries'
    shpfilename = shapereader.natural_earth(resolution, category, name)

    # Read the shapefile using geopandas
    return read_file(shpfilename)

def ne_states(state: str, scale: int = 10) -> GeoDataFrame:
    """Return a GeoDataFrame of the stats of a country.
    
    Download the counties shapefile from Natural Earth and
    return a GeoDataFrame of the countries.

    Parameters
    ----------
    state : str
        The country ISO3 code.

    scale : int, optional
        The scale of the shapefile, by default 10. The allowed values are
        10, 50 and 110.

    Returns
    -------
    GeoDataFrame
        A table of the world countries.
    """
    # Check if scale is one of the allowed values (10, 50, 110)
    if scale not in [10, 50, 110]:
        raise ValueError('Scale must be one of 10, 50, 110')

    # Setup rnaturalearth parameter
    resolution = str(scale) + 'm'
    category = 'cultural'
    name = 'admin_1_states_provinces'
    shpfilename = read_file(shapereader.natural_earth(resolution, category, name))

    states = shpfilename[shpfilename['adm0_a3'] == state]

    # Read the shapefile using geopandas
    return states