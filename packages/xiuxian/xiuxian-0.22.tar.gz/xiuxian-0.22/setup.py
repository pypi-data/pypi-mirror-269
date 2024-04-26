from setuptools import setup,find_namespace_packages,find_packages

setup(
name='xiuxian',
version='0.22',
description='修仙数据包',
#long_description=open('README.md','r').read(),
author='luoyefufeng',
author_email='2859385794@qq.com',
license='MIT license',
include_package_data=True,
packages=find_namespace_packages(include=["xiuxian"]),
platforms='all',
install_requires=[""],
url='https://github.com/luoyefufeng/nonebot_plugin_simulator_xiuxian',
)


