# epaaws

[![Tests](https://github.com/barronh/epaaws/actions/workflows/tests.yaml/badge.svg)](https://github.com/barronh/epaaws/actions/workflows/tests.yaml)
[![Sphinx](https://github.com/barronh/epaaws/actions/workflows/documentation.yaml/badge.svg)](https://github.com/barronh/epaaws/actions/workflows/documentation.yaml)
[![Docs](https://github.com/barronh/epaaws/actions/workflows/pages/pages-build-deployment/badge.svg)](https://barronh.github.io/epaaws)

Library of functions to facilitate analysis interaction with EPA's data on
AWS S3 buckets thru Amazon's Registry of Open Data.[1] At present, this only
includes the epa-2022-modeling-platform (see module mp2022). For more
information, see the [documentation pages](https://barronh.github.io/epaaws).


Citations:
1. https://registry.opendata.aws/epa-2022-modeling-platform/

Install for Python3
-------------------

```bash
python -m pip git+https://github.com/barronh/epaaws.git
```

Example
-------

Example of how to plot the terrain height from a GRIDCRO2D file.

```python
import epaaws

f = epaaws.mp2022.open_gridcro2d('2022-01-01')
levels = [-100, -10, 1, 100, 200, 400, 800, 1600, 3200]
f['HT'].plot(levels=levels, cmap='terrain')
f.csp.cno.drawstates()
```
