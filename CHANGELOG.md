# Changelog

## 0.2.0

- Improve quote handling of highlights with notes
- Extracted notes writer to separate module
- Improved type-safety
- Improve VSCode development environment

## 0.1.0

- Updated README and added CHANGELOG
- Updated pyproject.toml

## 0.0.1

- Initial version

## Release process

- Finish development on branch and merge to main
- Finalize [`CHANGELOG.md`](CHANGELOG.md), bump version number in [`pyproject.toml`](pyproject.toml) and commit
- Do a full build running `make build`
- Run

```shell
VERSION=$( poetry version --short ) &&\
echo "Release: ${VERSION}" &&\
git tag -a ${VERSION} -m "Version ${VERSION}" &&\
git push --tags
```

- Create a new release under <https://github.com/BastiTee/tolino-notes/releases> and link to changelog
- Publish to pypi running `poetry publish -u user-name -p "..."`
