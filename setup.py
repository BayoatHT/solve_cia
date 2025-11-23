# Update the setup.py file
from setuptools import setup, find_packages


def read_requirements():
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as file:
            requirements = file.read().splitlines()
        install_requires = []
        for req in requirements:
            req = req.strip()
            if req and not req.startswith('#'):
                if '==' in req:
                    install_requires.append(req.split('==')[0].strip())
                else:
                    install_requires.append(req)
        return install_requires
    except FileNotFoundError:
        return []


setup(
    name="proj_004_cia",
    version="0.1.0",
    description="CIA World Factbook data extraction and processing toolkit",
    author="Bayo",

    # FIXED: Map the proj_004_cia package to the proj_004_cia directory
    package_dir={'proj_004_cia': 'proj_004_cia'},

    # FIXED: Tell find_packages to look for the proj_004_cia package in the proj_004_cia directory
    packages=['proj_004_cia'] + ['proj_004_cia.' + pkg for pkg in find_packages(where='proj_004_cia', exclude=[
        "__config*",
        "__logger*",
        "_raw_data*",
        "_data_per_category*",
        "_data_per_country*",
        "analysis_folder*",
        "*.egg-info*"
    ])],

    include_package_data=True,
    install_requires=read_requirements(),
    python_requires=">=3.8",
)
