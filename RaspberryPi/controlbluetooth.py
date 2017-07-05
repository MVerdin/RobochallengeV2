from bluetooth import *
import threading
import time
import sys

bluetoothConectado=threading.Event()
comando=0
#variable comando indica la orden recibida por el controlador bluetooth
# 0=detenerse
# 1=avanzar
# 2=retroceder
# 3=girar a la derecha
# 4=girar a la izquierda
int2onehot={
    0:[1,0,0,0,0],
    1:[0,1,0,0,0],
    2:[0,0,1,0,0],
    3:[0,0,0,1,0],
    4:[0,0,0,0,1],
}

comandos_esperados={
    "b's'":0,
    "b'f'":1,
    "b'b'":2,
    "b'r'":3,
    "b'l'":4,
    "b'd'":5,
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
            print("Conexion aceptada ", client_info)
            bluetoothConectado.set()

            while True:

                data = client_sock.recv(1024)
                if len(data) == 0: break
                if (data in comandos_esperados):
                    comando = comandos_esperados[data]
                    procesarComando(comando)

        except IOError:
            pass
        except SystemExit:
            client_sock.close()
            server_sock.close()
            print("Conexion cerrada")
            break
        except KeyboardInterrupt:
            client_sock.close()
            server_sock.close()
            print("Conexion cerrada")

        print("Desconectado")

def obtenerComando():
    return int2onehot[comando]

def procesarComando(cmd):
    if(cmd==0):
        print("detenido")
    elif(cmd==1):
        print("avanzando")
    elif(cmd==2):
        print("retrocediendo")
    elif(cmd==3):
        print("girando a la derecha")
    elif(cmd==4):
        print("girando a la izquierda")
    elif(cmd==5):
        print("cerrando programa")
