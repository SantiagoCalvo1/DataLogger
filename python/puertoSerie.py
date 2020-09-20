import serial
import serial.tools.list_ports
import time
import numpy as np
"""
TODO:   Autodetección del puerto.
TODO:   Autodestrucción cuando no se puede inicializar el puerto
"""

class PuertoSerie:
    """ 
    Una clase basada en Pyserial que se ocupa de la configuracion del puerto serie
    y la comunicación con el microcontrolador.
    """
    def __init__(self, port_name = 'COM4', baudrate = 115200):
        """ Constructor """
        self.baudrate = baudrate
        self.name = port_name
        try:
            self.ser = serial.Serial(port_name, baudrate, timeout = 1)
            #self.ser.open()
            self.valido = True
        except:
            print("No es posible conectarse...")
            #self.ser.close()
            #self.ser.__del__()
            self.valido = False

############################################################################

    def __str__(self):
        return "Objeto PuertoSerie: %s con baudrate = %d" %(self.name, self.baudrate)

############################################################################

    def open(self):
        """ Cierra el puerto y lo elimina """
        # Abrir el puerto
        self.ser.open()   
        """     
        # Esperamos 1 segundo por las dudas
        #time.sleep(1)    
        self.actualizar_campos()    
        except Exception as e:
            print("Excepción:",e,sep=" ")
        """


############################################################################

    def close(self):
        """ Cierra el puerto y lo elimina """
        # Cerrar el puerto
        self.ser.close()
        # Esperamos 1 segundo por las dudas
        time.sleep(1)
        # Eliminamos la instancia
        self.ser.__del__()
        self.actualizar_campos()

############################################################################

    def write_ascii(self, char):        
        """ Enviar un caracter ASCII """
        # Verificar que sea sólo un caracter. 
        if (len(str(char)) > 1) or (char == ""):
            raise ValueError('Se debe enviar un sólo carater')
        # Valor condificado     
        #tx_dato = str.encode(char)
        tx_dato = char.encode(encoding='ascii')
        print(tx_dato)
        try:
            self.ser.write(tx_dato)
        except Exception as e:
            print("Excepción:", e, sep=" ")

############################################################################

    def read_ascii(self):
        """ Recibir un caracter ASCII """
        try:
            #rx_dato = self.ser.read(size=1).decode('ISO-8859-1')
            rx_dato = self.ser.read(size=1).decode('ascii')
            print(rx_dato)
            #rx_dato = chr(self.ser.read(size=1))
        except: print("Excepción: En read_ascii")
            #rx_dato = None
        return rx_dato

############################################################################

    def write_dec(self, dec):        
        """ Enviar un caracter DECIMAL """
        # Verificar que sea sólo un caracter. 
        if (int(dec) >= 256) or (int(dec) < 0):
            raise ValueError("El número es de 8 bits. Son validos entre 0 y 255.")
        # Valor condificado     
        tx_dato = chr(dec)
        #print(tx_dato)
        try:
            self.write_ascii(tx_dato)
        except Exception as e:
            print("Excepción:",e,sep=" ")

############################################################################

    def read_dec(self):
        """ Recibir un caracter DECIMAL """
        try:
            #n = self.ser.inWaiting()
            #print(n)
            rx_dato = ord(self.read_ascii())
        except:
            print("Excepción: En read_dec")
            rx_dato = None
        return rx_dato

############################################################################

############################################################################

    def read_n(self, array):
        n = np.size(array)
        try:
            for i in range(n):
                array[i] = self.read_dec()
                #time.sleep(0.1)
            return array
        except:
            print("Excepción: En read_n")
            return None
            
############################################################################

    def actualizar_campos(self):
        try:
            self.nombre = self.ser.name
            self.baudrate = self.ser.baudrate
            self.valido = True
        except:
            # Significa que no existe ser
            self.nombre = ""
            self.baudrate = None
            self.valido = False
