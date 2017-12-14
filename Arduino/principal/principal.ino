
//Configuracion
const int tiemposeguridad = 250;

//Pines de conexion
const int pinmotorA1 = 2;
const int pinmotorA2 = 3;
const int pinmotorB1 = 4;
const int pinmotorB2 = 5;


//0 detenido, 1 avanzando, 2 retrocediendo, 3 girandoderecha, 4 girandoizquierda
int estado = 0;

String mensaje;

void setup() {
  Serial.begin(38400);
  pinMode(pinmotorA1, OUTPUT);
  pinMode(pinmotorA2, OUTPUT);
  pinMode(pinmotorB1, OUTPUT);
  pinMode(pinmotorB2, OUTPUT);

}

void loop() {
  if(Serial.available() > 0){
    mensaje=Serial.readStringUntil('\n');
    //Serial.println(mensaje);
    if(mensaje.startsWith("M")){
      Serial.println(mensaje);
      procesar_comando_motores(mensaje);
    }
  }
  analizar_estado();
}
