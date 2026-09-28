# Setup health

We resolve this skill's real path to the Funfigs root and run `uv run --offline --no-project scripts/doctor.py` there. The check reads configuration and reports status without printing secret values or changing installations.

We distinguish broken links and invalid configuration from optional missing tools. Multiple executables on PATH or duplicate skill names are warnings, not permission to uninstall them. We do not inspect private project histories or company skill contents.

We explain failures and propose the smallest correction. A request to check health is read-only. Repairs, plugin installation and configuration replacement require a request to make those changes.
