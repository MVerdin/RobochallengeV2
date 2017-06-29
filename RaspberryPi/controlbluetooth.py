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
mapeo_comando={
    0:[1,0,0,0,0],
    1:[0,1,0,0,0],
    2:[0,0,1,0,0],
    3:[0,0,0,1,0],
    4:[0,0,0,0,1],
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
            print("Waiting for connection on RFCOMM channel %d" % port)
            bluetoothConectado.clear()
            client_sock, client_info = server_sock.accept()
            print("Accepted connection from ", client_info)
            bluetoothConectado.set()

            while True:

                data = client_sock.recv(1024)
                if len(data) == 0: break
                # print("received [%s]" % data)
                if (str(data)=="b's'"):
                    comando=detenerse()
                elif (str(data)=="b'f'"):
                    comando=avanzar()
                elif (str(data)=="b'b'"):
                    comando=retroceder()
                elif (str(data)=="b'r'"):
                    comando=derecha()
                elif (str(data)=="b'l'"):
                    comando=izquierda()
                elif (str(data)=="b'd'"):
                    break
                # print(str(data))
        except IOError:
            pass
        except SystemExit:
            client_sock.close()
            server_sock.close()
            print("all done")
            break
        except KeyboardInterrupt:
            client_sock.close()
            server_sock.close()
            print("all done")

        print("disconnected")

def obtenerComando():
    return mapeo_comando[comando]

def detenerse():
    print("detenido")
    return 0
def avanzar():
    print("avanzando")
    return 1
def retroceder():
    print("retrocediendo")
    return 2
def derecha():
    print("girando a la derecha")
    return 3
def izquierda():
    print("girando a la izquierda")
    return 4
