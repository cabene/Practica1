#Carlos Benjumea Neira
from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
import math

class Estacion:
    def __init__(self, geoposicion: str, estacionamientos: int, capacidad: int):
        self.geoposicion = geoposicion
        self.estacionamientos = estacionamientos
        self.capacidad = capacidad
        self.bicicletas = []  # Lista para almacenar Bicicleta

    def tieneBicicletasLibres(self) -> bool:
        for bici in self.bicicletas:
            if not bici.enUso:
                return True
        return False

    def tieneEspacioLibre(self) -> bool:
        return len(self.bicicletas) < self.capacidad

    def __str__(self):
        return (f"Estacion(geoposicion={self.geoposicion}, "
                f"estacionamientos={self.estacionamientos}, "
                f"capacidad={self.capacidad}, "
                f"bicicletas={len(self.bicicletas)})")


class Tarjeta:
    def __init__(self, numero_tarjeta: int, fechaCaducidad: date, Cvv: int, Titular: str):
        self.numero_tarjeta = numero_tarjeta
        self.fechaCaducidad = fechaCaducidad
        self.Cvv = Cvv
        self.Titular = Titular

    def __str__(self):
        return (f"Tarjeta(numero={self.numero_tarjeta}, "
                f"fechaCaducidad={self.fechaCaducidad}, "
                f"Cvv={self.Cvv}, Titular={self.Titular})")


class Usuario:
    def __init__(self, DNI: str, nombre: str, apellidos: str, tarjeta: Tarjeta = None):
        self.DNI = DNI
        self.nombre = nombre
        self.apellidos = apellidos
        self.tarjeta = tarjeta
        self.abono = None  # Para guardar el abono actual (Anual, Prepago o Turistico)

    def CambiarAbono(self, nuevoAbono):
        self.abono = nuevoAbono

    def puedeUsarBicicleta(self) -> bool:
        return self.abono is not None

    def __str__(self):
        return (f"Usuario(DNI={self.DNI}, nombre={self.nombre}, "
                f"apellidos={self.apellidos}, tarjeta={self.tarjeta}, "
                f"abono={self.abono})")


class Bicicleta:
    def __init__(self, Identificador: int, EstacionInicial: Estacion, enUso: bool = False):
        self.Identificador = Identificador
        self.EstacionInicial = EstacionInicial
        self.enUso = enUso

    def recoger(self):
        self.enUso = True

    def devolverEstacion(self) -> Estacion:
        self.enUso = False
        return self.EstacionInicial

    def __str__(self):
        return (f"Bicicleta(Identificador={self.Identificador}, "
                f"EstacionInicial={self.EstacionInicial.geoposicion}, "
                f"enUso={self.enUso})")


class UsoBicicleta:
    def __init__(self, estacionInicial: Estacion, estacionFinal: Estacion,
                 fecha_hora_inicial: datetime, fecha_hora_final: datetime):
        self.estacionInicial = estacionInicial
        self.estacionFinal = estacionFinal
        self.fecha_hora_inicial = fecha_hora_inicial
        self.fecha_hora_final = fecha_hora_final

    def CalcularDuracion(self) -> float:
        delta = self.fecha_hora_final - self.fecha_hora_inicial
        return delta.total_seconds() / 3600.0

    def finalizarUso(self) -> Estacion:
        return self.estacionFinal

    def __str__(self):
        return (f"UsoBicicleta(estacionInicial={self.estacionInicial.geoposicion}, "
                f"estacionFinal={self.estacionFinal.geoposicion}, "
                f"fecha_hora_inicial={self.fecha_hora_inicial}, "
                f"fecha_hora_final={self.fecha_hora_final})")


class Abono(ABC):

    def __init__(self, usuario: Usuario, costo: float):
        self.usuario = usuario
        self.costo = costo

    @abstractmethod
    def calcular_costo(self) -> float:
        pass

    def __str__(self):
        return f"Abono(usuario={self.usuario.DNI}, costo={self.costo})"


class Anual(Abono):
    def __init__(self, usuario: Usuario, costo: float):
        super().__init__(usuario, costo)

    def calcular_costo(self) -> float:
        return self.costo

    def __str__(self):
        return f"Anual(usuario={self.usuario.DNI}, costo={self.costo})"


class Prepago(Abono):
    def __init__(self, usuario: Usuario, costo: float):
        super().__init__(usuario, costo)

    def calcular_costo(self) -> float:
        return self.costo

    def __str__(self):
        return f"Prepago(usuario={self.usuario.DNI}, costo={self.costo})"


class Turistico(Abono):
    def __init__(self, usuario: Usuario, costo: float, dias: int):
        super().__init__(usuario, costo)
        self.dias = dias

    def calcular_costo(self) -> float:
        return self.costo * self.dias

    def __str__(self):
        return f"Turistico(usuario={self.usuario.DNI}, costo={self.costo}, dias={self.dias})"


class Payment:
    @staticmethod
    def processPayment(credit_card_number: str, amount: float) -> bool:
        print(f"Procesando pago de {amount}€ a la tarjeta {credit_card_number}")
        return True
    

