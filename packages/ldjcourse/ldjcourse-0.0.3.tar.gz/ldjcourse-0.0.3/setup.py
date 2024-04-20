from setuptools import setup, find_packages

VERSION = '0.0.3'

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