import json
from setuptools import setup, find_packages

with open('package.json') as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    packages=find_packages(),
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    install_requires=[
        'dash>=2.0.0',
    ],
    classifiers=[
        'Framework :: Dash',
    ],
)
