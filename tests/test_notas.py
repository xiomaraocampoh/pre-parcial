import pytest
from src.notas import RegistroNotas


def test_ingresar_nota_valida_tipica():
    registro = RegistroNotas()
    resultado = registro.registrar_nota(100, 200, "2026-1", 3.5)
    assert resultado == "Nota aceptada"
    assert registro.obtener_promedio(100) == pytest.approx(3.5)


def test_ingresar_nota_menor_que_cero():
    registro = RegistroNotas()
    with pytest.raises(ValueError, match="Nota fuera de rango"):
        registro.registrar_nota(100, 200, "2026-1", -1.0)
    assert registro.obtener_promedio(100) is None


def testingresar_nota_limite_inferior():
    registro = RegistroNotas()
    resultado = registro.registrar_nota(100, 200, "2026-1", 0.0)
    assert resultado == "Nota aceptada"
    assert registro.obtener_promedio(100) == 0.0


def test_nota_antes_del_umbral():
    registro = RegistroNotas()
    estado = registro.obtener_estado(2.99)
    assert estado == "Reprobado"


def test_nota_igual_al_umbral():
    registro = RegistroNotas()
    estado = registro.obtener_estado(3.0)
    assert estado == "Aprobado"


def test_nota_justo_despues_del_umbral():
    registro = RegistroNotas()
    estado = registro.obtener_estado(3.01)
    assert estado == "Aprobado"


def tes_promedio_estudiante_sin_notas():
    registro = RegistroNotas()
    assert registro.obtener_promedio(999) is None


def test_promedio_con_una_nota():
    registro = RegistroNotas()
    registro.registrar_nota(101, 201, "2026-1", 4.0)
    assert registro.obtener_promedio(101) == pytest.approx(4.0)


def test_promedio_con_varias_notas():
    registro = RegistroNotas()
    registro.registrar_nota(102, 202, "2026-1", 3.0)
    registro.registrar_nota(102, 203, "2026-1", 4.0)
    registro.registrar_nota(102, 204, "2026-1", 5.0)
    assert registro.obtener_promedio(102) == pytest.approx(4.0)


def test_insertar_nota_duplicada_mismo_semestre():
    registro = RegistroNotas()
    registro.registrar_nota(103, 300, "2026-1", 4.0)
    with pytest.raises(ValueError, match="Materia ya registrada este semestre"):
        registro.registrar_nota(103, 300, "2026-1", 4.0)


def test_insertar_misma_materia_semestre_diferente():
    registro = RegistroNotas()
    registro.registrar_nota(103, 300, "2026-1", 4.0)
    resultado = registro.registrar_nota(103, 300, "2026-2", 4.5)
    assert resultado == "Nota aceptada"
    assert registro.obtener_promedio(103) == pytest.approx((4.0 + 4.5) / 2)


def test_insertar_distinto_assessment_id_no_duplicado():
    registro = RegistroNotas()
    registro.registrar_nota(104, 300, "2026-1", 4.0, assessment_id=1)
    resultado = registro.registrar_nota(104, 300, "2026-1", 4.0, assessment_id=2)
    assert resultado == "Nota aceptada"
    assert registro.obtener_promedio(104) == pytest.approx(4.0)
