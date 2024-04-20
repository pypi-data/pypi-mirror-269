# Building a package to release

### Install Dependencies

```shell
python3 -m pip install --upgrade pip
pip install --upgrade setuptools build twine
```

### Tag release

```shell
git tag v0.1
git push origin v0.1
```

### Build a distribution (for releases, do this on main with a fresh tag)

```shell
python3 -m build
```

### To first test release that package

```shell
twine upload --repository testpypi dist/*
```

### To formally release that package

```shell
twine upload dist/*
```

### To see what the current version will be

```shell
python -m setuptools_scm
```
