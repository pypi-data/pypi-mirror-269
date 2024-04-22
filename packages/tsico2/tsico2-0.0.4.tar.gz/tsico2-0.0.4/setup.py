import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tsico2",
    version="0.0.4",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="A package for visualizing TSI and CO2 with r2 and p-value",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y-takefuji/tsico2",
    project_urls={
        "Bug Tracker": "https://github.com/y-takefuji/tsico2",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['tsico2'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'tsico2 = tsico2:main'
        ]
    },
)
