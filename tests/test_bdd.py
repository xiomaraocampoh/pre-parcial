import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.notas import RegistroNotas

scenarios('features/notas.feature')

@given("un sistema de registro académico", target_fixture="sistema")
def sistema_inicializado():
    return RegistroNotas()

@when(parsers.parse("el sistema evalúa una nota de {nota:f}"))
def evaluar_nota(sistema, nota):
    pytest.estado_actual = sistema.obtener_estado(nota)

@when(parsers.parse("consulto el promedio del estudiante {est_id:d}"))
def consulto_promedio_estudiante(sistema, est_id):
    pytest.promedio_actual = sistema.obtener_promedio(est_id)

@when(parsers.parse('registro la nota {nota:f} para el estudiante {est_id:d} en el curso {curso_id:d} semestre "{semestre}"'))
def registro_nota_valida(sistema, nota, est_id, curso_id, semestre):
    sistema.registrar_nota(est_id, curso_id, semestre, nota)

@when(parsers.parse('intento registrar nuevamente la nota {nota:f} para el estudiante {est_id:d} en el curso {curso_id:d} semestre "{semestre}"'))
def registro_nota_duplicada(sistema, nota, est_id, curso_id, semestre):
    try:
        sistema.registrar_nota(est_id, curso_id, semestre, nota)
    except ValueError as e:
        pytest.error_actual = str(e)

@then(parsers.parse('el estado devuelto debe ser "{estado_esperado}"'))
def verificar_estado(estado_esperado):
    assert pytest.estado_actual == estado_esperado

@then("el sistema indica que no hay promedio")
def verificar_promedio_nulo():
    assert pytest.promedio_actual is None

@then(parsers.parse("el promedio calculado debe ser {promedio_esperado:f}"))
def verificar_promedio_calculado(promedio_esperado):
    assert pytest.promedio_actual == promedio_esperado

@then("el sistema debe lanzar un error por duplicado")
def verificar_error():
    assert pytest.error_actual == "Materia ya registrada este semestre"