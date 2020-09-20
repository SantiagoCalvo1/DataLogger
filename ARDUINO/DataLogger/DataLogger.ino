/*
 * Prototipo en ARDUINO.
 * Objetivo: 
 *    Tomar datos con el ADC A0 cada 1 seg.
 *    Almacenarlos.        
 *    Enviarlos cuando se reciba 'E'.
 */


# define ARRAY_SIZE   512

// FLAG
/*
 * b7 b6  b5  b4  b3  b2  b1  b0
 * b7 == 1: Almacenar los datos en FLASH.
 * b6 == 1: Enviar por puerto serie.
 * b5 == 1: Nada
 * b4 == 1: Configurar
 * b3
 * b2
 * b1 
 * b0 .
 */
#define  ALMACENAR     B10000000
#define  B_ALMACENAR   7
#define  C_ALMACENAR   'A'

#define  ENVIAR        B01000000
#define  B_ENVIAR      6
#define  C_ENVIAR      'E'

#define  NADA          B00100000
#define  B_NADA        5
#define  C_NADA        'N'

#define  CONFIGURAR    B00010000
#define  B_CONFIGURAR  4
#define  C_CONFIGURAR  'C'

#define  DATOS_PERDIDOS     B00001000
#define  B_DATOS_PERDIDOS   3
#define  C_DATOS_PERDIDOS  'P'

byte flag = 0;

// Definiciones LED
const int LED_Pin =  13;

// Definiciones ADC
const int ADC_Pin = A0;
const byte ADC_N_promedio = 2;  // Número de muestras para promedio
byte ADC_Array[ARRAY_SIZE];
unsigned int ADC_Index = 0;
unsigned long ADC_Periodo = 500; // milisegundos

// Definiciones TIMER
unsigned long ADC_millis_anterior = 0;
unsigned long NADA_millis_anterior = 0;
const unsigned long NADA_Periodo = 500; // milisegundos

// Definiciones SERIAL
const long baudrate = 9600;
byte dato_recibido;

// Prototipo de funciones
void rutina_ALMACENAR(void);
void rutina_ENVIAR(void);
void rutina_SERIAL(void);
void rutina_NADA(void);
void rutina_CONFIGURAR(void);



void setup() {
  // LED como salida
  pinMode(LED_Pin, OUTPUT);
  flag = NADA;  // Se comienza en modo configuración
  // Comenzar el puerto serie
  Serial.begin(baudrate);
}

void loop() {
  // Verifica que no haya datos en puerto serie  
  if ((flag & NADA) >> (B_NADA)){
    rutina_NADA();
  }
  
  if ((flag & ALMACENAR) >> B_ALMACENAR){
    rutina_ALMACENAR();
  }
  
  if ((flag & ENVIAR) >> B_ENVIAR){
    rutina_ENVIAR();
  }

  if ((flag & CONFIGURAR) >> B_CONFIGURAR){
    rutina_CONFIGURAR();
  }
  
  if (!((flag & CONFIGURAR) >> B_CONFIGURAR)){
    // Solo entra si no se está configurando para no tener problemas con
    // que lea los datos del puerto serie antes que la otra función.
    rutina_SERIAL();
  }
}


/*----------------------------------------------------------------*/
/*
 * rutina_ALMACENAR hace una conversión ADC cada ADC_periodo [ms]
 * y las guarda en ADC_Array
 */
void rutina_ALMACENAR(void)
{
  // Apago el LED
  digitalWrite(LED_Pin, LOW);
  // Mide el tiempo actual, si paso el tiempo de periodo se ejecuta el código
  unsigned long millis_actual = millis();
  if (millis_actual - ADC_millis_anterior >= ADC_Periodo)
  {
    // Actualizar variable auxiliar
    ADC_millis_anterior = millis_actual;
    // Toggle al LED
    //digitalWrite(LED_Pin, !digitalRead(LED_Pin));
    // Tomar valor ADC y guardar 
    ADC_Array[ADC_Index] = (byte) analogRead(ADC_Pin);
    ADC_Index++;
    if (!(ADC_Index <= ARRAY_SIZE)){
      ADC_Index = 0;
      // Avisa que se perdieron datos, el buffer es circular
      flag |= DATOS_PERDIDOS;
    }
  }
}


