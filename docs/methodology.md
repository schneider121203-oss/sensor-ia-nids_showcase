# Metodología de evaluación

## Protocolo de aprendizaje

El sistema sigue un enfoque de **novelty detection con ajuste exclusivamente
benigno**. Ninguna etiqueta de ataque es necesaria para ajustar EIF, el
Autoencoder de reconstrucción, LOF, los artefactos de preprocesamiento o las
referencias empíricas de scores.

La recolección nativa de flujos benignos se ordenó cronológicamente y se dividió
70/15/15:

| Partición | Flujos | Propósito |
|---|---:|---|
| Entrenamiento | 2 520 | Ajustar preprocesamiento, detectores y referencias de scores |
| Validación | 540 | Calibrar el umbral con un FPR benigno objetivo predefinido |
| Prueba benigna interna | 540 | Estimar generalización benigna después de la calibración |

Los tres percentiles normalizados se combinan con pesos iguales. Un score más
alto representa consistentemente una anomalía mayor.

## Evaluación controlada

La evaluación se realizó en un laboratorio AWS aislado, utilizando sistemas
propios y comandos limitados. La cohorte bloqueada contiene:

| Clase de referencia | Flujos |
|---|---:|
| Asociados a ataques | 908 |
| Benignos | 544 |
| Total | 1 452 |

La matriz resultante es `TP=867`, `FP=25`, `TN=519`, `FN=41`. Las métricas
publicadas se derivan directamente de estos cuatro conteos.

## Restricciones de interpretación

- Las etiquetas describen la ejecución en la que se observó cada flujo; no son
  adjudicaciones forenses individuales por flujo.
- Los flujos pertenecientes a una misma corrida son observaciones correlacionadas.
- Solo existió una repetición válida por escenario ofensivo.
- El experimento mide comportamiento controlado en AWS, no rendimiento en
  producción.
- Los PCAP, datasets de flujos y artefactos entrenados no se publican por
  privacidad, seguridad y tamaño del repositorio.

En consecuencia, este repositorio permite verificar los cálculos y revisar la
arquitectura, pero no reproducir completamente el entrenamiento o el replay de
paquetes.
