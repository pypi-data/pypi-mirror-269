# Development

If you'd like to develop `redflag`, this page should help you get started.


## Installation

You can install this package with `pip` or `conda`. The `dev` option will install the packages you need for testing and building the documentation.

```shell
python -m pip install "redflag[dev]"
```


## Contributing

If you'd like to contribute pull requests back to the main `redflag ` project, please see [`CONTRIBUTING.md`](https://github.com/scienxlab/redflag/blob/main/CONTRIBUTING.md).


## Testing

You can run the tests (requires `pytest` and `pytest-cov`) with

```shell
pytest
```

Most of the tests are `doctest` tests, which are contained in the docstrings of this package's functions. There are further tests in the `tests` folder.


## Building the package

This repo uses PEP 518-style packaging. [Read more about this](https://setuptools.pypa.io/en/latest/build_meta.html) and [about Python packaging in general](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

To build `redflag` locally:

```shell
python -m build
```

This builds both `.tar.gz` and `.whl` files, either of which you can install with `pip`.


## Building the docs

You can build the docs with the following commands:

```shell
cd docs
make html
```

Don't just run `sphinx-build` manually: there is other stuff happening in the `Makefile`.

There is a continuous integration script to update the docs on published releases.


## Continuous integration

This repo has two GitHub 'workflows' or 'actions':

- Push to `main`: Run all tests on all version of Python. This is the **Build and test** workflow.
- Publish a new release: Build and upload to PyPI. This is the **Publish to PyPI** workflow. Publish using the GitHub interface, for example ([read more](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)).
