

String mensaje;

void setup() {
  Serial.begin(38400);

}

void loop() {
  if(Serial.available() > 0){
    mensaje=Serial.readStringUntil('\n');
    //Serial.println(mensaje);
    if(mensaje.startsWith('M')){
      Serial.print("Comando recibido: ")
      Serial.println(mensaje)
    }
  }

  

}
