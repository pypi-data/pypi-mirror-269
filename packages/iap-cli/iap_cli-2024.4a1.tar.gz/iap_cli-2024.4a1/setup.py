import pathlib

import setuptools

setuptools.setup(
    name="iap_cli",
    version="2024.4a1",
    description="Lightweight CLI tool to simplify the process of interacting with the Itential Automation Platform.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/awetomate/itential-iap-cli",
    author="John Frauchiger",
    author_email="john@awetomate.net",
    license="MIT",
    project_urls={
        "Documentation": "https://github.com/awetomate/itential-iap-cli",
        "Source": "https://github.com/awetomate/itential-iap-cli",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities"
    ],
    python_requires=">=3.9,<3.12",
    install_requires=[
        "iap-sdk",
        "pydantic >=2.5.0, <3.0.0",
        "python-dotenv",
        "typer==0.7.0",
        "typer-cli==0.0.13",
        "colorama >=0.4.3,<0.5.0",
        "shellingham >=1.3.0,<2.0.0",
        "rich >=10.11.0,<14.0.0"
    ],
    setup_requires=['setuptools-git-versioning'],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'iap = iap_cli:iap',
        ]
    },
    include_package_data=True,
)
