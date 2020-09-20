import puertoSerie
import numpy as np
import time 

class DataLogger:
    """ Esta clase es la que tiene las bases de datos y realiza el control real """
    def __init__ (self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        try:
            self.puerto = puertoSerie.PuertoSerie()
            if not self.puerto.valido:
                print('ERROR: En la creación del puerto. Puerto no válido')
        except: print('ERROR: En la creación del puerto')

    def __str__(self):
        return 'DataLogger -> %s: %s' %(self.nombre, self.descripcion)
    
    def enviar_instruccion(self, instruccion):
        try:
            self.puerto.write_ascii(instruccion)
            time.sleep(0.2)
            respuesta = self.puerto.read_ascii()
            print(respuesta)
            if (respuesta == instruccion):
                return True
            else:
                return False
            
        except: print('ERROR: En el envío de instrucción')

    def recibir_datos(self, array):
        try:
            #if self.enviar_instruccion('E'):
                return self.puerto.read_n(array)
            #else: return np.zeros(0)
        except:
            print('ERROR: En la recepcion de los datos')
            return np.zeros(0)

    def comenzar_adquisicion(self):
        try:
            return self.enviar_instruccion('A')
        except:
            print('ERROR: En el envio de comienzo a adquirir')
            return False