import socket
from _thread import *
import os
import pandas as pd
import openpyxl

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)


def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        msg = connection.recv(2048).decode('utf-8')
        data = msg.split('%')
        df = pd.read_excel("C:\\Users\\D. RHUTHVIK\\Desktop\\sock\\logs.xlsx")
        data_dict = df.to_dict(orient='list')
        if (data[0] == 'I'):
            data_dict['Ride ID'].append(data[1])
            data_dict['Date'].append(data[2])
            data_dict['Customer Name'].append(data[3])
            data_dict['Driver ID'].append(data[4])
            data_dict['Type'].append(data[5])
            data_dict['Distance(in km)'].append(float(data[6]))
            data_dict['Fare per km'].append(float(data[7]))
            data_dict['Base Fare'].append(float(data[8]))
            data_dict['Total Cost'].append(0)
            new = pd.DataFrame.from_dict(data_dict, orient='index').transpose()
            new.to_excel("C:\\Users\\D. RHUTHVIK\\Desktop\\sock\\logs.xlsx", index=False)
            send = "Successfully Inserted"

        elif (data[0] == 'UBF'):
            temp = data_dict['Date']
            for j in range(len(temp)):
                if temp[j] == data[1]:
                    data_dict['Base Fare'][j] = float(data[2])
            new = pd.DataFrame.from_dict(data_dict, orient='index').transpose()
            new.to_excel("C:\\Users\\D. RHUTHVIK\\Desktop\\sock\\logs.xlsx", index=False)
            send = "Successfully Updated"

        elif (data[0] == 'UF'):
            temp = data_dict['Date']
            for j in range(len(temp)):
                if temp[j] == data[1]:
                    data_dict['Fare per km'][j] = float(data[2])
            new = pd.DataFrame.from_dict(data_dict, orient='index').transpose()
            new.to_excel("C:\\Users\\D. RHUTHVIK\\Desktop\\sock\\logs.xlsx", index=False)
            send = "Successfully Updated"

        elif (data[0] == 'FD'):
            send = ""
            temp = data_dict['Date']
            lis = []
            for i in range(len(temp)):
                if temp[i] == data[1]:
                    lis.append(i)
            for j in data_dict.keys():
                send += j
                send += "*"
                for k in lis:
                    send += str(data_dict[j][k])
                    send += "%"
                send += "*"

        elif (data[0] == 'FDr'):
            send = ""
            temp = data_dict['Driver ID']
            lis = []
            for i in range(len(temp)):
                if temp[i] == data[1]:
                    lis.append(i)

            for j in data_dict.keys():
                send += j
                send += "*"
                for k in lis:
                    send += str(data_dict[j][k])
                    send += "%"
                send += "*"

        elif (data[0] == "TC"):
            for j in range(len(data_dict['Ride ID'])):
                data_dict['Total Cost'][j] = data_dict['Base Fare'][j] + (
                            data_dict['Fare per km'][j] * data_dict['Distance(in km)'][j])
            new = pd.DataFrame.from_dict(data_dict, orient='index').transpose()
            new.to_excel("C:\\Users\\D. RHUTHVIK\\Desktop\\sock\\logs.xlsx", index=False)
            send = "Successfully Updated"

        elif (data[0] == "T"):
            temp = data_dict['Type']
            send = ""
            In = 0
            Out = 0
            for j in range(len(temp)):
                if temp[j] == "Instation":
                    In += 1
                elif temp[j] == "Outstation":
                    Out += 1
            send += "Instation"
            send += "%"
            send += str(In)
            send += "%"
            send += "Outstation"
            send += "%"
            send += str(Out)

        elif (data[0] == "V"):
            send = ""
            for j in data_dict.keys():
                send += j
                send += "*"
                for k in data_dict[j]:
                    send += str(k)
                    send += "%"
                send += "*"
        elif (data[0] == "Quit"):
            connection.close()

        if not data:
            break
        connection.sendall(str.encode(send))
    connection.close()


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client,))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()
