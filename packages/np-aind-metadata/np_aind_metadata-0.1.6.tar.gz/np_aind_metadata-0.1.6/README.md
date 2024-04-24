# np-aind-metadata



[![PyPI](https://img.shields.io/pypi/v/np-aind-metadata.svg?label=PyPI&color=blue)](https://pypi.org/project/np-aind-metadata/)
[![Python version](https://img.shields.io/pypi/pyversions/np-aind-metadata)](https://pypi.org/project/np-aind-metadata/)

[![Coverage](https://img.shields.io/codecov/c/github/AllenInstitute/np-aind-metadata?logo=codecov)](https://app.codecov.io/github/AllenInstitute/np-aind-metadata)
[![CI/CD](https://img.shields.io/github/actions/workflow/status/AllenInstitute/np-aind-metadata/publish.yml?label=CI/CD&logo=github)](https://github.com/AllenInstitute/np-aind-metadata/actions/workflows/publish.yml)
[![GitHub issues](https://img.shields.io/github/issues/AllenInstitute/np-aind-metadata?logo=github)](https://github.com/AllenInstitute/np-aind-metadata/issues)

# Usage
```bash
conda create -n np_aind_metadata python>=3.10
conda activate np_aind_metadata
pip install np_aind_metadata
```

## Python
Initialize a neuropixels rig model.

```python
from np_aind_metadata.init import neuropixels_rig

rig_model = neuropixels_rig.init("NP3")
```

Update a neuropixels rig model. Currently only supports dynamic routing context.

```python
import pathlib
from np_aind_metadata.update import dynamic_routing

dynamic_routing.update_rig(
    pathlib.Path("./examples/rig.json"),
    open_ephys_settings_sources=[
        pathlib.Path("./examples/settings.xml")
    ],
    output_path=pathlib.Path("./updated_rig.json"),
)
```

## np-codeocean
This library can track and update rig jsons for `np-codeocean`. `np` dependency group must be installed

Initialize storage for a rig
```bash
np-aind-metadata init-rig-storage "/directory/to/store/rigs" "NP3" --date 2022/02/07
```

Updating via `np-codeocean`

```python
import pathlib
from np_aind_metadata import np_codeocean

np_codeocean.add_rig_to_dynamic_routing_session_dir(
    pathlib.Path("/session/directory"),
    pathlib.Path("/directory/to/store/rigs"),
)
```

# Local development

## Testing
Testing intended for cloned project from source control.

### Unit tests
```bash
pdm run pytest
```

### Storage tests
```bash
pdm run pytest-storage
```

### Onprem tests
Requires user to likely be on prem with np group dependencies installed.

Install np group dependencies 
```bash
pdm install -G np
```

Run tests
```bash
pdm run pytest-onprem
```

### All tests
Requires dependencies from onprem.
```bash
pdm run pytest-full
```

# Development
See instructions in https://github.com/AllenInstitute/np-aind-metadata/CONTRIBUTING.md and the original template: https://github.com/AllenInstitute/copier-pdm-npc/blob/main/README.md