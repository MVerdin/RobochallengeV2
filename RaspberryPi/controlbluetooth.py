from bluetooth import *
import threading
import sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

bluetoothConectado=threading.Event()
comando="s"
#Canales de salidas a motores
#(motorderA, motorderB, motorizqA, motorizqB)
canales_motores=(3,5,7,8)
GPIO.setup(canales_motores,GPIO.OUT)
#(motorderA, motorderB, motorizqA, motorizqB)
comandos_a_motores={
    "s":(0,0,0,0),
    "f":(1,0,1,0),
    "b":(0,1,0,1),
    "r":(1,0,0,1),
    "l":(0,1,1,0),
}
#mapeo de comandos a vector one hot para el entrenamiento
cmd2onehot={
    "s":[1,0,0,0,0],
    "f":[0,1,0,0,0],
    "b":[0,0,1,0,0],
    "r":[0,0,0,1,0],
    "l":[0,0,0,0,1],
}


def iniciarBT():

    global comando
    BTthread = threading.Thread(target=establecerConexionBT,name="conexionBT")
    try:
        BTthread.start()

    except RuntimeError:
        print("Error al iniciar hilo")

def establecerConexionBT():
    global comando
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "SampleServer",
                       service_id = uuid,
                       service_classes = [ uuid, SERIAL_PORT_CLASS ],
                       profiles = [ SERIAL_PORT_PROFILE ],
    #                   protocols = [ OBEX_UUID ]
                        )


    while True:
        try:
            print("Esperando conexion en puerto %d" % port)
            bluetoothConectado.clear()
            client_sock, client_info = server_sock.accept()
            print("Conectado a: ", client_info)
            bluetoothConectado.set()

            while True:

                data = client_sock.recv(1024)
                if len(data) == 0: break
                if (procesarComando(str(data, errors="strict"))):
                    comando = str(data, errors="strict")
                    if(comando=="d"):
                        sys.exit()

        except IOError:
            pass
        except SystemExit:
            client_sock.close()
            server_sock.close()
            print("Conexion cerrada")
            GPIO.cleanup(canales_motores)
            print("GPIO limpiados")
            sys.exit()
        except KeyboardInterrupt:
            client_sock.close()
            server_sock.close()
            print("Conexion cerrada")
            GPIO.cleanup(canales_motores)
            print("GPIO limpiados")
            sys.exit()

        print("Desconectado")

def obtenerComando():
    if (comando=="d"):
        sys.exit()
    return cmd2onehot[comando]

def procesarComando(cmd):
    if (cmd=="d"):
        return True
    elif(cmd in comandos_a_motores and cmd in cmd2onehot):
        GPIO.output(canales_motores, comandos_a_motores[cmd])
        return True
    else:
        print("Comando desconocido")
        return False
