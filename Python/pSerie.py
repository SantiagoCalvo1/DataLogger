import serial
import numpy as np

class PSerie:
    def __init__(self, port='COM4', baudrate=115200, timeout=10):
        try:
            self.puerto = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            #return True
        except Exception as e:
            print('ERROR: pSerie -> __init__.', e, sep=' ')
            #return False

    def start_ADC(self):
        """ ADQUIRIR desde el punto de vista del micro """
        dato = 'A'
        return self.__write_ascii(dato)

    def recibir_datos(self, rx_array):
        """ ENVIAR desde el punto de vista del micro """
        dato = 'E'
        return self.__write_ascii(dato, rx_array)

    def configurar_micro(self):
        """ CONFIGURAR desde el punto de vista del micro """
        dato = 'C'
        return self.__write_ascii(dato)

    def micro_en_espera(self):
        """ NADA desde el punto de vista del micro """
        dato = 'N'
        return self.__write_ascii(dato)

    def close(self):
        """ Cierra el puerto serie """
        self.puerto.close()

    def __write_ascii(self, dato, rx_array=np.zeros(0)):
        """ Envía el dato, si obtiene el echo se confirma la comunicación y devuelve True """
        # Verificar que sea sólo un caracter. 
        if (len(str(dato)) > 1) or (dato == ""):
            raise ValueError('Se debe enviar un sólo carater')
        # Valor condificado     
        tx_dato = dato.encode(encoding='ascii')
        #print(tx_dato)
        try:
            tx_exito = self.puerto.write(tx_dato)
        except Exception as e:
            print("Excepción: pSerie -> __write_ascii -> write", e, sep=" ")
            return False
        try:
            if tx_exito == 1:
                # Valor leer el primer valor (siempre echo y comprobar)
                echo = False
                rx_dato = self.puerto.read(size=1).decode('ascii')
                if rx_dato == dato:
                    # El echo positivo
                    echo = True
                # Si se lee un array, a continuación lo llena con datos
                if np.size(rx_array) > 0:
                    try:
                        for i in range(np.size(rx_array)):
                            # Se guardan como numero, en vez de letra
                            rx_array[i] = ord(self.puerto.read(size=1))#.decode('ascii')
                        echo = True
                    except Exception as e:
                        print("Excepción: pSerie -> __write_ascii -> read_array", e, sep=" ")
                        return False
            return echo
        except Exception as e:
            print("Excepción: pSerie -> __write_ascii -> read", e, sep=" ")
            return False
