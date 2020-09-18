Proyecto de adquisición. La idea es practicar:
    STM32 (en C y C++. ADC, RTC, SleepMode?)
    Python (pyserial, numpy, matplotlib, SQLite, API para mail)
    SQLite

PROCESO:
1.  Configurar RTC a través de puerto serie. Setear fecha y hora.
2.  Tomar datos con el ADC cada 2 seg.
3.  Almacenar los datos en FLASH. En conjunto con la fecha y hora del RTC.
4.  En algún momento enviar un mensaje por puerto serie para recolectar la información (Python).
5.  Enviar todos los datos (con su fecha) por puerto serie.
6.  Resetear el lugar donde se guardaban los datos y esperar ha que se de la instrucción de comenzar nuevamente.
7.  Guardar los datos (ADCValue, Fecha) en una base de datos SQLite.
8.  Proveer métodos para graficar, sacar máximos y mínimos y promedios, para distintos rangos de fechas.
9.  Enviar por mail, un dashboard con los datos.

Un paso más allá:
10. Proveer capacidad de orientación en objetos para agregar más ADCs, como si un ADC fuera un objeto.

TODO:
Programar RTC que parpadee el led cada 2s.
Programar SleepMode con Wakeup por RTC, parpadee el led y vuelva a dormir.
Programar ADC para trabajar con el led en el paso anterior y guardar en memoria.
El mismo caso anterior pero guardar en FLASH (así no se borra si se corta la energía y se tiene más espacio).
Enviar todos los datos de la memoria cuando se reciba un código especial por puerto serie.
Programar la fecha y hora del RTC a través del puerto serie. Y periodo de wakeup.
Puerto serie en python.
Preparar base de datos SQLite. Principal:[FechaHora, ADCid, ValorADC] y ADC:[ADCid, periodo, descripcion]
Funciones para cargar y eliminar filas.
Funciones de análisis y presentación de datos. Promedio, maximo-minimo, por hora, dia, mes o personalizado.
Enviar mails con python.
Enviar un mail con las gráficas más importantes del día a una determinada hora.
Agregar funcionalidad para agregar desde python más ADCs (modificar base de datos y hacer OOP para ADCs en STM32).
Hacer una interfaz gráfica para el programa.