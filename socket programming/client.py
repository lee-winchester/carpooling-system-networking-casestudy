import socket
import sys

import pandas as pd

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)
while True:
    print(" I - Insert New Record")
    print(" UBF - Update Base Fare based on Date")
    print(" UF - Update Fare per km based on Date")
    print(" FD - Fetch all records based on Date")
    print(" FDr - Fetch all records based on Driver ID")
    print(" TC - Update Total Cost = Base fare+(fare per km*dist)")
    print(" T - Print no.of each type of rides")
    print(" V - View all")
    print(" Quit - Quit from the System")
    Input = input("Choose from the options: ")
    data = Input
    data += '%'
    if (Input == 'I'):
        print("Enter Ride ID:", end="")
        temp = input()
        temp += '%'
        data += temp
        print("Enter Date:", end="")
        temp = input()
        temp += '%'
        data += temp
        print("Enter Customer Name:", end="")
        temp = input()
        temp += '%'
        data += temp
        print("Enter Driver ID:", end="")
        temp = input()
        temp += '%'
        data += temp
        print("Enter Type(Instation or Outstation):", end="")
        temp = input()
        temp += '%'
        data += temp
        print("Enter Distance(in km):", end="")
        temp = input()
        temp += '%'
        data += temp
        print("Enter Fare per km:", end="")
        temp = input()
        temp += '%'
        data += temp
        print("Enter Base Fare:", end="")
        temp = input()
        data += temp

    elif (Input == "UBF"):
        print('Enter the date:', end="")
        temp = input()
        temp += '%'
        data += temp
        print('Enter the new Base Fare :', end="")
        temp = input()
        data += temp

    elif (Input == "UF"):
        print('Enter the date:', end="")
        temp = input()
        temp += '%'
        data += temp
        print('Enter the new Fare per km :', end="")
        temp = input()
        data += temp

    elif (Input == "FD"):
        print('Enter the date:', end="")
        temp = input()
        data += temp

    elif (Input == "FDr"):
        print('Enter the Driver ID:', end="")
        temp = input()
        data += temp

    elif(Input == "Quit"):
        print('System is being quit')

    ClientMultiSocket.send(str.encode(data))
    res = ClientMultiSocket.recv(1024)
    if Input == "I":
        print(res.decode('utf-8'))
    elif Input == "UBF":
        print(res.decode('utf-8'))
    elif Input == "UF":
        print(res.decode('utf-8'))
    elif Input == "FD":
        x = res.decode('utf-8').split('*')
        fin = {}
        for i in range(1, len(x)):
            if (i % 2 != 0):
                temp = x[i].split("%")
                fin[x[i - 1]] = temp
        # print(fin)
        output = pd.DataFrame.from_dict(fin)
        size = len(output)
        print(output.head(size - 1))

    elif Input == "FDr":
        x = res.decode('utf-8').split('*')
        fin = {}
        for i in range(1, len(x)):
            if (i % 2 != 0):
                temp = x[i].split("%")
                fin[x[i - 1]] = temp
        # print(fin)
        output = pd.DataFrame.from_dict(fin)
        size = len(output)
        print(output.head(size - 1))

    elif Input == "TC":
        print(res.decode('utf-8'))

    elif Input == "T":
        x = res.decode('utf-8').split("%")
        print(x[0], end=":")
        print(x[1])
        print(x[2], end=":")
        print(x[3])

    elif Input == "V":
        x = res.decode('utf-8').split('*')

        fin = {}
        for i in range(1, len(x)):
            if (i % 2 != 0):
                temp = x[i].split("%")
                fin[x[i - 1]] = temp

        output = pd.DataFrame.from_dict(fin)
        size = len(output)
        print(output.head(size - 1))

    elif Input == "Quit":
        sys.exit()

ClientMultiSocket.close()
