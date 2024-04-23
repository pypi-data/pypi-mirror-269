# xsuite-kernels

## Simple installation

The package can be installed with `pip install xsuite-kernels`. Since it is
dependent on particular versions of the Xsuite packages, installing it might
automatically update your Xsuite packages to newer versions. You can use the
`-U` option to upgrade all packages to the latest versions.

This package provides a set of precompiled kernels for the Xsuite packages, so
that commonly used tracking scenarios can be run without the need to compile
the kernels on the target machine. The precompiled kernels are distributed as
binary Python wheels of the package `xsuite-kernels` on PyPI.

When the package is installed on a supported machine `pip` will automatically
download the appropriate kernel files and install them in the correct location,
so that Xtrack can use them. If `xsuite-kernels` is not installed, Xtrack will
fall back to the default behaviour of compiling the kernels on the fly.

If the package is installed from source (e.g. by cloning the repository or
downloading the source distribution in case of an unsupported platform), the
kernels will be compiled automatically during the installation process
(see `setup.py`).

## Developer notes

In case of a source installation, the building process can be skipped by setting
an environment variable `SKIP_KERNEL_BUILD` to `1` before running `pip install`.

If your local versions of `xtrack`, `xfields`, etc. have diverged from the
versions specified in `pyproject.toml`, you can install the package with the
`--no-deps` option to avoid upgrading the dependencies.

The package exposes a `xsuite-kernels` command that can be used to manage the
kernels on demand (add `--help` option for more information):

```bash
$ xsuite-kernels regenerate  # Regenerate all kernels
$ xsuite-kernels clean       # Remove all kernels
$ xsuite-kernels info        # Print some useful debug information
```
