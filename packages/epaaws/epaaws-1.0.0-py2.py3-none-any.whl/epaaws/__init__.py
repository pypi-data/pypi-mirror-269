__all__ = ['open_date', 'mp2022']
__doc__ = """
Library of functions to facilitate analysis interaction with EPA's data on
AWS S3 buckets thru Amazon's Registry of Open Data.[1] At present, this only
includes the epa-2022-modeling-platform (see module mp2022).

Citations:
1. https://registry.opendata.aws/epa-2022-modeling-platform/

Install for Python3
-------------------

.. code-block:: sh

    python -m pip install git+https://github.com/barronh/epaaws.git


Example
-------

Example of how to plot the terrain height from a GRIDCRO2D file.

.. code-block:: python

    import epaaws

    f = epaaws.mp2022.open_gridcro2d('2022-01-01')
    levels = [-100, -10, 1, 100, 200, 400, 800, 1600, 3200]
    f['HT'].plot(levels=levels, cmap='terrain')
    f.csp.cno.drawstates()

MODULES
-------

Each module provides access to.

mp2022 :
    provides an interface to EPA's Modeling Platform for 2022

util :
    provides basic utilities used by all the modeling platforms
"""
import importlib.metadata
from . import mp2022

__version__ = importlib.metadata.version('epaaws')


def open_date(
    date, tmpl, bucket
):
    """
    Open all files for specific date

    Arguments
    ---------
    date : str
        Date parsable by pandas.to_datetime
    tmpl : str
        strftime template for date file (e.g., MCIP/GRIDCRO2D.12US1.35L.%y%m%d)
    """
    import boto3
    import pandas as pd
    from botocore import UNSIGNED
    from botocore.client import Config
    import io
    import cmaqsatproc as csp

    client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    date = pd.to_datetime(date)
    path = date.strftime(tmpl)
    obj = client.get_object(Bucket=bucket, Key=path)
    bdy = io.BytesIO(obj['Body'].read())
    f = csp.open_ioapi(bdy, engine='scipy')
    return f
