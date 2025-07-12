from setuptools import setup, find_packages

setup(
    name='burplabs',
    version='0.1',
    description='PortSwigger Web Security Academy Automation CLI',
    author='Sneh',
    packages=find_packages(include=["burplabs", "burplabs.*"]),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'burplabs=burplabs.cli:main',
        ],
    },
    include_package_data=True,
)
