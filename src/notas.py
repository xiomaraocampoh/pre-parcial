class RegistroNotas:
    def __init__(self):
        self.notas_registradas = []

    def registrar_nota(self, student_id: int, course_id: int, semester: str, nota: float):
        if nota < 0.0 or nota > 5.0:
            raise ValueError("Nota fuera de rango")

        for reg in self.notas_registradas:
            if reg['student_id'] == student_id and reg['course_id'] == course_id and reg['semester'] == semester:
                raise ValueError("Materia ya registrada este semestre")
                
        self.notas_registradas.append({
            "student_id": student_id,
            "course_id": course_id,
            "semester": semester,
            "nota": nota
        })
        return "Nota aceptada"

    def obtener_estado(self, nota: float):
        if nota < 3.0:
            return "Reprobado"
        return "Aprobado"