""" Data: Fetch, Filter and Process NDVI trend data

License:
    BSD, see LICENSE.md
"""


import ee
import re
from datetime import datetime
from datetime import timedelta
from pprint import pprint
import numpy as np
import xarray as xr
import ndvi_trends.utils.ee as ee_utils


#
# CONSTANTS/CONFIG
#
EE_INITIALIZED = ee_utils.safe_init(quiet=True)
CLEAR_THRESHOLD = 0.60
CSP_BAND = 'cs_cdf'
MASK_VALUE = 2.1474836e9
MASK_VALUE_BAND = 'ndvi'
EE_CRS = 'EPSG:3857'
SCALE = 30
YMD_FMT = '%Y-%m-%d'
DEFAULT_RADIUS = SCALE * 10
MAX_ERR = 1


#
# ASSETS
#
if EE_INITIALIZED:
    S2 = ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
    S2_CSP = ee.ImageCollection("GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED")
    HLSL = ee.ImageCollection("NASA/HLS/HLSL30/v002")
    FIELDS_FC = ee.FeatureCollection("projects/yield-predict/assets/KnoxFields")


#
# MAIN
#
def start_and_end_dates_for_growing_year(
        year,
        start_day_index=260,
        end_day_index=175,
        buffer=20,
        str_fmt=YMD_FMT,
        return_dates_of_interest=True):
    """ get start and end dates for growing year
    Args:
        year (int):
            "growing-year". note actuall dates may fall outside of year
            based on start/end-day-indices and buffer
        start_day_index (int):
            the integer day-of-year to start. if <start_day_index> is less than
            <end_day_index> the year will be `<year> - 1`
        end_day_index (int):
            the integer day-of-year to stop.
        buffer (int):
            the ammount days to buffer the start/end dates by
        str_fmt (str|None):
            if None return datetime objects
            otherwise convert to str using `.strftime(str_fmt)`
        return_dates_of_interest (bool):
            if true return buffered_start_date, buffered_end_date, start_date, end_date
            otherwise only return buffered_start_date, buffered_end_date

    Returns:
        tuple of date strings or datetime objects (see args description above)
    """
    if start_day_index > end_day_index:
        start_year = year - 1
    else:
        start_year = year
    start_date = datetime(start_year, 1, 1) + timedelta(days=start_day_index - 1)
    end_date = datetime(year, 1, 1) + timedelta(days=end_day_index - 1)
    buffer_delta = timedelta(days=buffer)
    buffered_start_date = start_date - buffer_delta
    buffered_end_date = end_date + buffer_delta
    if str_fmt:
        start_date = start_date.strftime(str_fmt)
        end_date = end_date.strftime(str_fmt)
        buffered_start_date = buffered_start_date.strftime(str_fmt)
        buffered_end_date = buffered_end_date.strftime(str_fmt)
    if return_dates_of_interest:
        return buffered_start_date, buffered_end_date, start_date, end_date
    else:
        return buffered_start_date, buffered_end_date


def get_ndvi_dataset(geom, start_date=None, end_date=None, attrs={}, source=None):
    """
    Fetches cloud-masked ndvi xr.dataset from Google Earth Engine for
    a given geometry, start and end date.

    Args:
        geom (ee.geometry): area of interest
        start_date (str): start date as string
        end_date (str): end date as string
        attrs (dict): attributes-dict to add to resulting dataset
        source (str): filter data by datasource. one of ['S2','LSAT']

    Returns:
        xr.DataSet of ndvi values
    """
    geom = ee.Geometry(geom)
    if start_date is None:
        data_filter = ee.Filter.bounds(geom)
    else:
        data_filter = ee.Filter.And(
            ee.Filter.date(start_date, end_date),
            ee.Filter.bounds(geom))
    ndvi_ic = s2_lsat_ndvi_ic(data_filter)
    if source:
        ndvi_i = ndvi_ic.filter(ee.Filter.eq('source', source))
    ndvi_ic = ndvi_ic.sort('system:time_start')
    source_values = ndvi_ic.aggregate_array('source').getInfo()
    is_s2 = np.array([int(s == 'S2') for s in source_values])
    nb_s2 = is_s2.sum()
    nb_lsat = (1 - is_s2).sum()
    ds = get_ee_xrr(ndvi_ic, geom, attrs={'nb_s2': nb_s2, 'nb_landsat': nb_lsat})
    ds['is_sentinel_2'] = 'time', is_s2
    if attrs:
        ds = ds.assign_attrs(attrs)
    return ds


