# munge

[![PyPI](https://img.shields.io/pypi/v/munge.svg?maxAge=3600)](https://pypi.python.org/pypi/munge)
[![PyPI](https://img.shields.io/pypi/pyversions/munge.svg?maxAge=600)](https://pypi.python.org/pypi/munge)
[![Tests](https://github.com/20c/munge/workflows/tests/badge.svg)](https://github.com/20c/munge)
[![Release](https://github.com/20c/munge/actions/workflows/release.yaml/badge.svg)](https://github.com/20c/munge/actions/workflows/release.yaml)
[![Codecov](https://img.shields.io/codecov/c/github/20c/munge/main.svg?maxAge=3600)](https://codecov.io/github/20c/munge?branch=main)

data manipulation library and client

## Release Process

This project uses **automated PyPI releases** triggered by version tags. No local scripts needed!

### How to Release

1. **Update Version in `pyproject.toml`**:
   ```toml
   [project]
   version = "1.4.0"  # Update this line
   ```

2. **Commit the Version Change**:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 1.4.0"
   git push origin main
   ```

3. **Create and Push Tag** (triggers release):
   ```bash
   git tag v1.4.0
   git push origin v1.4.0
   ```

### Automated Release Process
When you push a version tag, GitHub Actions automatically:
- ✅ **Validates** tag version matches `pyproject.toml`
- ✅ **Builds** Python package (wheel + source distribution)
- ✅ **Publishes** to PyPI using trusted publishing (no API keys!)
- ✅ **Creates** GitHub Release with auto-generated release notes
- ✅ **Attaches** build artifacts to the release

### Alternative: GitHub Web Interface
You can also create tags through GitHub's web interface:
1. Go to https://github.com/20c/munge/releases
2. Click "Create a new release"
3. Enter tag (e.g., `v1.4.0`) and release title
4. Click "Publish release" → triggers automated PyPI release

### Detailed Documentation
For troubleshooting and advanced options, see [RELEASE.md](RELEASE.md).

## Changes

The current change log is available at <https://github.com/20c/munge/blob/main/CHANGELOG.md>


## License

Copyright 2015-2021 20C, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this softare except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.