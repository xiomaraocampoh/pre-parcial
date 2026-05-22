class RegistroNotas:
    APROBACION = 3.0

    def __init__(self):
        self.notas_registradas = []

    def registrar_nota(
        self,
        student_id: int,
        course_id: int,
        semester: str,
        nota: float,
        assessment_id: int | None = None,
    ):
        if nota is None or not isinstance(nota, (int, float)):
            raise ValueError("Nota inválida")

        if nota < 0.0 or nota > 5.0:
            raise ValueError("Nota fuera de rango")

        for reg in self.notas_registradas:
            if (
                reg["student_id"] == student_id
                and reg["course_id"] == course_id
                and reg["semester"] == semester
                and reg.get("assessment_id") == assessment_id
            ):
                raise ValueError("Materia ya registrada este semestre")

        self.notas_registradas.append(
            {
                "student_id": student_id,
                "course_id": course_id,
                "semester": semester,
                "nota": float(nota),
                "assessment_id": assessment_id,
            }
        )
        return "Nota aceptada"

    def obtener_estado(self, nota: float):
        if nota < self.APROBACION:
            return "Reprobado"
        return "Aprobado"

    def obtener_promedio(self, student_id: int):
        notas = [reg["nota"] for reg in self.notas_registradas if reg["student_id"] == student_id]
        if not notas:
            return None
        return sum(notas) / len(notas)
