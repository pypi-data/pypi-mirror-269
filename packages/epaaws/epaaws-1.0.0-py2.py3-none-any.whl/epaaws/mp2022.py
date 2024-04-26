__all__ = []
__doc__ = """
mp2022
======

The mp2022 module provides an interface to Modeling Platform 2022
interface.
"""

from .util import open_date
# for flake8
_open_date = open_date

mciptypes = [
    'GRIDCRO2D', 'GRIDBDY2D', 'GRIDDOT2D',
    'METCRO2D', 'METCRO3D', 'METBDY3D', 'METDOT3D',
    'SOI_CRO', 'LUFRAC_CRO'
]
for mciptype in mciptypes:
    tdoc = f"""open a {mciptype}
    Arguments
    ---------
    date : str or date-like
        Any date parsable by pandas.to_datetime
    domain : str
        Domain string (eg, .12US1.35L.)

    Returns
    -------
    {mciptype.lower()} : xarray.Dataset
        File from S3 loaded into memory.
    """
    exec(f"""def open_{mciptype.lower()}(date, domain='.12US1.35L.'):
    \"\"\"{tdoc}\"\"\"
    bucket = 'epa-2022-modeling-platform'
    tmpl = f'MCIP/{mciptype}{{domain}}%y%m%d'
    return open_date(date, tmpl=tmpl, bucket=bucket)
    """)
    __all__.append(f'open_{mciptype.lower()}')
