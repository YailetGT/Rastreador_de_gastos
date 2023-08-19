import csv
from datetime import datetime

MAX_LONGITUD_DESCRIPCION = 50

# Fecha usando la libreria
fecha_actual = datetime.now()
fecha_actual_formateada = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')

# Para que el orden se actualice diario
fecha_ultima = None  
transacciones = 0  
# Funciones de lectura y escritura

nombre_archivo = 'datos.csv'

def exportar_lista_csv(nombre_archivo, lista_datos, delimitador=';'):
    try:
        with open(nombre_archivo, 'a+', newline='') as archivo:
            escritor = csv.writer(archivo, delimiter=delimitador)
            for fila in lista_datos:
                escritor.writerow(fila)
        print(f"Datos exportados exitosamente a '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error: {e}")
        
def leer_archivo_csv_lista(nombre_archivo, delimitador=';'):
    try:
        with open(nombre_archivo, 'r', newline='') as archivo:
            lector = csv.reader(archivo, delimiter=delimitador)
            datos = [fila for fila in lector]
        return datos
    except FileNotFoundError:
        print(f"Error: Archivo '{nombre_archivo}' no encontrado.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
if fecha_ultima is None or fecha_actual.date() > fecha_ultima:
    fecha_ultima = fecha_actual.date()  # para comparar solo la fecha
    orden_registro = 1  # Reiniciar el orden en un nuevo día
else:
    orden_registro += 1


# Parametro de ID que es la cedula.
cedula = input("Ingresar cedula para el registro: ")
id_registro = cedula

# Monto ingresado por el usuario
monto_transaccion = input("Ingresa el monto gastado en $: ")
try:
    monto_float = float(monto_transaccion)
except ValueError:
    print("Monto inválido, debe ser un número decimal.")
    monto_float = 0.0

# Descripcion ingresada por el usuario
descripcion = input(f"Ingresa la descripción (máximo {MAX_LONGITUD_DESCRIPCION} caracteres): ")
if len(descripcion) > MAX_LONGITUD_DESCRIPCION:
    print(f"La descripción debe tener como máximo {MAX_LONGITUD_DESCRIPCION} caracteres.")
    exit()

# Preparar los datos para exportar
datos_a_exportar = [
    ["orden", "id", "fecha", "monto", "descripcion"],
    [orden_registro, id_registro, fecha_actual_formateada, monto_float, descripcion]
]

exportar_lista_csv(nombre_archivo, datos_a_exportar)

# Lectura del archivo csv

lectura_datos = leer_archivo_csv_lista(nombre_archivo)

# Lógica de la app 
# creacion de una clase para los registros de transaccion

class RegistroTransaccion:
    def __init__(self, orden, id_usuario, fecha, monto, descripcion):
        self.orden = orden
        self.id_usuario = id_usuario
        self.fecha = fecha
        self.monto = monto
        self.descripcion = descripcion
        self.categoria = None

        
#Para guardar esa informacion en una lista para la csv
        
    def convertir_a_lista(self):
        return [self.orden, self.id_usuario, self.fecha, self.monto, self.descripcion]
        
#Para registrar las transacciones diarias de los usuarios        
        
    def transacciones_diarias(orden_registro, id_registro, fecha_actual_formateada, monto_float, descripcion):
        agregar_transaccion = RegistroTransaccion(orden_registro, id_registro, fecha_actual_formateada, monto_float, descripcion)
        return agregar_transaccion

#Categorizar gastos segun los parametros establecidos en mi app xd

    def categorizar_gastos(self):
        tipos_de_gastos = [
            "Alimentos y bebidas",
            "Hobbie y pasatiempos",
            "Adquisición de vehículo o propiedad",
            "Pago de servicios",
            "Pago deudas",
            "Otros gastos"
        ]
        
        print("Tipos de gastos disponibles:")
        for i, categoria in enumerate(tipos_de_gastos, start=1):
            print(f"{i}. {categoria}")
        
        try:
            seleccion = int(input("Selecciona una categoría (número): "))
            self.categoria = tipos_de_gastos[seleccion - 1]
            print(f"Gasto categorizado como: {self.categoria}")
            
        except (ValueError, IndexError):
            print("Selección inválida.")

    def calcular_gastos_mensuales(self):
        gastos_por_id = {}
        for calcular in lista_datos_csv:
            if calcular.id_usuario == self.id_usuario:
                mes_año = calcular.fecha[:7] #Para tomar mes y año de la fecha
                monto = calcular.monto

                if mes_año in gastos_por_id:
                    gastor_por_id[mes_año] += monto
                else:
                    gastor_por_id = monto
                    
        print(f"Resumen de Gastos Mensuales para ID {self.id_usuario}:")
        for mes_año, total_gasto in gastos_por_id.items():
            print(f"{mes_año}: ${total_gasto:.2f}")
        print("\n")        
                
#Llamada a lo metodos
nueva_transaccion = RegistroTransaccion(orden_registro, id_registro, fecha_actual_formateada, monto_float, descripcion)

#Para que lea el archivo.csv y se registre en esta lista del metodo convertir_lista

lista_datos_csv = []

for nombre_archivo in lectura_datos:
    transaccion_csv = RegistroTransaccion(*nombre_archivo)# pasa los valores como argumentos individuales
    lista_datos_csv.append(transaccion_csv)

#Para imprimir la lista creada con los datos csv
    
for gastos in lista_datos_csv:
    lista_transaccion = gastos.convertir_a_lista()
    print(lista_transaccion)
    
#Llamada al metodo que categoriza los gastos
nueva_transaccion.categorizar_gastos()

#Llamada al metodo calcular gastos mensuales

nueva_transaccion.calcular_gastos_mensuales()


