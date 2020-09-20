/*
 * Test para el puerto serie:
 * 
 * Al recibir un dato, devuelve el mismo + 1
 * => si recibe A, devuelve B.
 * 
 * Al enviar P (devuelve Q) y aumente el 
 * periodo de parpadeo del LED en periodo/2.
 * Osea si arranca en 1s y recibe P, pasa a 1.5s.
 */

const byte LED = 13;

unsigned long t_actual;
unsigned long t_anterior;
unsigned long periodo;
char dato_rx;
char dato_tx;

void setup() {
  // put your setup code here, to run once:
  periodo = 1000; // 1 segundo
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  Serial.begin(9600);
  t_anterior = millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  t_actual = millis();
  if (t_actual - t_anterior >= periodo){
    t_anterior = t_actual;
    digitalWrite(LED, !digitalRead(LED));
  }
  if (Serial.available() > 0){
    Serial.print(Serial.read());
    /*
    dato_rx = Serial.read();
    if(dato_rx == 'a'){
      Serial.print('b');
    }
    //dato_tx = (char) (int)dato_rx + 1;
    //Serial.write(dato_tx);
    if (dato_rx == 'P'){
      periodo += periodo/2;
    }
    */
  }
}
