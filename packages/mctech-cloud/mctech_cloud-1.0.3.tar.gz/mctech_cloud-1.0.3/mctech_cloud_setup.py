from setuptools import setup, find_packages

setup(
    name="mctech_cloud",
    version="1.0.3",
    packages=find_packages(
        include=["mctech_cloud*"],
        exclude=["*.test"]
    ),
    install_requires=["log4py", "fastapi", "starlette",
                      "mctech-actuator", "mctech-discovery"]
)
