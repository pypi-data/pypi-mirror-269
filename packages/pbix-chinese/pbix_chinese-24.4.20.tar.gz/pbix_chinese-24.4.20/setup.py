from distutils.core import setup
import setuptools

packages = ['pbix_chinese']
setup(name='pbix_chinese',
      version='24.4.20',
      author='xigua, 刷新Power bi desktop(支持2023.09月及之前版本)',
      packages=packages,
      package_dir={'requests': 'requests'}, )
