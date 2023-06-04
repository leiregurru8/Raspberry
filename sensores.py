import Adafruit_DHT
import RPi.GPIO as GPIO
import threading
import time
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font


# Definir el tipo de sensor y el pin de conexión
sensor = Adafruit_DHT.DHT11
pin = 18
boton_pin = 16
led_pin = 22

# Configurar el modo de los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)


# Configurar el pin del botón como entrada con pull-up interno
GPIO.setup(boton_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Crear un nuevo libro de Excel
libro = Workbook()
hoja = libro.active


# Establecer las cabeceras de las columnas
hoja['A1'] = 'Humedad (%)'
hoja['B1'] = 'Temperatura (C)'
hoja['A1'].font = Font(bold=True)
hoja['B1'].font = Font(bold=True)


fila_actual = 2


def leer_sensor():
    global fila_actual


    # Intentar obtener los datos de humedad y temperatura
    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)


    # Comprobar si se pudo leer correctamente el sensor
    if humedad is not None and temperatura is not None:
        print('Humedad: {}%'.format(humedad))
        print('Temperatura: {}C'.format(temperatura))


        # Escribir los datos en la hoja de cálculo
        hoja['A{}'.format(fila_actual)] = humedad
        hoja['B{}'.format(fila_actual)] = temperatura


        fila_actual += 1
    else:
        print('Error al obtener los datos del sensor. Intentando de nuevo...')


def controlar_led():
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led_pin, GPIO.LOW)

# Función de callback para manejar el evento de pulsación del botón
def boton_pulsado(channel):
    print('Boton pulsado')
    t = threading.Thread(target=controlar_led)
    t.start()
    leer_sensor()

# Configurar la interrupción en el pin del botón
GPIO.add_event_detect(boton_pin, GPIO.FALLING, callback=boton_pulsado, bouncetime=200)


try:
    print('Esperando pulsacion del boton...')
    while True:
        pass


except KeyboardInterrupt:
    print('Programa interrumpido por el usuario')


finally:
    # Guardar el libro de Excel
    libro.save('datos.xlsx')


    # Limpiar la configuración de los pines GPIO
    GPIO.cleanup()