def get_ndvi_dataset_for_field(
        dn,
        start_date=None,
        end_date=None,
        attrs={},
        source=None,
        local_dir=None):
    """ TODO: MANAGE MULTI-GEOM FIELDS

    Fetches cloud-masked ndvi xr.dataset from Google Earth Engine for
    a given field, start and end date.

    The field geometries/attributes are contained in asset
    projects/yield-predict/assets/KnoxFields

    Args:
        dn (int|int-str): "DN"-property for field of interest
        start_date (str): start date as string
        end_date (str): end date as string
        attrs (dict): attributes-dict to add to resulting dataset
        source (str): filter data by datasource. one of ['S2','LSAT']

    Returns:
        xr.DataSet of ndvi values
    """
    if local_dir:
        ds = xr.open_dataset(f'{local_dir}/{dn}', engine='zarr', consolidated=False,)
        if start_date or end_date:
            ds = ds.sel(time=slice(start_date, end_date))
        if attrs:
            ds = ds.assign_attrs(attrs)
        return ds
    else:
        dn = int(dn)
        attrs = attrs.copy()
        attrs['DN'] = dn
        attrs['data_start_date'] = start_date
        attrs['data_end_date'] = end_date
        field = ee.Feature(FIELDS_FC.filter(ee.Filter.eq('DN', dn)).first())
        geom = field.geometry()
        attrs.update(field.toDictionary().getInfo())
        return get_ndvi_dataset(
            geom,
            start_date=start_date,
            end_date=end_date,
            attrs=attrs,
            source=source)


def get_ndvi_dataset_at_point(
        lon,
        lat,
        radius=DEFAULT_RADIUS,
        start_date=None,
        end_date=None,
        attrs={},
        mean_values=True,
        source=None):
    """

    Fetches cloud-masked ndvi xr.dataset from Google Earth Engine for
    a circle centered at point lon, lat.

    Args:
        lon (float): longitude of centroid
        lat (float): latitude of centroid
        radius (int): radius of circle
        start_date (str): start date as string
        end_date (str): end date as string
        attrs (dict): attributes-dict to add to resulting dataset
        mean_values (bool): if True return mean values, ie: `ds.mean(dim=('X', 'Y'))`
        source (str): filter data by datasource. one of ['S2','LSAT']

    Returns:
        xr.DataSet of ndvi values
    """
    attrs = attrs.copy()
    attrs['lon'] = lon
    attrs['lat'] = lat
    attrs['radius'] = radius
    attrs['data_start_date'] = start_date
    attrs['data_end_date'] = end_date
    geom = ee.Geometry.Point([lon, lat]).buffer(radius, MAX_ERR)
    ds = get_ndvi_dataset(
        geom,
        start_date=start_date,
        end_date=end_date,
        attrs=attrs,
        source=source)
    if mean_values:
        ds = ds.mean(dim=('X', 'Y'), skipna=True).assign_attrs(ds.attrs)
    return ds


def get_ndvi_dataset_for_region(
        bbox=None,
        coords=None,
        start_date=None,
        end_date=None,
        attrs={},
        mean_values=True,
        source=None):
    """

    Fetches cloud-masked ndvi xr.dataset from Google Earth Engine from either a
    bounding-box or a coordinate list for a polygon.

    Args:
        bbox (list[float]): bouding box for polygon (xmin, ymin, xmax, ymax)
        coords (list[float]): coordinates for polygon
        start_date (str): start date as string
        end_date (str): end date as string
        attrs (dict): attributes-dict to add to resulting dataset
        mean_values (bool): if True return mean values, ie: `ds.mean(dim=('X', 'Y'))`
        source (str): filter data by datasource. one of ['S2','LSAT']

    Returns:
        xr.DataSet of ndvi values
    """
    attrs = attrs.copy()
    if bbox:
        attrs['bbox'] = bbox
        geom = ee.Geometry.Rectangle(bbox)
    else:
        attrs['coords'] = coords
        geom = ee.Geometry.Polygon(coords)
    attrs['data_start_date'] = start_date
    attrs['data_end_date'] = end_date
    ds = get_ndvi_dataset(
        geom,
        start_date=start_date,
        end_date=end_date,
        attrs=attrs,
        source=source)
    if mean_values:
        ds = ds.mean(dim=('X', 'Y'), skipna=True).assign_attrs(ds.attrs)
    return ds


