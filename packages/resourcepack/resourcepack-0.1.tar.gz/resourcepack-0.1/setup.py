from setuptools import find_packages, setup

setup(
    name="resourcepack",
    version="0.1",
    packages=find_packages(),
    description="Basic python functions to connect to databases and other essential stuff.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Patrick Lucescu",
    author_email="patricklucescu@outlook.com",
    license="MIT",
    install_requires=["pandas", "clickhouse_driver"],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.11",
)
