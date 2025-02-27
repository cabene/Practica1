#Carlos Benjumea Neira
from typing import List

class Valoracion:
    def __init__(self, puntuacion: float, fecha: str, comentario: str):
        self.puntuacion = puntuacion
        self.fecha = fecha
        self.comentario = comentario

    def get_valoracion(self) -> float:
        return self.puntuacion

    def __str__(self) -> str:
        return f"Valoración(puntuacion={self.puntuacion}, fecha={self.fecha}, comentario={self.comentario})"


class Curso:
    def __init__(self, id_curso: int, nombre: str, descripcion: str, duracion: int):
        self.id_curso = id_curso
        self.nombre = nombre
        self.descripcion = descripcion
        self.duracion = duracion
        self.valoraciones: List[Valoracion] = []

    def agregar_valoracion(self, valoracion: Valoracion) -> None:
        self.valoraciones.append(valoracion)

    def calcular_valoracion_promedio(self) -> float:
        if not self.valoraciones:
            return 0.0
        total = sum(valoracion.puntuacion for valoracion in self.valoraciones)
        return total / len(self.valoraciones)

    def transmitir(self) -> None:
        raise NotImplementedError("Este método debe ser sobrescrito en las subclases.")

    def __str__(self) -> str:
        return f"Curso(id={self.id_curso}, nombre={self.nombre}, desc={self.descripcion})"


class CursoGrabado(Curso):
    def __init__(self, id_curso: int, nombre: str, descripcion: str, duracion: int, link_video: str):
        super().__init__(id_curso, nombre, descripcion, duracion)
        self.link_video = link_video

    def transmitir(self) -> None:
        print(f"Reproduciendo curso grabado '{self.nombre}' en {self.link_video}.")


class CursoEnVivo(Curso):
    def __init__(self, id_curso: int, nombre: str, descripcion: str, duracion: int, fecha: str, link_transmision: str):
        super().__init__(id_curso, nombre, descripcion, duracion)
        self.fecha = fecha
        self.link_transmision = link_transmision

    def transmitir(self) -> None:
        print(f"Transmitiendo curso en vivo '{self.nombre}' en {self.link_transmision} el día {self.fecha}.")


class Usuario:
    def __init__(self, id_usuario: int, nombre_usuario: str, contrasena: str, email: str):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.email = email
        self.valoraciones: List[Valoracion] = []
        self.transcripciones: List[str] = []
        self.cursos_inscritos: List[Curso] = []

    def add_valoracion(self, valoracion: Valoracion) -> None:
        self.valoraciones.append(valoracion)

    def ver_transcripciones(self) -> None:
        for i, transcripcion in enumerate(self.transcripciones, start=1):
            print(f"{i}. {transcripcion}")

    def filtrar_transcripciones(self, criterio: str) -> List[str]:
        return [t for t in self.transcripciones if criterio.lower() in t.lower()]

    def inscribirse(self, curso: Curso) -> None:
        if curso not in self.cursos_inscritos:
            self.cursos_inscritos.append(curso)
            print(f"Usuario '{self.nombre_usuario}' se ha inscrito en el curso '{curso.nombre}'.")
        else:
            print(f"Usuario '{self.nombre_usuario}' ya está inscrito en el curso '{curso.nombre}'.")

    def mostrar_inscripciones(self) -> None:
        if not self.cursos_inscritos:
            print(f"Usuario '{self.nombre_usuario}' no está inscrito en ningún curso.")
            return
        print(f"Usuario '{self.nombre_usuario}' está inscrito en:")
        for curso in self.cursos_inscritos:
            print(f" - {curso.nombre}")

    def __str__(self) -> str:
        return f"Usuario(id={self.id_usuario}, nombre={self.nombre_usuario})"


class SistemaAdministrativo:
    def __init__(self):
        self.usuarios: List[Usuario] = []

    def agregar_usuario(self, usuario: Usuario) -> None:
        self.usuarios.append(usuario)

    def administrar(self) -> None:
        print("Administrando el sistema...")

    def __str__(self) -> str:
        return f"SistemaAdministrativo con {len(self.usuarios)} usuarios registrados."
    

#ejemplo de uso: 
if __name__ == "__main__":
    sistema = SistemaAdministrativo()

    usuario1 = Usuario(
        id_usuario=1,
        nombre_usuario="carlos",
        contrasena="password",
        email="Carlos@gmail.com"
    )
    sistema.agregar_usuario(usuario1)

    curso_grabado = CursoGrabado(
        id_curso=101,
        nombre="modelado y diseñor de sistemas",
        descripcion="Modelado y diseño de sistemas",
        duracion=10,
        link_video="http://videos.python.com/intro"
    )

    curso_en_vivo = CursoEnVivo(
        id_curso=202,
        nombre="mates Live",
        descripcion="Curso en vivo sobre mates ",
        duracion=5,
        fecha="2025-03-10",
        link_transmision="http://live.mates.com"
    )

    usuario1.inscribirse(curso_grabado)
    usuario1.inscribirse(curso_en_vivo)

    valoracion_curso_grabado = Valoracion(
        puntuacion=5,
        fecha="2025-02-21",
        comentario="Excelente curso grabado, muy completo."
    )
    curso_grabado.agregar_valoracion(valoracion_curso_grabado)
    usuario1.add_valoracion(valoracion_curso_grabado)

    usuario1.mostrar_inscripciones()

    print("Valoración promedio del curso grabado:",
          curso_grabado.calcular_valoracion_promedio())

    sistema.administrar()
    print(sistema)
    curso_grabado.transmitir()
    curso_en_vivo.transmitir()