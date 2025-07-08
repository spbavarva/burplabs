from setuptools import setup, find_packages

setup(
    name='portswiggerlab',
    version='0.1',
    description='PortSwigger Web Security Academy Automation CLI',
    author='Sneh',
    packages=find_packages(include=["portswiggerlab", "portswiggerlab.*"]),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'portswiggerlab=portswiggerlab.cli:main',
        ],
    },
    include_package_data=True,
)
