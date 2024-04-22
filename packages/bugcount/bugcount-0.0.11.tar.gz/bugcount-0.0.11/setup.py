import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bugcount",
    version="0.0.11",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="A package for counting BLOB objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y-takefuji/counting-for-entomologists",
    project_urls={
        "Bug Tracker": "https://github.com/y-takefuji/counting-for-entomologists",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['bugcount'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'bugcount = bugcount:main'
        ]
    },
)
