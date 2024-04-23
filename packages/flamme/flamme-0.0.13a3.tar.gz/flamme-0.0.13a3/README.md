# flamme

<p align="center">
    <a href="https://github.com/durandtibo/flamme/actions">
        <img alt="CI" src="https://github.com/durandtibo/flamme/workflows/CI/badge.svg">
    </a>
    <a href="https://github.com/durandtibo/flamme/actions">
        <img alt="Nightly Tests" src="https://github.com/durandtibo/flamme/workflows/Nightly%20Tests/badge.svg">
    </a>
    <a href="https://github.com/durandtibo/flamme/actions">
        <img alt="Nightly Package Tests" src="https://github.com/durandtibo/flamme/workflows/Nightly%20Package%20Tests/badge.svg">
    </a>
    <br/>
    <a href="https://durandtibo.github.io/flamme/">
        <img alt="Documentation" src="https://github.com/durandtibo/flamme/workflows/Documentation%20(stable)/badge.svg">
    </a>
    <a href="https://durandtibo.github.io/flamme/">
        <img alt="Documentation" src="https://github.com/durandtibo/flamme/workflows/Documentation%20(unstable)/badge.svg">
    </a>
    <br/>
    <a href="https://codecov.io/gh/durandtibo/flamme">
        <img alt="Codecov" src="https://codecov.io/gh/durandtibo/flamme/branch/main/graph/badge.svg">
    </a>
    <a href="https://codeclimate.com/github/durandtibo/flamme/maintainability">
        <img src="https://api.codeclimate.com/v1/badges/b124c0a1a64ee041e189/maintainability" />
    </a>
    <a href="https://codeclimate.com/github/durandtibo/flamme/test_coverage">
        <img src="https://api.codeclimate.com/v1/badges/b124c0a1a64ee041e189/test_coverage" />
    </a>
    <br/>
    <a href="https://github.com/psf/black">
        <img  alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <a href="https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings">
        <img  alt="Doc style: google" src="https://img.shields.io/badge/%20style-google-3666d6.svg">
    </a>
    <a href="https://github.com/astral-sh/ruff">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;">
    </a>
    <a href="https://github.com/guilatrova/tryceratops">
        <img  alt="Doc style: google" src="https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black">
    </a>
    <br/>
    <a href="https://pypi.org/project/flamme/">
        <img alt="PYPI version" src="https://img.shields.io/pypi/v/flamme">
    </a>
    <a href="https://pypi.org/project/flamme/">
        <img alt="Python" src="https://img.shields.io/pypi/pyversions/flamme.svg">
    </a>
    <a href="https://opensource.org/licenses/BSD-3-Clause">
        <img alt="BSD-3-Clause" src="https://img.shields.io/pypi/l/flamme">
    </a>
    <br/>
    <a href="https://pepy.tech/project/flamme">
        <img  alt="Downloads" src="https://static.pepy.tech/badge/flamme">
    </a>
    <a href="https://pepy.tech/project/flamme">
        <img  alt="Monthly downloads" src="https://static.pepy.tech/badge/flamme/month">
    </a>
    <br/>
</p>

A library to generate custom reports of pandas DataFrames

## Installation

We highly recommend installing
a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
`flamme` can be installed from pip using the following command:

```shell
pip install flamme
```

To make the package as slim as possible, only the minimal packages required to use `flamme` are
installed.
To include all the dependencies, you can use the following command:

```shell
pip install flamme[all]
```

Please check the [get started page](https://durandtibo.github.io/flamme/get_started) to see how to
install only some specific dependencies or other alternatives to install the library.
The following is the corresponding `flamme` versions and tested dependencies.

| `flamme` | `coola`      | `jinja2`     | `markdown`   | `matplotlib` | `numpy`       | `objectory`  | `pandas`     | `pyarrow`      | `scipy`       | `tqdm`         | `python`      |
|----------|--------------|--------------|--------------|--------------|---------------|--------------|--------------|----------------|---------------|----------------|---------------|
| `main`   | `>=0.2,<1.0` | `>=3.0,<3.2` | `>=3.4,<3.6` | `>=3.6,<4.0` | `>=1.23,<2.0` | `>=0.1,<0.2` | `>=1.4,<3.0` | `>=10.0,<15.0` | `>=1.10,<2.0` | `>=4.65,<5.0`  | `>=3.9,<3.13` |
| `0.0.12` | `>=0.2,<0.3` | `>=3.0,<3.2` | `>=3.4,<3.6` | `>=3.6,<4.0` | `>=1.23,<2.0` | `>=0.1,<0.2` | `>=1.4,<3.0` | `>=10.0,<15.0` | `>=1.10,<2.0` | `>=4.65,<4.67` | `>=3.9,<3.13` |
| `0.0.11` | `>=0.2,<0.3` | `>=3.0,<3.2` | `>=3.4,<3.6` | `>=3.6,<4.0` | `>=1.23,<2.0` | `>=0.1,<0.2` | `>=1.4,<3.0` | `>=10.0,<15.0` | `>=1.10,<2.0` | `>=4.65,<4.67` | `>=3.9,<3.13` |
| `0.0.10` | `>=0.2,<0.3` | `>=3.0,<3.2` | `>=3.4,<3.6` | `>=3.6,<4.0` | `>=1.23,<2.0` | `>=0.1,<0.2` | `>=1.3,<2.2` | `>=10.0,<15.0` | `>=1.10,<2.0` | `>=4.65,<4.67` | `>=3.9,<3.13` |
| `0.0.9`  | `>=0.2,<0.3` | `>=3.0,<3.2` | `>=3.4,<3.6` | `>=3.6,<4.0` | `>=1.23,<2.0` | `>=0.1,<0.2` | `>=1.3,<2.2` | `>=10.0,<15.0` | `>=1.10,<2.0` | `>=4.65,<4.67` | `>=3.9,<3.13` |
| `0.0.8`  | `>=0.2,<0.3` | `>=3.0,<3.2` | `>=3.4,<3.6` | `>=3.6,<4.0` | `>=1.23,<2.0` | `>=0.1,<0.2` | `>=1.3,<2.2` | `>=10.0,<15.0` |               | `>=4.65,<4.67` | `>=3.9,<3.12` |
