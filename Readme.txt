
About the project

Remote Monitoring System(RMS) is a software that remotely monitors the clients PC in server-client architecture. The project has a great potentail
in educational systems, industries and any environment that demands system monitoring.Understanding the infrastructure and the health of the system is essential 
for ensuring reliability and stability of the services provided by the system. One of the best ways to gain this insight is with a robust monitoring system that gathers 
system information and visualizes data.


Built With
1.Python
2.Socket Programming
3.SMTP protocol
4.Streamlit
5.Hash tables
6. Google app password
7.SqlLite

Getting started

Prerequisties
Before running the client make sure that all the clients are connected to the same network as server.
Know the IP address and port of the server and ensure that same is updated in the client side

Server side:
1. In server side just run the executable file server.py
2. If there is no executable file convert the existing python file to executable file.
3. Once server is running , it runs indefinitely untill stopped manually .
4. To view the front end run "streamlit app.py" in command prompt.
5. For first time users sign-up and then login into the page to view the table and client disk storage details.
6. Please enter a hint while signing up , it is used to reset the password in case you forget it.

Client side
1. Client is free to use the system and utilise the resources to the fullest.
2. In case of disk storage exceeding more than 90% , sends an e-mail to the administrator. 
3. Please clean up the space as instructed by the administrator.

Installation
No installation as such , just make sure that server is running and both server and client are connected in same networked environmnet.

Usage
1.The main aim of this project is to reduce the burden on the System/Network administrators from responsibility of monitoring the Clients 
  connected to a Server in the Client–Server network architecture.
2.Monitors the Clients connected to the Server and provides the information such as Client Name, Drive Name, Total Memory available of particular drive, 
  Used Memory, Free Space available, Percentage used of particular drive and Timestamp of when the latest information from the client is been collected.
3.RMS stores the client information in a robust database in which the data can be updated dynamically.
4.If any one of the client’s disk storage values exceeds more than 90% the client system sends an alert email to the administrator to clear the storage.
5.RMS does not in any way disturb the Users working on the Remote Clients. Thus, it works only as a Remote Monitoring Tool but not as a Remote-Control Tool.


Contributed by:
Bhagyashri G Bhat
Misba Sawar
Prarathana Nayak
Raksha Udupi.


