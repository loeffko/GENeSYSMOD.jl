"""Interactive manager for the GENeSYS-MOD dispatch results database
(genesysmod_dispatch_results.duckdb) - same tool as manage_results_db.py,
pointed at the dispatch db by default. See that script for the feature list
(list / rename / split / purge / compact).

Usage:  python Scripts/manage_dispatch_db.py [path/to/db.duckdb]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manage_results_db as m

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.argv.append(os.path.join(m.REPO, "Results", "genesysmod_dispatch_results.duckdb"))
    m.main()
