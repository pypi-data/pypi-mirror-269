# linuxsysstat 
Linux System Statistics


# How to upload to pypi.org
- Note: We need a API token, if forgotten then create one in the pypi.org

# Confirm if the poetry can build the venv in local project directory using
```
$ poetry config ---list

# if not then
$ poetry config virtualenvs.in-project=true
```

# Poetry initilization
```
poetry init
```

# Build and Publish using Poetry
```bash
$ poetry build
$ poetry publish
```

- Once uploaded the package
```bash
$ pip install sysinfo
$ sysinfo
```

# Upgrade
- Make changes to code as needed
```bash
# Bump up the version e.g: 0.1.1
$ poetry version <bump> 
$ poetry publish --build
```

