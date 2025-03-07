# Versioning in ModMaker

ModMaker follows [Semantic Versioning 2.0.0](https://semver.org/) and uses an automated versioning system powered by GitHub Actions.

## Version Format

Versions follow the `MAJOR.MINOR.PATCH` format:

- **MAJOR**: Incremented for incompatible API changes
- **MINOR**: Incremented for new functionality in a backward-compatible manner
- **PATCH**: Incremented for backward-compatible bug fixes

## Automated Versioning

The version is automatically managed by GitHub Actions:

1. When code is merged to `develop`, the package is published to [Test PyPI](https://test.pypi.org) with the current version.
2. When code is merged to `main`, the workflow:
   - Automatically bumps the patch version
   - Creates a Git tag for the new version
   - Creates a GitHub release
   - Publishes to [PyPI](https://pypi.org)

For example, if the current version is `1.2.3` and a PR is merged to `main`, the package will be automatically published as version `1.2.4`.

## Manual Version Bumping

For significant changes, you can manually bump the version before merging to `main`:

```bash
# Install bump2version
pip install bump2version

# Bump patch version (1.2.3 -> 1.2.4)
bump2version patch

# Bump minor version (1.2.3 -> 1.3.0)
bump2version minor

# Bump major version (1.2.3 -> 2.0.0)
bump2version major
```

## Development Workflow

1. Develop features on feature branches
2. Open a PR to merge to `develop` for testing
3. When ready for a new release, merge `develop` to `main`
4. The GitHub Actions workflow will handle version bumping and publishing

## Version Files

The version is stored in:
- `pyproject.toml` (root directory)
- `modmaker/pyproject.toml` (package directory)
- `.bumpversion.cfg` (configuration for bump2version)

## Release History

All releases are documented on the [GitHub Releases page](https://github.com/yourusername/modmaker/releases) with automatically generated release notes that describe the changes since the previous release.