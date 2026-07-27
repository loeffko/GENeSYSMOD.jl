# NA model documentation

MkDocs (Material) documentation of the GENeSYS-MOD North America model,
prepared for GitLab Pages.

## Local preview

```bash
pip install mkdocs-material
mkdocs serve          # from this folder → http://127.0.0.1:8000
```

## Deploy to GitLab Pages

Option A — docs as their own GitLab repository: copy this folder's contents to
the repo root; the included `.gitlab-ci.yml` publishes on every push to the
default branch.

Option B — docs inside a larger repository: keep this folder as `docs/`, move
`.gitlab-ci.yml` to the repo root and use the subfolder variant commented
inside it.

## Structure

```
mkdocs.yml                 site config + navigation
.gitlab-ci.yml             Pages deployment (mkdocs build → public/)
docs/
  index.md                 overview + quick facts
  model.md                 framework, investment/dispatch setup, validation
  data.md                  data pipeline, scenario overlays, timeseries
  regions-north-america.md regional setup, assumptions, sources, methods
  scenarios.md             scenario tree
  results.md               databases, labels, reproducibility
```
