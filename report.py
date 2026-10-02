#!/usr/bin/env python3
"""CLI alias for gasket_catalog.main (same report as sierpinski-geometry-045)."""
from __future__ import annotations

from gasket_catalog import main as catalog_main


def main() -> int:
    try:
        catalog_main()
    except SystemExit as exc:
        code = exc.code
        if code in (None, 0):
            return 0
        if isinstance(code, int):
            return code
        print(code)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
