## Importante configurar el PATH del sistema con los drivers para que funcione bien el UTIL_WEB

## Para ejecutar los sctripts mediante los features:
`behave --tags=Prueba1`

## Para generar el reporte allure:
`allure generate`

## Para visualizar el reporte: 
`allure open`

## Puedes ejecutar todas las lineas en una sola:
`behave --tags=Prueba1 ; allure generate ; allure open`

## Server http para reporte en cualquier:
`python -m http.server 8000`


## Se agregan mas detalles a allure: 
`behave --tags=Prueba1 ; cp environment.properties allure-results/ ; allure generate ; allure open`

## Generar un archivo de requisitos que incluya todas las dependencias instaladas en tu entorno actual:
`pip freeze > requirements.txt`

## Para instalar todos los Prerequisitos:
`pip install -r requirements.txt` 

## Ejecutar con word:
`behave --tags=Prueba1; python ./src/test/library/generate_word_v2.py`