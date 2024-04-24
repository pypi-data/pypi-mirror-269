
from setuptools import setup, find_packages

setup(
    name='PluginSDK',
    version='0.1.0',
    packages=find_packages(),
    py_modules=['PluginSDK'],  # Explicitly include PluginSDK.py as a module
    url='https://github.com/TheD0ubleC/MusicalMoments-PluginSDK-Python/',
    license='MIT',
    author='D0ubleC',
    author_email='CC@scmd.cc',
    description='MM的插件SDK',
    install_requires=[
        'requests',
    ],
    python_requires='>=3.6',
)
