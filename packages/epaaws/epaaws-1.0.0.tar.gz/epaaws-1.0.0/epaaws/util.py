__all__ = ['open_date']


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
