#=======================================================================================================================
#This code contains the code for client.
#Developers : Bhagyashri G Bhat, Misba Sawar, Prarthana Nayak, Raksha Udupi
#Date of Completion : 29/June/2022
#College : SDM college of Engineering and Technology
#Description : The client basically refers to any machine whose disk storage is required to be collected.
#The client first gets connected to the server and immediately measures the disk storage space along with the name of
# the disk and name of the machine in the form of string and sends it to the server.
#The client also has a email functionality where if a drive's total memory percentage exceeds 90% then it will send a
#mail to the administrator.
#=======================================================================================================================
import string
import psutil
import time
import os
import socket
import sqlite3
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import datetime

from pyparsing import identbodychars

PORT_NUMBER=8002
#IP_ADDRESS='192.168.1.7'

#disk_partitions() method retrieves  information on all the mounted disk partitions.
diskParts = psutil.disk_partitions()

#for each individual drive in the client machine, do
for drives in diskParts:
    #creates the socket
    c=socket.socket()
    #connecting to the server using the ipv4 address of the server and the port number
    c.connect(('192.168.22.30',PORT_NUMBER))
    #str() function converts values to strings.
    driveName = str(drives).split("=")[1].split(",")[0]
    iDiskName = driveName
    data = psutil.disk_usage(driveName[1:-1])

    # The disk Usage method returns the disk usage statistics.
    # contains:
    # total: contains total amount of memory
    # used: This represents free memory
    # free: This represents free memory
    # percentage : This represents the percentage usage of the memory.
    iDiskTotal = str(data).split("=")[1].split(",")[0]
    iDiskUsed = str(data).split("=")[2].split(",")[0]
    iDiskFree = str(data).split("=")[3].split(",")[0]
    iDiskPercentage = str(data).split("=")[4].split(",")[0]
    iDiskPercentage=iDiskPercentage[:-1]
    diskpercentage = float(iDiskPercentage)
    iSystemName = socket.gethostname()

#This part of code is used to check if the disk storage percentage is exceeding 90%, if yes then the client will send a
#mail to the administrator informing the same.It uses smtp protocol to send the mail

    if diskpercentage >= 90:
        #creating smtp object
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()

        #loggining into our client machine email using email and app passwords.
        #app passwords allows us to access email from a third party.
        smtp.login('client.machine19078@gmail.com', 'xdwpxmwrcxsydwms')

        #parameters: subject, email body
        def message(subject="Memory exceeded notification", text=""):
            
            # build message contents
            msg = MIMEMultipart()
      
            # Add Subject
            msg['Subject'] = subject  
      
            # Add text contents
            msg.attach(MIMEText(text))  
            return msg

        #time stamp for connection
        rtimeStamp = datetime.datetime.now()
        date_time = rtimeStamp.strftime("%m/%d/%Y, %H:%M:%S")

        #message to be sent
        msg = message("Memory exceeded notification by"+iSystemName+".",
            "!!!!!WARNING!!!!!\nMachine name:"+iSystemName + "."+"\nDear user, the disk "+iDiskName+"has exceeded its memory over 90%,clear the space up.\nTime: "+date_time+"."
            )
  
        # Make a list of emails, where you wanna send mail
        to = ["prarthana1504@gmail.com"]
  
        # Provide some data to the sendmail function!
        smtp.sendmail(from_addr="hello@gmail.com",to_addrs=to, msg=msg.as_string())
  
        # Finally, don't forget to close the connection
        smtp.quit()

    #send the information collected to the server.
    c.send(bytes(iSystemName,'utf-8'))
    time.sleep(0.5)
    c.send(bytes(iDiskName, 'utf-8'))
    time.sleep(0.5)
    c.send(bytes(iDiskTotal, 'utf-8'))
    time.sleep(0.5)
    c.send(bytes(iDiskUsed, 'utf-8'))
    time.sleep(0.5)
    c.send(bytes(iDiskFree, 'utf-8'))
    time.sleep(0.5)
    c.send(bytes(iDiskPercentage, 'utf-8'))
