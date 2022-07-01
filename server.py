# ==========================================================================
# This code contains the code for server.
# Developers: Bhagyashree Bhat,Prarthana R Nayak,Raksha Udupi,Misba Sawar
# Date of completion: 29/June/2022
# College : SDM College of Engineering and Technology 
# Description :This contains the code for the server.
# The server intially waits for the clients to get connected
# After the clients get connected,It creates a database once and inserts the received values into the database.
# During subsequent client connections, it updates the database with the most recent value for that client machine.
# The server also keeps track of the timestamp of the client's connection              
# ..........................................
# Change History
# ..........................................
# ==========================================================================

import os
import socket
import sqlite3
from datetime import datetime
import psutil
import sqlite3
from sqlite3 import Connection
import datetime;

#=====================================================================================================================================
# Function name = create_connection(db_file)
# Parameters taken = Type: String, The name which we want our database file to be.This file holds the table with the client information  
# Description of the function:Creates a database connection for our passed DB.
# Returns: Connection object.
# ====================================================================================================================================

def create_connection(db_file):
    conn=None
    try:
        conn=sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

#====================================================================================================================================
# Function name = createTable()
# Parameters taken = Void
# Description of the function: Creates a database table called systemInfo if it doesnt exist already.
# The table consists of client's disk storage information along with the time the client got connected last.
# Returns: void.
# ===================================================================================================================================
 
def createTable():
    sql_create_table="""CREATE TABLE IF NOT EXISTS systemInfo (
                        SystemName text,
                        DiskName text,
                        DiskTotal text,
                        DiskUsed text,
                        DiskFree text,
                        DiskPercentage text,
                        timeStamp text
                        );"""
    conn=create_connection('Information.db')
    if conn is not None:
        cursor=conn.cursor()
        cursor.execute(sql_create_table)
        print("Table accessed successfully.............")
    else:
        print("Error cannot create database connection")


#========================================================================================================================================
# Function Name: socketHandler()
# Parameters taken: Void
# Description of the function: Creates a socket, Binds it to a port and listens for client connections.
# Calculates and stores the required values in the database.
# Returns: void
#========================================================================================================================================

def socketHandler():

    #socket created
    s = socket.socket()
    print("Socket created")

    #Binding Ipv4 adress of server and socket
    s.bind(('192.168.22.30',8002))
    #liatens and waits for connectionsS
    s.listen(50)
    print("Waiting for connections")
    while True:
        c,addr = s.accept()
        print("Connected with ",addr)

        #Receives the information from the client and stores it in variables
        rSystemName=c.recv(1024).decode()
        rDiskName=c.recv(1024).decode()
        rDiskTotal=c.recv(1024).decode()
        rDiskUsed=c.recv(1024).decode()
        rDiskFree=c.recv(1024).decode()
        rDiskPercentage=c.recv(1024).decode()

        #calculates the required values from the variables
        rDiskTotal=str(round(float(rDiskTotal)/(1024*1024*1024),2))
        rDiskUsed=str(round(float(rDiskUsed)/(1024*1024*1024),2))
        rDiskFree=str(round(float(rDiskFree)/(1024*1024*1024),2))
        rtimeStamp = datetime.datetime.now()

        #calls createTable function to create a table.
        createTable()

        #connection object to connect to the database.
        conn=create_connection('Information.db')
        cur=conn.cursor()

        #executes the query to insert the values into the said table.
        query="""SELECT * FROM systemInfo WHERE SystemName= ? AND DiskName= ?"""
        task=(rSystemName,rDiskName)
        listReq = cur.execute(query,task)
        data = listReq.fetchall()

        #Inserting the values..
        if not data:
            query = """INSERT INTO systemInfo(SystemName, DiskName, DiskTotal,DiskUsed,DiskFree,DiskPercentage,timeStamp) VALUES (?,?,?,?,?,?,?)"""
            task = (rSystemName,rDiskName,rDiskTotal,rDiskUsed,rDiskFree,rDiskPercentage,rtimeStamp)
            cur.execute(query, task)
            conn.commit()
            print("Data is inserted successfully")

        #This part updates the database if the client has previously connected and we have to update the database with the new values 
        else:
            cur.execute("UPDATE systemInfo SET DiskTotal=?,DiskUsed=?,DiskFree=?,DiskPercentage=?,timeStamp=? WHERE SystemName= ? AND DiskName=?",(rDiskTotal,rDiskUsed,rDiskFree,rDiskPercentage,rtimeStamp,rSystemName,rDiskName))
            conn.commit()
            print("Data is updated successfully")

        # This part just prints the database values received in the command prompt in the server side.
        query = """SELECT * FROM systemInfo"""
        listReq = cur.execute(query)
        data = listReq.fetchall()
        for i in data:
            host_name=i[0]
            disk_name=i[1]
            disk_total=i[2]
            disk_used=i[3]
            disk_free=i[4]
            disk_percentage=i[5]
            time_stamp = i[6]
            print("  "+host_name + "  "+disk_name +"  "+disk_total +"  "+disk_used +"  "+disk_free +"  "+disk_percentage +"  "+time_stamp)
        #closes the database connection.
        conn.close()
        c.close()

#main function call
if __name__ == '__main__':
    socketHandler()




