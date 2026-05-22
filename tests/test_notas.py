import pytest 
from src.notas import RegistroNotas

def test_registrar_nota_valida():
    registro = RegistroNotas()
    resultado = registro.registrar_nota(100, 200, "2026-1", 3.5)
    assert resultado == "Nota aceptada"

def test_registrar_nota_menor_a_cero():
    registro = RegistroNotas()
    with pytest.raises(ValueError, match="Nota fuera de rango"):
        registro.registrar_nota(100, 200, "2026-1", -1.0)

def test_estado_nota_antes_umbral():
    registro = RegistroNotas()
    resultado = registro.obtener_estado(2.99)
    assert resultado == "Reprobado"

def test_registrar_nota_duplicada():
    registro = RegistroNotas()
    registro.registrar_nota(100, 200, "2026-1", 4.0)
    with pytest.raises(ValueError, match="Materia ya registrada este semestre"):
        registro.registrar_nota(100, 200, "2026-1", 4.0)