from bluetooth import *
import threading
import time
import sys

bluetoothConectado=threading.Event()


def establecerConexionBT():
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
        print("Waiting for connection on RFCOMM channel %d" % port)
        bluetoothConectado.clear()
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)
        bluetoothConectado.set()
        try:
            while True:

                data = client_sock.recv(1024)
                if len(data) == 0: break
                # print("received [%s]" % data)
                if (str(data)=="b's'"):
                    detenerse()
                elif (str(data)=="b'f'"):
                    avanzar()
                elif (str(data)=="b'b'"):
                    retroceder()
                elif (str(data)=="b'r'"):
                    derecha()
                elif (str(data)=="b'l'"):
                    izquierda()
                elif (str(data)=="b'd'"):
                    sys.exit()
                # print(str(data))
        except IOError:
           pass
        except SystemExit:
           client_sock.close()
           server_sock.close()
           print("all done")
           break

        print("disconnected")



def iniciarBT():
    BTthread = threading.Thread(target=establecerConexionBT,name="conexionBT")
    try:
        BTthread.start()

    except RuntimeError:
        print("Error al iniciar hilo")


def detenerse():
    print("detenido")

def avanzar():
    print("avanzando")

def retroceder():
    print("retrocediendo")

def derecha():
    print("girando a la derecha")

def izquierda():
    print("girando a la izquierda")

iniciarBT()
print("hola")
while True:
    if (bluetoothConectado.is_set()):
        print("conectado")
    else:
        print("desconectado")

    time.sleep(1)
