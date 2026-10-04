# Práctica individual N° 2

**Caso:** tiempo de atención en la ferretería Construir a tu Alcance.
**Estudiante:** Rick Rodríguez (revisar el nombre antes de entregar).

Los 30 datos son **simulados y diseñados manualmente para esta práctica**.
No representan mediciones reales ni exportaciones del sistema de gestión.
La consigna permite proponer datos y estudiar un sistema real o simulado.

## Contenido

- `datos/datos.csv`: los 30 tiempos en minutos, separados por comas.
- `scripts/analisis.py`: programa comentado que calcula las estadísticas,
  detecta valores atípicos y genera el informe.
- `reporte/informe.txt`: informe completo con los diez apartados requeridos.
- `reporte/resultados_zscore.csv`: Z-Score y clasificación de cada cliente.
- `README.md`: estas instrucciones.

## Cómo ejecutarlo en Windows

1. Descomprimir el ZIP; no ejecutar desde dentro del archivo comprimido.
2. Abrir la carpeta del proyecto en VS Code.
3. Abrir **Terminal > Nueva terminal**, estando en la carpeta que contiene
   `datos`, `scripts`, `reporte` y este README.
4. Ejecutar:

```bash
python scripts/analisis.py
```

Si Windows reconoce Python con el comando `py`, usar:

```bash
py scripts/analisis.py
```

En Linux o macOS puede usarse `python3 scripts/analisis.py`.
Requiere Python 3.8 o posterior. No necesita instalar paquetes con pip.
Al ejecutarlo, muestra el informe y actualiza los dos archivos de `reporte`.
Los archivos ya están generados para poder leerlos sin ejecutar el programa.

## Qué significa cada cálculo

- **Media:** suma de tiempos dividida entre 30; es el promedio.
- **Mediana:** valor central de los tiempos ordenados (promedio de los dos
  centrales cuando hay 30 datos).
- **Desviación estándar:** indica cuánto varían los tiempos respecto a la media.
- **Z-Score:** `(tiempo - media) / desviacion`. Indica cuántas desviaciones
  estándar separan una atención del promedio.
- **Atípico:** en este ejercicio se señala cuando `abs(z) > 3`.

Se usa desviación estándar **muestral**, con divisor `n - 1`.
Las clasificaciones se realizan antes de redondear los resultados.
Una atención atípica se revisa; no se elimina automáticamente.

## Antes de entregar

Se utilizó Rick Rodríguez como nombre a partir del contexto del proyecto.
Si tu nombre académico es distinto, cambia `NOMBRE_ESTUDIANTE` al inicio de
`scripts/analisis.py`, actualiza este README, cambia el nombre de la carpeta
a `practica2_apPaterno_nombre` y ejecuta de nuevo el programa.
Entregar la carpeta completa o su ZIP según indique el docente.
El CSV cumple la estructura obligatoria; el Excel es una opción de la guía,
por lo que no hace falta para ejecutar ni presentar esta solución.

Si cambias los tiempos, el programa recalcula los resultados; también debes
revisar los supuestos y la interpretación para que describan tus nuevos datos.
