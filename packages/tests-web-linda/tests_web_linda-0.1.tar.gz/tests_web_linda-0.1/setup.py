from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
from install import *

class CustomInstallCommand(install):
    """Customized setuptools install command which uses the function from install.py to copy the 'app' directory."""
    def run(self):
        install.run(self)
        copy_app_directory()
        subprocess.run(["cd", "app"])
        install_and_check(get_npm_path())

setup(
    name='tests_web_linda',
    version='0.1',
    description='A simple functional test library using Selenium and Chrome driver',
    author='Linda Lopez',
    packages=find_packages(),
    cmdclass={
        'install': CustomInstallCommand,
    },
    install_requires=[
        "allure-behave==2.13.4",
        "allure-python-commons==2.13.4",
        "behave==1.2.6",
        "behave-html-formatter==0.9.10",
        "behave2cucumber==1.0.3",
        "docxcompose==1.4.0",
        "docxtpl==0.16.8",
        "playwright==1.42.0",
        "psutil==5.9.2",
        "PyPDF2==3.0.1",
        "python-docx==1.1.0",
        "pycparser==2.21",
        "screeninfo==0.8",
        "selenium==4.1.3",
        "webdriver-manager==4.0.1",
        "webdrivermanager==0.10.0",
        "keyboard==0.13.5"
    ],
    include_package_data=True,  # Esto hace que setuptools lea el archivo MANIFEST.in
    entry_points={
        'console_scripts': [
            'python_tests_web=python_tests_web.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
)