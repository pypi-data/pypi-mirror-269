from setuptools import setup, find_packages
import os

application_version = os.environ.get("APP_VERSION", "0.0.0")

with open("requirements.txt", "r") as fp:
    reqs = [line.strip("\n") for line in fp]

binary = "scaletorch"
if os.environ.get("PRODUCT_TYPE", "scaletorch") == "scalegen":
    binary = "scalegen"

setup(
    name=f"scalegen-cli",
    version=application_version,
    description="ScaleTorch CLI",
    long_description="Scalegen command line application",
    url="https://github.com/ScaleTorch/st-cli",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6, <3.12",
    install_requires=reqs,
    entry_points={"console_scripts": [f"{binary} = st_cli:cli"]},
)
