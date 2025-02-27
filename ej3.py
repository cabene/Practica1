#Carlos Benjumea Neira
class Archivo:
    def __init__(self, nombre: str, tipo: str, tamanio: int, es_publico: bool = False):
        self.nombre = nombre
        self.tipo = tipo
        self.tamanio = tamanio
        self.es_publico = es_publico
    
    def compartir_enlace_unico(self) -> str:
        return f"https://miarchivo.com/compartir/{self.nombre}"

    def __str__(self):
        return f"Archivo(nombre={self.nombre}, tipo={self.tipo}, tamaño={self.tamanio}, público={self.es_publico})"


class Directorio:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.subdirectorios = []   
        self.archivos = []        
    
    def agregar_subdirectorio(self, directorio: 'Directorio'):
        self.subdirectorios.append(directorio)
    
    def agregar_archivo(self, archivo: Archivo):
        self.archivos.append(archivo)
    
    def eliminar_archivo(self, archivo: Archivo):
        if archivo in self.archivos:
            self.archivos.remove(archivo)
    
    def get_lista_archivos(self) -> list:
        return self.archivos
    
    def __str__(self):
        return f"Directorio(nombre={self.nombre}, subdirectorios={len(self.subdirectorios)}, archivos={len(self.archivos)})"


class Usuario:
    def __init__(self, nombre: str, email: str, password: str):
        self.nombre = nombre
        self.email = email
        self.password = password
        self.directorio_raiz = Directorio(nombre=f"Directorio_{self.nombre}")
    
    def acceder_directorio(self) -> Directorio:
        return self.directorio_raiz
    
    def mover_archivo(
        self, archivo: Archivo, directorio_origen: Directorio, directorio_destino: Directorio
    ) -> bool:
        if archivo in directorio_origen.archivos:
            directorio_origen.eliminar_archivo(archivo)
            directorio_destino.agregar_archivo(archivo)
            return True
        return False
    
    def renombrar_archivo(self, archivo: Archivo, nuevo_nombre: str) -> bool:
        if archivo:
            archivo.nombre = nuevo_nombre
            return True
        return False
    
    def descargar_archivo(self, archivo: Archivo) -> str:
        return f"Descargando archivo {archivo.nombre}..."
    
    def __str__(self):
        return f"Usuario(nombre={self.nombre}, email={self.email})"


#ejemplo de uso
if __name__ == "__main__":
    usuario = Usuario("Carlos", "carlos@gmail.com", "1234")
    
    archivo1 = Archivo("documento1.pdf", "pdf", 1024, es_publico=True)
    archivo2 = Archivo("imagen.png", "png", 2048, es_publico=False)

    directorio_raiz = usuario.acceder_directorio()
    
    directorio_raiz.agregar_archivo(archivo1)
    directorio_raiz.agregar_archivo(archivo2)
    
    subdirectorio = Directorio("Fotos")
    directorio_raiz.agregar_subdirectorio(subdirectorio)
    
    usuario.mover_archivo(archivo2, directorio_raiz, subdirectorio)
    
    usuario.renombrar_archivo(archivo1, "documento_renombrado.pdf")
    
    mensaje_descarga = usuario.descargar_archivo(archivo1)
    print(mensaje_descarga)
    
    print(usuario)
    print(directorio_raiz)
    print(subdirectorio)
    for arch in subdirectorio.get_lista_archivos():
        print(arch)