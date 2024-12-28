# Changelog

## 0.3.2

- Upgraded dependencies
- Updated supported Python versions

## 0.3.1

- Fix issue [#3](https://github.com/BastiTee/tolino-notes/issues/3)

## 0.3.0

- Add language support for FR, IT, NL

## 0.2.0

- Improve quote handling of highlights with notes
- Extract notes writer to separate module
- Improve type-safety
- Improve VSCode development environment

## 0.1.0

- Update README and added CHANGELOG
- Update pyproject.toml

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
