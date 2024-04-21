# cli

## Code formatting

Install pre-commit hooks.

```shell
pre-commit install
```

## Install
```shell
pip3 install -e .
```

## Usage
Note: Create a scaletorch.yml file
```shell
cd <your_project>
scaletorch login -ki <key-id> -ks <key-secret>
scaletorch launch
```

## Developer Notes
Set the `PLATFORM_API` environment variable before using/test the cli.
