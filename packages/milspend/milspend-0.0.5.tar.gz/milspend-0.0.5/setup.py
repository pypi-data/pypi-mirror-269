import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="milspend",
    version="0.0.5",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="A package for visualizing military spending of up to 4 countries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y-takefuji/defense",
    project_urls={
        "Bug Tracker": "https://github.com/y-takefuji/defense",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['milspend'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'milspend = milspend:main'
        ]
    },
)
