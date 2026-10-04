"""Práctica 2: análisis de tiempos SIMULADOS de atención en una ferretería.

Ejecutar: python scripts/analisis.py
Solo utiliza módulos incluidos en Python 3; no requiere pip.
"""

import csv
import math
import statistics
from pathlib import Path


NOMBRE_ESTUDIANTE = "Rick Rodríguez"
UMBRAL_Z = 3.0  # Se considera atípico si abs(z) > 3.
BASE = Path(__file__).resolve().parent.parent


def main():
    # 1. Leer los datos. Las rutas funcionan aunque se ejecute desde otra carpeta.
    with (BASE / "datos" / "datos.csv").open(encoding="utf-8-sig", newline="") as archivo:
        registros = list(csv.DictReader(archivo))

    if len(registros) < 30:
        raise ValueError("La práctica requiere al menos 30 observaciones.")
    ids = [int(fila["id_cliente"]) for fila in registros]
    tiempos = [float(fila["tiempo_atencion_min"]) for fila in registros]
    if len(set(ids)) != len(ids):
        raise ValueError("Los identificadores de clientes no deben repetirse.")
    if any(not math.isfinite(t) or t <= 0 for t in tiempos):
        raise ValueError("Los tiempos deben ser números finitos mayores que cero.")

    # 2. Estadísticos. Se utiliza desviación MUESTRAL: divisor n - 1.
    n = len(tiempos)
    media = statistics.mean(tiempos)
    mediana = statistics.median(tiempos)
    desviacion = statistics.stdev(tiempos)
    varianza = statistics.variance(tiempos)
    minimo, maximo = min(tiempos), max(tiempos)
    modas = statistics.multimode(tiempos)
    moda_texto = (
        "No hay moda: todos los valores aparecen una sola vez."
        if len(modas) == n else "; ".join(f"{m:.2f} min" for m in modas)
    )

    # 3. Z-Score: distancia del dato a la media en desviaciones estándar.
    # Si todos los tiempos fueran iguales, se asigna z=0 y no hay atípicos.
    puntajes_z = [(t - media) / desviacion if desviacion else 0.0 for t in tiempos]
    atipicos = [
        (identificador, t, z)
        for identificador, t, z in zip(ids, tiempos, puntajes_z)
        if abs(z) > UMBRAL_Z
    ]

    # 4. Guardar el cálculo de cada cliente para poder revisarlo.
    destino = BASE / "reporte"
    destino.mkdir(parents=True, exist_ok=True)
    with (destino / "resultados_zscore.csv").open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["id_cliente", "tiempo_atencion_min", "z_score", "es_atipico"])
        for identificador, t, z in zip(ids, tiempos, puntajes_z):
            escritor.writerow([identificador, f"{t:.2f}", f"{z:.6f}", "SI" if abs(z) > UMBRAL_Z else "NO"])

    detalle_atipicos = "\n".join(
        f"- Cliente {identificador}: {t:.2f} min; Z-Score = {z:.4f}."
        for identificador, t, z in atipicos
    ) or "No se detectaron valores atípicos con el criterio establecido."
    normales = [t for t, z in zip(tiempos, puntajes_z) if abs(z) <= UMBRAL_Z]
    comparacion = ""
    if atipicos and normales:
        comparacion = (
            f"Como comparación exploratoria, la media de los {len(normales)} tiempos\n"
            f"no señalados es {statistics.mean(normales):.4f} min y su desviación\n"
            f"muestral es {statistics.stdev(normales):.4f} min. Esta comparación no\n"
            "elimina observaciones del análisis principal ni recalcula los atípicos.\n"
        ) if len(normales) > 1 else ""

    # 5. Informe con los diez apartados obligatorios de la consigna.
    informe = f"""PRÁCTICA INDIVIDUAL N° 2
Formulación y análisis preliminar de un sistema real o simulado

1. NOMBRE DEL ESTUDIANTE
{NOMBRE_ESTUDIANTE}

2. TÍTULO DEL CASO
Análisis preliminar del tiempo de atención de clientes en la ferretería
Construir a tu Alcance, mediante datos simulados.

3. FORMULACIÓN DEL PROBLEMA
La ferretería atiende pedidos de distinta complejidad. Conocer cuánto dura
la atención permite describir el servicio e identificar operaciones que
merecen revisión por su duración inusual.
Pregunta de estudio: ¿cuál es el comportamiento del tiempo de atención y
qué observaciones presentan una duración atípica según el Z-Score?
Objetivo: analizar {n} tiempos propuestos, calcular estadísticos descriptivos
y detectar observaciones atípicas. No se evalúa todo el sistema de gestión.
Alcance: atención en mostrador, desde que el vendedor inicia la atención
hasta que termina de registrar la venta o cotización. Se excluyen espera
en fila, preparación en almacén y entrega de mercadería.

4. VARIABLE PRINCIPAL
Nombre: tiempo_atencion_min.
Definición: duración de la atención de un cliente.
Tipo: cuantitativa continua, registrada con una cifra decimal.
Unidad: minutos. Unidad de observación: una atención a un cliente.
id_cliente solo identifica la observación; no es la variable de estudio.

5. SUPUESTOS
- Los {n} datos son SIMULADOS y propuestos para fines académicos. No provienen
  de mediciones reales ni de registros del sistema de la ferretería.
- Los valores se diseñaron manualmente: atenciones habituales de pocos
  minutos y una atención más larga para ilustrar el método.
- Se supone una misma definición de inicio y fin para todos los clientes.
- Se supone que las observaciones son independientes y las condiciones
  generales comparables; estos supuestos no se verificaron en campo.
- Se usa desviación estándar muestral (divisor n - 1).
- El criterio es |Z| > {UMBRAL_Z:.0f}. Es una regla exploratoria: no demuestra
  que el dato sea erróneo ni establece por sí sola una causa.
- No se ha demostrado normalidad; la regla Z debe interpretarse con cautela,
  especialmente porque los tiempos de servicio pueden ser asimétricos.

6. ESTADÍSTICOS DESCRIPTIVOS
Cantidad de observaciones: {n}.
Media: {media:.4f} min.
Mediana: {mediana:.4f} min.
Moda: {moda_texto}
Mínimo: {minimo:.4f} min.
Máximo: {maximo:.4f} min.
Rango (máximo - mínimo): {maximo - minimo:.4f} min.
Varianza muestral: {varianza:.4f} min².
Desviación estándar muestral: {desviacion:.4f} min.
Coeficiente de variación: {100 * desviacion / media:.2f} %.
Los cálculos usan todos los datos y se realizan sin redondear previamente.

7. VALORES ATÍPICOS DETECTADOS CON Z-SCORE
Fórmula: Z_i = (x_i - media) / desviación estándar muestral.
Criterio aplicado: un dato se señala cuando |Z_i| > {UMBRAL_Z:.0f}.
Cantidad detectada: {len(atipicos)} ({100 * len(atipicos) / n:.2f} % de las observaciones).
{detalle_atipicos}
El archivo resultados_zscore.csv contiene el cálculo de cada observación.
Los datos señalados se conservan en los estadísticos principales.

8. ANÁLISIS DESCRIPTIVO DE LA VARIABLE
El promedio de atención es {media:.2f} min y la mediana es {mediana:.2f} min.
La mediana divide los tiempos ordenados en dos mitades y representa una
referencia del centro menos sensible a duraciones extremas.
La diferencia entre media y mediana, junto con los tiempos más altos,
sugiere asimetría hacia duraciones largas en este conjunto propuesto.
El rango es {maximo - minimo:.2f} min y la desviación estándar es {desviacion:.2f} min.
{comparacion}
9. INTERPRETACIÓN TÉCNICA
Las observaciones señaladas por Z-Score requieren revisión si aparecieran
en registros reales. Una atención extensa podría relacionarse con pedidos
complejos, consultas de precios, descuentos o dificultades de registro;
son hipótesis y no causas demostradas por estos datos.
Para investigar, se propone registrar también cantidad de artículos,
tipo de operación e incidencias, sin cambiar la variable principal.
El análisis sirve como ejemplo de cómo el sistema de gestión podría
apoyar el seguimiento del servicio si registrara su inicio y fin.
No permite determinar tiempos de espera, capacidad de atención ni
saturación, porque no incluye llegadas de clientes ni número de vendedores.
Se recomienda recolectar datos reales en distintos días y horarios antes
de tomar decisiones operativas. Un atípico no debe eliminarse sin revisar
si representa una atención real o un error de registro.

10. CONCLUSIÓN
Se formuló el problema y se analizaron {n} tiempos simulados de atención.
La media fue {media:.2f} min, la mediana {mediana:.2f} min y la desviación
estándar muestral {desviacion:.2f} min. Con |Z| > {UMBRAL_Z:.0f}, la cantidad de
observaciones atípicas fue {len(atipicos)}; se detallan en el apartado 7.
El ejercicio muestra cómo describir tiempos e identificar atenciones
inusuales para su revisión. Al tratarse de datos diseñados con fines
didácticos, los resultados no describen el desempeño real de la ferretería.
La siguiente etapa sería medir atenciones reales y comprobar sus causas
antes de proponer cambios en el proceso.
"""
    (destino / "informe.txt").write_text(informe, encoding="utf-8")
    print(informe)
    print("Archivos generados en:", destino)


if __name__ == "__main__":
    main()
