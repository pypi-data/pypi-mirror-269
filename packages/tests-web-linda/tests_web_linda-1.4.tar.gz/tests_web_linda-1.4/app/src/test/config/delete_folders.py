import os
import shutil

def delete_folders():
    folders = ["allure-report", "allure-results", "screenshots", "Evidencias"]
    for folder in folders:
        try:
            shutil.rmtree(folder)
            print(f"La carpeta '{folder}' ha sido eliminada exitosamente.")
        except FileNotFoundError:
            print(f"La carpeta '{folder}' no existe.")

if __name__ == "__main__":
    delete_folders()