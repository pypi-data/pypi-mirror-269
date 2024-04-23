import sys
from .ngstoolkits import single_mutation
if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__

finally:
    del PackageNotFoundError
