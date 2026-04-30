"""
Registry sub-package of UQTestFuns.
"""

from .registry import DEFAULT_ROOT, PKG_ROOT, Registry

# Singleton registry
_registry = Registry(PKG_ROOT)
_registry.scan(DEFAULT_ROOT)
