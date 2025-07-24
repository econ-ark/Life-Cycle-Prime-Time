# Life-Cycle-Prime-Time

https://econ-ark.github.io/Life-Cycle-Prime-Time/

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/econ-ark/Life-Cycle-Prime-Time/HEAD)

To reproduces all the results in the repository first clone this repository
locally:

```
# Clone this repository
$ git clone https://github.com/econ-ark/Life-Cycle-Prime-Time

# Change working directory to Life-Cycle-Prime-Time
$ cd Life-Cycle-Prime-Time
```

Then you can either use a local virtual env(conda) or
[nbreproduce](https://github.com/econ-ark/nbreproduce) to reproduce to the
results.

#### A local conda environment and execute the do_all.py file.

```
$ conda env create -f environment.yml
$ conda activate Life-Cycle-Prime-Time
# execute the script, select the appropriate option and use it to reproduce the data and figures.
$ python do_all.py
```

#### [nbreproduce](https://github.com/econ-ark/nbreproduce) (requires Docker to be installed on the machine).

```
# Install nbreproduce
$ pip install nbreproduce

# Reproduce all results using nbreproduce
$ nbreproduce
```

## References

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]

<!-- SPHINX-START -->

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/econ-ark/Life-Cycle-Prime-Time/workflows/CI/badge.svg
[actions-link]:             https://github.com/econ-ark/Life-Cycle-Prime-Time/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/estimark
[conda-link]:               https://github.com/conda-forge/estimark-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/econ-ark/Life-Cycle-Prime-Time/discussions
[pypi-link]:                https://pypi.org/project/estimark/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/estimark
[pypi-version]:             https://img.shields.io/pypi/v/estimark
[rtd-badge]:                https://readthedocs.org/projects/estimark/badge/?version=latest
[rtd-link]:                 https://estimark.readthedocs.io/en/latest/?badge=latest

<!-- prettier-ignore-end -->
