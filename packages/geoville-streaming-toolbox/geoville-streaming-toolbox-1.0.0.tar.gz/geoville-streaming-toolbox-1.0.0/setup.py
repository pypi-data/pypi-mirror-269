from setuptools import find_packages, setup


setup(
    name='geoville-streaming-toolbox',
	version="1.0.0",
    packages=find_packages(exclude=["src/tests", "*tests.py"]),
    url='',
    author='Johannes Schmid',
    author_email='schmid@geoville.com',
    description='GeoVille`s toolbox for extracting time frames from '
                'online accessible satellite streams.',
    install_requires=['pyyaml>=5.3.1',
                      'requests>=2.22.0',
                      'pyproj>=3.3.0',
                      'ffmpeg-python==0.2.0']
)
