



unsigned long tiempo_inicio; 
boolean cambio_en_espera = false;
int estado_salidas = 0;
int estado_en_espera = 0;
int estado_anterior = 0;

void analizar_estado(){
    switch(estado){
        case 0:
            estado_salidas=estado;
            break;
        case 1:
        case 2:
        case 3:
        case 4:
            if(cambio_en_espera && estado != estado_en_espera){
                if(estado == estado_anterior){
                    estado_salidas = estado;
                    cambio_en_espera = false;
                    estado_en_espera= 0;
                    estado_anterior=0;
                }
                else{
                    estado_en_espera=estado;
                }
            }
            else{
                if(estado != 0 && estado != estado_salidas && estado_salidas!=0){
                    cambio_en_espera=true;
                    tiempo_inicio=millis();
                    estado_en_espera = estado;
                    estado_anterior = estado_salidas;
                    estado_salidas=0;
                }
                else{
                    estado_salidas=estado;
                }
            }
            break;
        default:
            estado_salidas=0;
            break;
    }
    if(cambio_en_espera){
        if(millis()-tiempo_inicio > tiemposeguridad){
            estado_salidas = estado_en_espera;
            cambio_en_espera = false;
        }
        else{
            estado_salidas=0;
        }
    }
    cambiar_salidas();
}

void cambiar_salidas(){
    switch(estado_salidas){
        case 0:
            detenerse();
            break;
        case 1:
            avanzar();
            break;
        case 2:
            retroceder();
            break;
        case 3:
            girarderecha();
            break;
        case 4:
            girarizquierda();
            break;
        default:
            detenerse();
            break;
    }
}

void avanzar(){
    digitalWrite(pinmotorA1, HIGH);
    digitalWrite(pinmotorA2, LOW);
    digitalWrite(pinmotorB1, HIGH);
    digitalWrite(pinmotorB2, LOW);
}

void retroceder(){
    digitalWrite(pinmotorA1, LOW);
    digitalWrite(pinmotorA2, HIGH);
    digitalWrite(pinmotorB1, LOW);
    digitalWrite(pinmotorB2, HIGH);
}

void girarderecha(){
    digitalWrite(pinmotorA1, HIGH);
    digitalWrite(pinmotorA2, LOW);
    digitalWrite(pinmotorB1, LOW);
    digitalWrite(pinmotorB2, HIGH);
}

void girarizquierda(){
    digitalWrite(pinmotorA1, LOW);
    digitalWrite(pinmotorA2, HIGH);
    digitalWrite(pinmotorB1, HIGH);
    digitalWrite(pinmotorB2, LOW);
}

void detenerse(){
    digitalWrite(pinmotorA1, LOW);
    digitalWrite(pinmotorA2, LOW);
    digitalWrite(pinmotorB1, LOW);
    digitalWrite(pinmotorB2, LOW);
}

void procesar_comando_motores(String comando){
    comando.remove(0,1);
    if(comando=="estado"){
        switch(estado_salidas){
            case 0:
                Serial.println("detenido");
                break;
            case 1:
                Serial.println("avanzando");
                break;
            case 2:
                Serial.println("retrocediendo");
                break;
            case 3:
                Serial.println("girandoderecha");
                break;
            case 4:
                Serial.println("girandoizquierda");
                break;
            default:
                break;
        }
    }
    else if(comando=="avanzar"){
        estado=1;
    }
    else if(comando=="retroceder"){
        estado=2;
    }
    else if(comando=="girarderecha"){
        estado=3;
    }
    else if(comando=="girarizquierda"){
        estado=4;
    }
    else if(comando=="detenerse"){
        estado=0;
    }

}