#ejemplo de uso
if __name__ == "__main__":
    estacion1 = Estacion(geoposicion="Centro", estacionamientos=10, capacidad=10)
    estacion2 = Estacion(geoposicion="Norte", estacionamientos=8, capacidad=8)
    print("Estaciones registradas:")
    print(estacion1)
    print(estacion2)
    bike1 = Bicicleta(Identificador=1, EstacionInicial=estacion1)
    bike2 = Bicicleta(Identificador=2, EstacionInicial=estacion1)
    bike3 = Bicicleta(Identificador=3, EstacionInicial=estacion2)
    
    estacion1.bicicletas.append(bike1)
    estacion1.bicicletas.append(bike2)
    estacion2.bicicletas.append(bike3)
    print("\nBicicletas registradas en las estaciones:")
    print(bike1)
    print(bike2)
    print(bike3)

    tarjeta1 = Tarjeta(numero_tarjeta=1234567890123456, fechaCaducidad=date(2025,12,31), Cvv=123, Titular="Carlos Benjumea")
    usuario1 = Usuario(DNI="12345678A", nombre="Carlos", apellidos="Benjumea", tarjeta=tarjeta1)
    print("\nUsuario registrado:")
    print(usuario1)

    abono_anual = Anual(usuario=usuario1, costo=150.0)
    usuario1.CambiarAbono(abono_anual)
    print("\nAbono asignado al usuario:")
    print(usuario1.abono)

    #Simulación de uso de bicicleta con abono anual
    print("\nSimulacion de uso de bicicleta (Abono Anual)")
    bike1.recoger()
    print(f"Bicicleta {bike1.Identificador} recogida en la estacion {estacion1.geoposicion}")
    uso1_inicio = datetime.now()
    uso1_fin = uso1_inicio + timedelta(minutes=45)
    uso1 = UsoBicicleta(estacionInicial=estacion1, estacionFinal=estacion2, 
                         fecha_hora_inicial=uso1_inicio, fecha_hora_final=uso1_fin)
    
    bike1.enUso = False
    estacion2.bicicletas.append(bike1)
    print(f"Bicicleta {bike1.Identificador} devuelta en la estacion {estacion2.geoposicion}")
    duracion_horas = uso1.CalcularDuracion()
    print(f"Duracion del uso: {duracion_horas:.2f} horas")
    cargo_extra = 0.0
    tiempo_gratis = 0.5  
    if duracion_horas > tiempo_gratis:
        exceso_minutos = (duracion_horas - tiempo_gratis) * 60
        periodos = int(exceso_minutos // 5)
        cargo_extra = periodos * 2.0
        print(f"Uso excede los 30 minutos. Se aplican {periodos} periodos extra por un total de {cargo_extra}€")
    
    if duracion_horas > 24:
        cargo_extra += 30
        print("Uso supera las 24 horas. Se añade un cargo de 30€")
    
    if cargo_extra > 0:
        if Payment.processPayment(credit_card_number=str(usuario1.tarjeta.numero_tarjeta), amount=cargo_extra):
            print("Cobro realizado correctamente.")
        else:
            print("Error en el cobro.")
    else:
        print("No se requiere cobro adicional.")

    # Simular que el usuario cambia de abono
    print("\nCambio de abono del usuario")
    abono_turistico = Turistico(usuario=usuario1, costo=50.0, dias=7)
    usuario1.CambiarAbono(abono_turistico)
    print("Nuevo abono asignado:")
    print(usuario1.abono)
    
    #Simulación de uso de bicicleta con abono prepago
    print("\nSimulacion de uso de bicicleta (Abono Prepago)")
    tarjeta2 = Tarjeta(numero_tarjeta=9876543210987654, fechaCaducidad=date(2024,11,30), Cvv=456, Titular="Luis Neira")
    usuario2 = Usuario(DNI="87654321B", nombre="Luis", apellidos="Neira", tarjeta=tarjeta2)
    abono_prepago = Prepago(usuario=usuario2, costo=20.0)
    usuario2.CambiarAbono(abono_prepago)
    print("Usuario con abono prepago registrado:")
    print(usuario2)
    bike2.recoger()
    print(f"Bicicleta {bike2.Identificador} recogida en la estacion {estacion1.geoposicion}")
    uso2_inicio = datetime.now()
    uso2_fin = uso2_inicio + timedelta(minutes=20)
    uso2 = UsoBicicleta(estacionInicial=estacion1, estacionFinal=estacion1, 
                         fecha_hora_inicial=uso2_inicio, fecha_hora_final=uso2_fin)

    bike2.enUso = False
    estacion1.bicicletas.append(bike2)
    print(f"Bicicleta {bike2.Identificador} devuelta en la estacion {estacion1.geoposicion}")
    
    duracion_horas2 = uso2.CalcularDuracion()
    print(f"Duracion del uso: {duracion_horas2:.2f} horas")
    minutos_uso = duracion_horas2 * 60
    periodos_prepago = math.ceil(minutos_uso / 15)
    costo_uso = periodos_prepago * 5.0
    print(f"Costo del uso (abono prepago): {costo_uso}€")
    abono_prepago.costo -= costo_uso
    print(f"Nuevo saldo del abono prepago: {abono_prepago.costo}€")
    if duracion_horas2 > 24:
        if Payment.processPayment(credit_card_number=str(usuario2.tarjeta.numero_tarjeta), amount=30):
            print("Cobro adicional por uso prolongado realizado.")
