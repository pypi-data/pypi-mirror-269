import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noaaco2",
    version="0.0.4",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="A package for displaying co2 graph based on NOAA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y-takefuji/noaaco2",
    project_urls={
        "Bug Tracker": "https://github.com/y-takefuji/noaaco2",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['noaaco2'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'noaaco2 = noaaco2:main'
        ]
    },
)
