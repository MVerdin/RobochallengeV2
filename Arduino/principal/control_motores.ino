//0 detenido, 1 avanzando, 2 retrocediendo, 3 girandoderecha, 4 girandoizquierda
int estado = 0;

void procesar_comando_motores(String comando){
    comando.remove(0,1);
    if(comando=="estado"){
        switch(estado){
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
