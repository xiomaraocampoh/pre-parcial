# Módulo de Registro de Notas Académicas

## PARTE 1: Análisis de Pruebas (Test Analysis)

A continuación, se presenta el análisis de calidad previo a la implementación, diseñado para identificar los escenarios de prueba críticos basados en las reglas de negocio entregadas por el Product Owner.

## PARTE 1 — Análisis escrito en el README (15 minutos)

### 1.1 — Particiones de equivalencia

| Partición | Rango cubierto | Valor representativo | Resultado esperado |
|---|---|---|---|
| Válida (nota típica) | 0.0 — 5.0 (incl.) | 3.5 | Aceptada (nota válida) |
| Válida (límite inferior) | 0.0 | 0.0 | Aceptada (nota válida) |
| Válida (límite superior) | 5.0 | 5.0 | Aceptada (nota válida) |
| Inválida (menor que mínimo) | < 0.0 | -1.0 | Rechazada (fuera de rango) |
| Inválida (mayor que máximo) | > 5.0 | 5.5 | Rechazada (fuera de rango) |
| Inválida (no numérico) | N/A | "abc" | Rechazada (tipo inválido / error de validación) |
| Inválida (nulo / ausente) | N/A | null / vacío | Rechazada (falta de dato / error) |

Notas: Se asume que el requisito define un rango inclusivo entre 0.0 y 5.0. Las particiones incluyen tanto casos numéricos válidos como entradas inválidas (tipo, nulo, valores fuera de rango).

### 1.2 — Análisis de valores límite

Para el rango [0.0, 5.0] aplicamos la regla de límite: valor justo antes, límite exacto, valor justo después.

| Valor de prueba | ¿Dentro del rango? | Resultado esperado |
|---|---|---|
| -0.01 (justo antes de 0.0) | Fuera | Rechazada (fuera de rango) |
| 0.00 (límite inferior) | Dentro | Aceptada |
| 0.01 (justo después de 0.0) | Dentro | Aceptada |
| 4.99 (justo antes de 5.0) | Dentro | Aceptada |
| 5.00 (límite superior) | Dentro | Aceptada |
| 5.01 (justo después de 5.0) | Fuera | Rechazada (fuera de rango) |

Observación: si el sistema trabaja con precisión limitada (por ejemplo, dos decimales), ajustar los valores "justo antes/después" al orden de magnitud soportado (ej. -0.01 / 0.01 o -0.001 / 0.001 según corresponda).

### 1.3 — Preguntas al Product Owner (Requerimiento 4: no duplicar nota)

1) ¿Cómo se determina que una nota es duplicada? (por ejemplo: combinación de `student_id` + `course_id` + `assessment_id`, o sólo `student_id` + `course_id`?)

	- Justificación: la clave de unicidad define los datos necesarios para construir los casos de prueba de duplicación. Sin esta información no podemos diseñar entradas que reproduzcan correctamente un duplicado.

2) ¿Cuál es el comportamiento esperado cuando se detecta una nota duplicada: rechazar la nueva entrada con un error, ignorarla, o actualizar la nota existente?

	- Justificación: la acción esperada cambia los criterios de verificación: si se debe rechazar, esperaremos un código de error y sin cambios en la BD; si se debe actualizar, los tests deben verificar que la nota anterior fue reemplazada; si se ignora, esperaríamos que no haya efecto.

3) (Opcional) ¿Hay alguna tolerancia temporal o de versiones (por ejemplo, notas permitidas si son de distintos periodos o importadas desde diferentes fuentes)?

	- Justificación: afecta casos límite y datos de precondición (mismos campos pero distinto periodo pueden ser válidos), y por tanto el diseño de pruebas.

---

He documentado las particiones de equivalencia, los análisis de valores límite y las preguntas al Product Owner necesarias para diseñar pruebas del requisito 1 y del requisito 4.


