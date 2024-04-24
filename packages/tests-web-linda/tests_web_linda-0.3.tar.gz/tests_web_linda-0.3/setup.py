from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil
import subprocess

class CustomInstallCommand(install):
    """Customized setuptools install command which uses the function from install.py to copy the 'app' directory."""
    def run(self):
        install.run(self)
        self.copy_app_directory()
        npm_path = self.get_npm_path()
        self.install_and_check(npm_path)

    def copy_app_directory(self):
        # Determina la ruta del directorio 'app' en tu paquete
        src_dir = os.path.join(os.path.dirname(__file__), "app")

        # Determina la ruta del directorio actual
        dst_dir = os.path.join(os.getcwd(), "app")

        # Copia el directorio 'app' al directorio actual
        shutil.copytree(src_dir, dst_dir)

    def get_npm_path(self):
        try:
            npm_path = subprocess.check_output('powershell "Get-Command npm | %{$_.Source}"', shell=True).decode().strip()
            return npm_path
        except subprocess.CalledProcessError as e:
            print("No se pudo encontrar la ruta a npm.")
            print(str(e))
            return None

    def install_and_check(self, npm_path):
        if npm_path is None:
            print("No se puede instalar el paquete sin una ruta válida a npm.")
            return
        try:
            subprocess.check_call([npm_path, "install"])
            print("Dependencias npm instaladas correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Hubo un error al instalar las librerías npm")
            print(str(e))


setup(
    name='tests_web_linda',
    version='0.3',
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