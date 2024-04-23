from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_6_0():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'diptest.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_6_0()
del _delvewheel_patch_1_6_0
# end delvewheel patch

import importlib.metadata

from diptest.diptest import dipstat, diptest
from diptest.lib import _diptest_core as _diptest
from diptest.lib._diptest_core import _has_openmp_support

__version__ = importlib.metadata.version("diptest")

__all__ = ["dipstat", "diptest", "_diptest", "_has_openmp_support", "__version__"]