/*----------------------------------------------------------------*/
/*
 * rutina_SERIAL se activa si recibe datos y modifica el flag
 */
void rutina_SERIAL(void)
{
  if (Serial.available() > 0)
  {
    dato_recibido = Serial.read();
  
    if (dato_recibido == C_ENVIAR)
    {
      // Se indica que se envien los datos
      flag = ENVIAR;
      // Aprueba la recepción del dato y da inicio al envio
      Serial.println(C_ENVIAR);
    }
    
    if (dato_recibido == C_ALMACENAR)
    {
      // Salgo de los otros modos
      flag = ALMACENAR;
      // Aprueba la recepción del dato y da inicio al almacenaje
      Serial.println(C_ALMACENAR);
    }

    if (dato_recibido == C_CONFIGURAR)
    {
      // Salgo de los otros modos
      flag = CONFIGURAR;
      // Aprueba la recepción del dato y da inicio al almacenaje
      Serial.println(C_CONFIGURAR);
    }

    if (dato_recibido == C_NADA)
    {
      // Salgo de los otros modos
      flag = NADA;
      // Aprueba la recepción del dato y da inicio al almacenaje
      Serial.println(C_NADA);
    }
    
    dato_recibido = 0;
  }
}


/*----------------------------------------------------------------*/
/*
 * rutina_ENVIAR transmite todo el ADC_Array
 * e indica si hubo error de overflow en el array
 */
void rutina_ENVIAR(void)
{
  // Apago el LED
  digitalWrite(LED_Pin, LOW);  
  if ((flag & DATOS_PERDIDOS) >> B_DATOS_PERDIDOS){
    // Si hubo datos perdidos lo informa
    Serial.print(C_DATOS_PERDIDOS);
  }
  for (unsigned int i=0; i<ARRAY_SIZE; i++)
  {
    // Envía todos los datos del array cada 20 ms un dato
    Serial.println(ADC_Array[i]);
    delay(20);
    // Borra los datos
    ADC_Array[i] = 0;
  }
  // Reinicia el ADC_Index = 0
  ADC_Index = 0;
  // Vuelve al estado de configuración
  flag = CONFIGURAR;
}


/*----------------------------------------------------------------*/
/*
 * rutina_NADA queda parpadeando un led únicamente
 */
void rutina_NADA(void)
{
  // Mide el tiempo actual, si paso el tiempo de periodo se ejecuta el código
  unsigned long millis_actual = millis();
  if (millis_actual - NADA_millis_anterior >= NADA_Periodo)
  {
  // Actualizar variable auxiliar
  NADA_millis_anterior = millis_actual;
  // Toggle al LED
  digitalWrite(LED_Pin, !digitalRead(LED_Pin));
  }
}


/*----------------------------------------------------------------*/
/*
 * rutina_CONFIGURAR realiza alguno cambios en el funcionamiento
 * Cambia el ADC_Periodo
 */
void rutina_CONFIGURAR(void)
{
  // Apago el LED
  digitalWrite(LED_Pin, LOW);
  // Reviso si hay datos por leer
  if(Serial.available() > 0){
    dato_recibido = Serial.read();  
  
    if (dato_recibido == 'p'){
      // Confirma la recepción del dato
      Serial.println('p');
      // Cambiar el periodo seteado por el próximo dato
      // Espera 1 seg hasta que venga el próximo dato
      delay(1000);
      if (Serial.available() > 0){
        ADC_Periodo = (unsigned long) (Serial.read()); // milisegundos
      }
      // Confirma la recepción del dato
      Serial.println(ADC_Periodo);    
    }

    if (dato_recibido == 'N'){
      // Confirma la recepción del dato
      Serial.println('N');
      // Sale del modo configuracion y entra al de NADA
      flag &= ~CONFIGURAR;
      flag |= NADA;
    }
  }
  // Agregar otras cosas que se puedan configurar...  
}
