# ===================================================================================================================================================================
# This code contains the code for front end.
# Theme for front end saved in config.toml file in .streamlit folder.
# The code is written using Streamlit 
# Developers: Bhagyashree Bhat,Prarthana R Nayak,Raksha Udupi,Misba Sawar
# Date of completion: 29/June/2022
# College : SDM College of Engineering and Technology 
# Description :This contains the code for the front end accessible by the user.
# The front end has a Sign up section for the users where the users have to sign up by entering their username,password and a hint incase they forget their password
# This data is stored in the users database.The password entered is stored in the form of hashes for extra security.
# After signing up,the users can log in anytime and check the client machine's information stored in the database in the form of easy to read, table format. 
# The table contains the various information of the client's such as the system name, the drive name, and the percentage of memory used, etc.
# The table displays the disk percentage of the clients drive as red if it has exceeded over 90%
# This also has a forget password functionality where the user can reset their password using their username and the hint they have given while signing up.
# ====================================================================================================================================================================
#required imports
from ast import Div
import streamlit as st
import pandas as pd
from pretty_html_table import build_table
import streamlit as st
import pandas as pd
import base64
from PIL import Image
from string import ascii_uppercase,digits
from random import choices
import os
import streamlit.components.v1 as stc
import numpy as np
import socket
import sqlite3
import string
from datetime import datetime
import time
import openpyxl as openpyxl
import psutil
from sqlite3 import Connection

#Image to be displayed on the frontend
image=Image.open('image.jpg')

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib

#=========================================================================
# Function name: make_hashes
# Parameters taken: String
# Description: takes a string and converts it into equivalent hashcode.
# useful for converting passwords before storing
# returns: String, the hashed value of the entered plaintext.
#=========================================================================
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


#=========================================================================
# Function name: check_hashes
# Parameters taken: String , String
# Description: takes a plain text password and its equivalent hash string
# and checks if both are same.
# useful during sign-in validation
# returns: Boolean value. True if both match, false if they dont.
#=========================================================================
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3
#connection object for the db files which stores username and password. 
conn = sqlite3.connect('data.db')
c = conn.cursor()

#=========================================================================
# Function name: create_usertable()
# Parameters taken: Void
# Description: Creates a table named usertable if it doesnt exist previously
# This database table holds the username, passowrd and the hint given during sign-up
# returns: void
#=========================================================================
def create_usertable():
    #executes query to create table
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY,password TEXT,hint TEXT)')

#====================================================================================
# Function name: add_userdata
# Parameters taken: String, String, String.
# Description: inserts the username,password and hint into the created database table
# returns: Void
#====================================================================================
def add_userdata(username,password,hint):
    #executes the query
    c.execute('INSERT INTO userstable(username,password,hint) VALUES (?,?,?)',(username,password,hint))
    conn.commit()

#=========================================================================
# Function name: login_user()
# Parameters taken: String , String
# Description: Searches for rows with same value as the passed username and password.
# fetches all the row(s) with matching values and returns them
# sign-in validation
# returns: Array of strings.(all the matching rows)
#=========================================================================
def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data

#===================================================================================
# Function name: login_forgot()
# Parameters taken: String , String
# Description: Searches for rows with same value as the passed username and hint.
# fetches all the row(s) with matching values and returns them
# useful when the user forgets the password and asks for password reset.
# returns: Array of strings.(all the matching rows)
#===================================================================================
def login_forgot(username,hint):
    c.execute('SELECT * FROM userstable WHERE username =? AND hint = ?',(username,hint))
    data = c.fetchall()
    return data

#===================================================================================
# Function name: reset_password()
# Parameters taken: String , String ,String
# Description: Upadates the password with the new password for the respective username
# and hint
# returns: Void
#===================================================================================
def reset_password(username,new_password,hint):
    c.execute('UPDATE userstable SET password = ? WHERE username = ? AND hint = ?',(make_hashes(new_password),username,hint))
    conn.commit()

#===================================================================================
# Function name: create_connection()
# Parameters taken: String
# Description: Creates a connection with the given db filen.
# returns: connection object.
#===================================================================================
def create_connection(db_file):
    conn1=None
    try:
        conn1=sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn1

