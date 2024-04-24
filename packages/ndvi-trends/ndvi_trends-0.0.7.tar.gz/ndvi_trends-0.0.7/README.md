#### NDVI TRENDS

A module for studying NDVI Trends (from S2/LSAT) with a particular emphasis on determining or deriving relvant features for cover-cropping.

1. Generate and Save NDVI Series for small Regions
	a. grab NDVI Series on the fly for any geom
	b. for a large set of geoms efficiently grab and save all
2. Smooth NDVI Series
	a. linear interpolation
	b. remove drops
	c. sg smoothing
	d. window smoothing
	e. 1 at a time or save a stack
3. Days over (normalized) NDVI Threshold
4. Cover Crop Detection
	* green-up dates
	* features (AUC, mean/median differences for set time periods, other metrics)

###### PROPOSED MODULES

```yaml
smoothing: handles smoothing data
data: get/save data (in real time, 1 at a time, map over a bunch)
gee: helpers for google earth engine
nb: helpers for visual outputs for notebooks
calc: smooths data, extracts features of interest, computes GREEN-DAYS
cli: automates batch jobs
```

--- 

#### REQUIREMENTS

Packages are managed through a conda yaml [file](./conda-env.yaml). To create/update the `ndvi_trends` environment:

```bash
# create
conda env create -f conda-env.yaml
# update
### NOTE: prune not working https://github.com/conda/conda/issues/7279
conda env update -f conda-env.yaml --prune
### use mamba as workaround: 
mamba env update -f conda-env.yaml --prune
```

Additionally this repo is using [config_args](https://github.com/SchmidtDSE/config_args) and [mproc](https://github.com/brookisme/mproc) still in developmemt.  Clone the repos and then (with ndvi_trends conda env activated) run `pip install --e .`

Note: the minimal conda-env does not specify the required package versions. [requirements.txt](./requirements.txt) can be used to recreate the exact env.

--- 

#### QUICK START

Usage example

---

#### DOCUMENTATION


###### DEPLOY TO PYPI:

```bash
# (optional) need to first remove old distributions or be more selective with * on twine-upload
rm -rf dist
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
python -m build
python -m twine upload dist/*
```

NOTE:  When testing locally the editable environment (`pip install -e .`) might behave differently than the pacakage. For example, the pyproject.toml should explicitly include submodules. In this case:

```toml
[tool.setuptools]
packages = [
	"ndvi_trends",
	"ndvi_trends.utils"
]
```

My original file did not include `ndvi_trends.utils` but behaved correctly locally. However when deployed this lead to problems.  Before deploying drop the `-e`!


###### MODULES:

├── ndvi_trends
│		├── calc: extracts features and statistics from NDVI Series
│		├── data: methods for fetching NDVI data from Harmonized S2-Landsat using GEE
│		├── smoothing: gap filling and smoothing utilities
│		└── utils
│				└── ee: helper methods for GEE

See doc-strings for documentation of python modules.

--- 

#### STYLE-GUIDE

Following PEP8. See [setup.cfg](./setup.cfg) for exceptions. Keeping honest with `pycodestyle .`
