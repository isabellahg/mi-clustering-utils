## summary.py: Generador de Métricas y Gráficos

Este script en Python está diseñado para procesar y analizar datos de clustering, generar métricas promedio y visualizaciones, y consolidar los resultados en un archivo Excel y un informe en formato PDF.

## Funcionalidades

- Lectura de múltiples archivos CSV para recopilar datos de ejecuciones de algoritmos de clustering.
- Filtrado y promediado de métricas basadas en diferentes configuraciones y algoritmos.
- Generación de un archivo Excel con resúmenes y datos detallados.
- Creación de gráficos de cajas para cada métrica y algoritmo.
- Consolidación de gráficos en un informe PDF.

## Requisitos

Para ejecutar este script, asegúrate de tener instalados los siguientes paquetes de Python:

- pandas
- numpy
- matplotlib
- seaborn
- shutil
- os
- re

## Estructura del Directorio

- `to-generate`: Contiene los directorios `seeds` y `no-seeds` con archivos CSV.
- `generated-summary`: Directorio donde se guarda el resumen en Excel y los gráficos.
  - `plots`: Subdirectorio para los gráficos generados.

## Uso

1. Coloca tus archivos CSV en los directorios correspondientes dentro de `to-generate`.
2. Ejecuta el script. Esto generará un archivo Excel y un informe PDF en el directorio `generated-summary`.

## Detalles de Implementación

- `get_all_executions(dir)`: Lee y combina datos de múltiples archivos CSV.
- `filter_bad_executions(df)`: Filtra ejecuciones basadas en criterios específicos.
- `create_excel_with_sheets(dataframe, average_results, output_excel_path)`: Crea un archivo Excel con múltiples hojas.
- `calculate_global_averages(all_executions)`: Calcula promedios globales de métricas.
- `seed_average(data)`: Calcula promedios removiendo semillas de configuraciones.
- `generate_boxplots_and_save(all_executions)`: Genera y guarda gráficos de cajas.

## Contribuciones

Si deseas contribuir o mejorar este script, siéntete libre de hacerlo. Cualquier feedback o pull request es bienvenido.