#===================================================================================
# Function name: color_survived()
# Parameters taken: integer
# Description: sets the background color for the table with the client memory info 
# users view.
# The color is set to red for the disk percentage coloumn if the percentage >= 90
# Else the color is green 
# returns: css property.
#===================================================================================
def color_survived(val):
    color = '#F76C5C' if float(val) >= 90 else '#85F271'
    return f'background-color: {color}'

#=====================================================================================
# Function name: display_data()
# Parameters taken: void
# Description: displays the data from the database table into easy to read table format
# returns: void
#======================================================================================
def display_data():
    #connects with the databse where the client memeory info is stored.
    conn1=create_connection('Information.db')
    cur=conn1.cursor()

    #featches all the data from the database
    query="""SELECT * FROM systemInfo """
    listReq = cur.execute(query)
    data=listReq.fetchall()

    #renders in the front end
    st.markdown("### Storage details ")
    #sets the coloumn name for the table to be displayed
    df = pd.DataFrame(data,columns=['HostName','DriveName','Total (GB)','Used(GB)','Free(GB)','%Used','Updated on'])

    #applies red color if %used >=90 else green color
    st.dataframe(df.reset_index(drop=True).style.applymap(color_survived,subset=['%Used']))
    conn1.close()

global result1

#===================================================================================
# Function name: main()
# Parameters taken: void
# Description: The main function where all the Ui components are rendered if run.
# returns: void.
#===================================================================================
def main():
    """Simple Login App"""

    #sets the page title shown in tab
    st.set_page_config(page_title="Login")

    #used to apply css propeties, acts like link herf in html files
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    #The main page title
    st.title('Remote Monitoring system')

    #sidebar options
    menu = ["Login","SignUp"]
    #select one out of the two
    choice = st.sidebar.selectbox("Menu",menu)
    
    if choice == "Login":
        #what should render if login is chosen:
        #ask for usernam and password
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            
            #create usertable which holds username and password if doesnt exist(just a saftey measure for bugs)
            create_usertable()
            #hash the entered passwords for matching with the hashed password in the database
            hashed_pswd = make_hashes(password)
            
            #login_user() function validates the entered username and the entered password
            result1 = login_user(username,check_hashes(password,hashed_pswd))

            #if creadentials are vaild
            if result1:
                st.title("Welcome, {}".format(username))
                st.success("Logged In as {}".format(username))
                st.sidebar.image('.\image.jpg',width=200)
                #display the table with the client machine info.
                display_data()                       
            else:
                st.warning("Incorrect Username/Password")

        #else if the user forgets passoword while logging in 
        elif st.sidebar.checkbox("Forgot password?"):
            #asks for username and the hint given while signing up.
            username_forgot = st.text_input("username")
            hint_forgot = st.text_input("Hint given while signing up")

            #if checked change password
            if(st.checkbox("change password")):

                #if username or hint field is empty, display error message
                if len(username_forgot) <= 0 or len(hint_forgot) <= 0:
                    st.error("Dont leave the fields empty!")

                #if not empty,    
                else:
                    #call the function to validate the given hint and username
                    result_forgot_pass = login_forgot(username_forgot,hint_forgot)

                    #if credentials are correct
                    if result_forgot_pass:
                        new_password_forgot = st.text_input("Reset your password",type='password')

                        #call function to reset the password
                        if st.checkbox("reset"):
                            reset_password(username_forgot,new_password_forgot,hint_forgot)
                            st.success("You have successfully reset your password")
                            st.info("Go to Login Menu to login")
                    
                    #if credentials are not correct.
                    else:
                        st.warning("Incorrect Username/Hint")

    #if users choice is signing up
    elif choice == "SignUp":
        #st.container container for adding CSS
        with st.container():
            st.subheader("Create New Account")
            #Ask for user to insert username, password and hint for signing up.
            new_user = st.text_input("Username")   
            new_password = st.text_input("Password",type='password') 
            hint = st.text_input("Add a hint in case you forget password")  
            isclicked = st.button("SignUp")

        #if signup button is clicked.
        if isclicked:
            #if any of the fields are empty
            if len(new_user) <= 0 or len(new_password) <= 0:
                st.error("Invalid username or password")
            elif len(hint)== 0:
                st.error("Add a hint!")                    
            else:
                #create the databse table to hold the users in case it isnt created
                create_usertable()
                #add_userdata adds the entered username,password and hint to databse table.
                add_userdata(new_user,make_hashes(new_password),hint)

                #sucess message                
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")

#calling of main function for rendering
if __name__ == '__main__':
    main()