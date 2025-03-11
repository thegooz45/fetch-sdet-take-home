from setuptools import setup, find_packages

setup(
    name="geoloc_util",
    version="1.0",
    packages=find_packages(where="srs"),
    package_dir={"": "src"},
    install_requires=["requests", "argparse"],
    entry_points={
        "console_scripts": [
            "geoloc_util = geoloc_util:main"
        ],
    },

    author="brianna guzman",
    description="a utility to fetch the coordinates for a given location using OpenWeatherMap's API",
    python_requires=">=3.6",
)