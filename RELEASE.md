# Release Process Documentation

This document describes the automated release process for the munge package.

## Overview

The munge project uses GitHub Actions to automatically publish releases to PyPI when version tags are pushed to the repository. This ensures consistent, reliable releases and reduces manual errors.

## Release Process

### 1. Prepare the Release

```bash
# Ensure you're on main and up to date
git checkout main
git pull origin main

# Check working directory is clean
git status
```

### 2. Update Version

Edit `pyproject.toml`:
```toml
[project]
version = "1.4.0"  # Update this line
```

### 3. Commit and Tag

```bash
# Commit version change
git add pyproject.toml
git commit -m "Bump version to 1.4.0"

# Create tag (must match version with 'v' prefix)
git tag v1.4.0

# Push everything
git push origin main
git push origin v1.4.0
```

## Automated Workflow Details

When a version tag is pushed, the GitHub Action performs these steps:

### 1. Validation
- ✅ Verifies tag version matches `pyproject.toml` version
- ✅ Ensures both wheel and source distributions are built correctly

### 2. Build Process
- 🏗️ Sets up Python 3.11 environment
- 🏗️ Installs uv and dependencies
- 🏗️ Builds wheel (`.whl`) and source distribution (`.tar.gz`)

### 3. Publication
- 📦 Publishes to PyPI using trusted publishing (no API keys needed)
- 🏷️ Creates GitHub Release with auto-generated release notes
- 📎 Attaches build artifacts to GitHub Release

## Prerequisites

### PyPI Trusted Publishing
The repository must be configured for PyPI trusted publishing:

1. Go to [PyPI project settings](https://pypi.org/manage/project/munge/)
2. Navigate to "Publishing" → "Add a new pending publisher"
3. Configure:
   - **Owner**: `20c`
   - **Repository name**: `munge`
   - **Workflow filename**: `release.yaml`
   - **Environment name**: (leave blank)

### Repository Permissions
- Maintainer must have push access to create tags
- Repository must have Actions enabled

## Version Guidelines

### Semantic Versioning
Follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., `1.4.0`)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Pre-release Versions
Supported formats:
- `1.4.0-alpha.1` (alpha release)
- `1.4.0-beta.2` (beta release)
- `1.4.0-rc.1` (release candidate)

## Troubleshooting

### Tag Version Mismatch
**Error**: "Tag version does not match project version"

**Solution**: Ensure the git tag exactly matches the version in `pyproject.toml`:
```bash
# If pyproject.toml has version = "1.4.0"
# Tag must be exactly "v1.4.0"
git tag v1.4.0
```

### Build Failure
**Error**: "Build artifacts missing"

**Solution**: Check the build logs in GitHub Actions for uv build errors.

### PyPI Upload Failure
**Error**: "Failed to publish to PyPI"

**Solutions**:
1. Verify trusted publishing is configured correctly
2. Ensure the version doesn't already exist on PyPI
3. Check PyPI status page for service issues

### Tag Already Exists
**Error**: "Tag already exists"

**Solution**: Use a different version number or delete the existing tag:
```bash
# Delete local tag
git tag -d v1.4.0

# Delete remote tag (careful!)
git push origin --delete v1.4.0
```

## Security Considerations

### Trusted Publishing Benefits
- ✅ No API keys stored in repository secrets
- ✅ Short-lived tokens generated per release
- ✅ Cryptographic verification of workflow identity
- ✅ Audit trail of all releases

### Access Control
- Only repository maintainers can create tags
- Workflow runs are visible and auditable
- All releases are logged in GitHub and PyPI

## Monitoring

### Release Status
Monitor releases at:
- **GitHub Actions**: https://github.com/20c/munge/actions
- **GitHub Releases**: https://github.com/20c/munge/releases
- **PyPI**: https://pypi.org/project/munge/

### Notifications
- GitHub will email tag creators about workflow status
- Releases appear in repository activity feeds
- PyPI sends confirmation emails to maintainers

## Rollback Process

If a release needs to be rolled back:

### PyPI
⚠️ **PyPI deletions are permanent and strongly discouraged**
- Contact PyPI support only for critical security issues
- Generally, publish a new patch version instead

### GitHub
```bash
# Delete GitHub release (keeps tag)
gh release delete v1.4.0

# Delete tag if necessary
git tag -d v1.4.0
git push origin --delete v1.4.0
```

## Best Practices

1. **Test Before Release**: Ensure all tests pass in CI
2. **Update Changelog**: Document changes before releasing
3. **Coordinate Team**: Notify team members of releases
4. **Monitor After Release**: Check PyPI and test installation
5. **Semantic Versioning**: Follow semver strictly
6. **Security Updates**: Release security fixes promptly

## Support

For issues with the release process:
1. Check GitHub Actions logs
2. Review this documentation
3. Open an issue in the repository
4. Contact repository maintainers