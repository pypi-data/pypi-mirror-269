import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imap_box_up",
    version="0.0.4",
    author="porter",
    author_email="porter.pan@outlook.com",
    description="High-resolution map visualization and conversion tool, opendrive hdmap convert to appollo base map!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/porterpan/imap_box_up",
    project_urls={
        "Bug Tracker": "https://github.com/porterpan/imap_box_up/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    install_requires=[
        'protobuf<=3.19.4',
        'matplotlib',
        'pyproj',
        'record_msg<=0.1.1',
        'concave-hull<=0.0.7',
        'scipy<=1.13.0',
    ],
    entry_points={
        'console_scripts': [
            'imap_box_up = imap.main:main',
        ],
    },
    python_requires=">=3.6",
)
