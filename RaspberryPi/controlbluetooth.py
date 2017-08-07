#!/usr/bin/env python3
import sys, os
sys.path.insert(len(sys.path), os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
import configuracion

from bluetooth import *
import multiprocessing
import numpy as np
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

canales_motores, comandos_a_motores, cmd2onehot = configuracion.ObtenerConfigMotores()

#Configuracion de pines de salida a motores
GPIO.setup(canales_motores,GPIO.OUT)

bluetoothConectado=multiprocessing.Event()

comando=multiprocessing.Value("u","s")

def iniciarBT():
    BTthread = multiprocessing.Process(target=establecerConexionBT,name="conexionBT")
    try:
        BTthread.start()

    except RuntimeError as e:
        print("Error al iniciar proceso")
        print(e)

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
        try:
            print("Esperando conexion en puerto %d" % port)
            bluetoothConectado.clear()
            client_sock, client_info = server_sock.accept()
            print("Conectado a: ", client_info)
            bluetoothConectado.set()

            while True:

                data = client_sock.recv(1024)
                if len(data) == 0: break
                mensaje = str(data, errors="strict")
                if (procesarComando(mensaje) and len(mensaje)==1):
                    comando.value = mensaje
                    if(comando.value=="d"):
                        sys.exit()
                else:
                    comando.value = "s"
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
    if (comando.value=="d"):
        sys.exit()
    return comando.value

def procesarComando(cmd):
    if (cmd=="d"):
        return True
    elif(cmd in cmd2onehot):
        if(cmd2onehot[cmd] in comandos_a_motores):
            GPIO.output(canales_motores, comandos_a_motores[cmd2onehot[cmd]])
            return True
    else:
        print("Comando desconocido")
        GPIO.output(canales_motores, comandos_a_motores[cmd2onehot["s"]])
        return False