#
# XARRAY
#
def get_ee_xrr(
        ic,
        geom,
        attrs=None,
        mask_value=MASK_VALUE,
        mask_value_band=MASK_VALUE_BAND,
        load=True):
    """ get ee data using xarray
    Args:
        ic (ee.ImageCollection):
        geom (ee.Geometry):
        attrs (dict): attributes-dict to add to xr-dataset
        mask_value (float): set <mask_value> pixels to nan
        mask_value_band (str):
            name of band (or dataset data_var) to check for <mask_value>
        load (bool): if true load dataset

    Returns:
        data as xarray
    """
    ds = xr.open_dataset(
        ic,
        engine='ee',
        crs=EE_CRS,
        scale=SCALE,
        geometry=geom,
        mask_and_scale=True,
        cache=True)
    ds = ds.chunk().sortby('time')
    if load:
        ds = ds.load()
    if mask_value is not None:
        ds = ds.where(ds[mask_value_band] != MASK_VALUE)
    if attrs:
        ds = ds.assign_attrs(attrs)
    return ds


#
# EARTH ENGING SENTINEL-2/HLS NDVI
#
def s2_lsat_ndvi_ic(data_filter=None):
    """ get cloud masked ndvi based on Harmonized S2-Landsat

    * S2 images are masked using CLOUD_SCORE_PLUS.
    * Landsat images are masked using QA-band.

    Args:
        data_filter (ee.Filter): filter for S2/Landsat image-collections

    Returns:
         (ee.ImageCollection) cloud masked ndvi
    """
    s2_ndvi = cloud_masked_s2_ndvi_ic(data_filter)
    lsat_ndvi = cloud_masked_landsat_ndvi_ic(data_filter)
    ndvi = s2_ndvi.merge(lsat_ndvi).sort('system:time_start')
    return ndvi


def cloud_masked_s2_ndvi_ic(data_filter=None):
    """ get cloud masked S2-ndvi

    Removes clouds from S2 image-collection using CLOUD_SCORE_PLUS.

    Args:
        data_filter (ee.Filter): filter for S2 image-collection

    Returns:
         (ee.ImageCollection) cloud masked ndvi
    """
    s2 = S2
    if data_filter:
        s2 = S2.filter(data_filter)
    s2 = s2.linkCollection(S2_CSP, [CSP_BAND])
    return s2.map(cloud_masked_s2_ndvi)


def cloud_masked_landsat_ndvi_ic(data_filter=None):
    """ get cloud masked Landsat-ndvi

    Removes clouds from Landsat image-collection using QA-band.

    Args:
        data_filter (ee.Filter): filter for Landsat image-collection

    Returns:
         (ee.ImageCollection) cloud masked ndvi
    """
    lsat = HLSL
    if data_filter:
        lsat = lsat.filter(data_filter)
    return lsat.map(cloud_mask_landsat_ndvi)


def cloud_masked_s2_ndvi(im):
    """
    Args:
        im (ee.Image): s2 image joined with "cloud_prob" ee.Image

    Returns:
         (ee.Image) cloud masked ndvi (maintains im props and timestamps)
    """
    im = ee.Image(im)
    im = im.updateMask(im.select(CSP_BAND).gte(CLEAR_THRESHOLD))
    ndvi = im.normalizedDifference(['B8', 'B4']).rename(['ndvi']).set('source', 'S2')
    return ee.Image(ndvi.copyProperties(im).set('system:time_start', im.date().millis()))


def cloud_mask_landsat_ndvi(im):
    """
    Args:
        im (ee.Image): landsat image

    Returns:
         (ee.Image) cloud masked ndvi (maintains im props and timestamps)
    """
    cirrus = 1 << 0
    cloud = 1 << 1
    cloudadj = 1 << 2
    cloudshd = 1 << 3
    qa = im.select("Fmask")
    mask = qa.bitwiseAnd(cirrus).eq(0).And(
        qa.bitwiseAnd(cloud).eq(0).And(
            qa.bitwiseAnd(cloudadj).eq(0).And(
                qa.bitwiseAnd(cloudshd).eq(0))))
    im.updateMask(mask)
    ndvi = im.normalizedDifference(['B5', 'B4']).rename(['ndvi']).set('source', 'LANDSAT')
    return ee.Image(ndvi.copyProperties(im).set('system:time_start', im.date().millis()))
