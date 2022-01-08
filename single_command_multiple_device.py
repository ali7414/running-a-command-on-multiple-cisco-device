import paramiko 
import os.path
import time
import sys 
import re
import threading
#creating thread 
username1=input("\n#Enter Your device Username:")
password1=input("\n#Enter Your device Password:")
cmd=input("\n#Enter your command: ")
def create_threads(list,function):
    threads=[]
    for ip in list:
        th= threading.Thread(target=function,args=(ip,))
        th.start()
        threads.append(th)
    for th in threads:
        th.join()
def ip_file_valid():
    #prompting user for input 
    ip_file=input("\n #Enter IP file path and name (e.g. D:\myfile\ip_list.txt):")
    #checking if the file exist
    if os.path.isfile(ip_file)==True:
        print("\n IP file is valid :) \n")
    else:
        print("\n * file {} does not exist :( please check and try again.\n".format(ip_file))
        sys.exit()
    #open user selected file for reading 
    selected_ip_file=open(ip_file,'r')
    #Starting from the begining of the file 
    selected_ip_file.seek(0)
    #Reading each ip address (line) in the file 
    ip_list= selected_ip_file.readlines()
    #closing the file 
    selected_ip_file.close()
    return ip_list
def ssh_connection(ip):

    #creating SSH CONNECTION 
    try:
        #logging into device 
        session= paramiko.SSHClient()
        #This will auto accept Unknown host key. do not use in production! the default whould RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #connect to the device using username and password 
        session.connect(ip.rstrip("\n"),username=username1,password=password1)
        #start an interactive shell session on the router 
        connection=session.invoke_shell() 
        #Starting terminal lenght for entire output
        connection.send("\n")
        connection.send("enable\n")
        time.sleep(1)
        connection.send("\terminal lenght 0\n")
        time.sleep(1)
        #Entering Global confing mode 
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        connection.send(cmd + "\n")
        time.sleep(1)
        #closing the command file 
        #Checking command output for IOS syntax errors
        router_output= connection.recv(65535)
        if re.search(b"% invalid output",router_output):
            print("* there was at least one IOS syntax error on device {}".format(ip))
        else:
            print("\n Done for device {} \n".format(ip))
        session.close()
    except paramiko.AuthenticationException:
        print("Invalid Username or password ")
        print("closing program bye")
#prompting user for username and password and command 
device_ips=ip_file_valid()
create_threads(device_ips,ssh_connection)

