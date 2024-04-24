from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A Python Library for Efficient MPU6050 DMP Access.'
LONG_DESCRIPTION = 'This library aims to simplify the use of digital motion processor (DMP) inside inertial motion unit (IMU), along with other motion data.'

# Setting up
setup(
    name="mpu6050",
    version=VERSION,
    author="Majid Alekasir",
    author_email="<majid.alekasir@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['quat'],
    keywords=['python', 'quaternion', 'vector', 'XYZVector', 'IMU', 'DMP', 'INS', 'Accelometer', 'Gyrometer', 'MPU6050', 'Fusion', 'EKF', 'Kalman Filter'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)