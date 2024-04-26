# main.py
import argparse
import os
import shutil
import subprocess
from .version import __version__

def copy_app_directory():
    # Obtener la ruta absoluta de la carpeta 'app' dentro del paquete
    package_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(package_dir, 'app')
    
    # Copiar el directorio 'app' al directorio actual
    shutil.copytree(app_dir, './app')

def install_dependencies():
    # Ejecutar npm install en el directorio actual
    subprocess.run(['cd', 'app'])
    subprocess.run(['npm', 'install'])

def main():
    parser = argparse.ArgumentParser(description='Tests Web Linda')
    parser.add_argument('--dependencies', action='store_true', help='Copy app directory and install dependencies')
    parser.add_argument('--version', action='store_true', help='Show version')
    args = parser.parse_args()

    if args.dependencies:
        copy_app_directory()
        print('App directory copied successfully.')
        install_dependencies()
        print('Npm dependencies installed successfully.')
    elif args.version:
        print(f'Version: {__version__}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

