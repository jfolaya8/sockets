#!/usr/bin/env python3
import socket
import pickle
import enquiries


class client:

    def __init__(self):
        # Definimos variable socket son sus atributos
        self.clientSokect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connec = True
        try:
            # realizamos conexión con el servidor
            self.clientSokect.connect( ("192.168.0.2", 8000) )
        except:
            # Si la conexión falla
            print("Could not connect to the server")
            self.connec = False


    def sendMesagge(self, message):
        self.clientSokect.send(message.encode())
        return pickle.loads(self.clientSokect.recv(1024))

    
    def closeConnection(self):
        self.clientSokect.send("Finalizar".encode())
        self.clientSokect.close()
        self.connec = False


    def connectServer(self):        
        try:
            if self.connec: 
                # Se solicitan las opciones disponibles 
                options = client.sendMesagge(self, "options")
            while self.connec:
                # Se imprime en pantalla las opciones
                request = enquiries.choose('Indica la operación que desea realizar: ', options)

                # Se realiza la acción según la opción seleccionada por el usuario
                if request == "Finalizar":
                    response = client.sendMesagge(self, request)
                    print(response)
                    client.closeConnection(self)
                if request == "Consultar":
                    self.clientSokect.send(request.encode())
                    accountNumber = enquiries.freetext("Ingrese el número de cuenta a consultar:")
                    response = client.sendMesagge(self, accountNumber)
                    print(response["message"])
                    client.closeConnection(self)
                if request == "Agregar cuenta":
                    self.clientSokect.send(request.encode())
                    accountNumber = int(enquiries.freetext("Ingrese el número de cuenta que desea agregar:"))
                    value = enquiries.freetext("Ingrese el valor:")
                    response = client.sendMesagge(self, "{},{}".format(accountNumber, value))
                    print(response["message"])
                    client.closeConnection(self)
        except KeyboardInterrupt:
            # Se finaliza la conexión
            print("\nOperación finalizada por el usuario")
            client.closeConnection(self)
                

connections = client()
connections.connectServer()
