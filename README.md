# Módulo de Registro de Notas Académicas

## PARTE 1: Análisis de Pruebas (Test Analysis)

A continuación, se presenta el análisis de calidad previo a la implementación, diseñado para identificar los escenarios de prueba críticos basados en las reglas de negocio entregadas por el Product Owner.

## PARTE 1 — Análisis escrito en el README (15 minutos)

### 1.1 — Particiones de equivalencia

| Partición | Rango cubierto | Valor representativo | Resultado esperado |
|---|---|---|---|
| Válida (nota típica) | 0.0 — 5.0| 3.5 | Aceptada (nota válida) |
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

## Casos de prueba

ID | Requerimiento | Descripción | Precondición | Datos de entrada | Pasos | Resultado esperado | Tipo
:-- | :-- | :-- | :-- | :-- | :-- | :-- | :--
T01 | Req 1 | Ingresar nota válida típica | Sistema listo para recibir notas; estudiante y materia existen | nota = 3.5, student_id=100, course_id=200 | 1) Ir a formulario de nota 2) Ingresar datos 3) Enviar | Nota aceptada y almacenada; mensaje de éxito | Positivo
T02 | Req 1 | Ingresar nota menor que 0.0 (inválida) | Sistema listo; estudiante y materia existen | nota = -1.0 | 1) Abrir formulario 2) Ingresar -1.0 3) Enviar | Rechazo con mensaje de validación: "Nota fuera de rango"; no se guarda | Negativo
T03 | Req 1 | Ingresar nota en límite inferior 0.0 | Sistema listo; estudiante y materia existen | nota = 0.0 | 1) Completar formulario 2) Enviar | Aceptada; guardada como nota válida | Borde
T04 | Req 2 | Nota justo antes del umbral de aprobación | Umbral de aprobación definido como 3.0 (precondición) | nota = 2.99 | 1) Ingresar nota 2) Enviar | Considerada NO aprobatoria; estado "Reprobado" o equivalente | Borde
T05 | Req 2 | Nota igual al umbral de aprobación | Umbral = 3.0 | nota = 3.00 | 1) Ingresar nota 3.00 2) Enviar | Considerada aprobatoria; estado "Aprobado" | Borde
T06 | Req 2 | Nota justo después del umbral | Umbral = 3.0 | nota = 3.01 | 1) Ingresar nota 3.01 2) Enviar | Considerada aprobatoria; estado "Aprobado" | Positivo
T07 | Req 3 | Consultar promedio de estudiante sin notas | Estudiante sin registros de notas en la BD | student_id = 999 (sin notas) | 1) Abrir perfil del estudiante 2) Ver sección de notas/promedio | Mostrar indicación "Sin notas" o promedio nulo; no error | Negativo
T08 | Req 3 | Consultar promedio con una nota | Estudiante con una nota registrada | student_id=101 notas=[4.0] | 1) Abrir perfil 2) Ver promedio | Promedio mostrado = 4.0 | Positivo
T09 | Req 3 | Consultar promedio con múltiples notas | Estudiante con varias notas registradas | student_id=102 notas=[3.0,4.0,5.0] | 1) Abrir perfil 2) Ver promedio | Promedio calculado = 4.0 (suma/contador) | Positivo
T10 | Req 4 | Insertar nota duplicada (misma student+course+semester) | Existe nota previa con mismos identificadores | nueva nota = 4.0 para student_id=103, course_id=300, semester=2026-1 (ya existe) | 1) Intentar crear la nueva nota 2) Enviar | Rechazada con mensaje de duplicado; no se crea registro adicional | Negativo
T11 | Req 4 | Insertar misma materia en semestre diferente (permitido) | Existe nota previa en semestre distinto | nueva nota = 4.5 para student_id=103, course_id=300, semester=2026-2 (existe 2026-1) | 1) Crear nota 2) Enviar | Aceptada y almacenada como registro distinto | Positivo
T12 | Req 4 | Insertar nota con distinto assessment_id (no duplicado) | Existe nota con mismo student+course pero distinto assessment_id | nueva nota = 4.0, assessment_id=2; existe assessment_id=1 | 1) Crear nota 2) Enviar | Aceptada; ambas notas coexistirán si la clave incluye assessment_id | Positivo

Notas generales: muchos resultados esperan comportamientos que deben confirmarse con el Product Owner (por ejemplo el `umbral de aprobación` y la política exacta sobre duplicados: rechazar vs actualizar). Ajustar `Datos de entrada` y `Resultado esperado` tras la confirmación.


## PARTE 6 — Reflexión

- ¿qué diferencia notaste entre diseñar los casos de prueba en la tabla antes de escribir código versus simplemente ponerte a programar directamente?

R// Diseñar los casos de prueba primero obliga a pensar en el software desde las restricciones del negocio y los caminos de error. Al hacer la tabla, se identifican variables ocultas como el para evitar bloqueos falsos pero si se hubiera programado directamente, habría construido el "camino feliz" y parcheado los errores después, lo que suele generar código frágil.

- ¿qué fue lo más difícil de seguir el ciclo TDD y en qué momento sentiste la tentación de saltarte algún paso?

R// No saber como iniciar a escribir la prueba sin antes tener la logica de negocio codificada, ya que por lo general se acostumbra a escribir codigo y luego probar o refactorizar ese codigo-