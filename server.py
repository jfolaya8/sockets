#!/usr/bin/env python3
import socket
import threading
import pickle

# Definición de los parámetros para la comunicación del socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind( ("192.168.0.2", 8000) )
# Funcionalidades
options = ["Agregar cuenta", "Consultar", "Finalizar"]


def searchAccount(accountNumber):
    # Se abre el archivo
    with open("accounts.txt", "r") as file:
        # Se recurre el archivo línea por línea
        for line in file:
            line = line.split(",")
            if accountNumber.decode() == line[0]:
                return {"message": "Número de cuenta {} con valor {}".format(line[0], line[1].strip())}
    return {"message": "No se encontro en número de cuenta"}


def addAccount(dataAccount):
    try:
        # Se abre el archivo y se busca el número de cuenta
        dataAccount = dataAccount.decode().split(",")
        with open("accounts.txt", "a") as file:
            file.write("{}, {}\n".format(int(dataAccount[0]), int(dataAccount[1])))
        return {"message": "OK"}
    except:
        return {"message": "NOT OK"}


def attendRequest(conecction, clientAddress):
    print(f"[NEW CONNECTION FROM] {clientAddress}")

    conecc = True
    while conecc:
        try:
            # Se realiza la acción según la solicitud
            # enviada por el cliente
            request = conecction.recv(1024)
            if request.decode() == "options":
                conecction.send(pickle.dumps(options))
            elif request.decode() == "Agregar cuenta":
                dataAccount = conecction.recv(1024)
                message = addAccount(dataAccount)
                conecction.send(pickle.dumps(message))
            elif request.decode() == "Consultar":
                countNumber = conecction.recv(1024)
                message = searchAccount(countNumber)
                conecction.send(pickle.dumps(message))
            elif request.decode() == "Finalizar":
                print("CLOSE CONNECTION FROM {}".format(clientAddress))
                conecction.send(pickle.dumps("Transacción finalizada."))
                conecction.close()
                conecc = False
            else:
                conecction.send(pickle.dumps("Opción incorrecta"))
        except:
            # En caso de existir un error se cierra la conexión
            print("LOSE CONNECTION FROM {}".format(clientAddress))
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
            conecction.close()
            conecc = False


def serverStart():
    # Inicilización del servidor
    print("[Server started]")
    serverSocket.listen(5)
    while True:
        # Servidor en espera de conexión
        conecction, clientAddress = serverSocket.accept()
        thread = threading.Thread(target=attendRequest, args=(conecction, clientAddress))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


serverStart()