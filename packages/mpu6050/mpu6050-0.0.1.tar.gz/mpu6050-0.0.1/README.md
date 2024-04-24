# MPU6050 DMP Library
## Abstract
This library is primarily derived from the contributions of Geir Istad and has been released as a pip-installable package. This library aims to simplify the use of digital motion processor (DMP) inside inertial motion unit (IMU), along with other motion data. The main focus of this package is on providing orientaion of the device in space as quaternion, which is convertable to euler angles. The resulting data are processed and denoised using extended Kalman filter (EKF), inside the DMP module.

My main contributions to this library are towards enhancing the DMP results, detailed examples, usage description and making the library PyPI-installable. Apart from the great work done by Geir Istad, there were some issues encounterd in practice.

The enhancements are listed below:
- Quaternion to euler angles conversion (roll, pitch, yaw) enhanced using scipy library
- Linear (world-frame) acceleration rewritten using new formulas, based on quaternion
- Better access to DMP frequency
- Comprehensible, Practical examples with detailed explanation
- Available on PyPI (pip installable)

**This library is tested on Nvidia Jetson with I2C communication.**

For more details, please refer to my github repository,
[mpu6050](https://github.com/OmidAlek/mpu6050).