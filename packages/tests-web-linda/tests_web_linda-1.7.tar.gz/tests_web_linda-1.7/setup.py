from setuptools import setup, find_packages
from setuptools.command.install import install

setup(
    name='tests_web_linda',
    version='1.7',
    description='A simple functional test library using Selenium and Chrome driver',
    author='Linda Lopez',
    packages=find_packages(),
    include_package_data=True, #Esto hace que setuptools lea el archivo MANIFEST.in
    package_data={
        'tests_web_linda': ['app/*'],
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
    entry_points={
        'console_scripts': [
            'tests_web_linda=tests_web_linda.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
)