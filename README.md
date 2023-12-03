# Scripts

## epsilon-refinement

Este script en Python está diseñado para analizar y refinar los parámetros de configuración de algoritmos de clustering, específicamente el valor de epsilon, basado en los resultados de ejecuciones iniciales.

### Funcionalidades

- Análisis de resultados de clustering para identificar configuraciones que requieren ajuste.
- Ajuste automático del valor de epsilon para mejorar la formación de clusters.
- Generación de nuevas configuraciones de clustering basadas en el análisis.

### Requisitos

Para ejecutar este script, asegúrate de tener instalados los siguientes paquetes de Python:

- pandas
- numpy
- os
- re

### Estructura del Script

El script consta de varias funciones clave:

- `get_new_config(configuration, scale)`: Ajusta el valor de epsilon en la configuración dada, según el factor de escala proporcionado.
- `refine_epsilon()`: Lee los resultados de clustering de un archivo CSV, analiza el número de clusters formados, y refina el valor de epsilon según sea necesario.

### Uso

1. Define la variable `INITIAL_RUNS` con la ruta al archivo CSV que contiene los resultados de tus ejecuciones de clustering.
2. Ejecuta el script. Esto analizará los resultados y generará configuraciones ajustadas.

### Proceso de Afinación

El script realiza los siguientes pasos:

1. Lee los resultados de clustering de un archivo CSV.
2. Analiza cada configuración en función del número de clusters formados.
3. Ajusta el valor de epsilon:
   - Si el número de clusters es menor que 2, reduce el valor de epsilon.
   - Si el número de clusters es mayor que 2, aumenta el valor de epsilon.
4. Genera y muestra las nuevas configuraciones.


## summary.py: Generador de Métricas y Gráficos

Este script en Python está diseñado para procesar y analizar datos de clustering, generar métricas promedio y visualizaciones, y consolidar los resultados en un archivo Excel y un informe en formato PDF.

### Funcionalidades

- Lectura de múltiples archivos CSV para recopilar datos de ejecuciones de algoritmos de clustering.
- Filtrado y promediado de métricas basadas en diferentes configuraciones y algoritmos.
- Generación de un archivo Excel con resúmenes y datos detallados.
- Creación de gráficos de cajas para cada métrica y algoritmo.
- Consolidación de gráficos en un informe PDF.

### Requisitos

Para ejecutar este script, asegúrate de tener instalados los siguientes paquetes de Python:

- pandas
- numpy
- matplotlib
- seaborn
- shutil
- os
- re

### Estructura del Directorio

- `to-generate`: Contiene los directorios `seeds` y `no-seeds` con archivos CSV.
- `generated-summary`: Directorio donde se guarda el resumen en Excel y los gráficos.
  - `plots`: Subdirectorio para los gráficos generados.

### Uso

1. Coloca tus archivos CSV en los directorios correspondientes dentro de `to-generate`.
2. Ejecuta el script. Esto generará un archivo Excel y un informe PDF en el directorio `generated-summary`.

### Detalles de Implementación

- `get_all_executions(dir)`: Lee y combina datos de múltiples archivos CSV.
- `filter_bad_executions(df)`: Filtra ejecuciones basadas en criterios específicos.
- `create_excel_with_sheets(dataframe, average_results, output_excel_path)`: Crea un archivo Excel con múltiples hojas.
- `calculate_global_averages(all_executions)`: Calcula promedios globales de métricas.
- `seed_average(data)`: Calcula promedios removiendo semillas de configuraciones.
- `generate_boxplots_and_save(all_executions)`: Genera y guarda gráficos de cajas.
