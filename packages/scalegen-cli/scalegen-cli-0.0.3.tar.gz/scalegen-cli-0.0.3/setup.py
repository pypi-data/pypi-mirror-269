from setuptools import setup, find_packages
import os
import requests
from distutils.version import LooseVersion


def versions(package_name, limit_releases=10):
    url = f"https://pypi.org/pypi/{package_name}/json"
    data = requests.get(url).json()
    versions = list(data["releases"].keys())
    versions.sort(key=LooseVersion, reverse=True)
    return versions[:limit_releases]


# application_version = os.environ.get("APP_VERSION", "0.0.0")
application_version = "0.0." + str(int(versions("scalegen-cli")[0].split(".")[2]) + 1)

with open("requirements.txt", "r") as fp:
    reqs = [line.strip("\n") for line in fp]

binary = "scaletorch"
if os.environ.get("PRODUCT_TYPE", "scaletorch") == "scalegen":
    binary = "scalegen"

setup(
    name=f"scalegen-cli",
    version=application_version,
    description="ScaleGenAI CLI",
    long_description="ScaleGenAI command line application",
    url="https://github.com/ScaleTorch/st-cli",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6, <3.12",
    install_requires=reqs,
    entry_points={"console_scripts": [f"{binary} = st_cli:cli"]},
)
