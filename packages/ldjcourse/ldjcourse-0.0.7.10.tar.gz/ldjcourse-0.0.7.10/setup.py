from setuptools import setup, find_packages

VERSION = '0.0.7.10'

setup(
    name='ldjcourse',
    version=VERSION,
    author='元蓝先生',
    description='B站：元蓝先生 https://space.bilibili.com/3546564903569609',
    license='MIT',

    packages=find_packages()
)

# 打包
# python setup.py sdist

# 上传
# twine upload dist/*

'''
pypi-AgEIcHlwaS5vcmcCJDQzOTg2NzQwLWI2ZDktNGE4Zi05MGRmLWRmMzM2Y2QzYjFlMQACEVsxLFsibGRqY291cnNlIl1dAAIsWzIsWyI5ZDdjMjczNy1kMTlhLTQyMWYtOTRjZC05OTdlOGY2NDJkM2IiXV0AAAYgxNoAqXcDpDpylxHqj1l8UvSpg9oegUFPrQ9AMNCV-wg

'''