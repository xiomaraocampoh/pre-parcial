Feature: Gestión y cálculo de registros académicos
  Como sistema de administración universitaria
  Quiero procesar las notas de los estudiantes
  Para determinar sus promedios y aprobaciones

  @smoke
  Scenario Outline: Determinar si un estudiante aprueba o reprueba
    Given un sistema de registro académico
    When el sistema evalúa una nota de <nota_ingresada>
    Then el estado devuelto debe ser "<estado_esperado>"

    Examples:
      | nota_ingresada | estado_esperado |
      | 2.99           | Reprobado       |
      | 3.0            | Aprobado        |
      | 5.0            | Aprobado        |

  @regression
  Scenario: Consultar promedio de un estudiante sin notas registradas
    Given un sistema de registro académico
    When consulto el promedio del estudiante 999
    Then el sistema indica que no hay promedio

  @critical
  Scenario: Error al intentar registrar nota duplicada
    Given un sistema de registro académico
    When registro la nota 4.0 para el estudiante 103 en el curso 300 semestre "2026-1"
    And intento registrar nuevamente la nota 4.0 para el estudiante 103 en el curso 300 semestre "2026-1"
    Then el sistema debe lanzar un error por duplicado