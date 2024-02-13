import pandas as pd
import geopandas as gpd
import requests
from shapely.wkt import loads as shapely_loads

def parse_geo(wkt):
    wkt = wkt.replace("geography'SRID=4326;","")
    wkt = wkt.replace("'","")
    return shapely_loads(wkt)

def reproject(geom):
    #TODO: create the function to reproject (using pyproj for example)
    return geom     

def get_images(d1,
               d2,
               geom,
               out_format="json",
               cloud=1.0,
               verbose=True
               ):
    
    """
    Function parameters:
    - d1:           Date 1 for the date range in the search
    - d2:           Date 2 for the date range in the search
    - geom:         Shapely geometry from where images will be searched.
    - out_format:   Output format, three options: "json", "dataframe" and "geodataframe"
    - cloud:        Maximum cloud cover coverage.
    - verbose:      If function will print things explaining step by step 
    """
    
    d1 = d1.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    d2 = d2.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    geom = reproject(geom)
    wkt = geom.wkt
    
    main_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$"

    cc = f"Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value lt {cloud})"
    l1 = 'S2MSI1C'
    l2 = 'S2MSI2A'
    S2L2A = f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq '{l2}')"
    date = f"ContentDate/Start gt {d1} and ContentDate/Start lt {d2}"
    location = f"OData.CSC.Intersects(area=geography'SRID=4326;{wkt}')"

    URL = f"{main_url}filter={cc} and {S2L2A} and {date} and {location}"

    json = requests.get(URL).json()
    if out_format=="json":
        return json
    
    df = pd.DataFrame.from_dict(json['value'])
    if out_format=="dataframe":
        return df
    geom = df["Footprint"].map(parse_geo)

    gdf = gpd.GeoDataFrame(df,geometry=geom)
    gdf.set_crs(epsg=4326,inplace=True)

    # columns = ["Id", "Name", "OriginDate", "S3Path", "ContentLength", "geometry" ]
    # gdf = gdf[columns]
    if out_format=="geopandas":
        return gdf
    
    raise TypeError("Provided format is incorrect.")