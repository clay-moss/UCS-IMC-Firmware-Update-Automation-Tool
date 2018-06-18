import multiprocessing
from multiprocessing import Pool
from multiprocessing import Process
from imcsdk.utils.imcfirmwareinstall import firmware_huu_update
from imcsdk.utils.imcfirmwareinstall import firmware_huu_update_monitor
from imcsdk.imchandle import ImcHandle
import time
import datetime
import imcsdk.imchandle
import getpass
import sys
import os

ucs_hosts = []
user_database = []
passwds = []
handles = {}

#
# Reminder, replace handles[key] with session in 1.2 FINAL, remove update exception here.
#

def connect():
    count = 0
    increment = 0
#stores multiple handle calls in a dictionary
    for hosts in ucs_hosts:
        key = count
        handle = ImcHandle(hosts,user_database[count],passwds[count],timeout=None)
        handles[key] = handle
        count += 1
#attempts to login to each handle/server, odd retry thing I came up with.        
    for key in handles:
        increment += 1
        session = handles[key]
        try:
            session.__enter__()
        except:
            session.__enter__()
        else:
            pass
#confirms connectivity to server, or else removes handle 
        if session._validate_connection() == False:
            try:
                session.__enter__()
            except:
                print("Connection to server #%d %s Failed.." % (increment,session.ip))
                print("")
                print("Deleting entry for server #%d %s and continuing.." % (increment,session.ip))
                del handles[increment - 1]
                del ucs_hosts[increment - 1]
                del user_database[increment - 1]
                del passwds[increment - 1]
                pass
            else:
                pass
       
        if session._validate_connection() == True:
            print("Connection to UCS Server #%d %s in list, successful.." % (increment,session.ip))
        
    file_server = input("Enter file server IP or localhost: ")
    server_login = input("Does file server need login? [y/n]: ").lower()
    if server_login == 'y':
        user = input("Enter Username: ")
        password = getpass.getpass()
    elif server_login == 'n':
            user = ""
            password = ""
    else:
        print('Invalid Input, using defaults "n"..')
        user = ""
        password = ""
  
    protocol = input("Enter file sharing protocol ('www','cifs','nfs'): ").lower()
    directory = input("Enter fully specified path to file: ")
    up_all = "all"
    stop = "yes"
    time = 60
    timeout = 240
    interval = 30
    no = "no"
    tick = 0

    for key in handles:
        if handles[key]._validate_connection() == True:
            tick += 1
            session = handles[key]
            print("")
            print("Sending update request to server #%d %s.." % (tick,session.ip))
             
            p = Process(target=firmware_huu_update, args=(session,directory,protocol,file_server,user,password,up_all,stop,timeout,no,no))
            p.start()
            p.join()
            
            monitor = multiprocessing.Pool(None)
            monitor.apply_async(firmware_huu_update_monitor, args=(session,time,interval))
                     
        else:
            print("Connection failed to server #%d %s in list, continuing.." % (tick,session.ip))
    monitor.close()
    monitor.join()

    for key in handles:
        session = handles[key]
        session._logout()
        print("Server #%d %s Updated.." % (int(key) + 1,session.ip))
    return True

def main():
    end_program = 'exit'
    
    def end(a):
        if a == end_program:
            return sys.exit()
        else:
            return

    while True:
        host_ips = input("Enter UCS CIMC IP:  ").lower()
        end(host_ips)
        username = input("Enter Username: ")
        end(username)
        password = getpass.getpass()
        ucs_hosts.append(host_ips)
        user_database.append(username)
        passwds.append(password)
        print ("Servers Added to update list:  " + str(len(ucs_hosts)))
        add_hosts = input('Add UCS Servers to update list? Or "show" to see UCS Server list [y/n]: ').lower()

        if add_hosts == 'n':
            print("Initiating connection(s) to UCS Server(s) in list..")
            return connect()
        elif add_hosts == 'y':
            continue
        else:
            print("Invalid Input..")
            continue

if __name__ == '__main__':
    print("")
    print("Cisco UCS Server Firmware Update Automation Tool - Made by clmoss@cisco.com")
    print("")
    multiprocessing.freeze_support()
    main()
