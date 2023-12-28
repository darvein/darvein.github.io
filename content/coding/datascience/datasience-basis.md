# Datascience basis

## Intro
Data VS Big Data!!! ---> Se trata de las mismas ideas y objetivos aplicadas a 2 situaciones:
* cuando el volumen, la velocidad, la variedad, la veracidad/confiabilidad, y el valor del corpus de datos en uso son manejables dentro de los parámetros básicos en cuanto a infraestructura lógica y técnicas de procesamiento
* cuando el volumen, la velocidad, la variedad, la veracidad/confiabilidad, y el valor del corpus de datos en uso son tales (en un caso o en los cinco) que hacen necesario el despliegue, operaciones y procesamiento en un ecosistema distribuido

## Steps:

En la práctica estos pasos no son lineales e incrementales, sino q pueden ser iterativos o simultáneos ...como puede verse, los pasos 1 y 2 corresponden a lo q normalmente se entiende como Data Engineering, en tanto q los pasos 3 al 6 son más bien lo q corresponde al Data Scientist como tal. Sin embargo es fundamental tener presente el hecho de que, según [reporte de Anaconda](https://www.anaconda.com/state-of-data-science-2020), al 2020 las tareas de preparación de datos continúan consumiendo al menos el 45% del tiempo (hasta el doble, en casos extremos) del Data Scientis. Por ello se considera de importancia la comprensión no sólo de DS, sino también de Data Engineering

1. Obtaining data
2. Cleaning/Scrubbing data
3. Exploring data
4. Modeling data
5. Interpreting data
6. Reporting/Communicating data products

![Data Science Process](./data_sci_process.jpeg "Data Science Process")

### Data Science VS Data Engineering
Data Science VS Data Engineering ---> Ambos se complementan. Ambos necesitan base en análisis, programación, y Big Data.
* Data Engineer: Mucho más avanzado en programación y software tooling, e infraestructuras distribuidas. Su input es el Raw Data (múltiple, no estructurado, messy) de los diversos Business Systems. Su output serían las Data Pipelines.
* Data Scientist: Mucho más avanzado en recursos/tooling cuantitativos (Matemática, Estadística) y métodos científicos, Machine Learning, y Modeling/Analytics. Su input serían las Data Pipelines. Su output serían los Data Products.

### Lógica del Análisis Cuantitativo, y algunas de las técnicas principales
1. Descubrir estructura en el corpus de datos (que normalmente es muy grande y sin orden aparente), así como extraer factores clave del mismo. Cómo se ve la data y qué información contiene. Aprendizaje no supervisado: Clustering, Análisis de Componentes Principales PCA.
2. Podemos modelizar la data como una relación de función (regresión)? Podemos usar datos continuos para realizar predicciones?. Aprendizaje Supervisado: Regresión Lineal, Inferencia, Regresión No Lineal, Causalidad.
3. Podemos modelizar la data como una relación de función (test de hipótesis y clasificación)? Podemos usar datos discretos para realizar predicciones?. Test de Hipótesis, Intervalos de Confianza, Estimación de Probabilidad, Clasificadores SVM y Perceptrones, Regresión Logística.
